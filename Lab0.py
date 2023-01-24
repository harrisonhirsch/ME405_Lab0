# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 2023
@file Lab0.py
@brief 
@description 

@author: Peyton Archibald
@author: Harrison Hirsch
@date: 1/24/2023
@copyright license info. Open Source

"""
import time
import utime
import math
import pyb

def led_setup ():
    ''' @brief                                  Sets up the LED
        @details                                This function sets up the timer channel
        @return									Returns timer/Pin channel for the LED to be called later on to change the brightness of the LED
    '''
    pinA5 = pyb.Pin (pyb.Pin.cpu.A5)
    tim2 = pyb.Timer(2, freq = 20000)
    return tim2.channel(1, pyb.Timer.PWM, pin=pinA5)
    
    
    
def led_brightness (current_time):
    ''' @brief                                  Calculates the brightness value
        @details                                This function sets up the timer channel
        @return									Returns timer/Pin channel for the LED to be called later on to change the brightness of the LED
    '''
    return 100*((current_time/5000) % 1.0)
   
if __name__ == "__main__":
    startTime = utime.ticks_ms()
    t2ch1 = led_setup()
    while True:
        try:
            stopTime = utime.ticks_ms()
            duration = utime.ticks_diff(stopTime, startTime)
            t2ch1.pulse_width_percent(led_brightness(duration))
        except KeyboardInterrupt:
            break #Breakout of loop on ctrl+C
    
    print('Program Terminating')
