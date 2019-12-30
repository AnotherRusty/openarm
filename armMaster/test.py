#!/usr/bin/env python3
#coding=utf-8

from opmlib.robot import Robot
import random
from time import sleep

NUM = 5

robot = Robot()
robot.configure(name='neo5', port='/dev/ttyACM0', baudrate=9600)
robot.initialize()
robot.start()

sleep(3)

while True:
    angles = [random.randint(30,150) for i in range(NUM)]
    neo5.set_joint_angles(angles)
    sleep(2)