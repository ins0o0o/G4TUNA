import RPi.GPIO as GPIO
import time

sensTouch = 5

GPIO.setmode(GPIO.BCM)
GPIO.setup(sensTouch, GPIO.IN)
GPIO.setup(sensDH, GPIO.IN)
        
while True:
    if GPIO.input(sensTouch) == 1:
        print("터치되었습니다")
    else:
        print("터치 되지 않았습니다")
    time.sleep(0.5)
