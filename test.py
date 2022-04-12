#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import time
import sys

from bottle import get, post, run, request, template
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

while True:
    # 自定义的模式及控制GPIO引脚
    GPIO.setup(18, GPIO.OUT)
    GPIO.output(18, GPIO.HIGH)
