import RPi.GPIO as GPIO
import threading
import time
import Adafruit_DHT

buttonPin = 25

ledRed = 17
ledYello = 27
ledGreen = 22

sensTouch = 5
sensDH = 6

DistanceTrig = 23
DistanceEcho = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(ledRed, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ledYello, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ledGreen, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(sensTouch, GPIO.IN)
GPIO.setup(sensDH, GPIO.IN)
GPIO.setup(DistanceTrig, GPIO.OUT)
GPIO.setup(DistanceEcho, GPIO.IN)

flag = 0
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
