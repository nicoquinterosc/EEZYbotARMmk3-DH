import RPi.GPIO as GPIO
import dill
import marshal as ms
import math
import numpy as np
import re
import sympy as sp
import time

d2r = np.deg2rad
r2d = np.degrees

dill.settings['recurse'] = True

fx=dill.load(open("fx", "rb"))
fy=dill.load(open("fy", "rb"))
fz=dill.load(open("fz", "rb"))

print('Loading DH functions...')

# Distancia euclidiana
def distance(p1, p2):
    dist = np.linalg.norm(p1-p2)
    return dist

# Direct kinematics function
def DK(param):
    p0 = param[0]
    p1 = param[1]
    p2 = param[2]
    
    point = []
    point = ([fx(p0, p1, p2),
              fy(p0, p1, p2),
              fz(p0, p1, p2)])
    
    return np.array(point)

def IK(target):
    n_theta = 24

    target = np.array(target)

    print 'total:', n_theta**3

    params = []

    theta1s = np.linspace(d2r(-30), d2r(30), n_theta) # desired range of motion for joint 1
    theta2s = np.linspace(d2r(-36), d2r(56), n_theta) # desired range of motion for joint 2
    theta3s = np.linspace(d2r(-60), d2r(60), n_theta) # desired range of motion for joint 3

    for theta1 in theta1s:
            for theta2 in theta2s:
                for theta3 in theta3s:
                    params.append([theta1, theta2, theta3])

    params = np.array(params)
    np.random.shuffle(params)

    actual_err = 100
    required_err = 0.001

    counter = 0

    points = []

    for param in params:
        points.append(DK(param))
        new_err = distance(DK(param), target)
        counter += 1
        if new_err<actual_err:
            actual_err = new_err
            best_param = param
        if new_err<required_err:
            break

    print 'iteraciones:', counter
    return best_param


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
    def __init__(self, IN1, IN2, IN3, IN4, three_law, setup):
        # Set GPIO pin
        self.pos = 0
        self.setup = setup
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

    def calculateDegrees(self, newpos):
        degrees = newpos - self.pos
        self.pos = newpos
        print 'degrees', degrees
        print 'position', self.pos
        return degrees

    def runDegrees(self, degrees):
        steps = int(abs(math.ceil(degrees*self.three_law)))
        if not self.setup:
            degrees = self.calculateDegrees(degrees)
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

setup = False
# Base motor
xStepper = Stepper(6,13,19,26, 150/50, setup)
# Forward and backward motor
yStepper = Stepper(12,16,20,21, 300/92, setup)
# Up and down motor
zStepper = Stepper(2,3,4,17, 60/12, setup)

if setup:
    while True:
        string = raw_input('Ingresar grados: ')
        regex = re.search(r'(-?)(\w)(\d+)', string)
        motor = regex.group(2)
        degrees = int(regex.group(1)+regex.group(3))
        if motor is 'x':
            xStepper.runDegrees(degrees)
        elif motor is 'y':
            yStepper.runDegrees(degrees)
        elif motor is 'z':
            zStepper.runDegrees(degrees)
else:
    while True:
        x = float(raw_input('Ingresar x: '))/100
        y = float(raw_input('Ingresar y: '))/100
        z = float(raw_input('Ingresar z: '))/100
        target = [x,y,z]
        print 'target point', target
        radparam = IK(target)
        print 'best point', DK(radparam)
        param = r2d(radparam)
        print 'param', param
        xStepper.runDegrees(param[0])
        yStepper.runDegrees(param[1])
        zStepper.runDegrees(param[2])
        print 'degrees x:', xStepper.pos
        print 'degrees y:', yStepper.pos
        print 'degrees z:', zStepper.pos