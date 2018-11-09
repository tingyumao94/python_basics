import numpy as np
import mxnet as mx
from mxnet import profiler
profiler.set_config(profile_all=True, aggregate_stats=True, filename='profile_output.json')


def build_network():
    net = mx.sym.Variable('data')
    net = mx.sym.FullyConnected(net, name='fc1', num_hidden=64)
    net = mx.sym.Activation(net, name='relu1', act_type="relu")
    net = mx.sym.FullyConnected(net, name='fc2', num_hidden=64)
    net = mx.sym.Activation(net, name='relu2', act_type="relu")
    net = mx.sym.FullyConnected(net, name='fc3', num_hidden=64)
    net = mx.sym.Activation(net, name='relu3', act_type="relu")
    net = mx.sym.FullyConnected(net, name='fc4', num_hidden=26)
    net = mx.sym.SoftmaxOutput(net, name='softmax')

    return net


if __name__ == '__main__':

    fname = mx.test_utils.download(
        'https://s3.us-east-2.amazonaws.com/mxnet-public/letter_recognition/letter-recognition.data')
    data = np.genfromtxt(fname, delimiter=',')[:, 1:]
    label = np.array([ord(l.split(',')[0]) - ord('A') for l in open(fname, 'r')])

    batch_size = 32
    ntrain = int(data.shape[0] * 0.8)
    train_iter = mx.io.NDArrayIter(data[:ntrain, :], label[:ntrain], batch_size, shuffle=True)
    val_iter = mx.io.NDArrayIter(data[ntrain:, :], label[ntrain:], batch_size)

    sym = build_network()

    mod = mx.mod.Module(symbol=sym,
                        context=mx.cpu(),
                        data_names=['data'],
                        label_names=['softmax_label'])

    # allocate memory given the input data and label shapes
    mod.bind(data_shapes=train_iter.provide_data, label_shapes=train_iter.provide_label)
    # initialize parameters by uniform random numbers
    mod.init_params(initializer=mx.init.Uniform(scale=.1))
    # use SGD with learning rate 0.1 to train
    mod.init_optimizer(optimizer='sgd', optimizer_params={'learning_rate': 0.1})
    # use accuracy as the metric
    metric = mx.metric.create('acc')

    train_iter.reset()
    metric.reset()

    profiler.set_state('run')
    for batch in train_iter:
        mod.forward(batch, is_train=True)  # compute predictions
        mod.update_metric(metric, batch.label)  # accumulate prediction accuracy
        mod.backward()  # compute gradients
        mod.update()  # update parameters
        break

    mx.nd.waitall()
    profiler.set_state('stop')
    print(profiler.dumps())