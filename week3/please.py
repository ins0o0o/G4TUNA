from flask import Flask, render_template_string, jsonify
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

        /* 슬라이더 스타일 */
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
    </style>
</head>
<body>
    <div class="container">
        <h1>Embeded CAR Controller</h1>
        <div class="row">
            <label for="systemSlider">Automation</label>
            <label class="switch">
                <input type="checkbox" id="systemSlider" checked onchange="toggleSystem()" />
                <span class="slider"></span>
            </label>
        </div>
        <div class="row">
            <p>온도: <span id="temperature">0</span>°C</p>
            <p>습도: <span id="humidity">0</span>%</p>
            <p>거리: <span id="distance">0</span>cm</p>
        </div>
        <div class="image-slider-container">
            <div class="slider-container">
                <p>에어컨</p> <!-- 에어컨 표시 -->
                <img src="{{ url_for('static', filename='temperature.png') }}" alt="Temperature">
                <br>
                <label class="switch">
                    <input type="checkbox" id="temperatureSlider" disabled>
                    <span class="slider"></span>
                </label>
            </div>
            <div class="slider-container">
                <p>브레이크</p> <!-- 브레이크 표시 -->
                <img src="{{ url_for('static', filename='STOP.png') }}" alt="STOP">
                <br>
                <label class="switch">
                    <input type="checkbox" id="stopSlider" disabled>
                    <span class="slider"></span>
                </label>
            </div>
            <div class="slider-container">
                <p>엑셀</p> <!-- 엑셀 표시 -->
                <img src="{{ url_for('static', filename='break.png') }}" alt="Break">
                <br>
                <label class="switch">
                    <input type="checkbox" id="breakSlider" disabled>
                    <span class="slider"></span>
                </label>
            </div>
        </div>
    </div>

    <script>
        var systemOn = true; // 시작 상태를 ON으로 설정

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
            
            // 온도가 28도 이상이면 temperature slider ON
            if (temperature >= 28 && systemOn) {
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
            fetch('/sensor_data')
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
        GPIO.wait_for_edge(sensTouch, GPIO.FALLING)
        flag = 1 - flag
        if flag == 1:
            print("\n<<< Process Start!! >>>\n")
        else:
            print("\n<<< Process Terminated >>>\n")
        time.sleep(0.5)

touch_thread = threading.Thread(target=check_touch)
touch_thread.daemon = True
touch_thread.start()

def readDH():
    sensor = Adafruit_DHT.DHT11
    global humidity
    global temperature
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, sensDH)
        time.sleep(0.5)

DH_thread = threading.Thread(target=readDH)
DH_thread.daemon = True
DH_thread.start()

def measure_distance():
    global distance
    while True:
        GPIO.output(DistanceTrig, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(DistanceTrig, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(DistanceTrig, GPIO.LOW)
        
        while GPIO.input(DistanceEcho) == GPIO.LOW:
            pulse_start = time.time()
        while GPIO.input(DistanceEcho) == GPIO.HIGH:
            pulse_end = time.time()
        
        pulse_duration = pulse_end - pulse_start
        distance = int(pulse_duration * 34300 / 2)
        time.sleep(0.5)

distance_thread = threading.Thread(target=measure_distance)
distance_thread.daemon = True
distance_thread.start()

@app.route('/')
def index():
    return render_template_string(html_page)

@app.route('/sensor_data')
def sensor_data():
    return jsonify({
        'temperature': temperature,
        'humidity': humidity,
        'distance': distance
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
