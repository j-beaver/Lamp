
import os
f_out = open('Data/lampdata.csv', 'w+')

directory = 'Data/orig'
for file in os.listdir(directory):
    f_in = open(os.path.join(directory, os.fsdecode(file)), 'r')
    str = f_in.read()
    f_in.close()
    str=str.split(' ')
    prev_elem = '0.0;0.0;'
    for l in str:
        if not l: l = '0.0;0.0'
        f_out.write(prev_elem + l + '\n')
        prev_elem = l + ';'

f_out.close()
