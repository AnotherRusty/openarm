////////////////////////////

/**** MODIFY WITH CAUTION : May cause problems. ****/
#pragma once

# include <Arduino.h>

// 8-bit
typedef signed char int8_t;
typedef unsigned char uint8_t;

// 16-bit
typedef signed int int16_t;
typedef unsigned int uint16_t;

// 32-bit
typedef signed long int int32_t; 
typedef unsigned long int uint32_t;

// 64-bit (not always work!)
typedef signed long long int int64_t;
typedef unsigned long long int uint64_t;


#ifdef ARDUINO_AVR_UNO
    #define DEBUG_ENABLE   0
#elif ARDUINO_AVR_MEGA2560
    #define DEBUG_ENABLE   1
    #define DEBUG_SERIAL    Serial3
    #define DEBUG_BAUDRATE  9600
#endif
#define MAIN_SERIAL     Serial  

