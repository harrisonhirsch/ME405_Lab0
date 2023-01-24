# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 15:18:59 2021
@file Lab1.py
@brief Takes user input in the form of a button press and switches between stages with different waveforms for the LED
@description Allows for interaction with board through PuTTY. Prompts user for input and goes on standby until input is recieved when the button is pressed. Once it is pressed it switches into stage 2, which contains a square wave. The LED then lights up in the square wave pattern. The button is pressed again and the LED behaves in a sine wave pattern. The button is pressed again and the led behaves in a sawtooth wave pattern. The button is pressed again and the cycle repeats, with the LED behaving in a square wave pattern. Each time the button is pressed the wave resets and each stage starts at the desired start time of the wave.

@author: Peyton Archibald
@date: 10/7/2021
@copyright license info. Open Source

"""
import time
import utime
import math
import pyb
#all functions should be defined before the if __name__ ... block below


pinA5 = pyb.Pin (pyb.Pin.cpu.A5)
tim2 = pyb.Timer(2, freq = 20000)
t2ch1 = tim2.channel(1, pyb.Timer.PWM, pin=pinA5)

pinC13 = pyb.Pin (pyb.Pin.cpu.C13)

def onButtonPressFCN(IRQ_src):
    ''' @brief                                  Allows for button input
        @details                                Sets the value of button to be true so that the code knows when to switch between stages
        @param IRQ_src                          
        @return                                 Changes value of button to be true
    '''
    global button
    ##  @brief                                  The button has beed pressed
    #   @details                                When the button is physically pressed, this variable is set to true. 
    #                                           This is what notifies the code to switch to the next stage in the cycle. 
    #
    button = True
    
def update_sqw(current_time):
    ''' @brief                                  Generates square wave
        @details                                Takes the current_time parameter and generates a square wave based off of the value of the parameter. This is done by using modulus to keep the value at either 100 or 0. 
        @param current_time                     The current time recorded since initializing
        @return                                 Current value on square wave
    '''
    return 100*((current_time/1000) % 1 < 0.5)

def update_stw(current_time):
    ''' @brief                                  Generates sawtooth wave
        @details                                Takes the current_time parameter and generates a sawtooth wave based off of the value of the parameter. This is done by using modulus to have the value increase to 100 and then drop back to zero once it reaches 100. 
        @param                                  The current time recorded since initializing
        @return                                 Current value on sawtooth wave
    '''
    return 100*((current_time/1000) % 1.0)

def update_sin(current_time):
    ''' @brief                                  Generates sine wave
        @details                                Takes the current_time parameter and generates a sine wave based off of the value of the parameter. This is done by using the math module to generate the sine wave with a period of 10 seconds. 
        @param                                  The current time recorded since initializing
        @return                                 Current value on sine wave
    '''
    return 50*math.sin((current_time/10000) * math.pi*2) + 50
    
ButtonInt = pyb.ExtInt(pinC13, mode=pyb.ExtInt.IRQ_FALLING, pull=pyb.Pin.PULL_NONE, callback=onButtonPressFCN)


if __name__ == '__main__':
    print('Welcome to the terminal. To begin, press the blue user button B1 on the Nucleo. Keep pressing to cycle through LED patterns')
    
    ##  @brief                                  number of complete cycles
    #   @details                                records how many times the stages have switched from the stage 1 to 2 to 3 to 4 and back to 2
    #
    runs = 0
   
    ##  @brief                                  the current state of the program
    #   @details                                sets the current state of the program, determines what wave form is being produced
    #
    state = 0
    
    button = False
    while(True):            #main while look
        try:
            if(state == 0):
                #State zero Initialization
             
                state = 1
                pass
            elif(state == 1):
                #State 1 Standby for Initial User Input
                
                if button == True:
                    state = 2
                    button = False
                    
                    ##  @brief                  Records the ticks since starting
                    #   @details                utilizes module utime to keep track of the time for the wave to generate. This value resets when the states switch.
                    #
                    startTime = utime.ticks_ms()
                    print('Square wave pattern selected')
                pass
            elif(state == 2):
                #State 2 running Square wave pattern
                
                ##  @brief                      Records new point in time
                #   @details                    Records a 'stopping point' in time.
                #
                stopTime = utime.ticks_ms()
                ##  @brief                      duration between stopTime and startTime
                #   @details                    the difference between the values of stopTime and startTime. This determines the values that the wave functions utilize.
                #
                duration = utime.ticks_diff(stopTime, startTime)
                #print(update_sqw(duration))            #Used for debugging to see amplitude of function output
                t2ch1.pulse_width_percent(update_sqw(duration))
                if button == True:              #if a button press is detected, change the state and print selected state
                    state = 3
                    button = False
                    startTime = utime.ticks_ms()
                    print('Sine wave pattern selected')
                pass
            elif(state == 3):
                #State 3 running Sine wave pattern
                
                stopTime = utime.ticks_ms()
                duration = utime.ticks_diff(stopTime, startTime)
                #print(update_sin(duration))            #Used for debugging to see amplitude of function output
                t2ch1.pulse_width_percent(update_sin(duration))
                if button == True:              #if a button press is detected, change the state and print selected state
                    state = 4
                    button = False
                    startTime = utime.ticks_ms()
                    print('Sawtooth pattern selected')
                pass
            elif(state == 4):
                #State 4 running Sawtooth wave pattern
                
                stopTime = utime.ticks_ms()
                duration = utime.ticks_diff(stopTime, startTime)
                #print(update_stw(duration))            #Used for debugging to see amplitude of function output
                t2ch1.pulse_width_percent(update_stw(duration))
                if button == True:          #if a button press is detected, change the state and print selected state
                    state = 2
                    button = False
                    startTime = utime.ticks_ms()
                    ('Square Wave pattern selected')
                pass
            runs += 1
            time.sleep(0)
        except KeyboardInterrupt:
            break #Breakout of loop on ctrl+C
    
    print('Program Terminating')