#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import time

from bottle import get, post, run, request, template

from components.listener import KeyListener
from components.vehicle import Car


# 直接测试，Web业务
def main():
    # 初始化
    car = Car()
    keyboard_control = KeyListener(car)

    # 网络服务初始化
    @get("/")
    def index():
        return template("panels/index")

    @post("/cmd")
    def cmd():
        button_pressed = request.body.read().decode()
        print("按下了按钮:" + button_pressed)
        car.move(button_pressed)
        return "OK"

    run(host="0.0.0.0", port=12345)


if __name__ == '__main__':
    main()
