#include "ServoJoint.h"
#include "Debugger.h"
#include "Config.h"


#define INTERVAL 20000  // 默认控制间隔，实际除以SERVO_SPEED（platformio.ini）

// 构造函数
// 参数： pin        舵机信号引脚
//       max_angle  最大转动角度
ServoJoint::ServoJoint(uint8_t pin, unsigned short max_angle){
    _pin = pin;
    _max_angle = max_angle;
    _move_interval = double(INTERVAL) / SERVO_SPEED;
    _reverse_flag = false;
}

// 初始化
// 参数： None
// 返回值： None
void ServoJoint::init(){
    Debugger::get()->printf("Servo on pin %d", _pin);
    _servo.attach(_pin);
    delayMicroseconds(50);
    _servo.write(90);   // 默认初始位 90度
    _angle = 90;
}

// move
// 参数： angle     目标角度
// 返回值： None
void ServoJoint::move(unsigned short angle){
    Debugger::get()->printf("Move sevo on pin%d to angle: %d", _pin, angle);

    unsigned short target;
    if(!_reverse_flag)
        target = min(max(0, angle), _max_angle);
    else
        target = min(max(0, _max_angle-angle), _max_angle);

    if((micros()-_t_last)>_move_interval){
        if(target ==_angle)
            return;
        if(target >_angle)
        {
            _servo.write(++_angle);
        }
        else if (target <_angle)
        {
            _servo.write(--_angle);
        }
        _t_last = micros();
    }
}

void ServoJoint::direct_move(unsigned short angle){
    if(!_reverse_flag)
        _angle = angle;
    else
        _angle = _max_angle - angle;
    _servo.write(_angle);
}

// get_position，获取当前角度
// 参数： None
// 返回值 unsigned short 当前角度
unsigned short ServoJoint::get_position(){
    if(!_reverse_flag)
        return _angle;
    else
        return (_max_angle-_angle);
}

void ServoJoint::set_reverse(bool reverse){
    _reverse_flag = reverse;
}