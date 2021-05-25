#!/usr/bin/env python
#coding=utf-8

from pynput import keyboard
import yaml

Terminated = False
ConfigFile = 'config/config.yaml'

CurrentJointPosisitons = []

Increment = 0.1
KeyBindings = {
    'Key.left':(0, False),
    'Key.right':(0, True),
    'Key.up':(1,False),
    'Key.down':(1, True),
    'q':(2, False),
    'a':(2, True),
    'w':(3, False),
    's':(3, True),
    'Key.ctrl_l':(4, False),
    'Key.space':(4, True)
}


def on_press(key):
    key = str(key).strip("'")
    if key in KeyBindings.keys():
        joint = KeyBindings[key][0]
        increase = KeyBindings[key][1]
        if increase:
            CurrentJointPosisitons[joint]+=Increment
        else:
            CurrentJointPosisitons[joint]-=Increment

def on_release(key):
    global Terminated
    if key == keyboard.Key.esc:
        Terminated = True
        return False

KeyListener = keyboard.Listener(on_press=on_press,on_release=on_release)

def setting_up():
    with open(ConfigFile) as f:
        conf = yaml.safe_load(f)
        f.close()

    start_up_positions = conf['StartUpJointPositions'].copy()
    num_of_joints = len(start_up_positions)
    for i in range(num_of_joints):
        CurrentJointPosisitons.append(float(start_up_positions[i]))

    KeyListener.start()

def control_loop():
    # check for joint position changes and send commands to the robot
    print(CurrentJointPosisitons)


if __name__ == '__main__':
    setting_up()
    
    while not Terminated:
        control_loop()

    print("Keyboard control terminated.")