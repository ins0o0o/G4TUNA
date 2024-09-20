from flask import Flask, render_template_string, jsonify
import RPi.GPIO as GPIO
import threading
import time
import Adafruit_DHT

app = Flask(__name__)

# GPIO 핀 설정
ledRed = 17      # 브레이크
ledYello = 27    # 에어컨
ledGreen = 22    # 액셀

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

humidity = 0
temperature = 0
distance = 0

# HTML 페이지
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
            <p>온도: <span id="temperature">0</span>°C</p>
            <p>습도: <span id="humidity">0</span>%</p>
            <p>거리: <span id="distance">0</span>cm</p>
        </div>
        <div class="image-slider-container">
            <div class="slider-container">
                <p>에어컨</p>
                <label class="switch">
                    <input type="checkbox" id="acSlider" onchange="toggleAC()" />
                    <span class="slider"></span>
                </label>
            </div>
            <div class="slider-container">
                <p>브레이크</p>
                <label class="switch">
                    <input type="checkbox" id="brakeSlider" onchange="toggleBrake()" />
                    <span class="slider"></span>
                </label>
            </div>
            <div class="slider-container">
                <p>액셀</p>
                <label class="switch">
                    <input type="checkbox" id="accelSlider" onchange="toggleAccel()" />
                    <span class="slider"></span>
                </label>
            </div>
        </div>
    </div>

    <script>
        function toggleAC() {
            var acSlider = document.getElementById('acSlider').checked;
            fetch('/toggle_ac?status=' + acSlider);
        }

        function toggleBrake() {
            var brakeSlider = document.getElementById('brakeSlider').checked;
            fetch('/toggle_brake?status=' + brakeSlider);
        }

        function toggleAccel() {
            var accelSlider = document.getElementById('accelSlider').checked;
            fetch('/toggle_accel?status=' + accelSlider);
        }

        function fetchSensorData() {
            fetch('/sensor_data')
            .then(response => response.json())
            .then(data => {
                document.getElementById('temperature').innerText = data.temperature;
                document.getElementById('humidity').innerText = data.humidity;
                document.getElementById('distance').innerText = data.distance;
            })
            .catch(error => console.error('Error fetching sensor data:', error));
        }

        setInterval(fetchSensorData, 500); // 0.5초마다 갱신
    </script>
</body>
</html>
'''

# GPIO 제어 함수들
@app.route('/toggle_ac')
def toggle_ac():
    status = request.args.get('status') == 'true'
    GPIO.output(ledYello, GPIO.HIGH if status else GPIO.LOW)  # 에어컨 슬라이더 상태에 따른 LED 제어
    return jsonify({'status': status})

@app.route('/toggle_brake')
def toggle_brake():
    status = request.args.get('status') == 'true'
    GPIO.output(ledRed, GPIO.HIGH if status else GPIO.LOW)  # 브레이크 슬라이더 상태에 따른 LED 제어
    return jsonify({'status': status})

@app.route('/toggle_accel')
def toggle_accel():
    status = request.args.get('status') == 'true'
    GPIO.output(ledGreen, GPIO.HIGH if status else GPIO.LOW)  # 액셀 슬라이더 상태에 따른 LED 제어
    return jsonify({'status': status})

# 센서 데이터를 JSON 형태로 반환
@app.route('/sensor_data')
def sensor_data():
    return jsonify({
        'temperature': temperature,
        'humidity': humidity,
        'distance': distance
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
