#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'xianglun918'

import RPi.GPIO as GPIO


# 自定义的模式及控制GPIO引脚
GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)
WHEELS = ((27, 22, 18, "leftWheel"), (23, 24, 13, "rightWheel"))

# 定义轮子
class Wheel:
    def __init__(self, pin1, pin2, pwm_pin=None, name='New wheel'):
        self._pin1 = pin1
        self._pin2 = pin2
        # Setup
        print('Setup %s...' % name)
        GPIO.setup(self._pin1, GPIO.OUT)
        GPIO.setup(self._pin2, GPIO.OUT)
        if pwm_pin:
            # fq是初始设定频率，频率越高响应速度越快；dc是占空比（调整速度）
            GPIO.setup(pwm_pin, GPIO.OUT)
            self.fq, self.dc = 50, 50 # 单位分别是 ms, %
            self.pwm = GPIO.PWM(pwm_pin, self.fq) # self.pwm.ChangeFrequency, self.pwm.ChangeDutyCycle
            self.pwm.start(self.dc)
    
    def forward(self):
        GPIO.output(self._pin1, GPIO.HIGH)
        GPIO.output(self._pin2, GPIO.LOW)

    def backward(self):
        GPIO.output(self._pin1, GPIO.LOW)
        GPIO.output(self._pin2, GPIO.HIGH)
    
    def stop(self):
        GPIO.output(self._pin1, GPIO.LOW)
        GPIO.output(self._pin2, GPIO.LOW)

    def accelerate(self):
        self.dc = min(100, self.dc + 5)
        self.pwm.ChangeDutyCycle(self.dc)
        
    def decelerate(self):
        self.dc = max(0, self.dc - 5)
        self.pwm.ChangeDutyCycle(self.dc)
    



# 定义Car 类
class Car(object):
    def __init__(self):
        print("Initialize the car...")
        self.leftWheel = Wheel(*WHEELS[0])
        self.rightWheel = Wheel(*WHEELS[1])

    # 小车前进
    def forward(self):
        print('Moving forward...')
        self.leftWheel.forward()
        self.rightWheel.forward()

    #  小车左拐
    def leftTurn(self):
        print("Turn left...")
        self.leftWheel.backward()
        self.rightWheel.forward()

    # 小车右拐
    def rightTurn(self):
        print('Turn right...')
        self.leftWheel.forward()
        self.rightWheel.backward()

    # 小车后退
    def backward(self):
        print('Moving backward...')
        self.leftWheel.backward()
        self.rightWheel.backward()
    
    # 小车停止
    def stop(self):
        print('Stop...')
        self.leftWheel.stop()
        self.rightWheel.stop()
    
    # 小车加速
    def accelerate(self):
        print('Accelerating...')
        self.leftWheel.accelerate()
        self.rightWheel.accelerate()

    # 小车减速
    def decelerate(self):
        print('Deccelerating...')
        self.leftWheel.decelerate()
        self.rightWheel.decelerate()
    
    # 执行具体命令
    def move(self, status):
        # 这里有些线接的有些错位，所以改成错位了。
        options = {
            'forward': self.backward,
            'leftTurn': self.rightTurn,
            'rightTurn': self.leftTurn,
            'backward': self.forward,
            'stop': self.stop,
            'accelerate': self.accelerate,
            'decelerate': self.decelerate
        }
        options[status]()   

