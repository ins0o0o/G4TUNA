from flask import Flask, render_template_string, url_for, redirect, jsonify
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
    return jsonify(button_states)

# 버튼 1의 상태를 토글하는 라우트
@app.route('/toggle_button1', methods=['GET'])
def toggle_button1():
    global button_states
    button_states['button1'] = not button_states['button1']  # 상태 토글
    return redirect(url_for('index'))

# 버튼 2의 상태를 토글하는 라우트
@app.route('/toggle_button2', methods=['GET'])
def toggle_button2():
    global button_states
    button_states['button1'] = False
    button_states['button2'] = not button_states['button2']
    return redirect(url_for('index'))

# 버튼 3의 상태를 토글하는 라우트
@app.route('/toggle_button3', methods=['GET'])
def toggle_button3():
    global button_states
    button_states['button1'] = False
    button_states['button3'] = not button_states['button3']
    return redirect(url_for('index'))

# 버튼 4의 상태를 토글하는 라우트
@app.route('/toggle_button4', methods=['GET'])
def toggle_button4():
    global button_states
    button_states['button4'] = not button_states['button4']
    return redirect(url_for('index'))

@app.route('/toggle_button5', methods=['GET'])
def toggle_button5():
    global button_states
    button_states['button4'] = False
    button_states['button5'] = not button_states['button5']
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
