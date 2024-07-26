# Alvik Spinning Drinking Game
# Roni Bandini, July 2024
# Buenos Aires, Argentina
# MIT License

from arduino_alvik import ArduinoAlvik
from time import sleep
import random
import sys
import time

alvik = ArduinoAlvik()
alvik.begin()

def turnRight(myTime, mySpeed):
  alvik.set_wheels_speed(mySpeed,0)
  sleep(myTime)

def turnLeft(myTime, mySpeed):
  alvik.set_wheels_speed(0,mySpeed)
  sleep(myTime)
  
def hitBreak():
  alvik.brake()

def getCenterDistance():
  distance_l, distance_cl, distance_c, distance_r, distance_cr  = alvik.get_distance()  
  return distance_c 

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
  if myColor=='off':
    alvik.left_led.set_color(0, 0, 0)
    alvik.right_led.set_color(0, 0, 0)
    
def randomRotate():
  
  print("Start rotation") 
  changeLights('red')
  direction=random.randint(1, 2)
  rotationTime=random.randint(5, 15)
  rotationSpeed=random.randint(20, 50)
    
  if direction==1:
    turnLeft(rotationTime,rotationSpeed)
  else:
    turnRight(rotationTime,rotationSpeed)

  hitBreak()
  changeLights('green')
    
print('')
print('Alvik Spinning Drinking Game - Roni Bandini')

  
print("Bateria al "+str(alvik.get_battery_charge())+"%")
print("Toque Ok para comenzar...")

changeLights('green')

start = time.time()

while True:

  while alvik.get_touch_ok()==False:
    print(".")  
    sleep(1)
    
  randomRotate()


