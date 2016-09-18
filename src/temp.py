# -*- coding: utf-8 -*-
import serial
import time
import os.path
import datetime
import smtplib
from email import Encoders
from email.Utils import formatdate
from email.MIMEBase import MIMEBase
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

# Google Account
ADDRESS = "XXXX@gmail.com"
PASSWD = "xxxx"

# SMTP Server
SMTP = "smtp.gmail.com"
PORT = 587

# Temperature Log File
FILE = "/home/yamajun/GitRepos/fridgeProtection/src/temp.log"

def create_message(from_addr, to_addr, subject, body):
  msg = MIMEMultipart()
  msg["From"] = from_addr
  msg["To"] = ",".join(to_addr)
  msg["Date"] = formatdate()
  msg["Subject"] = subject
  body = MIMEText(body)
  msg.attach(body)
  return msg

def send(from_addr, to_addrs, msg):
  smtp_obj = smtplib.SMTP(SMTP, PORT)
  smtp_obj.ehlo()
  smtp_obj.starttls()
  smtp_obj.login(ADDRESS, PASSWD)
  smtp_obj.sendmail(from_addr, to_addrs, msg.as_string())
  smtp_obj.close()

def connect(device_name, baud_rate):
  ser = serial.Serial(device_name, baud_rate)
  print "device name: %s" % ser.portstr
  return ser

def monitor(sensor):
  prev_temp = ""
  curr_temp = 0
  curr_time = time.ctime()
  to_addr = ["YYYY@gmail.com", "ZZZZ@gmail.com"]

  while True:     # Wait staible data.
    curr_temp = int(sensor.readline(), 10)
    if curr_temp < 100: break

  try:
    with open(FILE, "r") as f:
      prev_temp = int(f.read(), 10)
  except IOError as e:
    print e

  if curr_temp > 3 and curr_temp > prev_temp:
    subject = "[!!Alert!!] FridgeTemp is high!"
    body = """
Current Temperature %s degree.
You'd better check your fridge condition.
""" % (curr_temp)
    msg = create_message(ADDRESS, to_addr, subject, body)
    send(ADDRESS, to_addr, msg)
    print "send alert message."
  else:
    if prev_temp >= 3:
      if curr_temp > 3:
        subject = "[!!Alert!!] FridgeTemp has been high yet!"
        body = """
  Current Temperature %s degree.
  You'd better check your fridge condition.
  """ % (curr_temp)
        msg = create_message(ADDRESS, to_addr, subject, body)
        send(ADDRESS, to_addr, msg)
        print "send alert message continuously."
      else:
        subject = "[Info] FridgeTemp is recovered!"
        body = """
  Current Temperature %s degree.
  An emergency was avoided.
  """ % (curr_temp)
        msg = create_message(ADDRESS, to_addr, subject, body)
        send(ADDRESS, to_addr, msg)
        print "send recovery message."
    else:
      print "Stable."

  try:
    with open(FILE, "w") as f:
      f.write(str(curr_temp))
  except IOError as e:
    print e

  sensor.close()

  print "%s, %s" % (curr_time, curr_temp)
  print "Current Temperature : %s" % (curr_temp)
  print "Previous Temperature: %s" % (prev_temp)

if __name__ == '__main__':
  sensor = connect('/dev/ttyACM0', 9600)
  monitor(sensor)
