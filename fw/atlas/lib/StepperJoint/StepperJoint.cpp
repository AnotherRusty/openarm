#include "StepperJoint.h"
#include "Debugger.h"

#define SPR 200
#define INTERVAL 10000

StepperJoint::StepperJoint(uint8_t step_pin, uint8_t dir_pin, uint8_t enable_pin, 
                        unsigned short max_angle, uint16_t max_speed, uint16_t max_accel)
{
    _step_pin = step_pin;
    _dir_pin = dir_pin;
    _enable_pin = enable_pin;
    _max_speed = max_speed;
    _max_accel = max_accel;
}

StepperJoint::StepperJoint(uint8_t step_pin, uint8_t dir_pin, uint8_t enable_pin, uint8_t stop_cw_pin, uint8_t stop_ccw_pin,
                        unsigned short max_angle, uint16_t max_speed=MAX_SPEED, uint16_t max_accel=MAX_ACCEL);

void StepperJoint::init(){
    _stepper = AccelStepper(AccelStepper::DRIVER, _step_pin, _dir_pin);
    _stepper.setMaxSpeed(_max_speed);
    _stepper.setAcceleration(_max_accel);
    _stepper.setPinsInverted(false, false, false);
    _stepper.setEnablePin(_enable_pin);
    _stepper.disableOutputs();
}

void StepperJoint::move(unsigned short angle){
    

}

unsigned short StepperJoint::get_position(){
    _angle = _stepper.currentPosition() / SPR * 360;
    return _angle;
}

void StepperJoint::set_speed(uint16_t speed){
    _stepper.setMaxSpeed(speed);
}

void StepperJoint::set_acceleration(uint16_t accel){
    _stepper.setAcceleration(accel);
}

void StepperJoint::enable(){
    _stepper.enableOutputs();
}

void StepperJoint::disable(){
    _stepper.disableOutputs();
}

void StepperJoint::set_position(unsigned short angle){
    _angle = angle;
}