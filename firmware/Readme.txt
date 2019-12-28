DOC 6001-0000-0900
OPENARM, COPYRIGHT 2019

#单片机代码教程


###开发环境：
openarm单片机（Arduino UNO / mega2560）源码用platformio开发。

首先需要安装vscode，https://code.visualstudio.com
安装完成后在扩展插件（Extension）中搜索并安装platformio IDE


###编译上传
安装platformio插件后打开源码文件夹，例如firmware/victor(neo)/
点击下方 √ 进行编译
成功后点击 → 进行烧录


###代码解析
以victor(neo)机械臂代码为例：
源码文件目录
├── lib
│   ├── Config
│   │   └── Config.h
│   ├── Debugger
│   │   ├── Debugger.cpp
│   │   └── Debugger.h
│   ├── Gateway
│   │   ├── Gateway.cpp
│   │   ├── Gateway.h
│   │   └── Protocol.h
│   ├── Interface
│   │   ├── IJoint.h
│   │   ├── IObserver.h
│   │   └── ITransport.h
│   ├── Joystick
│   │   ├── Joystick.cpp
│   │   ├── Joystick.h
│   │   └── PS2X_lib
│   │       ├── examples
│   │       │   ├── PS2X_Example
│   │       │   │   └── PS2X_Example.ino
│   │       │   └── PS2XMouse
│   │       │       └── PS2XMouse.ino
│   │       ├── keywords.txt
│   │       ├── PS2X_lib.cpp
│   │       └── PS2X_lib.h
│   ├── README
│   ├── Robot
│   │   ├── Robot.cpp
│   │   └── Robot.h
│   ├── RobotData
│   │   └── RobotData.h
│   ├── SerialTransport
│   │   ├── SerialTransport.cpp
│   │   └── SerialTransport.h
│   └── ServoJoint
│       ├── ServoJoint.cpp
│       └── ServoJoint.h
├── platformio.ini
├── readme.md
└── src
    └── main.cpp


1. platformio.ini
这个是platformio工程的配置文件，这里主要包括两部分：
    × 程序中所有宏定义都在这里定义，不需要在每个C++文件中用#define来定义
    × 编译参数（芯片类型，依赖库等）
具体见platformio.ini中的解释。 
platformio.ini编写规则详见http://docs.platformio.org/en/latest/projectconf.html

2. main.cpp
主程序入口位于src/main.cpp，这个文件对应arduino的setup() 和 loop()函数
    × setup()函数在单片机上电或reset后首先执行且只运行一次
    × loop()函数为单片机主循环程序

3. lib文件夹
程序中所有用到的类的定义（头文件和实现）都位于lib/文件夹下的相应文件夹中。
目前程序包括：
    × Config            一些固定配置，用户无需修改
    × Debugger          串口调试类（单例），用于调试串口输出
    × Gateway           通讯类及通讯协议
    × Interface         接口类，抽象一些关键的类为接口，提高程序扩展性
    × Joystick          遥控手柄类
    × Robot             机器人类
    × RobotData         机器人状态数据类（单例），用于保存机器人的状态信息
    × SerialTransport   串口类，负责串口的收发
    × ServoJoint        舵机关节类，具体控制舵机
具体见文件中的解释。

