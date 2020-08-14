import random
import math
import numpy as np

random.seed(12)

def obs_move(distance=0.0, prev_distance=0.0, energy=0.0, prev_energy=0.0):
    distance_delta = distance - prev_distance
    energy_delta = energy - prev_energy
    new_distance = math.sqrt(distance ** 2 + prev_distance ** 2 + energy ** 2) / 2
    return new_distance

arr = np.linspace (0, 1, num = 1001)

energy = 1
distance = 0
prev_distance = 0

for x in arr:
    prev_distance = distance
    distance = x

    move_back = obs_move(distance, prev_distance, energy)
    print(str(x) + ' : ' + str(move_back))


