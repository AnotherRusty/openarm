#!/usr/bin/env python3
#coding=utf-8

from opmlib.robot import Robot
import random
from time import sleep

NUM = 5

neo5 = Robot()
neo5.configure(name='neo5', port='/dev/ttyACM0', baudrate=9600)
neo5.initialize()
neo5.start()

sleep(5)

while True:
    angles = [random.randint(30,150) for i in range(NUM)]
    neo5.set_joint_angles(angles)
    sleep(2)