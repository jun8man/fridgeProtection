# -*- coding: utf-8 -*-
import serial
import json

def connect(device_name, baud_rate):
  ser = serial.Serial(device_name, baud_rate)
  return ser

def measure(sensor):
  data = {"temperature": 0}

  while True:     # Wait staible data.
    temp = sensor.readline()
    data["temperature"] = int(temp, 10)
    if data["temperature"] < 100: break

  sensor.close()

  return json.dumps(data)

if __name__ == '__main__':
  sensor = connect('/dev/ttyACM0', 9600)
  print measure(sensor)
