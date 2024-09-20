from flask import Flask, render_template_string
import RPi.GPIO as GPIO
import threading
import time

sensTouch = 5
flag = 0

html_page = '''
<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Flag Checker</title>
        <meta http-equiv="refresh" content="1">  <!-- 1초마다 페이지 새로고침 -->
    </head>
    <body>
        <h1>Flag Checker</h1>
        <p>{% if flag==1 %} 터치됨 {% else %} 터치안됨 {% endif %}</p>
        <p>이 페이지는 1초마다 새로고침됩니다.</p>
    </body>
    </html>
'''

def generate_flag_values():
    global flag
    while True:
        if GPIO.input(sensTouch) == 1:
            flag = 1
        else:
            flag = 0
        time.sleep(0.1)



app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string(html_page, flag=flag)

if __name__ == '__main__':
    thread = threading.Thread(target=generate_flag_values)
    thread.daemon = True  # 메인 프로세스 종료 시 자동으로 종료
    thread.start()
    app.run(host='0.0.0.0', port=5000, debug=True)
