import random
import math
import numpy as np
import os

f_out = open('Data/lampdata1.csv', 'w+')


random.seed(39)

slice_num = 100
pain_point = .5

noize_amp = 5
blink_amp = .2

# training sample coefficients
k1 = 0.5
k2 = 2

a = np.linspace(1 - 1/slice_num, 0, num=slice_num)
b = np.linspace(1 - 1/slice_num, 0, num=slice_num)

# create result matrix with noize inititalization
d = np.random.randint(- noize_amp, noize_amp, (slice_num ** 2, 4)) / 1000

# populate result matrix
# energy = k1 * (1 - distance) + (pain point - distance) * k2  if distance < pain point
# energy = k1 * (1 - distance) if distance > pain point
for ind_a, i in np.ndenumerate(a):
    for ind_b, j in np.ndenumerate(b):

        index = ind_a[0]*slice_num + ind_b[0]
        d[index, 2] = i + d[index, 2]
        d[index, 0] = j + d[index, 0]
        if j >= pain_point:
            d[index, 1] = (1-j)*k1 + d[index, 1]
        else:
            d[index, 1] = (1-j)*k1 + (pain_point-j) * k2 + d[index, 1]
        if i >= pain_point:
            d[index, 3] = (1-i)*k1 + d[index, 3]
        else:
            d[index, 3] = (1-i)*k1 + (pain_point-i) * k2 + d[index, 3]

        if d[index, 0] > 1:
            d[index, 0] = 1
        if d[index, 1] > 1:
            d[index, 1] = 1
        if d[index, 2] > 1:
            d[index, 2] = 1
        if d[index, 3] > 1:
            d[index, 3] = 1

        if d[index, 0] < 0:
            d[index, 0] = 0
        if d[index, 1] < 0:
            d[index, 1] = 0
        if d[index, 2] < 0:
            d[index, 2] = 0
        if d[index, 3] < 0:
            d[index, 3] = 0

        line = str(d[index, 0]) + ';' + str(d[index, 1]) + ';' + str(d[index, 2]) + ';' + str(d[index, 3]) + '\n'
        f_out.write(line)


# adding pulse samples
# blink_pattern = [0, 0.4, 1, 0.6, 0]
# i = 0

# while i < slice_num:
#     j_prev = 0
#     i += 1
#     for j in blink_pattern:
#         line = '1;' + str(j_prev) + ';1;' + str(j) + '\n'
#         j_prev = j
#         f_out.write(line)
#         print(line)
#     print(i)

f_out.close()

#print(d[-100:])
