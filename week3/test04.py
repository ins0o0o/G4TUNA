from flask import Flask, render_template_string, url_for, redirect
import RPi.GPIO as GPIO

# GPIO 설정
GPIO.setmode(GPIO.BCM)
sensDH = 6

GPIO.setup(sensDH, GPIO.IN)
def readDH():
    sensor = Adafruit_DHT.DHT11  # sensor 객체 생성
    humidity, temperature = Adafruit_DHT.read_retry(sensor, sensDH)
    return humidity, temperature



# LED 상태 업데이트 함수
def updateLeds():
    for num, value in enumerate(ledStates):
        GPIO.output(ledPin[num], value)

# HTML 페이지 템플릿
html_page = '''
<!doctype html>
<html>
<head>
    <title>Humidity and Temperature Sensor</title>
</head>
<body>
    <h1>Embedded System Humidity and Temperature Sensor</h1>
    <hr>
    <div style="padding-left:20px;">
        <h3>Humidity and Temperature</h3>
        <p>
            <b>Humidity:</b> 
            <a href="{{ url_for('ledswitch', LEDN=0, state=1) }}"><input type="button" value="ON"></a>
            <a href="{{ url_for('ledswitch', LEDN=0, state=0) }}"><input type="button" value="OFF"></a>
        </p>
        <p>
            <b>LED2:</b> 
            <a href="{{ url_for('ledswitch', LEDN=1, state=1) }}"><input type="button" value="ON"></a>
            <a href="{{ url_for('ledswitch', LEDN=1, state=0) }}"><input type="button" value="OFF"></a>
        </p>
    </div>
</body>
</html>
'''

app = Flask(__name__)

# 메인 페이지 라우트
@app.route('/')
def index():
    return render_template_string(html_page, ledStates=ledStates)

# LED 스위치 라우트
@app.route('/<int:LEDN>/<int:state>')
def ledswitch(LEDN, state):
    ledStates[LEDN] = state
    updateLeds()
    return redirect(url_for('index'))