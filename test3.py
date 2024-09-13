import RPi.GPIO as GPIO
import threading
import time

DistanceTrig = 23  # Trig 핀
DistanceEcho = 24  # Echo 핀

GPIO.setmode(GPIO.BCM)
GPIO.setup(DistanceTrig, GPIO.OUT)
GPIO.setup(DistanceEcho, GPIO.IN)

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

while True:
    distance = measure_distance()
    print(f"장애물이 {distance:.1f}cm 거리에 있습니다.")
    
    time.sleep(1)  # 1초 간격으로 거리 측정
