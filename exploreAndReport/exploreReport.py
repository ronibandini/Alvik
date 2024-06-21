# Arduino Alvik 
# Explore and report 
# Roni Bandini, June 2024
# Buenos Aires, Argentina
# MIT License

from arduino_alvik import ArduinoAlvik
import random
import time
from time import sleep
import network
import espnow

# settings
reportEvery=15
safeDistance=15
peer = b'\x00\x00\x0\x00\x00\x00' 

turns=0

e = espnow.ESPNow()
e.active(True)  
e.add_peer(peer)  

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
  alvik.set_wheels_speed(30,30)
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
  myRand=random.randint(1, 4)
  
  if myRand==1:
    alvik.rotate(90, 'deg')
  if myRand==2:
    alvik.rotate(-90, 'deg')
  if myRand==3:
    alvik.rotate(45, 'deg')
  if myRand==4:
    alvik.rotate(-45, 'deg')

def reportStatus():
  global start 
  global turns
  hitBreak()
  changeLights('blue')
  print("Bateria al "+str(alvik.get_battery_charge())+"%")
  print("Superficie "+str(alvik.get_color_label()))  
  print("Timer "+str(time.time() - start)+" segundos")
  print("Turns "+str(turns))  
  e.send(peer, str(alvik.get_battery_charge()) +","+ str( alvik.get_color_label()) +","+ str(time.time() - start) +","+ str(turns)+" " )   
  changeLights('off')

print('')
print('Arduino Alvik - Explorar y reportar')
print('Roni Bandini, Junio 2024, Argentina')
print('')

sta = network.WLAN(network.STA_IF)   
sta.active(True)

partialTime=time.time()

print()

print("Toque Ok para comenzar...")

while alvik.get_touch_ok()==False:
  print(".")  
  sleep(1)

# inicia el contador de tiempo transcurrido
start = time.time()

while True:

  # Imprime timer
  print(time.time() - partialTime)
  print(turns)
  
  if getCenterDistance()>safeDistance:    
    # No hay obstáculo
    changeLights('green')
    alvik.set_illuminator(True)
    goForward(1)
  else:
    # Hay obstáculo
    alvik.set_illuminator(False)
    changeLights('red')   
    turns=turns+1
    randomRotate()

  if time.time() - partialTime>reportEvery:
    # reporto a base
    reportStatus()
    # reseteo el timer
    partialTime=time.time()



