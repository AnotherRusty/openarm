#!/usr/bin/env python
#coding=utf-8

from pynput import keyboard
import yaml
from time import sleep
import sys, os
sys.path.append(os.path.join(sys.path[0], '..', 'armMaster', 'lib'))
from robot import Robot

Terminated = False
ConfigFile = 'config/config.yaml'

MinJointPosition = None
MaxJointPosition = None
CurrentJointPosisitons = []

Increment = None
KeyBindings = {
    'Key.left':(0, False),
    'Key.right':(0, True),
    'Key.up':(1,False),
    'Key.down':(1, True),
    'w':(2, False),
    's':(2, True),
    'a':(3, False),
    'd':(3, True),
    'q':(4, False),
    'e':(4, True)
}

RobotInstance = None

def on_press(key):
    key_type = type(key).__name__
    if (key_type == 'Key'):
        key = str(key)
    elif (key_type == 'KeyCode'):
        key = key.char
    if key in KeyBindings.keys():
        joint = KeyBindings[key][0]
        increase = KeyBindings[key][1]
        if increase:
            CurrentJointPosisitons[joint]+=Increment
            if (CurrentJointPosisitons[joint] > MaxJointPosition):
                CurrentJointPosisitons[joint] = MaxJointPosition
        else:
            CurrentJointPosisitons[joint]-=Increment
            if (CurrentJointPosisitons[joint] < MinJointPosition):
                CurrentJointPosisitons[joint] = MinJointPosition

def on_release(key):
    global Terminated
    if key == keyboard.Key.esc:
        Terminated = True
        return False

KeyListener = keyboard.Listener(on_press=on_press,on_release=on_release)

def setting_up():
    global MinJointPosition, MaxJointPosition, Increment
    global RobotInstance

    with open(ConfigFile) as f:
        conf = yaml.safe_load(f)
        f.close()

    MinJointPosition = int(conf['MinJointPosition'])
    MaxJointPosition = int(conf['MaxJointPosition'])

    Increment = conf['Increment']
    
    start_up_positions = conf['StartUpJointPositions'][:]
    num_of_joints = len(start_up_positions)
    for i in range(num_of_joints):
        CurrentJointPosisitons.append(float(start_up_positions[i]))

    model = conf['Model']
    port = conf['Port']
    baudrate = conf['Baudrate']
    configfile = os.path.join(sys.path[0], '..', 'armMaster', 'config', model+'.yaml')
    RobotInstance = Robot()
    print('Configuring robot ...')
    if not RobotInstance.configure(model, port, baudrate, configfile):
        return
    print('Initializing robot ...')
    if not RobotInstance.initialize():
        return
    sleep(2)
    print('Start ...')
    RobotInstance.start()

    print('Starting keyboard listener ...')
    KeyListener.start()

def control_loop():
    # check for joint position changes and send commands to the robot
    print(CurrentJointPosisitons)

if __name__ == '__main__':
    setting_up()
    
    while not Terminated:
        #control_loop()
        pass

    print("Keyboard control terminated.")