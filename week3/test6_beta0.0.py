from flask import Flask, render_template

app = Flask(__name__)

html_page = '''
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KU Embedded System Controller</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f4e3;
            text-align: center;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #fff;
            border: 1px solid #ddd;
            border-radius: 10px;
        }
        .status {
            display: inline-block;
            width: 48%;
            margin-bottom: 20px;
        }
        .status img {
            width: 30px;
            vertical-align: middle;
        }
        .controls {
            margin-top: 20px;
        }
        .controls .item {
            display: inline-block;
            margin: 10px 20px;
        }
        .item img {
            width: 50px;
        }
        .on {
            color: green;
        }
        .off {
            color: red;
        }
        .mode {
            margin-bottom: 20px;
        }
        .mode span {
            font-size: 1.2em;
            font-weight: bold;
        }
    </style>
</head>
<body>

<div class="container">
    <h1>KU Embedded System Controller</h1>
    
    <div class="mode">
        <div>모드: <span>{{ data['mode'] }}</span></div>
        <button>모드 전환</button>
    </div>

    <div class="status">
        <div><img src="themperature.png" alt="온도"> 온도: {{ data['temperature'] }} &#8451;</div>
        <div><img src="humidity.png" alt="습도"> 습도: {{ data['humidity'] }} %</div>
    </div>

    <div class="status">
        <div><img src="gun.png" alt="침입자 거리"> 침입자 거리: {{ data['intruder_distance'] }} m</div>
    </div>

    <div class="controls">
        <div class="item">
            <img src="break.png" alt="에어컨">
            <div>에어컨: <span class="{{ 'on' if data['aircon_status'] == 'ON' else 'off' }}">{{ data['aircon_status'] }}</span></div>
        </div>
        <div class="item">
            <img src="break.png" alt="히터">
            <div>히터: <span class="{{ 'on' if data['heater_status'] == 'ON' else 'off' }}">{{ data['heater_status'] }}</span></div>
        </div>
        <div class="item">
            <img src="break.png" alt="제습기">
            <div>제습기: <span class="{{ 'on' if data['humidifier_status'] == 'ON' else 'off' }}">{{ data['humidifier_status'] }}</span></div>
        </div>
    </div>
</div>

</body>
</html>

''' 
@app.route('/')
def index():
    data = {
        'temperature': 37.5,
        'humidity': 45.0,
        'intruder_distance': 3.5,
        'aircon_status': 'ON',
        'heater_status': 'OFF',
        'humidifier_status': 'OFF',
        'mode': 'AUTO'
    }
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)