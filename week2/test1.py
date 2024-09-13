import RPi.GPIO as GPIO
import time

ledRed = 17  # LED가 연결된 GPIO 핀 번호

GPIO.setmode(GPIO.BCM)
GPIO.setup(ledRed, GPIO.OUT, initial=GPIO.LOW)

while True:
    GPIO.output(ledRed, GPIO.HIGH)  # LED 켜기
    time.sleep(1)  # 1초 대기
    GPIO.output(ledRed, GPIO.LOW)   # LED 끄기
    time.sleep(1)  # 1초 대기
