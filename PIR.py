import RPi.GPIO as GPIO
import time
from gpiozero import LED
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
PIR_PIN=26
GPIO.setup(PIR_PIN, GPIO.IN)
'''
while True:
    if GPIO.input(PIR_PIN):
        print('motion detected')
    else:
        print('ready')
'''
def get_reading():
  # time.sleep(1)
  if GPIO.input(PIR_PIN):
    #print('Motion Detected')
    #led.on()
    return 1
  else:
    #led.off()
    return 0
    #print ('Ready')
    