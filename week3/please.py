from flask import Flask, render_template_string, url_for, redirect
import RPi.GPIO as GPIO
import threading
import time
import Adafruit_DHT

app = Flask(__name__)

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
distance = 0
warning_message = ""

html_page = '''
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>G4TUNA Dashboard</title>
    <style>
        .container {
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-top: 50px;
        }
        .row {
            display: flex;
            justify-content: space-between;
            margin: 20px 0;
        }
        .image-slider-container {
            display: flex;
            justify-content: space-around;
            width: 100%;
        }
        .image-slider-container img {
            width: 100px;
            height: 100px;
        }
        .slider-container {
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>G4TUNA</h1>
        <div class="row">
            <label for="systemSlider">전체 동작</label>
            <input type="checkbox" id="systemSlider" onchange="toggleSystem()" />
        </div>
        <div class="row">
            <p>온도: <span id="temperature">0</span>°C</p>
            <p>습도: <span id="humidity">0</span>%</p>
            <p>거리: <span id="distance">0</span>cm</p>
        </div>
        <div class="image-slider-container">
            <div class="slider-container">
                <img src="{{ url_for('static', filename='temperature.png') }}" alt="Temperature">
                <br>
                <input type="checkbox" id="temperatureSlider" disabled>
            </div>
            <div class="slider-container">
                <img src="{{ url_for('static', filename='STOP.png') }}" alt="STOP">
                <br>
                <input type="checkbox" id="stopSlider" disabled>
            </div>
            <div class="slider-container">
                <img src="{{ url_for('static', filename='break.png') }}" alt="Break">
                <br>
                <input type="checkbox" id="breakSlider" disabled>
            </div>
        </div>
    </div>

    <script>
        var systemOn = false;

        function toggleSystem() {
            systemOn = !systemOn;
            if (systemOn) {
                document.getElementById('temperatureSlider').disabled = true;
                document.getElementById('stopSlider').disabled = true;
                document.getElementById('breakSlider').disabled = true;
            } else {
                document.getElementById('temperatureSlider').disabled = false;
                document.getElementById('stopSlider').disabled = false;
                document.getElementById('breakSlider').disabled = false;
            }
        }

        function updateSliders(temperature, distance) {
            var tempSlider = document.getElementById('temperatureSlider');
            var stopSlider = document.getElementById('stopSlider');
            var breakSlider = document.getElementById('breakSlider');
            
            // 온도가 24도 이상이면 temperature slider ON
            if (temperature >= 24 && systemOn) {
                tempSlider.checked = true;
            } else if (systemOn) {
                tempSlider.checked = false;
            }

            // 거리가 25cm 미만일 때 STOP slider ON
            if (distance < 25 && systemOn) {
                stopSlider.checked = true;
                breakSlider.checked = false;
            } else if (systemOn) {
                stopSlider.checked = false;
                breakSlider.checked = true;
            }
        }

        function fetchSensorData() {
            fetch('/')
            .then(response => response.json())
            .then(data => {
                document.getElementById('temperature').innerText = data.temperature;
                document.getElementById('humidity').innerText = data.humidity;
                document.getElementById('distance').innerText = data.distance;
                updateSliders(data.temperature, data.distance);
            })
            .catch(error => console.error('Error fetching sensor data:', error));
        }

        setInterval(fetchSensorData, 500); // 0.5초마다 갱신
    </script>
</body>
</html>
'''


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


def measure_distance():
    global distance
    # Trig 핀을 LOW로 설정하고 짧은 시간 대기
    while True:
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
        time.sleep(0.5)

distance_thread = threading.Thread(target=measure_distance)
distance_thread.daemon = True  # 메인 프로세스 종료 시 자동으로 종료
distance_thread.start() 
GPIO.setup(DistanceTrig, GPIO.OUT)
GPIO.setup(DistanceEcho, GPIO.IN)

distance = 0  # 거리 값을 저장할 변수
warning_message = ""  # 경고 메시지를 저장할 변수

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
