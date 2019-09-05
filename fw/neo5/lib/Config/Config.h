#pragma once

# include <Arduino.h>

// general
#define ROBOT_NAME  "NEO5"
#define BAUDRATE    9600
#define NUM_JOINTS  5
#define SERVO_SPEED  1.0

// pins
#define JOINT0_PIN  8
#define JOINT1_PIN  9
#define JOINT2_PIN  10
#define JOINT3_PIN  11
#define JOINT4_PIN  12

// debug
#define DEBUG_ON    false

// PS2
#define USE_PS2     false
#define pressures   false
#define rumble      false
#define PS2_DAT        4
#define PS2_CMD        5
#define PS2_SEL        6
#define PS2_CLK        7


////////////////////////////

/**** MODIFY WITH CAUTION : 
 * May cause problems. ****/
typedef signed char int8_t;   //8bit有符号类型
typedef unsigned char uint8_t; // 8bit无符号类型


typedef signed int int16_t; //16bit有符号类型
typedef unsigned int uint16_t;//16bit有符号类型


typedef signed long int int32_t;   //32bit有符号类型
typedef unsigned long int uint32_t;  //32bit有符号类型


typedef signed long long int int64_t;   //64bit有符号类型.可能无法使用
typedef unsigned long long int uint64_t;     //64bit有符号类型，可能无法使用


#ifdef ARDUINO_AVR_UNO
#define DEBUG_ENABLE   0
#elif ARDUINO_AVR_MEGA2560
#define DEBUG_ENABLE   1
#define DEBUG_SERIAL    Serial3
#define DEBUG_BAUDRATE  9600
#endif

#define MAIN_SERIAL     Serial  

