#ifndef STEPPER_JOINT_H_
#define STEPPER_JOINT_H_


#include <Arduino.h>
#include "IJoint.h"
#include "AccelStepper.h"
#include "Config.h"


class StepperJoint: public IJoint
{
public:
    StepperJoint(uint8_t step_pin, uint8_t dir_pin, uint8_t enable_pin, unsigned short max_angle, 
                        uint16_t max_speed=MAX_SPEED, uint16_t max_accel=MAX_ACCEL);
    StepperJoint(uint8_t step_pin, uint8_t dir_pin, uint8_t enable_pin, uint8_t stop_cw_pin, uint8_t stop_ccw_pin,
                        unsigned short max_angle, uint16_t max_speed=MAX_SPEED, uint16_t max_accel=MAX_ACCEL);
    ~StepperJoint(){};
    void init();
    void move(unsigned short angle);
    unsigned short get_position();
    
    void set_speed(uint16_t speed);
    void set_acceleration(uint16_t accel);
    void enable();
    void disable();
    void set_position(unsigned short angle);

private:
    uint8_t _step_pin, _dir_pin, _enable_pin;
    uint16_t _max_speed, _max_accel;
    unsigned short _angle;
    unsigned short _max_angle;
    AccelStepper _stepper;
};


#endif