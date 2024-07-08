# Alvik AI Computer Vision
# Roni Bandini, June 2024
# Buenos Aires, Argentina
# MIT License
# https://bandini.medium.com

from arduino_alvik import ArduinoAlvik
import network
import espnow
from time import sleep
import time

def changeLights(myColor):
  if myColor=='red':
    alvik.left_led.set_color(1, 0, 0)
    alvik.right_led.set_color(1, 0, 0)
  if myColor=='green':
    alvik.left_led.set_color(1, 1, 0)
    alvik.right_led.set_color(1, 1, 0)
  if myColor=='blue':
    alvik.left_led.set_color(0, 1, 1)
    alvik.right_led.set_color(0, 1, 1)
  if myColor=='white':
    alvik.left_led.set_color(1, 1, 1)
    alvik.right_led.set_color(1, 1, 1)
  if myColor=='off':
    alvik.left_led.set_color(0, 0, 0)
    alvik.right_led.set_color(0, 0, 0)
    
def goForward(myTime):
  alvik.set_wheels_speed(10,10)
  sleep(myTime)

def goBackward(myTime):
  alvik.set_wheels_speed(-10,-10)
  sleep(myTime)

def turnRight(myTime):
  alvik.set_wheels_speed(20,0)
  sleep(myTime)

def turnLeft(myTime):
  alvik.set_wheels_speed(0,20)
  sleep(myTime)
  
def hitBreak():
  alvik.brake()

def saveLog(myLine):  
  year, month, day, hour, mins, secs, weekday, yearday = time.localtime()  
  f = open('log.txt', 'a')
  f.write(str(hour)+':'+str(mins)+':'+str(secs)+' '+myLine+'\n')
  
alvik = ArduinoAlvik()
alvik.begin()

sta = network.WLAN(network.STA_IF)
sta.active(True)

e = espnow.ESPNow()
e.active(True)

changeLights('green')

sleep(3)
saveLog('Alvik AI Computer Vision started...')

while True:
    goBackward(1)
    host, msg = e.recv()
    if msg:             
      print(host, msg)   
      saveLog("Msg received")
      if msg == b'end':
        break
      if msg == b'\x01\x00\x00\x00':
        saveLog("Police")
        print('Police')
        changeLights('red')
        turnLeft(6)
        changeLights('off')
      if msg == b'\x02\x00\x00\x00':
        print('Ball')
        saveLog("Ball")
        changeLights('blue')
        turnRight(3)
        changeLights('off')      
        