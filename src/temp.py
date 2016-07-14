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
ADDRESS = "xxxx@gmail.com"
PASSWD = "yyyy"

# SMTP Server
SMTP = "smtp.gmail.com"
PORT = 587

def create_message(from_addr, to_addr, subject, body):
  msg = MIMEMultipart()
  msg["From"] = from_addr
  msg["To"] = to_addr
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

ser = serial.Serial('/dev/ttyACM0', 9600)
print(ser.portstr)
time.sleep(3)
count = 0
prev_temp = 0

while True:
  time.sleep(1)
  curr_temp = int(ser.readline(), 10)
  if count > 0:
    print "%s, %s" % (time.ctime(), curr_temp)
    if count == 1:
      prev_temp = curr_temp
    else:
      if curr_temp > 32 and prev_temp < curr_temp:
        to_addr = "zzzz@gmail.com"
        subject = "[!!Alert!!] FridgeTemp is high!"
        body = """
Current Temperature %s degree.
You'd better check your fridge condition.
""" % (curr_temp)
        msg = create_message(ADDRESS, to_addr, subject, body)
        #send(ADDRESS, [to_addr], msg)
        print("send alert message.\n")
      prev_temp = curr_temp
  count = count + 1
ser.close()
