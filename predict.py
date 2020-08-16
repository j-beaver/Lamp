
import numpy as np
import random

from tensorflow import keras
import keras.backend as K

model = keras.models.load_model('Data/model')

random.seed(42)
random_amp = 5

start_point = .8
vol_start = .7

pulse_pattern = [0, 0.5, 1, 0.5, 0]
pulse_index = 0
# pulse_amp is the max pulse brightness
pulse_amp = 0.3

distance_curr = 0
distance_prev = 0

bright_curr = 0
bright_prev = 0

vol_curr = 0
vol_prev = 0

vel_curr = 0
vel_prev = 0

lfo_curr = 0
lfo_prev = 0

success_stories = [[1, 0, 1, 0]]

def predict(distance):


# normalize distance after cutting start point
    if distance > start_point:
        distance = start_point
    distance = distance/start_point

    global pulse_index

# pulse with light on distance over start_point
    if distance == 1:
        pulse_index = (pulse_index + 1) % len(pulse_pattern)
        return pulse_pattern[pulse_index - 1], pulse_pattern[pulse_index - 1], pulse_pattern[pulse_index - 1], pulse_pattern[pulse_index - 1]

    global distance_curr
    global bright_curr
    global distance_prev
    global bright_prev
    global vol_curr
    global vel_curr
    global lfo_curr

# keep prev step in history if it caused observer's turning back
    if(distance > distance_curr) & (distance_curr < distance_prev):
        success_stories.append([[distance_prev, bright_prev, distance_curr, bright_curr, vol_curr, vel_curr, lfo_curr]])

    distance_prev = distance_curr
    distance_curr = distance
    bright_prev = bright_curr

    x = np.array([[distance_prev, bright_prev, distance_curr]])
    bright_curr = model(x)[0][0].numpy()

    vol_curr = bright_curr+vol_start+(random.randint(- random_amp, random_amp))/1000
    vel_curr = bright_curr+(random.randint(- random_amp, random_amp))/1000
    lfo_curr = bright_curr+(random.randint(- random_amp, random_amp))/1000
    bright_curr = bright_curr+(random.randint(- random_amp, random_amp))/1000

    if bright_curr > 1:
        bright_curr = 1
    if vol_curr > 1:
        vol_curr = 1
    if vel_curr > 1:
        vel_curr = 1
    if lfo_curr > 1:
        lfo_curr = 1

    if bright_curr < 0:
        bright_curr = 0
    if vol_curr < 0:
        vol_curr = 0
    if vel_curr < 0:
        vel_curr = 0
    if lfo_curr < 0:
        lfo_curr = 0

    return bright_curr, vol_curr, vel_curr, lfo_curr


# check memory leakage
i = 100000
j = .0
while i > 0:
    i -= 1
    j = i / 100000
    brightness = predict(j)[0]
    print(brightness)

# predict
brightness, volume, velocity, lfo = predict(0.5)
brightness = predict(0.225)[0]
brightness, volume, velocity, lfo = predict(0.27)


print(distance_prev, bright_prev, distance_curr, brightness)
