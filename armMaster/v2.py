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


# load app configuration
with open("config/app.yaml") as f:
    conf = yaml.safe_load(f)
    f.close()

window_size = conf["window_size"]
page_width = conf["page_width"]
page_height = conf["page_height"]

update_interval = conf["update_interval"]
model_list = conf["models"]
port_list = conf["ports"]
baudrate_list = conf["baudrates"]


class ControlPage(Frame):
    def __init__(self, root):
        Frame.__init__(self, width=page_width, height=page_height)
        self._root = root

        self._initialized = False
        self._active = False
    
    '''override'''
    def pack(self):
        self._create()
        super().pack()

    '''override'''
    def pack_forget(self):
        self._destroy()
        super().pack_forget()

    def _create(self):
        self._active = True

        if self._initialized:
            return
         
        if not self._root.robot_is_connected():
            self._root.status_info("机器人未连接。")
            return

        model = self._root.robot_model
        config_file = 'config/'+model+'.yaml'
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

    # control container
        self.control_container = Frame(self)
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
        Button(self.control_container, text="设置", activebackground='grey', command=self._set_joints).grid(row=6, column=0, pady=20, sticky=W+E+N+S)
        Button(self.control_container, text="重置", activebackground='grey', command=self._reset_joints).grid(row=6, column=1, pady=20, sticky=W+E+N+S)
        
        self.control_container.grid(row=0, column=0, rowspan=6, columnspan=2, padx=10, sticky=W+E+N+S)

    # monitor container
        self.monitor_contrainer = Frame(self)
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

    # monitor thread
        self.monit_loop = threading.Thread(name='monitor', target=self._monitor)
        self.monit_loop.setDaemon(True)
        self.monit_loop.start()

    # init complete
        self._initialized = True
    
    def _set_joints(self):
        angles = []
        for i in range(self.num_joints):
            angles.append(self.joint_angles[i].get())
        self._root.get_robot().set_joint_angles(angles) 

    def _reset_joints(self):
        angles = []
        for i in range(self.num_joints):
            self.joint_angles[i].set(90)
            angles.append(90)
        self._root.get_robot().set_joint_angles(angles) 
    
    def _monitor(self):
        t = now()
        while True:
            if (now()- t)>update_interval:
                if not self._active:
                    continue
                current_angles = self._root.get_robot().get_joint_angles()
                if current_angles:
                    for i in range(self.num_joints):
                        self.current_angles[i].set(current_angles[i])
                    t = now()

    def _destroy(self):
        self._active = False

class SettingPage(Frame):
    def __init__(self, root):
        Frame.__init__(self, width=page_width, height=page_height)
        self._root = root

    '''Override'''
    def pack(self):
        self._create()
        super().pack()

    def _create(self):
        # self.robot = Robot()
        Label(self, text="类型").grid(row=0, column=0, pady=20, sticky=W)
        self.robot_model = ttk.Combobox(self, values=model_list)
        self.robot_model.grid(row=0, column=1, pady=20)
        self.robot_model.current(0)

        Label(self, text="端口").grid(row=1, column=0, sticky=W)
        self.port = ttk.Combobox(self, values=port_list)
        self.port.grid(row=1, column=1, sticky=W+E)
        self.port.current(0)

        Label(self, text="波特率").grid(row=2, column=0, pady=5, sticky=W)
        self.baudrate = ttk.Combobox(self, values=baudrate_list)
        self.baudrate.grid(row=2, column=1, pady=5, sticky=W+E)
        self.baudrate.current(4)    # default option 9600

        Button(self, text="连接", width=10, command=self._connect).grid(row=3, column=1, pady=10, sticky=E)

    def _connect(self):
        name = self.robot_model.get()
        port = self.port.get()
        baudrate = self.baudrate.get()

        self._root.connect_robot(name, port, baudrate)


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

        self.robot_model = ""   # todo - get from robot instance
        self._create_gui()

    def start(self):
        self.status_info('欢迎使用armMaster!')
        self._root.mainloop()

    def get_robot(self):
        if self._robot is None:
            messagebox.showerror("InternalErr", "No robot instance!")
        else:
            return self._robot

    def robot_is_connected(self):
        return self._connected

    def connect_robot(self, name, port, baudrate):
        self.robot_model = name # to be optimised

        # create robot 
        if self._robot is None:
            self._robot = Robot()
            if not self._robot.configure(name, port, baudrate):
                self.status_error("配置机械臂参数失败。检查参数设置是否正确。")
                return
            if not self._robot.initialize():
                self.status_error("机械臂初始化失败。检查USB是否连接，端口及波特率是否正确。")
            else:
                self._robot.start()
                self.status_info("机械臂就绪 型号：{} 端口：{} 波特率：{}".format(name, port, baudrate))
                self._connected = True
        else:
            # 是否需要建立新的连接？
            yes = messagebox.askokcancel("提示","已连接机械臂，是否建立新连接？")
            if yes:
                pass

    def status_info(self, val):
        self._statusbar.config(bg='white')
        self._statustext.set(val)

    def status_error(self, val):
        self._statusbar.config(bg='Red')
        self._statustext.set(val)

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

    def _control(self):
        self._change_page(self._control_page)

    def _setting(self):
        self._change_page(self._setting_page)
    
    def _exit(self):
        self._root.quit()

    def _change_page(self, page):
        self._current_page.pack_forget()
        self._current_page = page
        self._current_page.pack()


if __name__ == "__main__":
    app = Application()
    app.start()
