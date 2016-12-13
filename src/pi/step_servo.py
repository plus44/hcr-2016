#! /usr/bin/python
''' Steps a given servo, a specified duty cycle (multithreaded)
'''

# STANDARD PYTHON IMPORTS
import time
import argparse
import sys
import threading

# EXTERNAL PYTHON LIBRARIES
import RPi.GPIO as GPIO

# USER LIBRARIES

# GLOBAL VARIABLES
MIN_DUTY_CYCLE_100 = 380
MAX_DUTY_CYCLE_100 = 1050
DEFAULT_TIMEDELAY = 1 # second

# CLASSES
class ServoStepThread(threading.Thread):
    ''' Runs a single servo thread on a given pin/deg combo
    '''
    def __init__(self, pin, deg, tim):
        threading.Thread.__init__(self)
        self.pin = pin
        self.init_gpio(pin)
        self.deg = deg
        self.tim = tim

    def init_gpio(self, servo_pin):
        ''' Initialises the given servo pin on the Pi.
        '''
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(servo_pin, GPIO.OUT)

    def step_servo(self, servo_pin, degrees):
        ''' Steps the servo on servo_pin to 'degrees', based on the
            global MIN/MAX duty cycle values for mapping. 
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

        print "Stepping servo pin %d by %f duty cycle" % ( \
            servo_pin, mapped_dc)

        pwm.start(0)
        pwm.ChangeDutyCycle(mapped_dc)
        time.sleep(self.tim)
        pwm.stop()

    def run(self):
        ''' Runs the thread
        '''
        self.step_servo(self.pin, self.deg)

    def deinit_all_gpio(self):
        ''' Deinitialises ALL GPIOs. Call ONLY after all threads are finished.
        '''
        GPIO.cleanup()


# FUNCTIONS
def deinit_all_gpio():
    ''' Deinitialises all GPIOs
    '''
    GPIO.cleanup()

def parse_pins_and_degrees(args=None):
    ''' Returns a dictionary of servo pins and degrees from argv
    '''
    parser = argparse.ArgumentParser(description= \
            "Takes CSV lists of servo pins and degrees. Steps each servo to " +\
            "the desired angle.")
    parser.add_argument('-p', '--pins', help="CSV list of servo pins", \
                        required=True, default='11')
    parser.add_argument('-d', '--degrees', help="CSV list of degrees to step" +\
                        " servos", required=True, default='90')
    parser.add_argument('-t', '--timedelay', help="The amount of time to " +\
                        "wait after actuating", required=False, default=None)

    results = parser.parse_args(args)
    # Parse CSV lists
    pins = [int(pin) for pin in results.pins.split(',')]
    
    if results.degrees != None:
        degs = [int(deg) for deg in results.degrees.split(',')]
        if len(degs) != len(pins):
            return None
    else:
        return None
    
    if results.timedelay != None:
        times = [float(tim) for tim in results.timedelay.split(',')]
    else:
        times = [DEFAULT_TIMEDELAY]*len(pins)
        
    pin_lookup = {pin : tup for pin, tup in zip(pins, zip(degs, times))}
    return pin_lookup
    
def main(pin_lookup):
    ''' Steps each servo in pin_lookup by the necessary amount
    '''
    threads = []
    
    for pin, tup in pin_lookup.iteritems():
        threads.append(ServoStepThread(pin, tup[0], tup[1]))

    for t in threads:
        t.start()

    for t in threads:
        t.join()
        
    deinit_all_gpio()


# CODE

if __name__ == '__main__':
    pin_lookup = parse_pins_and_degrees(sys.argv[1:])
    if pin_lookup == None:
        print "Invalid argument lengths passed."
    else:
        main(pin_lookup)
else:
    print "Run step_servo.py from __main__."
# END OF FILE
