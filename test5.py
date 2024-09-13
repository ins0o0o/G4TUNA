import RPi.GPIO as GPIO
import time
import Adafruit_DHT

sensDH = 6

GPIO.setmode(GPIO.BCM)
GPIO.setup(sensDH, GPIO.IN)

def readDH():
    sensor = Adafruit_DHT.DHT11
    humidity, temperature = Adafruit_DHT.read_retry(sensor, sensDH)
    print('온도:{0:0.1f}도, 습도:{1:0.1f}%'.format(temperature, humidity))

while True:
    readDH()
    time.sleep(1)