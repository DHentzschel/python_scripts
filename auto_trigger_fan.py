#!/usr/bin/python

import os
import time
import RPi.GPIO as GPIO
from datetime import datetime

pin = 14
sleep_seconds = 58
high_temp = 47

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)

def log(message):
    now = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    print("[" + now + " ps/ATF]: " + message)

# get temperature from command
def get_cpu_temperature():
    res: str = os.popen('vcgencmd measure_temp').readline()
    return res.replace("temp=", "").replace("'C\n", "")


def enable_fan():
    print_temp()
    log("Power on fan ...")
    GPIO.output(pin, True)


def disable_fan():
    print_temp()
    log("Power off fan ...")
    GPIO.output(pin, False)


def print_temp():
    print("Current temperature: " + get_cpu_temperature())


temp = float(get_cpu_temperature())

try:
    loop_counter = 0
    while temp > high_temp:
        enable_fan()

        time.sleep(sleep_seconds)
        temp = float(get_cpu_temperature())
        loop_counter += 1
        if loop_counter > 5:
            break
    disable_fan()

# Turn off fan when interrupted
except KeyboardInterrupt:
    disable_fan()
    log("KeyboardInterrupt. Cancelling operation...")
    
