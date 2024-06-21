# Alvik Obstacles Avoidance
# Roni Bandini, June 2024
# Buenos Aires, Argentina
# MIT License
# https://bandini.medium.com

from arduino_alvik import ArduinoAlvik
from time import sleep
import random
import sys
import network
import urequests
import time

alvik = ArduinoAlvik()
alvik.begin()

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

def getCenterDistance():
  distance_l, distance_cl, distance_c, distance_r, distance_cr  = alvik.get_distance()  
  return distance_c 

def randomRotate():
  if random.randint(1, 3)==1:
    alvik.rotate(90, 'deg')
  else:
    alvik.rotate(-90, 'deg')

def getColor():
  return alvik.get_color_label()
  
def sendTelegram(message):
  global telegramEnabled
  global telegramBot
  global telegramChatId
  url="https://api.telegram.org/"+telegramBot+"/sendMessage?chat_id="+telegramChatId+"&text="+message
  if telegramEnabled==1:
    response = urequests.get(url)
    
print('')
print('Arduino Alvik - Roni Bandini')

changeLights('blue')

WIFI_NETWORK=''
WIFI_PASSWORD=''
telegramBot=""
telegramChatId=""

parkingColor='ORANGE'
telegramEnabled=1
safeDistance=10

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_NETWORK, WIFI_PASSWORD)

print()
print("Alvik se conectó a",WIFI_NETWORK)

sleep(3)
print('Listo...')
changeLights('off')
  
print("Bateria al "+str(alvik.get_battery_charge())+"%")
print("Toque Ok para comenzar...")

while alvik.get_touch_ok()==False:
  print(".")  
  sleep(1)

start = time.time()

while alvik.get_touch_cancel()==False:
  myColor=getColor()
  print(myColor)
  
  if myColor==parkingColor:  
    hitBreak()
    end = time.time()
    elapsedTime = end - start
    print('Llegó en '+str(elapsedTime)+' segundos')
    sendTelegram('Alvik llegó al estacionamiento en '+str(elapsedTime)+' segundos 🚗 ')
    break 
    
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


