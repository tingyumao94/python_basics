#!/usr/bin/python
from __future__ import print_function, division
import os
import cv2 as cv


def generate_fab_seq(max_limit):

    old_num = 1
    num = 1

    while num < max_limit:
        yield num
        tmp = num
        num = old_num + num
        old_num = tmp


def generate_batch(data_path, label_file, batch_size=32):
    img_path = os.path.join(data_path, 'images')

    labels = []
    with open(label_file, 'r') as f:
        for line in f:
            img_file, label = line.split(' ')
            labels.append((img_file, label))

    for b in range(0, len(labels), batch_size):
        batch_xs = []
        batch_ys = []
        for j in range(batch_size):
            img = cv.imread(os.path.join(img_path, labels[b+j][0]))
            batch_xs.append(img)
            batch_ys.append(labels[b+j][1])

        yield batch_xs, batch_ys


if __name__ == '__main__':

    for n in generate_fab_seq(10):
        print(n)