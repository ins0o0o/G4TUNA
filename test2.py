import RPi.GPIO as GPIO
import threading
import time
import Adafruit_DHT

GPIO.setmode(GPIO.BCM)
GPIO.setup(ledRed, GPIO.OUT, initial=GPIO.LOW)
buttonPin = 25

ledRed = 17
ledYello = 27
ledGreen = 22

sensTouch = 5
sensDH = 6
touch = 0
def check_button():
    global touch
    while True:
        if GPIO.input(sensTouch) == 1:
            touch = 1

touch_thread = threading.Thread(target=check_button)
touch_thread.daemon = True  # 메인 스레드가 종료되면 이 스레드도 종료되도록 설정
touch_thread.start()


def mainProcess():
    global touch
    
    if touch == 1:
        GPIO.output(ledRed, GPIO.HIGH)
        GPIO.output(ledYello, GPIO.HIGH)
        GPIO.output(ledGreen, GPIO.HIDH)
    else:
        GPIO.output(ledRed, GPIO.LOW)
        GPIO.output(ledYello, GPIO.LOW)
        GPIO.output(ledGreen, GPIO.LOW)


while True:
    mainProcess()
