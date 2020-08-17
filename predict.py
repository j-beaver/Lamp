from time import gmtime, strftime, sleep

import numpy as np
import random
import threading

from tensorflow import keras
from sklearn.model_selection import train_test_split

model = keras.models.load_model('Data/model')

random.seed(42)
# noise generator's amplifier (x1000)
random_amp = 5

# distance above start_point will be cut and distance below it will be additionally normalized
start_point = .8
# minimal value of volume prediction
vol_start = .5
# vel_stable is predicted when distance = 1
vel_stable = .2

# pulse sequence
pulse_pattern = [0, 0.3, 0.7, 1, 0.7, 0.3]
pulse_index = 0
# pulse_amp is the max pulse brightness
pulse_amp = 0.3

# batch size for reinforcement process
batch_size = 100

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

success_stories = np.empty((0, 7), float)

def reinforce():
    global success_stories
    global model
    X = np.array(success_stories)[:, :3]
    y = success_stories[:, 3]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1 / 3, random_state=42)
    model.fit(X_train, y_train, epochs=30, validation_split=0.3)
    print("Reinforcement completed successfully")
    success_stories = np.empty((0, 7), float)
    return 0

def predict(distance):


# normalize distance after cutting start point
    if distance > start_point:
        distance = start_point
    distance = distance/start_point

    global pulse_index

# pulse with light on distance over start_point
    if distance == 1:
        pulse_index = (pulse_index + 1) % len(pulse_pattern)
        pulse_value = pulse_pattern[pulse_index - 1]*pulse_amp
        return pulse_value, vol_start + pulse_value*(1 - vol_start), vel_stable, pulse_value

    global distance_curr
    global bright_curr
    global distance_prev
    global bright_prev
    global vol_curr
    global vel_curr
    global lfo_curr
    global success_stories

# keep prev step in history if it caused observer's turning back
    if(distance > distance_curr) & (distance_curr < distance_prev):
        temp = np.array([[distance_prev, bright_prev, distance_curr, bright_curr, vol_curr, vel_curr, lfo_curr]])
        success_stories = np.concatenate((success_stories, temp))

    if len(success_stories) >= batch_size:
        t = threading.Thread(name='reinforcement', target=reinforce)
        t.start()
        np.savetxt('Data/samples/' + str(strftime("%Y-%m-%d-%H-%M-%S", gmtime())) + '.csv', success_stories, fmt='%.4e', delimiter=";")
        success_stories = np.empty((0, 7), float)

    distance_prev = distance_curr
    distance_curr = distance
    bright_prev = bright_curr

    x = np.array([[distance_prev, bright_prev, distance_curr]])
    bright_curr = model(x)[0][0].numpy()

    vol_curr = bright_curr*(1-vol_start)+vol_start+(random.randint(- random_amp, random_amp))/1000
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

brightness, volume, velocity, lfo = predict(0.5)
brightness = predict(0.225)[0]
brightness, volume, velocity, lfo = predict(0.27)

i = 0
while i < 10000:
    j = 0
    i += 1
    while j < batch_size:
        j += 1
        brightness = predict(0.23)[0]
        brightness = predict(0.26)[0]
    sleep(3)

print(distance_prev, bright_prev, distance_curr, brightness)

print (success_stories)
