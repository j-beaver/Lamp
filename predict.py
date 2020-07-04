import tensorflow as tf
import numpy as np

import matplotlib.pyplot as plt
import pandas as pd
from tensorflow import keras
from tensorflow.keras import layers

model = keras.models.load_model('Data/model')
x = np.array([[0.120,0.336,0.128]])
y = model.predict(x)
print(y)