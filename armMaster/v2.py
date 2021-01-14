#coding=utf-8

import sys
if sys.version < '3':   # python 2.x
    import Tkinter as tk
    from Tkinter import *
    import tkMessageBox as messagebox
    import ttk
else:                   # python 3.x
    import tkinter as tk
    from tkinter import *
    from tkinter import messagebox
    from tkinter import ttk

import yaml
import os, platform, sys
from lib.robot import Robot
import threading
from time import time as now, sleep


window_size = "600x400"
page_width = 600
page_height = 300

UPDATE_INTERVAL = 0.5 # seconds
MODEL_LIST = ["victor", "neo"]
PORT_LIST = ["/dev/openarm", "/dev/ttyUSB0", "/dev/ttyACM0"]
BAUDRATE_LIST = [300, 1200, 2400, 4800, 9600, 14400, 19200, 28800, 38400, 57600, 115200]


class ControlPage(Frame):
    def __init__(self, root):
        Frame.__init__(self, width=page_width, height=page_height)
        self._root = root
        self._create()

    def _create(self):
        pass


class SettingPage(Frame):
    def __init__(self, root):
        Frame.__init__(self, width=page_width, height=page_height)
        self._root = root
        self._create()
    
    def _create(self):
        # self.robot = Robot()
        Label(self, text="类型").grid(row=0, column=0, pady=20, sticky=W)
        self.robot_model = ttk.Combobox(self, values=MODEL_LIST)
        self.robot_model.grid(row=0, column=1, pady=20)
        self.robot_model.current(0)

        Label(self, text="端口").grid(row=1, column=0, sticky=W)
        self.port = ttk.Combobox(self, values=PORT_LIST)
        self.port.grid(row=1, column=1, sticky=W+E)
        self.port.current(0)

        Label(self, text="波特率").grid(row=2, column=0, pady=5, sticky=W)
        self.baudrate = ttk.Combobox(self, values=BAUDRATE_LIST)
        self.baudrate.grid(row=2, column=1, pady=5, sticky=W+E)
        self.baudrate.current(4)    # default option 9600

        Button(self, text="连接", width=10, command=self._connect).grid(row=3, column=1, pady=10, sticky=E)

    def _connect(self):
        model = self.robot_model.get()
        port = self.port.get()
        baudrate = self.baudrate.get()

        #self._root.get_robot()

        self._root._status_info("连接机械臂 型号：{} 端口：{} 波特率：{}".format(self.robot_model.get(), self.port.get(), self.baudrate.get()))


class Application(object):
    _root = tk.Tk()

    def __init__(self):
        self._root.geometry(window_size)
        self._root.title("ArmMaster - 机械臂测试程序")
        self._root.resizable(0, 0)
        sysstr = platform.system()
        if sysstr == "Windows":
            self._root.iconbitmap(bitmap='res/logo.ico')
        elif sysstr == "Linux":
            self._root.iconbitmap(bitmap='@res/logo.xbm')

        self._connected = False
        self._robot = None

        self._create_gui()

    def start(self):
        self._status_info('欢迎使用armMaster!')
        self._root.mainloop()

    def _create_gui(self):
        # 页面
        self._control_page = ControlPage(self)
        self._setting_page = SettingPage(self)
        self._current_page = self._setting_page
        self._current_page.pack()

        # 菜单栏
        self._menubar = tk.Menu(self._root)
        self._menubar.add_command(label="控制", command=self._control)
        self._menubar.add_command(label="设置", command=self._setting)
        self._menubar.add_command(label="退出", command=self._exit)
        self._root.config(menu=self._menubar)

        # 状态栏
        self._statustext = StringVar()
        self._statusbar = Label(self._root, textvariable=self._statustext, bd=1, anchor=W)
        self._statusbar.pack(side=BOTTOM, fill=X)

    def get_robot(self):
        if self._robot is None:
            messagebox.showerror("InternalErr", "No robot instance!")
        else:
            return self._robot

    def _control(self):
        self._change_page(self._control_page)

    def _setting(self):
        self._change_page(self._setting_page)
    
    def _exit(self):
        self._root.quit()

    def _status_info(self, val):
        self._statusbar.config(bg='white')
        self._statustext.set(val)

    def _status_error(self, val):
        self._statusbar.config(bg='Red')
        self._statustext.set(val)

    def _change_page(self, page):
        self._current_page.pack_forget()
        self._current_page = page
        self._current_page.pack()


if __name__ == "__main__":
    app = Application()
    app.start()
