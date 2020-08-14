
import numpy as np
import random

from tensorflow import keras

model = keras.models.load_model('Data/model')

random.seed(39)
random_amp = 5

distance_curr = 0
bright_curr = 0
distance_prev = 0
bright_prev = 0

start_point = .0

success_stories = [[0, 0, 0, 0]]

def predict(distance):
    global distance_curr
    global bright_curr
    global distance_prev
    global bright_prev

    if (distance > distance_curr) & (distance_curr < distance_prev):
        success_stories.append([[distance_prev, bright_prev, distance_curr, bright_curr]])

    distance_prev = distance_curr
    distance_curr = distance
    bright_prev = bright_curr

    x = np.array([[distance_prev, bright_prev, distance_curr]])
    bright_curr = model.predict(x)[0][0]

    return bright_curr

y = predict(0.5)
y = predict(0.225)
y = predict(0.3)
print(y)
print(success_stories)