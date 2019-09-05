#coding=utf-8

import sys
if sys.version > '3':   # python 2.x
    import Tkinter as tk
    from Tkinter import *
    import ttk
else:                   # python 3.x
    import tkinter as tk
    from tkinter import *
    from tkinter import ttk

import yaml
import os, platform, sys
from lib.robot import Robot
import threading
from time import time as now, sleep

WINDOW_SIZE = "600x400" # width*height
UPDATE_INTERVAL = 0.5 # seconds


class Application(object):
    def __init__(self, master=None, robot=None):
        self.root = master
        self.robot = robot

        config_file = 'config/'+self.robot.name+'.conf.yaml'
        with open(config_file) as f:
            conf = yaml.safe_load(f)
            f.close()

        self.joints = conf['Joints']
        self.num_joints = len(self.joints)
        self.joint_scales = []
        self.joint_angles = [IntVar() for i in range(self.num_joints)]
        self.current_angles = [IntVar() for i in range(self.num_joints)]
        self.joint_progresses = []
        self.joint_feedback = []

        self.monit_loop = threading.Thread(name='monitor', target=self.monitor)
        self.monit_loop.setDaemon(True)

        self.robot.initialize()
        sleep(2)
        self.robot.start()
        self.init_gui()

    def init_gui(self):
    # control
        self.control_container = Frame(self.root)
        # joint scales
        for i in range(self.num_joints):
            Label(self.control_container, text=self.joints[i]["name"]).grid(row=i, column=0, padx=10, pady=10)
            sc = Scale(self.control_container, orient=HORIZONTAL, sliderlength=10, resolution=1, \
                            from_=self.joints[i]['params']['min_angle'], \
                                to=self.joints[i]['params']['max_angle'], \
                                    variable=self.joint_angles[i])
            sc.grid(row=i, column=1, pady=10)
            sc.set(self.joints[i]['params']['norm'])
            self.joint_scales.append(sc)
        
        # set button
        Button(self.control_container, text="设置", activebackground='grey', command=self.set_joints).grid(row=6, column=0, pady=20, sticky=W+E+N+S)
        Button(self.control_container, text="重置", activebackground='grey', command=self.reset_joints).grid(row=6, column=1, pady=20, sticky=W+E+N+S)
        
        self.control_container.grid(row=0, column=0, rowspan=6, columnspan=2, padx=10, sticky=W+E+N+S)

    # monitor
        self.monitor_contrainer = Frame(self.root)
        # current angles info
        Label(self.monitor_contrainer, text='当前关节角度: ').grid(row=0, column=1)
        for i in range(self.num_joints):
            pb = ttk.Progressbar(self.monitor_contrainer, orient=HORIZONTAL, maximum=180, length=300, mode='determinate', variable=self.current_angles[i])
            pb.grid(row=i+1, column=1, pady=20)
            self.joint_progresses.append(pb)
            lb = Label(self.monitor_contrainer, width=10, textvariable=self.current_angles[i])
            lb.grid(row=i+1, column=2, pady=20)
            self.joint_feedback.append(lb)

        self.monitor_contrainer.grid(row=0, column=2, rowspan=6, columnspan=3, padx=30, sticky=W+E+N+S)

    def loop(self):
        self.monit_loop.start()
        self.root.mainloop()
    
    def set_joints(self):
        angles = []
        for i in range(self.num_joints):
            angles.append(self.joint_angles[i].get())
        self.robot.set_joint_angles(angles)

    def reset_joints(self):
        angles = []
        for i in range(self.num_joints):
            self.joint_angles[i].set(90)
            angles.append(90)
        self.robot.set_joint_angles(angles) 

    def monitor(self):
        t = now()
        while True:
            if (now()- t)>UPDATE_INTERVAL:
                current_angles = self.robot.get_joint_angles()
                if current_angles:
                    for i in range(self.num_joints):
                        self.current_angles[i].set(current_angles[i])
                    t = now()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry(WINDOW_SIZE)
    root.title("ArmMaster - OPENARM control console")
    sysstr = platform.system()
    if sysstr == "Windows":
        root.iconbitmap(bitmap='res/logo.ico')
    elif sysstr == "Linux":
        root.iconbitmap(bitmap='@res/logo.xbm')

    robot = Robot()
    robot.configure(name='neo5', port='/dev/ttyUSB0', baudrate=9600)

    app = Application(master=root, robot=robot)
    app.loop()
