import board
import busio
import pwmio
import time
import digitalio
from adafruit_apds9960.apds9960 import APDS9960
from adafruit_apds9960 import colorutility
import analogio
from board import *
adc = analogio.AnalogIn(GP27)
act = digitalio.DigitalInOut(board.GP26)
ledg = pwmio.PWMOut(board.GP16, frequency=5000, duty_cycle=0)
ledr = pwmio.PWMOut(board.GP17, frequency=5000, duty_cycle=0)
ledb= pwmio.PWMOut(board.GP18, frequency=5000, duty_cycle=0)
brightness = 0
flag = 0
def rgb():
    global flag
    apds.enable_color = True
    while not apds.color_data_ready:
        time.sleep(0.005)

    # get the data and print the different channels
    r, g, b, c = apds.color_data
    print("red: ", r)
    print("green: ", g)
    print("blue: ", b)
    print("clear: ", c)
    
    lx = colorutility.calculate_lux(r, g, b)
    print("color temp {}".format(colorutility.calculate_color_temperature(r, g, b)))
    print("light lux {}".format(lx))
    apds.enable_color = False    
    if(lx<=750):
        brightness = 65000
    elif(lx>750 and lx<1800):
        brightness = 32000
    elif(lx>=1800):
        brightness = 0
    if(brightness != 0):
        x = brightness#color combination of warm white has RGB ratio of (35%:34%:31%)
        y = x
        z = x
        y = int(y*0.9715)
        z = int(z*0.8868)
        ledr.duty_cycle = x-r
        ledb.duty_cycle = y-b
        ledg.duty_cycle = z-g
        flag +=1
    else:
        flag = 0
        rgboff()
    print("Values for RGB lights : ",ledr.duty_cycle,ledg.duty_cycle,ledb.duty_cycle)
    apds.enable_proximity = True
    apds.enable_gesture = True
    if(flag == 1):
        time.sleep(2)
        rgb()
def rgboff():
    global flag
    flag = 0
    ledr.duty_cycle = 0
    ledb.duty_cycle = 0
    ledg.duty_cycle = 0
    


i2c = busio.I2C(board.GP3, board.GP2)

apds = APDS9960(i2c)

apds.enable_proximity = True
apds.enable_gesture = True


gesturels = [0x02,0x03]
gestureoff = [0x01,0x04]
def apdss():
    apds.enable_color = False
    apds.enable_proximity = True
    apds.enable_gesture = True
    gesture = apds.gesture()
    if gesture == 0x01:
        print("up")
    elif gesture == 0x02:
        print("down")
    elif gesture == 0x03:
        print("left")
    elif gesture == 0x04:
        print("right")
         
    if(gesture in gesturels):
        rgb()
    elif(gesture in gestureoff):
        rgboff()

  
while True:
    act.direction = digitalio.Direction.INPUT
    if(act.value == True):
        apdss()
        
