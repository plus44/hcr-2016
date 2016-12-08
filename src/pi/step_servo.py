#! /usr/bin/python
''' Steps a given servo, a specified duty cycle
'''

# STANDARD PYTHON IMPORTS
import time
import argparse
import sys

# EXTERNAL PYTHON LIBRARIES
import RPi.GPIO as GPIO

# USER LIBRARIES

# GLOBAL VARIABLES
MIN_DUTY_CYCLE_100 = 380
MAX_DUTY_CYCLE_100 = 1050

# CLASSES

# FUNCTIONS
def init_gpio(servo_pin):
    ''' Initialises the given servo pin on the Pi.
    '''
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servo_pin, GPIO.OUT)

def deinit_all_gpio():
    ''' Deinitialises all GPIOs
    '''
    GPIO.cleanup()

def step_servo(servo_pin, degrees):
    ''' Steps the servo on servo_pin to 'degrees', based on the global MIN/MAX
        duty cycle values for mapping. 
    '''
    # Create a PWM object on servo_pin at 50Hz
    pwm = GPIO.PWM(servo_pin, 50)

    if degrees < 0:
        degrees = 0
    elif degrees > 180:
        degrees = 180

    mapped_dc = MIN_DUTY_CYCLE_100 + (float(degrees) / 180) * \
                (MAX_DUTY_CYCLE_100 - MIN_DUTY_CYCLE_100)
    mapped_dc = mapped_dc / 100

    print "Stepping servo pin %d by %f duty cycle" % (servo_pin, mapped_dc)

    pwm.start(0)
    pwm.ChangeDutyCycle(mapped_dc)
    time.sleep(1)
    pwm.stop()

def parse_pins_and_degrees(args=None):
    ''' Returns a dictionary of servo pins and degrees from argv
    '''
    parser = argparse.ArgumentParser(description= \
            "Takes CSV lists of servo pins and degrees. Steps each servo to " +\
            "the desired angle.")
    parser.add_argument('-p', '--pins', help="CSV list of servo pins", \
                        required='True', default='11')
    parser.add_argument('-d', '--degrees', help="CSV list of degrees to step" +\
                        " servos", required='True', default='90')

    results = parser.parse_args(args)
    # Parse CSV lists
    pins = [int(pin) for pin in results.pins.split(',')]
    degs = [int(deg) for deg in results.degrees.split(',')]
    pin_lookup = {pin : deg for pin, deg in zip(pins, degs)}
    return pin_lookup

def main(pin_lookup):
    ''' Steps each servo in pin_lookup by the necessary amount
    '''
    for pin, deg in pin_lookup.iteritems():
        init_gpio(pin)
        step_servo(pin, deg)
        
    deinit_all_gpio()

# CODE
if __name__ == '__main__':
    pin_lookup = parse_pins_and_degrees(sys.argv[1:])
    main(pin_lookup)
else:
    print "Run step_servo.py from __main__."
# END OF FILE
