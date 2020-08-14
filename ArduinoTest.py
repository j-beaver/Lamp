import serial
import numpy as np
from tensorflow import keras

START_CYCLE = 'New Cycle Started'
END_CYCLE = 'New Cycle Ended'

ser = serial.Serial('COM3', 9600)

i = 0
distance_prev = 0.00
bright_prev = 0.00
distance = 0.00
bright = np.array([[0.20]])

model = keras.models.load_model('Data/model')

while True:
    try:
        b = ser.readline()
        string_n = b.decode()
        string = string_n.rstrip()
        if string == START_CYCLE:
            distance_prev = distance
            bright_prev = bright[0,0]
            data = []
            i += 1
            print(START_CYCLE + ' #' + str(i))

            b = ser.readline()
            string_n = b.decode()
            string = string_n.rstrip()
            while string != END_CYCLE:
                try:
                    data.append(float(string))
                except:
                    print("Not a float value")
#                print(string)
                b = ser.readline()
                string_n = b.decode()
                string = string_n.rstrip()
                distance = max(data) / 1000
            print('Max value in cycle: ' + str(distance))
            x = np.array([[distance_prev, bright_prev, distance]])
            print (x)
            bright = model.predict(x)
            print('Predicted brightness: ' + str(bright))
    except:
        print("Keyboard Interrupt")
        break