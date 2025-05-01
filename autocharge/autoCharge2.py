# Alvik autocharge 2.0
# Roni Bandini, April 2025
# Buenos Aires, Argentina
# MIT License

from arduino_alvik import ArduinoAlvik
import time
from time import sleep
import sys
import random

# settings
safeDistance=10
kp = 50.0
lineSpeed = 15
standardSpeed=30
chargingTime=8
lineLimit=250
batteryLimit=95
alwaysCharge=0
endPathColor1="YELLOW" # sometimes white gets detected as yellow
endPathColor2="LIGHT GREY"

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
    global standardSpeed
    alvik.set_wheels_speed(standardSpeed,standardSpeed)
    sleep(myTime)

def goBackward(myTime):
    alvik.set_wheels_speed(-20,-20)
    sleep(myTime)

def turnRight(myTime):
    global standardSpeed
    alvik.set_wheels_speed(standardSpeed,0)
    sleep(myTime)

def turnLeft(myTime):
    global standardSpeed
    alvik.set_wheels_speed(0,standardSpeed)
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

def standardNavigation():  
    print("Standard navigation")
    changeLights('green')

    # is there an obstacle?
    if getCenterDistance()>safeDistance:    
        goForward(0.1)
    else:
        hitBreak()
        sleep(1)
        randomRotate()

def chargingStationPath():
    global chargingPath
    chargingPath = 1
    print("Charging station path")
    changeLights('red')

    # Read IR sensor values
    ir_left, ir_center, ir_right = alvik.get_line_sensors()

    # Calculate error using centroid
    error = calculate_center(ir_left, ir_center, ir_right)

    # Proportional control
    control = kp * error

    # Compute motor speeds
    left_speed = lineSpeed - control
    right_speed = lineSpeed + control

    # Limit motor speeds to avoid negative values or overflow
    left_speed = max(min(int(left_speed), 20), -20)
    right_speed = max(min(int(right_speed), 20), -20)

    alvik.set_wheels_speed(left_speed, right_speed)

def chargeAlvik():   
    global chargingPath
    print('🥃 Charging... ') 
    chargingPath=0
    changeLights('blue')
    goForward(2)
    hitBreak()   
    print("Battery level start: "+str(alvik.get_battery_charge())+"%")
    while alvik.get_battery_charge()<99:      
      sleep(chargingTime)
      print("Charging: "+str(alvik.get_battery_charge())+"%")
    print('Out... ')   
    print("Battery level end: "+str(alvik.get_battery_charge())+"%")    
    changeLights('off')
    goBackward(4)
    turnLeft(3)

def searchPath():
  changeLights("off")
  abort=0
  if random.randint(1, 3)==1:
    side="right"
  else:
    side="left"
  ir_left, ir_center, ir_right = alvik.get_line_sensors()
  counter=0
  while (ir_left<=lineLimit and ir_center<=lineLimit and ir_right<=lineLimit):
    print("Rotating to find line")
    if side=="right":
      turnRight(0.1)
    else:
      turnLeft(0.1)
    ir_left, ir_center, ir_right = alvik.get_line_sensors()
    counter=counter+1    
    if counter==20:
      print("Did not find the line, abort")
      chargingPath=0
      abort=1
      break 

  if abort==0:
    hitBreak()
    chargingStationPath()
  else:
    standardNavigation()
        
  
############################################################################################

alvik = ArduinoAlvik()
alvik.begin()

print('')
print('Arduino Alvik Autocharge 2.0')  
print('Roni Bandini, April 2025')  
print("Battery level "+str(alvik.get_battery_charge())+"%")

chargingPath=0
error = 0
control = 0

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

                if (chargingPath==0):
                  standardNavigation()
                else:
                  if (getColor()==endPathColor1 or getColor()==endPathColor2):  
                    chargeAlvik()
                  else: 
                    print("Search where the path is")
                    searchPath()  
                    chargingStationPath()
            else:

                # found charging path and the battery is down
                if (alvik.get_battery_charge()<batteryLimit or alwaysCharge==1):                   
                  chargingStationPath() 
                else:
                  print("Charger path found but battery is charged")


except KeyboardInterrupt as e:
    print('Keyboard interrumpted')
    alvik.stop()
    sys.exit()
