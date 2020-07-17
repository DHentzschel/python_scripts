#!/usr/bin/python
import os
import time
import RPi.GPIO as GPIO

pin = 14
sleep_seconds = 58
high_temp = 47

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)

# get temperature from command
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))
    
def enable_pin():
    GPIO.output(pin, True)
    
def disable_pin():
    GPIO.output(pin, False)
    
def print_temp():
    print("Current temperature: " + getCPUtemperature())

temp = float(getCPUtemperature())

try:
    # if temperature > 47 then enable fan
    if (temp > high_temp):
        print_temp()
        print("power on fan...")
        # On
        enable_pin()
        time.sleep(sleep_seconds)
        print("power off fan...")
        # Off
        disable_pin()
        print_temp()
    else:
        print(temp)
        print("temp low")
    
# Turn off fan when interrupted
except KeyboardInterrupt:
    print_temp()
    print("Power off fan...")
    disable_pin()
    print("cancelling...")
    
