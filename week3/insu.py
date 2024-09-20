from flask import Flask, render_template_string, url_for
import threading
import time
import Adafruit_DHT
import RPi.GPIO as GPIO

app = Flask(__name__)

# GPIO 설정
GPIO.setmode(GPIO.BCM)

# 거리 센서 설정
DistanceTrig = 23
DistanceEcho = 24
GPIO.setup(DistanceTrig, GPIO.OUT)
GPIO.setup(DistanceEcho, GPIO.IN)

# 온/습도 센서 설정
sensDH = 6
GPIO.setup(sensDH, GPIO.IN)

# 전역 변수 설정
humidity = 0
temperature = 0
distance = 0
warning_message = ""

# 온도 및 습도 측정 함수
def readDH():
    sensor = Adafruit_DHT.DHT11  # DHT11 센서 객체 생성
    global humidity
    global temperature
    while True:  # 0.5초마다 온도와 습도 값을 불러옴
        humidity, temperature = Adafruit_DHT.read_retry(sensor, sensDH)
        time.sleep(0.5)

# 거리 측정 함수
def measure_distance():
    global distance
    GPIO.output(DistanceTrig, GPIO.LOW)
    time.sleep(0.1)
    
    GPIO.output(DistanceTrig, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(DistanceTrig, GPIO.LOW)
    
    pulse_start, pulse_end = 0, 0
    
    while GPIO.input(DistanceEcho) == GPIO.LOW:
        pulse_start = time.time()
    
    while GPIO.input(DistanceEcho) == GPIO.HIGH:
        pulse_end = time.time()
    
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 34300 / 2  # 초음파 속도 34300 cm/s

# 거리와 온도/습도 측정 업데이트 함수
def update_sensors():
    global warning_message
    while True:
        measure_distance()  # 거리 측정
        if distance < 10:  # 10cm 이하일 때 경고 메시지 설정
            warning_message = "Warning: 정지! 정지! 정지! 손들어 움직이면 쏜다"
        else:
            warning_message = ""

        # 1초마다 측정값 업데이트
        time.sleep(1)

# HTML 템플릿
html_page = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Distance and Temperature Checker</title>
    <meta http-equiv="refresh" content="1">
    <style>
        /* 이미지 위치 설정 */
        .image-temperature {
            position: absolute;
            top: calc(100px + {{ humidity }}px); /* 습도 값 아래 100px */
            left: 0; /* 왼쪽 가장자리 */
            width: 100px;
            height: 100px;
        }

        .image-stop {
            position: absolute;
            top: calc(100px + {{ humidity }}px); /* 습도 값 아래 100px */
            left: 300px; /* temperature.png 기준 오른쪽 300px */
            width: 100px;
            height: 100px;
        }

        .image-break {
            position: absolute;
            top: calc(100px + {{ humidity }}px); /* 습도 값 아래 100px */
            left: 600px; /* STOP.png 기준 오른쪽 300px */
            width: 100px;
            height: 100px;
        }
    </style>
</head>
<body>
    <h1>Distance and Temperature Checker</h1>
    <p>현재 거리: {{ distance }} cm</p>
    <p>현재 온도: {{ temperature }} °C</p>
    <p>현재 습도: {{ humidity }}%</p>

    <!-- 습도 값 아래 이미지 배치 -->
    <img src="{{ url_for('static', filename='temperature.png') }}" alt="Temperature Image" class="image-temperature">
    <img src="{{ url_for('static', filename='STOP.png') }}" alt="STOP Image" class="image-stop">
    <img src="{{ url_for('static', filename='break.png') }}" alt="Break Image" class="image-break">

    <p style="color: red;">{{ warning_message }}</p>
</body>
</html>

'''

# Flask 라우트 설정
@app.route('/')
def index():
    return render_template_string(html_page, distance=int(distance), temperature=int(temperature), humidity=int(humidity), warning_message=warning_message)

# 메인 함수
if __name__ == '__main__':
    # 온/습도 및 거리 측정 스레드 실행
    thread_dht = threading.Thread(target=readDH)
    thread_dht.daemon = True
    thread_dht.start()

    thread_distance = threading.Thread(target=update_sensors)
    thread_distance.daemon = True
    thread_distance.start()

    # Flask 서버 실행
    app.run(host='0.0.0.0', port=5000, debug=True)
