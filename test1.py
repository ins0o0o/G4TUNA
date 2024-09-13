# 버튼 -> 전체 ON/OFF
# 초음파 센서 -> 거리 측정해서 단계별로 LED 점등
# 터치 센서 -> 터치 때 마다 온습도 출력

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
    global flag
    while True:
        GPIO.wait_for_edge(buttonPin, GPIO.FALLING)  # 버튼이 눌렸을 때까지 대기 (FALLING 엣지 감지)
        flag = 1 - flag  # flag 값 토글
        if flag == 1:
            print("<<<<Process Start!!>>>>\n")
        else:
            print("<<<<Process Terminated>>>>\n")
        time.sleep(0.5)

button_thread = threading.Thread(target=check_button)
button_thread.daemon = True  # 메인 스레드가 종료되면 이 스레드도 종료되도록 설정
button_thread.start()

def check_touch():
    global touch
    while True:
        if GPIO.input(sensTouch) == 1:
            touch = 1

touch_thread = threading.Thread(target=check_touch)
touch_thread.daemon = True  # 메인 스레드가 종료되면 이 스레드도 종료되도록 설정
touch_thread.start()

def measure_distance():
    # Trig 핀을 LOW로 설정하고 짧은 시간 대기
    GPIO.output(DistanceTrig, GPIO.LOW)
    time.sleep(0.1)
    
    # Trig 핀에 짧은 펄스(10μs) 발생
    GPIO.output(DistanceTrig, GPIO.HIGH)
    time.sleep(0.00001)  # 10μs 대기
    GPIO.output(DistanceTrig, GPIO.LOW)
    
    # Echo 핀이 HIGH로 될 때까지 대기
    while GPIO.input(DistanceEcho) == GPIO.LOW:
        pulse_start = time.time()
    
    # Echo 핀이 LOW로 될 때까지 대기
    while GPIO.input(DistanceEcho) == GPIO.HIGH:
        pulse_end = time.time()
    
    # 펄스 지속 시간 계산
    pulse_duration = pulse_end - pulse_start
    
    # 초음파 속도는 34300 cm/s, 따라서 거리 = 시간 * 속도 / 2 (왕복이므로 2로 나눔)
    distance = pulse_duration * 34300 / 2
    
    return distance

def readDH():
    sensor = Adafruit_DHT.DHT11     #  sensor 객체 생성
    humidity, temperature = Adafruit_DHT.read_retry(sensor, sensDH)
    print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))


def mainProcess():
    global touch
    distance = measure_distance()
    if distance <= 10:
        GPIO.output(ledRed, GPIO.HIGH)
        GPIO.output(ledYello, GPIO.LOW)
        GPIO.output(ledGreen, GPIO.LOW)
    elif distance > 10 and distance <= 20:
        GPIO.output(ledRed, GPIO.LOW)
        GPIO.output(ledYello, GPIO.HIGH)
        GPIO.output(ledGreen, GPIO.LOW)
    elif distance > 20 and distance <= 30:
        GPIO.output(ledRed, GPIO.LOW)
        GPIO.output(ledYello, GPIO.LOW)
        GPIO.output(ledGreen, GPIO.HIGH)
    else:
        print("Out of Range")
        GPIO.output(ledRed, GPIO.LOW)
        GPIO.output(ledYello, GPIO.LOW)
        GPIO.output(ledGreen, GPIO.LOW)
    
    if touch == 1:
        readDH()
        touch = 0
        

while True:
    if flag == 0:
        GPIO.output(ledRed, GPIO.LOW)
        GPIO.output(ledYello, GPIO.LOW)
        GPIO.output(ledGreen, GPIO.LOW)
    else:
        mainProcess()
