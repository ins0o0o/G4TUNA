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

distance_thread = threading.Thread(target=measure_distance)
distance_thread.daemon = True  # 메인 프로세스 종료 시 자동으로 종료
distance_thread.start()

# HTML 페이지 템플릿
html_page = '''
<!doctype html>
<html>
<head>
    <title>LED Controller</title>
</head>
<body>
    <h1>Embedded System LED Controller</h1>
    <hr>
    <div style="padding-left:20px;">
        <h3>LED1, LED2</h3>
        <p>
            <b>LED1: {% if ledStates[0]==1 %} ON {% else %} OFF {% endif %}</b> 
            <a href="{{ url_for('ledswitch', LEDN=0, state=1) }}"><input type="button" value="ON"></a>
            <a href="{{ url_for('ledswitch', LEDN=0, state=0) }}"><input type="button" value="OFF"></a>
        </p>
        <p>
            <b>LED2: {% if ledStates[1]==1 %} ON {% else %} OFF {% endif %}</b> 
            <a href="{{ url_for('ledswitch', LEDN=1, state=1) }}"><input type="button" value="ON"></a>
            <a href="{{ url_for('ledswitch', LEDN=1, state=0) }}"><input type="button" value="OFF"></a>
        </p>
        <p>
            <b>LED3: {% if ledStates[2]==1 %} ON {% else %} OFF {% endif %}</b> 
            <a href="{{ url_for('ledswitch', LEDN=2, state=1) }}"><input type="button" value="ON"></a>
            <a href="{{ url_for('ledswitch', LEDN=2, state=0) }}"><input type="button" value="OFF"></a>
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
