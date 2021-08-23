#!/usr/bin/python
# -*- coding: utf-8 -*-
import time, os
from bottle import get, post, run, request, template
from components.vehicle import Car
from components.listener import KeyListener

# 直接测试，Web业务
def main():

    # 初始化
    car = Car()
    keyboard_control = KeyListener(car)

    # 网络服务初始化
    @get("/")
    def index():
        return template("index")
        
    @post("/cmd")
    def cmd():
        adss=request.body.read().decode()
        print("按下了按钮:"+adss)
        car.move(adss)
        return "OK"
        
    run(host="0.0.0.0", port=12345)


if __name__ == '__main__':
    main()
