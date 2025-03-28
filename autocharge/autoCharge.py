# Alvik autocharge
# Roni Bandini, March 2025
# Buenos Aires, Argentina
# MIT License

from arduino_alvik import ArduinoAlvik
import time
from time import sleep
import sys
import random


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
    
def getColor():
    print(alvik.get_color_label())
    return alvik.get_color_label()

def randomRotate():
    if random.randint(1, 3)==1:
        alvik.rotate(90, 'deg')
    else:
        alvik.rotate(-90, 'deg')    

def hitBreak():
    alvik.brake()

def goForward(myTime):
    alvik.set_wheels_speed(30,30)
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

def calculate_center(left: int, center: int, right: int):
    centroid = 0
    sum_weight = left + center + right
    sum_values = left + 2 * center + 3 * right
    if sum_weight != 0:
        centroid = sum_values / sum_weight
        centroid = 2 - centroid
    return centroid

def getCenterDistance():
  distance_l, distance_cl, distance_c, distance_r, distance_cr  = alvik.get_distance()  
  return distance_c 

def chargeAlvik():
    hitBreak()                
    print('🥃 Charging... ') 
    changeLights('blue')
    print("Battery level start"+str(alvik.get_battery_charge())+"%")
    sleep(chargingTime)
    print('Out... ') 
    print("Battery level end"+str(alvik.get_battery_charge())+"%")
    chargingPath=0
    changeLights('off')
    turnLeft(2)
    goForward(1)

def standardNavigation():    
    changeLights('off')
    #print(ir_left, ir_center, ir_right)

    # is there an obstacle?
    if getCenterDistance()>safeDistance:    
        goForward(0.1)
    else:
        hitBreak()
        sleep(1)
        randomRotate()

def chargingStationPath():
    chargingPath=1
    print("Charging station path")
    changeLights('red')
    #print(ir_left, ir_center, ir_right)

    # follow the line
    if ir_center > lineLimit:        
        alvik.set_wheels_speed(baseSpeed, baseSpeed)
    elif ir_left > lineLimit:        
        alvik.set_wheels_speed(0, baseSpeed)
    elif ir_right > lineLimit:        
        alvik.set_wheels_speed(baseSpeed, 0)

############################################################################################

alvik = ArduinoAlvik()
alvik.begin()

print('')
print('Arduino Alvik Autocharge')  
print('Roni Bandini, March 2025')  
print("Battery level "+str(alvik.get_battery_charge())+"%")

# settings
chargeColor='WHITE'
safeDistance=7
error = 0
control = 0
kp = 50.0
baseSpeed = 15
chargingTime=8
lineLimit=250
batteryLimit=105
chargingPath=0

alvik.left_led.set_color(0, 0, 1)
alvik.right_led.set_color(0, 0, 1)

try:
    while True:
        while not alvik.get_touch_cancel():
            sleep(0.01)
            
            # get line sensor info
            ir_left, ir_center, ir_right = alvik.get_line_sensors()                        

            # not black path 
            if (ir_left<=lineLimit and ir_center<=lineLimit and ir_right<=lineLimit):
                                                                
                # it was searching for the base and base stop is there
                if (getColor()==chargeColor):  
                    chargeAlvik()
                else:
                    standardNavigation()
                  
            else:

                # charge path and battery is down
                if (alvik.get_battery_charge()<batteryLimit):                          
                  chargingStationPath()                  
                else:
                  print("Charger path found but battery is charged")


except KeyboardInterrupt as e:
    print('Keyboard interrumpted')
    alvik.stop()
    sys.exit()
