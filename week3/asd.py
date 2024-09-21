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

button_states = {
    'button1': True,
    'button2': False,
    'button3': False,
    'button4': True,
    'button5': False
}

AutoAccBrk = 0  # 차간 거리 유지 ON / OFF
AutoAC = 0      # 에어컨 자동 ON / OFF

humidity = 0
temperature = 0
distance = 0

def check_touch():
    global button_states
    while True:
        GPIO.wait_for_edge(sensTouch, GPIO.FALLING)  # 버튼이 눌렸을 때까지 대기 (FALLING 엣지 감지)
        button_states['button1'] = not button_states['button1']  # button_states['button1'] 값 토글
        time.sleep(0.2)

touch_thread = threading.Thread(target=check_touch)
touch_thread.daemon = True  # 메인 스레드가 종료되면 이 스레드도 종료되도록 설정
touch_thread.start()

def measure_DH():
    sensor = Adafruit_DHT.DHT11
    global temperature
    global humidity
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, sensDH)
        if button_states['button4'] == True:
            if temperature > 25:
                button_states['button5'] = True
            else:
                button_states['button5'] = False
        time.sleep(0.2)

DH_thread = threading.Thread(target=measure_DH)
DH_thread.daemon = True  # 메인 스레드가 종료되면 이 스레드도 종료되도록 설정
DH_thread.start()

def measure_distance():
    global distance
    while True:
        GPIO.output(DistanceTrig, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(DistanceTrig, GPIO.HIGH)
        time.sleep(0.00001)  # 10μs 대기
        GPIO.output(DistanceTrig, GPIO.LOW)
        while GPIO.input(DistanceEcho) == GPIO.LOW:
            pulse_start = time.time()  # Echo 핀이 LOW에서 HIGH로 바뀌는 순간 기록
        while GPIO.input(DistanceEcho) == GPIO.HIGH:
            pulse_end = time.time()  # Echo 핀이 HIGH에서 LOW로 바뀌는 순간 기록
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 34300 / 2
        
        if button_states['button1'] == True:
                if distance < 10:
                    button_states['button2'] = False
                    button_states['button3'] = True
                elif distance > 10:
                    button_states['button2'] = True
                    button_states['button3'] = False
        time.sleep(0.2)

distance_thread = threading.Thread(target=measure_distance)
distance_thread.daemon = True  # 메인 프로세스 종료 시 자동으로 종료
distance_thread.start()

app = Flask(__name__)

@app.route('/')
def index():
    GPIO.output(ledGreen, button_states['button2'])
    GPIO.output(ledRed, button_states['button3'])
    GPIO.output(ledYello, button_states['button5'])
    html = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="refresh" content="1">
        <title>G4TUNA WEEK3</title>
        <style>
            body {
                background-color: #C8BFE7; /* 배경색 설정 */
            }
            .container {
                display: flex;
                justify-content: center;
                align-items: center;
                flex-wrap: wrap;
                margin-top: -60px; /* button2,3,5의 위치 조정을 위해 125px 아래로 이동 */
            }
            .module {
                margin: 10px;
                text-align: center;
            }
            .container .module {
                margin-right: 75px; /* button2,3,5 사이의 간격을 75px로 설정 */
            }
            .container .module:last-child {
                margin-right: 0; /* 마지막 버튼에는 margin-right를 적용하지 않음 */
            }
            .top-buttons {
                display: flex;
                justify-content: center;
                margin-top: 50px; /* 제목 바로 밑에 배치 */
            }
            .top-buttons .module {
                margin-right: 150px; /* button1과 button4 사이 간격 150px */
            }
            .top-buttons .module:last-child {
                margin-right: 0; /* 마지막 버튼에는 margin-right를 적용하지 않음 */
            }
            img {
                width: 100px; /* 이미지 크기 */
            }
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
                background-color: #4CAF50;
            }
            input:checked + .slider:before {
                transform: translateX(26px);
            }
            .label-text {
                margin-top: 8px;
                font-size: 16px;
            }
            .distance-section {
                display: flex;
                align-items: center;
                margin-left: 150px; /* button4 옆 150px 간격으로 위치 */
                margin-top: 20px; /* 간격 추가 */
            }
            .distance-section img {
                margin-right: 10px;
            }
            .temperature-section {
                display: flex;
                align-items: center;
                margin-left: 150px;
                margin-top: 100px; /* distance 섹션과의 간격 */
            }
            .temperature-section img {
                margin-right: 10px;
            }
            .info-text {
                font-size: 15px; /* 폰트를 15로 설정 */
            }
        </style>
    </head>
    <body>
        <h1 style="text-align: center;">G4TUNA WEEK3</h1>
    
        <!-- Button 1, Button 4 - ADAS, Auto Air Conditional -->
        <div class="top-buttons">
            <div class="module">
                <form method="POST" action="/toggle_button1">
                    <label class="switch">
                        <input type="checkbox" name="button1" {% if button_states['button1'] %}checked{% endif %} onchange="this.form.submit()">
                        <span class="slider"></span>
                    </label>
                    <div class="label-text">ADAS</div>
                </form>
            </div>
            <div class="module">
                <form method="POST" action="/toggle_button4">
                    <label class="switch">
                        <input type="checkbox" name="button4" {% if button_states['button4'] %}checked{% endif %} onchange="this.form.submit()">
                        <span class="slider"></span>
                    </label>
                    <div class="label-text">Auto Air Conditional</div>
                </form>
            </div>
        </div>
    
        <!-- Distance Section -->
        <div class="distance-section">
            <img src="{{ url_for('static', filename='distance.png') }}" alt="Distance">
            <p class="info-text">거리: {{distance}} cm</p>
        </div>
    
        <!-- Temperature Section -->
        <div class="temperature-section">
            <img src="{{ url_for('static', filename='temperature.png') }}" alt="Temperature">
            <p class="info-text">온도: {{temperature}} °C</p>
        </div>
    
        <!-- Button 2, 3, 5 - 아래 125px 밑에 배치, 간격 75px -->
        <div class="container">
            <div class="module">
                <img src="{{ url_for('static', filename='break.png') }}">
                <form method="POST" action="/toggle_button2">
                    <label class="switch">
                        <input type="checkbox" name="button2" {% if button_states['button2'] %}checked{% endif %} onchange="this.form.submit()">
                        <span class="slider"></span>
                    </label>
                    <div class="label-text">Acceration</div>
                </form>
            </div>
            <div class="module">
                <img src="{{ url_for('static', filename='break.png') }}">
                <form method="POST" action="/toggle_button3">
                    <label class="switch">
                        <input type="checkbox" name="button3" {% if button_states['button3'] %}checked{% endif %} onchange="this.form.submit()">
                        <span class="slider"></span>
                    </label>
                    <div class="label-text">Break</div>
                </form>
            </div>
            <div class="module">
                <img src="{{ url_for('static', filename='break.png') }}">
                <form method="POST" action="/toggle_button5">
                    <label class="switch">
                        <input type="checkbox" name="button5" {% if button_states['button5'] %}checked{% endif %} onchange="this.form.submit()">
                        <span class="slider"></span>
                    </label>
                    <div class="label-text">Air Conditional</div>
                </form>
            </div>
        </div>
    </body>
    </html>


    '''
    
    return render_template_string(html, button_states=button_states, distance=round(distance,2), temperature=temperature, humidity=humidity)

# 버튼 1의 상태를 토글하는 라우트
@app.route('/toggle_button1', methods=['POST'])
def toggle_button1():
    global button_states
    button_states['button1'] = not button_states['button1']  # 상태 토글
    return redirect(url_for('index'))

# 버튼 2의 상태를 토글하는 라우트
@app.route('/toggle_button2', methods=['POST'])
def toggle_button2():
    global button_states
    button_states['button1'] = False
    button_states['button2'] = not button_states['button2']
    return redirect(url_for('index'))

# 버튼 3의 상태를 토글하는 라우트
@app.route('/toggle_button3', methods=['POST'])
def toggle_button3():
    global button_states
    button_states['button1'] = False
    button_states['button3'] = not button_states['button3']
    return redirect(url_for('index'))

# 버튼 4의 상태를 토글하는 라우트
@app.route('/toggle_button4', methods=['POST'])
def toggle_button4():
    global button_states
    button_states['button4'] = not button_states['button4']
    return redirect(url_for('index'))

@app.route('/toggle_button5', methods=['POST'])
def toggle_button5():
    global button_states
    button_states['button4'] = False
    button_states['button5'] = not button_states['button5']
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
