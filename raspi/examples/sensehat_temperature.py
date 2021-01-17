#!/usr/bin/python3
from sense_hat import SenseHat

sense = SenseHat()
sense.clear()

temp = sense.get_temperature_from_humidity()
temp = round(temp, 1)

print(temp)
