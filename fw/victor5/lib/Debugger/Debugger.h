/* OPENARM Firmware *****************
    -Arm model: Victor
    -Version 1.0

    Danny @ openarm 2019
************************************/
#ifndef DEBUGGER_H_
#define DEBUGGER_H_

#include <Arduino.h>
#include "Config.h"


class Debugger
{
public:
    static Debugger* get(){
        static Debugger instance;
        return &instance;
    }

    int printf(char *fmt, ...);

private:
    Debugger();
    char sprint_buf[1024];
};

#endif