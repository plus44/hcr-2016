#! /bin/python

# STANDARD PYTHON IMPORTS
import time
import argparse
import sys
import threading

# PYTHON LIBRARIES
import RPi.GPIO as GPIO

# USER LIBRARIES
from step_servo import ServoStepThread

# GLOBAL VARIABLES
DEFAULT_TIMEDELAY = 1 # second

# CLASSES

# FUNCTIONS
def measure_servo(pin):
    ''' Measures the time it takes from a fully discharged capacitor to a
        threshold voltage to be reached on it.
    '''
    pass

def deinit_all_gpio():
    ''' Deinitialises all GPIOs
    '''
    GPIO.cleanup()
    
def main(pin_lookup):
    ''' Steps each servo in pin_lookup across the full range and measures the
        ADC response at the ends of the range.
    '''
    step_threads = []
    
    for pin in pin_lookup:
        step_threads.append(ServoStepThread(pin, 0, DEFAULT_TIMEDELAY))

    for t in step_threads:
        t.start()

    for t in step_threads:
        t.join()

    deinit_all_gpio()

    # Measure the poor man's ADC at 0 degrees
    for pin in pin_lookup:
        measure_servo(pin)
    


# CODE
if __name__ == '__main__':
    pin_lookup = parse_pins(sys.argv[1:])
    if pin_lookup == None:
        print "Invalid argument lengths passed."
    else:
        try:
            main(pin_lookup)
        except: KeyboardInterrupt:
            print "Exiting."

# END OF FILE
