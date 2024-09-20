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

humidity = 0
temperature = 0
distance = 0

ledStates = [0, 0, 0]  # Red, Yellow, Green LED 상태

# LED 상태 업데이트 함수
def updateLeds():
    GPIO.output(ledRed, ledStates[0])
    GPIO.output(ledYello, ledStates[1])
    GPIO.output(ledGreen, ledStates[2])

# 터치 센서 스레드
def check_touch():
    global button_states
    while True:
        GPIO.wait_for_edge(sensTouch, GPIO.FALLING)
        button_states['button1'] = not button_states['button1']
        time.sleep(0.2)

touch_thread = threading.Thread(target=check_touch)
touch_thread.daemon = True
touch_thread.start()

# 거리 측정 스레드
def measure_distance():
    sensor = Adafruit_DHT.DHT11
    global button_states
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

        if button_states['button1'] == True:
            if distance < 10:
                button_states['button2'] = False
                ledStates[0] = 1  # Red LED ON
                button_states['button3'] = True
                ledStates[2] = 0  # Green LED OFF
            elif distance > 10:
                button_states['button2'] = True
                ledStates[0] = 0  # Red LED OFF
                button_states['button3'] = False
                ledStates[2] = 1  # Green LED ON
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

    <form method="POST" action="/toggle_led/0">
        <p>Red LED: {% if ledStates[0] == 1 %} ON {% else %} OFF {% endif %} 
        <input type="submit" value="{% if ledStates[0] == 1 %} Turn OFF {% else %} Turn ON {% endif %}"></p>
    </form>

    <form method="POST" action="/toggle_led/1">
        <p>Yellow LED: {% if ledStates[1] == 1 %} ON {% else %} OFF {% endif %} 
        <input type="submit" value="{% if ledStates[1] == 1 %} Turn OFF {% else %} Turn ON {% endif %}"></p>
    </form>

    <form method="POST" action="/toggle_led/2">
        <p>Green LED: {% if ledStates[2] == 1 %} ON {% else %} OFF {% endif %} 
        <input type="submit" value="{% if ledStates[2] == 1 %} Turn OFF {% else %} Turn ON {% endif %}"></p>
    </form>
</body>
</html>
'''

# 메인 페이지 라우트
@app.route('/')
def index():
    return render_template_string(html_page, ledStates=ledStates, distance=distance, temperature=temperature)

# LED 토글 라우트
@app.route('/toggle_led/<int:led>', methods=['POST'])
def toggle_led(led):
    ledStates[led] = 1 if ledStates[led] == 0 else 0
    updateLeds()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
