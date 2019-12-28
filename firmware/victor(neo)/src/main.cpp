#include <Arduino.h>
#include "Debugger.h"
#include "Config.h"
#include "SerialTransport.h"
#include "Gateway.h"
#include "ServoJoint.h"
#include "Robot.h"
#include "Joystick.h"


/* 创建全局对象 */
SerialTransport trans(MAIN_SERIAL, BAUDRATE);
Gateway gateway(&trans);    // 创建gateway，传入串口作为负责实际通讯的transport    
Robot robot;
Joystick ps2;

// 舵机关节
ServoJoint joint0 = ServoJoint(JOINT0_PIN, 180);
ServoJoint joint1 = ServoJoint(JOINT1_PIN, 180);
ServoJoint joint2 = ServoJoint(JOINT2_PIN, 180);
ServoJoint joint3 = ServoJoint(JOINT3_PIN, 180);
ServoJoint joint4 = ServoJoint(JOINT4_PIN, 180);

/* setup()函数只运行一次 */
void setup() {
    // 初始化gateway
    gateway.init();

    // 配置robot，添加关节
    robot.add_joint(0, &joint0);
    robot.add_joint(1, &joint1);
    robot.add_joint(2, &joint2);
    robot.add_joint(3, &joint3);
    robot.add_joint(4, &joint4);
    
    // 初始化robot
    robot.init();

#if USE_PS2
    // init ps2
    ps2.init();
#endif
}

/* 主循环 */
// 主要分为两部分：
//     1.gateway - 从串口读取数据并解析
//     2.robot - 执行动作
void loop() {
    gateway.run();
#if USE_PS2
    ps2.check_command();
#endif
    robot.run();
}
