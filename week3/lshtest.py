from flask import Flask, render_template_string, redirect, url_for, request

app = Flask(__name__)

# 전역 변수로 버튼 상태 관리
button_states = {
    'button1': True,
    'button2': False,
    'button3': True,
    'button4': False
}
humidity = 42
temperature = 27
distance = 13

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
                <span class="label-text">Button 1</span>
            </div>
        </form>

        <form method="POST" action="/toggle_button2">
            <div class="switch-container">
                <label class="switch">
                    <input type="checkbox" name="button2" {% if button_states['button2'] %}checked{% endif %} 
                    onchange="this.form.submit()">
                    <span class="slider"></span>
                </label>
                <span class="label-text">Button 2</span>
            </div>
        </form>

        <form method="POST" action="/toggle_button3">
            <div class="switch-container">
                <label class="switch">
                    <input type="checkbox" name="button3" {% if button_states['button3'] %}checked{% endif %} 
                    onchange="this.form.submit()">
                    <span class="slider"></span>
                </label>
                <span class="label-text">Button 3</span>
            </div>
        </form>

        <form method="POST" action="/toggle_button4">
            <div class="switch-container">
                <label class="switch">
                    <input type="checkbox" name="button4" {% if button_states['button4'] %}checked{% endif %} 
                    onchange="this.form.submit()">
                    <span class="slider"></span>
                </label>
                <span class="label-text">Button 4</span>
            </div>
        </form>

    </body>
    </html>
    '''
    
    return render_template_string(html, button_states=button_states)

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
    app.run(debug=True)
