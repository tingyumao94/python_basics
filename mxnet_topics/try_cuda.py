import mxnet as mx

source = r'''
template<typename DType>
__global__ void axpy(const DType *x, DType *y, DType alpha) {
    int i = threadIdx.x + blockIdx.x * blockDim.x;
    y[i] += alpha * x[i];
}
'''
module = mx.rtc.CudaModule(source, exports=['axpy<float>', 'axpy<double>'])
func32 = module.get_kernel("axpy<float>", "const float *x, float *y, float alpha")
x = mx.nd.ones((10,), dtype='float32', ctx=mx.gpu(0))
y = mx.nd.zeros((10,), dtype='float32', ctx=mx.gpu(0))
func32.launch([x, y, 3.0], mx.gpu(0), grid_dims=(1, 1, 1), block_dims=(10, 1, 1))
print(y)

func64 = module.get_kernel("axpy<double>", "const double *x, double *y, double alpha")
x = mx.nd.ones((10,), dtype='float64', ctx=mx.gpu(0))
y = mx.nd.zeros((10,), dtype='float64', ctx=mx.gpu(0))
func64.launch([x, y, 3.0], mx.gpu(0), grid_dims=(1, 1, 1), block_dims=(10, 1, 1))
print(y)