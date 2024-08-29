# Alvik Disco light show
# Roni Bandini, Aug 2024
# MIT License

from arduino_alvik import ArduinoAlvik
import machine 
import time
import random

alvik = ArduinoAlvik()
alvik.begin()

# pin settings for ESP32RGB Led
pin1 = machine.Pin(0, machine.Pin.OUT)
pin2 = machine.Pin(45, machine.Pin.OUT)
pin3 = machine.Pin(46, machine.Pin.OUT)
pin4 = machine.Pin(48, machine.Pin.OUT)

# behaviour settings
mySpeed=80
myDelay=0.3

def iluminatorOn():
  alvik.set_builtin_led(True)
def iluminatorOff():
  alvik.set_builtin_led(False)

def builtinOn():
  alvik.set_builtin_led(True)
def builtinOff():
  alvik.set_builtin_led(False)

def builtinESPOn():
  pin4.value(True)
def builtinESPOff():
  pin4.value(False)

def rgbLed(myColor):
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

def rgbLedLeft(p1, p2, p3):
  alvik.left_led.set_color(p1, p2, p3)    

def rgbLedRight(p1,p2,p3):  
  alvik.right_led.set_color(p1, p2, p3)     
        
def rgbLedESP(myColor):
  if myColor=='red':
    pin1.value(True)
    pin2.value(False)
    pin3.value(False)
  if myColor=='green':
    pin1.value(True)
    pin2.value(True)
    pin3.value(False)
  if myColor=='blue':
    pin1.value(False)
    pin2.value(True)
    pin3.value(True)
  if myColor=='white':
    pin1.value(False)
    pin2.value(False)
    pin3.value(False)
  if myColor=='off':
    pin1.value(True)
    pin2.value(True)
    pin3.value(True)

def rgbLedESPValues(p1,p2,p3):
  pin1.value(p1)
  pin2.value(p2)
  pin3.value(p3)

def lightsOff():  
  iluminatorOff()
  rgbLedESP('off')
  builtinESPOff()
  rgbLed('off')
  builtinOff() 
  
def turnRight():
  alvik.set_wheels_speed(mySpeed,0)

def turnLeft():
  alvik.set_wheels_speed(0,mySpeed)  
  
def hitBreak():
  alvik.brake()

def goForward():
  alvik.set_wheels_speed(mySpeed,mySpeed)

def goBackward():
  alvik.set_wheels_speed(-mySpeed,-mySpeed)
    
print("Alvik Disco Light Show started 🪩")
print("Roni Bandini - August 2024")
print("")

print("Lights sequence...")

print("Iluminator")
iluminatorOn()
time.sleep(1)
iluminatorOff()

print("ESP32 RGB")
rgbLedESP('green')
time.sleep(1)
rgbLedESP('off')

print("ESP32 Built in")
builtinESPOn()
time.sleep(1)
builtinESPOff()

print("Alvik RGB") 

rgbLed('green')
time.sleep(1)
rgbLed('off')

print("Alvik Built In")
builtinOn()
time.sleep(1)
builtinOff()

lightsOff() 

iluminatorOn()
time.sleep(myDelay)
rgbLedESP('green')
time.sleep(myDelay)
builtinESPOn()
time.sleep(myDelay)
rgbLed('green')
time.sleep(myDelay)
builtinOn()
time.sleep(myDelay)


while True:
      
  myP1=random.randint(0,1)
  myP2=random.randint(0,1)
  myP3=random.randint(0,1)
  myP4=random.randint(0,1)
  myP5=random.randint(0,1)
  myP6=random.randint(0,1)
  myP7=random.randint(0,1)
  myP8=random.randint(0,1)
  myP9=random.randint(0,1)
  rgbLedLeft(myP1,myP2,myP3)
  rgbLedRight(myP4,myP5,myP6)
  rgbLedESPValues(myP7, myP8, myP9)
  builtinOn()
  builtinESPOn()
  iluminatorOn()
  
  goForward()
  time.sleep(myDelay*2)
  hitBreak()
      
  goBackward()  
  time.sleep(myDelay*2) 
  hitBreak()
      


     
  
  

  
 
    
