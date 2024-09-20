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
ledPin = [ledRed, ledYello, ledGreen]
ledStates = [0, 0, 0]  # Red, Yellow, Green 순서로 상태 저장

GPIO.setup(ledPin[0], GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ledPin[1], GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ledPin[2], GPIO.OUT, initial=GPIO.LOW)

GPIO.setup(sensTouch, GPIO.IN)
GPIO.setup(sensDH, GPIO.IN)
GPIO.setup(DistanceTrig, GPIO.OUT)
GPIO.setup(DistanceEcho, GPIO.IN)

AutoAccBrk = 0  # 차간 거리 유지 ON / OFF
AutoAC = 0      # 에어컨 자동 ON / OFF

humidity = 0
temperature = 0
distance = 0

# LED 상태 업데이트 함수
def updateLeds():
    for num, value in enumerate(ledStates):
        GPIO.output(ledPin[num], value)

# 터치 센서 스레드
def check_touch():
    while True:
        GPIO.wait_for_edge(sensTouch, GPIO.FALLING)
        ledStates[0] = not ledStates[0]  # 터치 시 Red LED 토글
        updateLeds()
        time.sleep(0.2)

touch_thread = threading.Thread(target=check_touch)
touch_thread.daemon = True  # 메인 스레드 종료 시 자동 종료
touch_thread.start()

# 거리 측정 스레드
def measure_distance():
    sensor = Adafruit_DHT.DHT11
    global distance
    global temperature
    global humidity
    
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, sensDH)

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
        distance = pulse_duration * 34300 / 2

        if distance < 10:
            ledStates[0] = 1  # Red LED ON
            ledStates[2] = 0  # Green LED OFF
        elif distance < 30:
            ledStates[2] = 1  # Green LED ON
            ledStates[0] = 0  # Red LED OFF
        updateLeds()
        
        time.sleep(0.2)

measure_thread = threading.Thread(target=measure_distance)
measure_thread.daemon = True
measure_thread.start()

app = Flask(__name__)

# HTML 페이지 템플릿
html_page = '''
<!doctype html>
<html>
<head>
    <title>LED Controller</title>
</head>
<body>
    <h1>G4TUNA WEEEK3</h1>
    <p>거리: {{distance}} cm</p>
    <p>온도: {{temperature}} °C</p>

    <div style="padding-left:20px;">
        <p>
            <b>Red LED: {% if ledStates[0]==1 %} ON {% else %} OFF {% endif %}</b> 
            <a href="{{ url_for('ledswitch', LEDN=0, state=1) }}"><input type="button" value="ON"></a>
            <a href="{{ url_for('ledswitch', LEDN=0, state=0) }}"><input type="button" value="OFF"></a>
        </p>
        <p>
            <b>Yellow LED: {% if ledStates[1]==1 %} ON {% else %} OFF {% endif %}</b> 
            <a href="{{ url_for('ledswitch', LEDN=1, state=1) }}"><input type="button" value="ON"></a>
            <a href="{{ url_for('ledswitch', LEDN=1, state=0) }}"><input type="button" value="OFF"></a>
        </p>
        <p>
            <b>Green LED: {% if ledStates[2]==1 %} ON {% else %} OFF {% endif %}</b> 
            <a href="{{ url_for('ledswitch', LEDN=2, state=1) }}"><input type="button" value="ON"></a>
            <a href="{{ url_for('ledswitch', LEDN=2, state=0) }}"><input type="button" value="OFF"></a>
        </p>
    </div>
</body>
</html>
'''

# 메인 페이지 라우트
@app.route('/')
def index():
    return render_template_string(html_page, ledStates=ledStates, distance=distance, temperature=temperature)

# LED 스위치 라우트
@app.route('/<int:LEDN>/<int:state>')
def ledswitch(LEDN, state):
    ledStates[LEDN] = state
    updateLeds()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
