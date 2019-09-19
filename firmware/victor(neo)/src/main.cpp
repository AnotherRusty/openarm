#include <Arduino.h>
#include "Debugger.h"
#include "Config.h"
#include "SerialTransport.h"
#include "Gateway.h"
#include "ServoJoint.h"
#include "Robot.h"
#include "Joystick.h"


SerialTransport trans(MAIN_SERIAL, BAUDRATE);
Gateway gateway(&trans);
Robot robot;
Joystick ps2;


ServoJoint joint0 = ServoJoint(JOINT0_PIN, 180);
ServoJoint joint1 = ServoJoint(JOINT1_PIN, 180);
ServoJoint joint2 = ServoJoint(JOINT2_PIN, 180);
ServoJoint joint3 = ServoJoint(JOINT3_PIN, 180);
ServoJoint joint4 = ServoJoint(JOINT4_PIN, 180);


void setup() {
    // start gateway
    gateway.init();

    // configuring robot
    robot.add_joint(0, &joint0);
    robot.add_joint(1, &joint1);
    robot.add_joint(2, &joint2);
    robot.add_joint(3, &joint3);
    robot.add_joint(4, &joint4);
    
    // start robot
    robot.init();

#if USE_PS2
    // init ps2
    ps2.init();
#endif
}

void loop() {
    gateway.run();
#if USE_PS2
    ps2.check_command();
#endif
    robot.run();
}
