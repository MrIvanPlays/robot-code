#!/usr/bin/env python3

import RPi.GPIO as GPIO

# If IN11=True and IN21=False, then front right motor moves forwards
# If IN11=False and IN21=True, then front right motor moves backwards
IN11 = 16  # GPIO23 - front right wheel direction
IN21 = 18  # GPIO24 - front right wheel direction

# If IN31=True and IN41=False, then front left wheel moves forwards
# If IN31=False and IN41=True, then front left motor moves backwards
IN31 = 13  # GPIO 27 - front left wheel direction
IN41 = 15  # GPIO 22 - front left wheel direction

ENA1 = 12  # GPIO 18 to ENA PWM speed of front right motor
ENB1 = 32  # GPIO 12 to ENB PWM speed of front left motor

# If IN12=True and IN22=False, then back right motor moves forwards
# If IN12=False and IN22=True, then back right motor moves backwards
IN12 = 29  # GPIO 5 - back right wheel direction
IN22 = 31  # GPIO 6 - back right wheel direction

# If IN32=True and IN42=False, then back left motor moves forwards
# If IN32=False and IN42=True, then back left motor moves backwards
IN32 = 36  # GPIO 16 - back left wheel direction
IN42 = 22  # GPIO 25 - back left wheel direction

ENA2 = 35  # GPIO 19 to ENA PWM speed of back right motor
ENB2 = 33  # GPIO 13 to ENB PWM speed of back left motor


def initialize():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    GPIO.setup(IN11, GPIO.OUT)
    GPIO.setup(IN21, GPIO.OUT)
    GPIO.setup(IN31, GPIO.OUT)
    GPIO.setup(IN41, GPIO.OUT)
    GPIO.setup(IN12, GPIO.OUT)
    GPIO.setup(IN22, GPIO.OUT)
    GPIO.setup(IN32, GPIO.OUT)
    GPIO.setup(IN42, GPIO.OUT)

    GPIO.setup(ENA1, GPIO.OUT)
    GPIO.setup(ENB1, GPIO.OUT)
    GPIO.setup(ENA2, GPIO.OUT)
    GPIO.setup(ENB2, GPIO.OUT)


initialize()

frontRightMotor = GPIO.PWM(ENA1, 1000)
frontLeftMotor = GPIO.PWM(ENB1, 1000)

backRightMotor = GPIO.PWM(ENA2, 1000)
backLeftMotor = GPIO.PWM(ENB2, 1000)

print("Start motors")
frontRightMotor.start(0)
frontLeftMotor.start(0)
backRightMotor.start(0)
backLeftMotor.start(0)


def stop():
    initialize()

    GPIO.output(IN11, False)
    GPIO.output(IN21, False)
    GPIO.output(IN31, False)
    GPIO.output(IN41, False)
    GPIO.output(IN12, False)
    GPIO.output(IN22, False)
    GPIO.output(IN32, False)
    GPIO.output(IN42, False)


def cleanup():
    GPIO.cleanup()


def forward(duty_cycle):
    frontRightMotor.ChangeDutyCycle(duty_cycle)
    frontLeftMotor.ChangeDutyCycle(duty_cycle)
    backRightMotor.ChangeDutyCycle(duty_cycle)
    backLeftMotor.ChangeDutyCycle(duty_cycle)

    initialize()

    GPIO.output(IN11, False)
    GPIO.output(IN21, True)
    GPIO.output(IN31, True)
    GPIO.output(IN41, False)
    GPIO.output(IN12, True)
    GPIO.output(IN22, False)
    GPIO.output(IN32, False)
    GPIO.output(IN42, True)


def backward(duty_cycle):
    frontRightMotor.ChangeDutyCycle(duty_cycle)
    frontLeftMotor.ChangeDutyCycle(duty_cycle)
    backRightMotor.ChangeDutyCycle(duty_cycle)
    backLeftMotor.ChangeDutyCycle(duty_cycle)

    initialize()

    GPIO.output(IN11, True)
    GPIO.output(IN21, False)
    GPIO.output(IN31, False)
    GPIO.output(IN41, True)
    GPIO.output(IN12, False)
    GPIO.output(IN22, True)
    GPIO.output(IN32, True)
    GPIO.output(IN42, False)


# makes front right and back left motor turn forward
def right(duty_cycle):
    frontRightMotor.ChangeDutyCycle(duty_cycle)
    backLeftMotor.ChangeDutyCycle(duty_cycle)

    initialize()

    GPIO.output(IN11, False)
    GPIO.output(IN21, False)
    GPIO.output(IN31, True)
    GPIO.output(IN41, False)
    GPIO.output(IN12, True)
    GPIO.output(IN22, False)
    GPIO.output(IN32, False)
    GPIO.output(IN42, False)


# makes front and back left motors to turn forward
def parallel_right(duty_cycle):
    frontLeftMotor.ChangeDutyCycle(duty_cycle)
    backLeftMotor.ChangeDutyCycle(duty_cycle)

    initialize()

    GPIO.output(IN11, False)
    GPIO.output(IN21, False)
    GPIO.output(IN31, True)
    GPIO.output(IN41, False)
    GPIO.output(IN12, False)
    GPIO.output(IN22, False)
    GPIO.output(IN32, True)
    GPIO.output(IN42, False)


# Makes front left and back right motor turn forward
def left(duty_cycle):
    frontLeftMotor.ChangeDutyCycle(duty_cycle)
    backRightMotor.ChangeDutyCycle(duty_cycle)

    initialize()

    GPIO.output(IN11, False)
    GPIO.output(IN21, True)
    GPIO.output(IN31, False)
    GPIO.output(IN41, False)
    GPIO.output(IN12, False)
    GPIO.output(IN22, False)
    GPIO.output(IN32, False)
    GPIO.output(IN42, True)


# makes front and back right motors to turn forward
def parallel_left(duty_cycle):
    frontRightMotor.ChangeDutyCycle(duty_cycle)
    frontLeftMotor.ChangeDutyCycle(duty_cycle)
    backRightMotor.ChangeDutyCycle(duty_cycle)
    backLeftMotor.ChangeDutyCycle(duty_cycle)

    initialize()

    GPIO.output(IN11, True)
    GPIO.output(IN21, False)

    GPIO.output(IN31, False)
    GPIO.output(IN41, True)

    GPIO.output(IN12, False)
    GPIO.output(IN22, True)

    GPIO.output(IN32, True)
    GPIO.output(IN42, False)
