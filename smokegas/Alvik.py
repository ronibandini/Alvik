# Alvik smoke and methane detector
# Roni Bandini, July 2024
# Buenos Aires, Argentina
# MIT License

from arduino_alvik import ArduinoAlvik
from time import sleep
import random
import time

alvik = ArduinoAlvik()
alvik.begin()
  
def goForward(myTime):
  alvik.set_wheels_speed(20,20)
  sleep(myTime)

def goBackward(myTime):
  alvik.set_wheels_speed(-20,-20)
  sleep(myTime)

def turnRight(myTime):
  alvik.set_wheels_speed(30,0)
  sleep(myTime)

def turnLeft(myTime):
  alvik.set_wheels_speed(0,30)
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
  if random.randint(1, 3)==1:
    alvik.rotate(90, 'deg')
  else:
    alvik.rotate(-90, 'deg')

def getColor():
  return alvik.get_color_label()

parkingColor='WHITE'
safeDistance=7

print('')
print('Arduino Alvik')
  
print("Battery "+str(alvik.get_battery_charge())+"%")
print("Ok to start...")

while alvik.get_touch_ok()==False:
  print(".")  
  sleep(1)

start = time.time()

while alvik.get_touch_cancel()==False:
  myColor=getColor()
  print(myColor)     
    
  if getCenterDistance()>safeDistance:    
    changeLights('green')
    alvik.set_illuminator(True)
    goForward(1)
  else:
    changeLights('red')
    alvik.set_illuminator(False)
    hitBreak()
    sleep(1)
    randomRotate()

changeLights('off')
hitBreak()


