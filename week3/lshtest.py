from flask import Flask, render_template_string, url_for, redirect
import threading
import time
import random

ledRed = 17
ledYello = 27
ledGreen = 22

sensTouch = 5
sensDH = 6

DistanceTrig = 23
DistanceEcho = 24


button_states = {
    'button1': True,
    'button2': False,
    'button3': False,
    'button4': True,
    'button5': False
}

humidity = 0
temperature = 0
distance = 0

def measure_DH():
    global temperature
    while True:
        temperature = random.randint(1,50)
        if button_states['button4'] == True:
            if temperature > 25:
                button_states['button5'] = True
            else:
                button_states['button5'] = False
        time.sleep(2)

DH_thread = threading.Thread(target=measure_DH)
DH_thread.daemon = True  # 메인 스레드가 종료되면 이 스레드도 종료되도록 설정
DH_thread.start()

def measure_distance():
    global distance
    while True:
        distance = random.randint(1,20)
        if button_states['button1'] == True:
                if distance < 10:
                    button_states['button2'] = False
                    button_states['button3'] = True
                elif distance > 10:
                    button_states['button2'] = True
                    button_states['button3'] = False
        time.sleep(2)

distance_thread = threading.Thread(target=measure_distance)
distance_thread.daemon = True  # 메인 프로세스 종료 시 자동으로 종료
distance_thread.start()


app = Flask(__name__)

@app.route('/')
def index():
    html = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="refresh" content="1">
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
        <h1>G4TUNA WEEK3</h1>
        <p>거리: {{distance}} </p>
        <p>온도: {{temperature}} </p>

        <form method="POST" action="/toggle_button1">
            <div class="switch-container">
                <label class="switch">
                    <input type="checkbox" name="button1" {% if button_states['button1'] %}checked{% endif %} 
                    onchange="this.form.submit()">
                    <span class="slider"></span>
                </label>
                <span class="label-text">ADAS</span>
            </div>
        </form>

        <form method="POST" action="/toggle_button2">
            <div class="switch-container">
                <label class="switch">
                    <input type="checkbox" name="button2" {% if button_states['button2'] %}checked{% endif %} 
                    onchange="this.form.submit()">
                    <span class="slider"></span>
                </label>
                <span class="label-text">Acceration</span>
            </div>
        </form>

        <form method="POST" action="/toggle_button3">
            <div class="switch-container">
                <label class="switch">
                    <input type="checkbox" name="button3" {% if button_states['button3'] %}checked{% endif %} 
                    onchange="this.form.submit()">
                    <span class="slider"></span>
                </label>
                <span class="label-text">Break</span>
            </div>
        </form>

        <form method="POST" action="/toggle_button4">
            <div class="switch-container">
                <label class="switch">
                    <input type="checkbox" name="button4" {% if button_states['button4'] %}checked{% endif %} 
                    onchange="this.form.submit()">
                    <span class="slider"></span>
                </label>
                <span class="label-text">Auto Air Conditional</span>
            </div>
        </form>

        <form method="POST" action="/toggle_button5">
            <div class="switch-container">
                <label class="switch">
                    <input type="checkbox" name="button5" {% if button_states['button5'] %}checked{% endif %} 
                    onchange="this.form.submit()">
                    <span class="slider"></span>
                </label>
                <span class="label-text">Air Conditional</span>
            </div>
        </form>

    </body>
    </html>
    '''
    
    return render_template_string(html, button_states=button_states, distance=round(distance,2), temperature=temperature)

@app.route('/toggle_button1', methods=['POST'])
def toggle_button1():
    global button_states
    button_states['button1'] = not button_states['button1']  # 상태 토글
    return redirect(url_for('index'))

@app.route('/toggle_button2', methods=['POST'])
def toggle_button2():
    global button_states
    button_states['button1'] = False
    button_states['button2'] = not button_states['button2']
    return redirect(url_for('index'))

@app.route('/toggle_button3', methods=['POST'])
def toggle_button3():
    global button_states
    button_states['button1'] = False
    button_states['button3'] = not button_states['button3']
    return redirect(url_for('index'))

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
