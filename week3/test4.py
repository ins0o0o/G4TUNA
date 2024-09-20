from flask import Flask, render_template_string, url_for, redirect
import RPi.GPIO as GPIO
import threading
import time
import Adafruit_DHT

# GPIO 설정
GPIO.setmode(GPIO.BCM)
sensDH = 6

humidity = 0
temperature = 0

GPIO.setup(sensDH, GPIO.IN)
def readDH():
    sensor = Adafruit_DHT.DHT11  # sensor 객체 생성
    global humidity
    global temperature
    while True: #0.5초마다 온도와 습도 값을 불러옴
        humidity, temperature = Adafruit_DHT.read_retry(sensor, sensDH)
        time.sleep(0.5)



# HTML 페이지 템플릿
html_page = '''
<!doctype html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Humidity and Temperature Sensor</title>
        <meta http-equiv="refresh" content="1">
    </head>
    <body>
        <h1>Embedded System Humidity and Temperature Sensor</h1>        
        <ul>
            <li>Humidity: {{Humidity}}</li>
            <li>Temperature: {{Temperature}}</li>
        </ul>
    </body>
</html>
'''

app = Flask(__name__)

# 메인 페이지 라우트
@app.route('/')
def index():
    thread = threading.Thread(target=readDH)
    thread.daemon = True  # 메인 프로세스 종료 시 자동으로 종료
    thread.start()
    return render_template_string(html_page, Humidity = humidity, Temperature = temperature)

# LED 스위치 라우트
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
