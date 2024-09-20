from flask import Flask, render_template_string, url_for, redirect
import RPi.GPIO as GPIO
import threading
import time
import Adafruit_DHT

ledRed = 17
ledYello = 27
ledGreen = 22

sensTouch = 5
sensDH = 6

DistanceTrig = 23
DistanceEcho = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(ledRed, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ledYello, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ledGreen, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(sensTouch, GPIO.IN)
GPIO.setup(sensDH, GPIO.IN)
GPIO.setup(DistanceTrig, GPIO.OUT)
GPIO.setup(DistanceEcho, GPIO.IN)

AutoAccBrk = 0  # 차간 거리 유지 ON / OFF
AutoAC = 0      # 에어컨 자동 ON / OFF

humidity = 0
temperature = 0


def check_touch():
    global flag
    while True:
        GPIO.wait_for_edge(sensTouch, GPIO.FALLING)  # 버튼이 눌렸을 때까지 대기 (FALLING 엣지 감지)
        flag = 1 - flag  # flag 값 토글
        if flag == 1:
            print("\n<<< Process Start!! >>>\n")
        else:
            print("\n<<< Process Terminated >>>\n")
        time.sleep(0.5)

touch_thread = threading.Thread(target=check_touch)
touch_thread.daemon = True  # 메인 스레드가 종료되면 이 스레드도 종료되도록 설정
touch_thread.start()


def readDH():
    sensor = Adafruit_DHT.DHT11     # sensor 객체 생성
    global humidity
    global temperature
    while True:                     #0.5초마다 온도와 습도 값을 불러옴
        humidity, temperature = Adafruit_DHT.read_retry(sensor, sensDH)
        time.sleep(0.5)
        
DH_thread = threading.Thread(target=readDH)
DH_thread.daemon = True  # 메인 프로세스 종료 시 자동으로 종료
DH_thread.start()