from flask import Flask
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
ledPin = [18, 23]
ledStates = [0, 0]

GPIO.setup(ledPin[0], GPIO.OUT)
GPIO.setup(ledPin[1], GPIO.OUT)

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World'

@app.route('/LED1on')
def LED1on():
    GPIO.output(ledPin[0], 1)
    return 'Here is LED 1 ON page'

@app.route('/LED1off')
def LED1off():
    GPIO.output(ledPin[0], 0)
    return 'Here is LED 1 OFF page'

@app.route('/LED2on')
def LED2on():
    GPIO.output(ledPin[1], 1)
    return 'Here is LED 2 ON page'

@app.route('/LED2off')
def LED2off():
    GPIO.output(ledPin[1], 0)
    return 'Here is LED 2 OFF page'
