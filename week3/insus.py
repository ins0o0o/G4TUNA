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
            warning_message = "Warning!"
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
    <style>
        /* 스위치 스타일 */
        .switch {
            position: relative;
            display: inline-block;
            width: 60px;
            height: 34px;
        }
        .switch input { 
            opacity: 0;
            width: 0;
            height: 0;
        }
        .slider {
            position: absolute;
            cursor: pointer;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: #ccc;
            transition: .4s;
            border-radius: 34px;
        }
        .slider:before {
            position: absolute;
            content: "";
            height: 26px;
            width: 26px;
            left: 4px;
            bottom: 4px;
            background-color: white;
            transition: .4s;
            border-radius: 50%;
        }
        input:checked + .slider {
            background-color: #2196F3;
        }
        input:checked + .slider:before {
            transform: translateX(26px);
        }

        /* 이미지 위치 설정 */
        .image {
            display: none; /* 기본적으로 숨김 */
            width: 100px;
            height: 100px;
            position: absolute;
            top: 250px;
        }
        .image-temperature {
            left: 0;
        }
        .image-stop {
            left: 300px;
        }
        .image-break {
            left: 600px;
        }
        .warning-text {
            position: absolute;
            top: 360px;
            left: 300px;
            color: red;
            font-size: 18px;
            font-weight: bold;
            display: none;
        }
    </style>
</head>
<body>
    <h1>Distance and Temperature Checker</h1>
    <label class="switch">
        <input type="checkbox" id="toggleSwitch">
        <span class="slider"></span>
    </label>

    <p>현재 거리: {{ distance }} cm</p>
    <p>현재 온도: {{ temperature }} °C</p>
    <p>현재 습도: {{ humidity }}%</p>

    <img src="{{ url_for('static', filename='temperature.png') }}" alt="Temperature Image" id="temperatureImage" class="image image-temperature">
    <img src="{{ url_for('static', filename='STOP.png') }}" alt="STOP Image" id="stopImage" class="image image-stop">
    <img src="{{ url_for('static', filename='break.png') }}" alt="Break Image" id="breakImage" class="image image-break">
    <p id="warningText" class="warning-text">Warning!</p>

    <script>
        document.getElementById('toggleSwitch').addEventListener('change', function() {
            var temperatureImage = document.getElementById('temperatureImage');
            var stopImage = document.getElementById('stopImage');
            var breakImage = document.getElementById('breakImage');
            var warningText = document.getElementById('warningText');
            var temperature = {{ temperature }};
            var distance = {{ distance }};

            if (this.checked) {
                // Toggle ON: Display all images
                temperatureImage.style.display = 'block';
                stopImage.style.display = 'block';
                breakImage.style.display = 'block';
                warningText.style.display = 'block';
            } else {
                // Toggle OFF: Display based on conditions
                temperatureImage.style.display = temperature >= 24 ? 'block' : 'none';
                stopImage.style.display = distance < 50 ? 'block' : 'none';
                breakImage.style.display = distance >= 50 ? 'block' : 'none';
                warningText.style.display = distance < 10 ? 'block' : 'none';
            }
        });
    </script>
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
