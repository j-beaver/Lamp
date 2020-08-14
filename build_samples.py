import random
import math
import numpy as np
import os

f_out = open('Data/lampdata1.csv', 'w+')


random.seed(39)

slice_num = 100
pain_point = .4

noize_amp = 5

a = np.linspace(1 - 1/slice_num, 0, num=slice_num)
b = np.linspace(1 - 1/slice_num, 0, num=slice_num)

d = np.random.randint(0, noize_amp, (slice_num ** 2, 4)) / 1000
#d = np.zeros(shape=(slice_num ** 2, 4))

for ind_a, i in np.ndenumerate(a):
    for ind_b, j in np.ndenumerate(b):

        index = ind_a[0]*slice_num + ind_b[0]
        d[index, 2] = i + d[index, 2]
        d[index, 0] = j + d[index, 0]
        if j >= pain_point:
            d[index, 1] = (1-j)*0.5 + d[index, 1]
        else:
            d[index, 1] = (1-j)*0.5 + (pain_point-j) * 2 + d[index, 1]
        if i >= pain_point:
            d[index, 3] = (1-i)*0.5 + d[index, 3]
        else:
            d[index, 3] = (1-i)*0.5 + (pain_point-i) * 2 + d[index, 3]

        if d[index, 0] > 1:
            d[index, 0] = 1
        if d[index, 1] > 1:
            d[index, 1] = 1
        if d[index, 2] > 1:
            d[index, 2] = 1
        if d[index, 3] > 1:
            d[index, 3] = 1

        line = str(d[index, 0]) + ';' + str(d[index, 1]) + ';' + str(d[index, 2]) + ';' + str(d[index, 3]) + '\n'
        f_out.write(line)

f_out.close()

print(d[-100:])

