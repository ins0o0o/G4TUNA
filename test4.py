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
    distance = measure_distance()
    if touch == 1:
        print("터치되었습니다.")
    else:
        print("터치 되지 않았습니다.")


while True:
    mainProcess()