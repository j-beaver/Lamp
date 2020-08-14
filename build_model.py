import tensorflow as tf
import numpy as np

import matplotlib.pyplot as plt
import pandas as pd

# Importing the dataset
lamp_data = pd.read_csv('Data/lampdata1.csv', delimiter=';')

# from sklearn import preprocessing

# Normalizing the dataset

# min_max_scaler = preprocessing.MinMaxScaler()
# lamp_data = pd.DataFrame(min_max_scaler.fit_transform(lamp_data.values))

X = lamp_data.iloc[:, :-1].values
y = lamp_data.iloc[:, 3].values

#X = lamp_data.iloc[:100, :-1].values
#y = lamp_data.iloc[:100, 3].values

# Splitting the dataset into the Training set and Test set

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1/3, random_state=42)

from tensorflow import keras
from tensorflow.keras import layers

model = keras.Sequential()
model.add(layers.Dense(12, input_shape=(3,), activation="relu"))
model.add(layers.Dense(12, activation="relu"))
model.add(layers.Dense(1))

model.compile(loss="mean_squared_error",
           optimizer="adam",
           metrics=['accuracy'])

model.summary()

model.fit(X_train, y_train, epochs=30, validation_split=0.3)
preds = model.predict(X_test)

print('Predictions: \n', preds, y_test)

# Evaluate  model's accuracy on the test data
accuracy = model.evaluate(X_test, y_test)[1]
print('Accuracy:', accuracy)

model.save('Data/model')


# Output prediction vs test data
x = X_test[:, 2]
#plt.scatter(x, y_test, c='g', s=0.5)
#plt.scatter(x, preds, c='r', s=0.5, alpha=0.4)