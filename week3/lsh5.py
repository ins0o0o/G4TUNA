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
    'button3': True,
    'button4': False
}

AutoAccBrk = 0  # 차간 거리 유지 ON / OFF
AutoAC = 0      # 에어컨 자동 ON / OFF

humidity = 0
temperature = 0
distance = 0

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

@app.route('/')
def index():
    html = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Slide Toggle Buttons</title>
        <style>
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

            /* 스타일 버튼 옆에 텍스트 추가 */
            .label-text {
                margin-left: 10px;
                vertical-align: middle;
                font-size: 16px;
            }

            .switch-container {
                margin: 10px 0;
            }
        </style>
    </head>
    <body>
        <h1>Slide Toggle Buttons</h1>

        <form method="POST" action="/toggle_button1">
            <div class="switch-container">
                <label class="switch">
                    <input type="checkbox" name="button1" {% if button_states['button1'] %}checked{% endif %} 
                    onchange="this.form.submit()">
                    <span class="slider"></span>
                </label>
                <span class="label-text">AUTO</span>
            </div>
        </form>

        <form method="POST" action="/toggle_button2">
            <div class="switch-container">
                <label class="switch">
                    <input type="checkbox" name="button2" {% if button_states['button2'] %}checked{% endif %} 
                    onchange="this.form.submit()">
                    <span class="slider"></span>
                </label>
                <span class="label-text">거리: {{ distance }}</span>
            </div>
        </form>

        <form method="POST" action="/toggle_button3">
            <div class="switch-container">
                <label class="switch">
                    <input type="checkbox" name="button3" {% if button_states['button3'] %}checked{% endif %} 
                    onchange="this.form.submit()">
                    <span class="slider"></span>
                </label>
                <span class="label-text">온도: {{ temperature }}</span>
            </div>
        </form>

        <form method="POST" action="/toggle_button4">
            <div class="switch-container">
                <label class="switch">
                    <input type="checkbox" name="button4" {% if button_states['button4'] %}checked{% endif %} 
                    onchange="this.form.submit()">
                    <span class="slider"></span>
                </label>
                <span class="label-text">습도: {{ humidity }}</span>
            </div>
        </form>

    </body>
    </html>
    '''
    
    return render_template_string(html, button_states=button_states, distance=distance, temperature=temperature, humidity=humidity)

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
    button_states['button1'] = False
    button_states['button4'] = not button_states['button4']
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
