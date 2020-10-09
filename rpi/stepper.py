import RPi.GPIO as GPIO
import time
import math
import re

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# adjust if different
StepCount = 8
Seq = range(0, StepCount)
Seq[0] = [1,0,0,0]
Seq[1] = [1,1,0,0]
Seq[2] = [0,1,0,0]
Seq[3] = [0,1,1,0]
Seq[4] = [0,0,1,0]
Seq[5] = [0,0,1,1]
Seq[6] = [0,0,0,1]
Seq[7] = [1,0,0,1]

class Stepper:
    def __init__(self, IN1, IN2, IN3, IN4, three_law):
        # Set GPIO pin
        self.pos = 0
        self.three_law = three_law
        self.delay = 0.001
        self.IN1 = IN1
        self.IN2 = IN2
        self.IN3 = IN3
        self.IN4 = IN4
        GPIO.setup(IN1, GPIO.OUT)  # blue
        GPIO.setup(IN2, GPIO.OUT) # white
        GPIO.setup(IN3, GPIO.OUT) # yellow
        GPIO.setup(IN4, GPIO.OUT) # red
        print('GPIO pinout set as output')

    def setStep(self, w1, w2, w3, w4):
        GPIO.output(self.IN1, w1)
        GPIO.output(self.IN2, w2)
        GPIO.output(self.IN3, w3)
        GPIO.output(self.IN4, w4)

    def CW(self, steps):
        for _ in range(steps):
            for j in range(StepCount):
                self.setStep(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
                time.sleep(self.delay)

    def CCW(self, steps):
        for _ in range(steps):
            for j in reversed(range(StepCount)):
                self.setStep(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
                time.sleep(self.delay)

    def runDegrees(self, degrees):
        steps = int(abs(math.ceil(degrees*self.three_law)))
        self.pos += degrees
        self.CW(steps) if degrees > 0 else self.CCW(steps)

    def runSteps(self, steps):
        _steps = abs(steps)
        self.pos += steps
        self.CW(_steps) if steps > 0 else self.CCW(_steps)

def degreesToSteps(degrees):
    result = (degrees*512) / 360
    steps = int(abs(math.ceil(result)))
    return steps

print(degreesToSteps(360))

#xStepper = Stepper(4,17,23,24)
zStepper = Stepper(2,3,4,17, 60/12)
yStepper = Stepper(12,16,20,21, 300/92)
xStepper = Stepper(6,13,19,26, 150/50)

# while True:
#     string = raw_input('Ingresar grados: ')
#     regex = re.search(r'(-?)(\w)(\d+)', string)
#     motor = regex.group(2)
#     degrees = int(regex.group(1)+regex.group(3))
#     if motor is 'x':
#         xStepper.runDegrees(degrees)
#     elif motor is 'y':
#         yStepper.runDegrees(degrees)
#     elif motor is 'z':
#         zStepper.runDegrees(degrees)

while True:
    x = raw_input('Ingresar x: ')
    y = raw_input('Ingresar y: ')
    z = raw_input('Ingresar z: ')
    target = [x,y,z]
    print(target)
    # motor = regex.group(2)
    # degrees = int(regex.group(1)+regex.group(3))
    # if motor is 'x':
    #     xStepper.runDegrees(degrees)
    # elif motor is 'y':
    #     yStepper.runDegrees(degrees)
    # elif motor is 'z':
    #     zStepper.runDegrees(degrees)