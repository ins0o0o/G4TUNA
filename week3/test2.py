from flask import Flask, render_template_string
import threading
import time
import random

app = Flask(__name__)
flag = 0

html_page = '''
<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Flag Checker</title>
        <meta http-equiv="refresh" content="1">  <!-- 5초마다 페이지 새로고침 -->
    </head>
    <body>
        <h1>Flag Checker</h1>
        <p>현재 Flag 값: {{ flag }}</p>
        <p>이 페이지는 1초마다 새로고침됩니다.</p>
    </body>
    </html>
'''

def generate_flag_values():
    global flag
    while True:
        # 라즈베리파이의 연산을 통해 flag 값을 결정한다고 가정
        flag = random.randint(0, 10)  # 이 부분을 라즈베리파이 연산으로 대체
        time.sleep(5)  # 5초마다 flag 값 전송 (필요에 맞게 조정 가능)

@app.route('/')
def index():
    thread = threading.Thread(target=generate_flag_values)
    thread.daemon = True  # 메인 프로세스 종료 시 자동으로 종료
    thread.start()
    return render_template_string(html_page, flag=flag)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
