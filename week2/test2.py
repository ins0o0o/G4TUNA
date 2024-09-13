import RPi.GPIO as GPIO
import time

ledRed = 17
ledYello = 27
ledGreen = 22

buttonPin = 5

GPIO.setmode(GPIO.BCM)
GPIO.setup(ledRed, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ledYello, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ledGreen, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(buttonPin, GPIO.IN)

while True:
    if GPIO.input(buttonPin) == 1:
        GPIO.output(ledRed, GPIO.HIGH)
        GPIO.output(ledYello, GPIO.HIGH)
        GPIO.output(ledGreen, GPIO.HIGH)
    else:
        GPIO.output(ledRed, GPIO.LOW)
        GPIO.output(ledYello, GPIO.LOW)
        GPIO.output(ledGreen, GPIO.LOW)
