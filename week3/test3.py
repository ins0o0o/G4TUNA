from flask import Flask, render_template_string
import threading
import time
import RPi.GPIO as GPIO

app = Flask(__name__)

# GPIO 핀 설정
GPIO.setmode(GPIO.BCM)
DistanceTrig = 23
DistanceEcho = 24
GPIO.setup(DistanceTrig, GPIO.OUT)
GPIO.setup(DistanceEcho, GPIO.IN)

distance = 0  # 거리 값을 저장할 변수
warning_message = ""  # 경고 메시지를 저장할 변수

html_page = '''
<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Distance Checker</title>
        <meta http-equiv="refresh" content="1">  <!-- 1초마다 페이지 새로고침 -->
    </head>
    <body>
        <h1>Distance Checker</h1>
        <p>현재 거리: {{ distance }} cm</p>
        {% if warning_message %}
        <p style="color: red;">{{ warning_message }}</p>  <!-- 경고 메시지 빨간색으로 표시 -->
        {% endif %}
        <p>이 페이지는 1초마다 새로고침됩니다.</p>
    </body>
    </html>
'''

def measure_distance():
    global distance
    # Trig 핀을 LOW로 설정하고 짧은 시간 대기
    GPIO.output(DistanceTrig, GPIO.LOW)
    time.sleep(0.1)
    
    # Trig 핀에 짧은 펄스(10μs) 발생
    GPIO.output(DistanceTrig, GPIO.HIGH)
    time.sleep(0.00001)  # 10μs 대기
    GPIO.output(DistanceTrig, GPIO.LOW)
    
    # Echo 핀이 HIGH로 될 때까지 대기
    while GPIO.input(DistanceEcho) == GPIO.LOW:
        pulse_start = time.time()  # Echo 핀이 LOW에서 HIGH로 바뀌는 순간 기록
    
    # Echo 핀이 LOW로 될 때까지 대기
    while GPIO.input(DistanceEcho) == GPIO.HIGH:
        pulse_end = time.time()  # Echo 핀이 HIGH에서 LOW로 바뀌는 순간 기록
    
    # 펄스 지속 시간 계산
    pulse_duration = pulse_end - pulse_start
    
    # 초음파 속도는 34300 cm/s, 따라서 거리 = 시간 * 속도 / 2 (왕복이므로 2로 나눔)
    distance = pulse_duration * 34300 / 2

def update_distance():
    global warning_message
    while True:
        measure_distance()  # 1초마다 거리 측정
        if distance < 10:  # 10cm 이하일 때 경고 메시지 설정
            warning_message = "Warning: 정지! 정지! 정지! 손들어 움직이면 쏜다 "
        else:
            warning_message = ""  # 거리가 5m 이상일 때 경고 메시지 없음
        time.sleep(1)

@app.route('/')
def index():
    return render_template_string(html_page, distance=int(distance), warning_message=warning_message)

if __name__ == '__main__':
    # 거리 측정 스레드 실행
    thread = threading.Thread(target=update_distance)
    thread.daemon = True
    thread.start()
    
    # Flask 서버 실행
    app.run(host='0.0.0.0', port=5000, debug=True)
