#!/usr/bin/env python
#coding=utf-8

from pynput import keyboard

Terminated = False

def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def on_release(key):
    global Terminated
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        Terminated = True
        return False


if __name__ == '__main__':
    with keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
        listener.join()

    while not Terminated:
        pass

    print("Keyboard control terminated.")