#! /usr/bin/python
''' Performs the hardware level functions of the page-turning mechanism
'''

# STANDARD PYTHON IMPORTS

# PYTHON LIBRARIES
import RPi.GPIO as GPIO

# USER LIBRARIES
from step_servo import ServoStepThread

# GLOBAL VARIABLES
DEFAULT_SETTLING_TIME = 1 # second
DEFAULT_WHEEL_DEGREES = 39 # degrees
DEFAULT_HOLDER_ARM_DEGREES = 100 # degrees

# CLASSES
class PageTurner():
	''' Implements the pre-defined page turner actions
	'''
	def __init__(self, state_machine=None):
		''' Initialises the page turner. 

			'state_machine' should contain a reference to a PiStateMachine() 
				object.
		'''
		self._state_machine = state_machine
		self.is_init = False
		self.wheel_degrees = DEFAULT_WHEEL_DEGREES
		self.holder_arm_degrees = DEFAULT_HOLDER_ARM_DEGREES
		self.init_all_servo_gpio()
		self.init_servo_positions()

	def __del__(self):
		''' Destructor for the page turner. Deinit all servo GPIOs
		'''
		self.deinit_all_servo_gpio()

	def _run_servos(self, pin_lookup):
		''' Runs every servo in the pin_lookup table that looks like:
			{ pin : (degrees, settling_time) }
		'''
		threads = []
		for pin, tup in pin_lookup.iteritems():
			threads.append(ServoStepThread(pin, tup[0], tup[1]))

		# Run the servos
		for t in threads:
			t.start()

		# Wait for all servos to settle
		for t in threads:
			t.join()

	def init_all_servo_gpio(self):
		''' Initialises the GPIO module and the individual servo pins
		'''
		self._init_servo_gpio(9)
		self._init_servo_gpio(11)
		self._init_servo_gpio(10)
		self._init_servo_gpio(14)
		self._init_servo_gpio(7)
		self._init_servo_gpio(8)
		self._init_servo_gpio(15)
		print "Successfully init all servo GPIO"

	def _init_servo_gpio(self,pin):
		''' Initialises a single servo GPIO pin.
		'''
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(pin, GPIO.OUT)

	def deinit_all_servo_gpio(self):
		''' Deinitialises all GPIOs
		'''
		GPIO.cleanup()
		print "Successfully deinit all servo GPIO"

	def set_wheel_degrees(self, wheel_degrees):
		''' Sets the wheel degrees value, usually passed from the server through
		the state machine
		'''
		self.wheel_degrees = wheel_degrees

	def get_wheel_degrees(self):
		''' Returns the value of wheel degrees currently in use.
		'''
		return self.wheel_degrees

	def set_holder_arm_degrees(self, holder_arm_degrees):
		''' Sets the holder arm degrees values.
		'''
		self.holder_arm_degrees = holder_arm_degrees

	def get_holder_arm_degrees(self):
		''' Returns the holder arm degrees currently in use
		''' 
		return self.holder_arm_degrees

	def init_servo_positions(self):
		''' Takes the servos to their defined starting positions. 
		'''
		pin_lookup = {9  : (90,  DEFAULT_SETTLING_TIME), \
					  11 : (120, DEFAULT_SETTLING_TIME), \
					  10 : (0,   DEFAULT_SETTLING_TIME), \
					  14 : (180, DEFAULT_SETTLING_TIME), \
					  7  : (100, DEFAULT_SETTLING_TIME), \
					  8  : (75,  DEFAULT_SETTLING_TIME), \
					  15 : (90,  DEFAULT_SETTLING_TIME)}

		self._run_servos(pin_lookup)
		self.is_init = True

	def queue_turn_page(self):
		''' Queues a page turn on a background thread. When the page turning is
		complete, the state_machine's handler_turned_page is called.

		TODO: Background thread
		'''

		# Signal to the state machine that we have finished turning the page
		self.turn_page()
		self._state_machine.handler_turned_page()

	def turn_page(self):
		''' Turns a page using the experimentally adjusted degree values. Calls
		the state_machine's handler_turned_page() function once done.
		'''
		if not self.is_init:
			self.init_servo_positions()
		self.is_init = False

		pin_lookup = {11 : (self.wheel_degrees, DEFAULT_SETTLING_TIME)}
		self._run_servos(pin_lookup)
		pin_lookup.clear()

		pin_lookup = {9  : (0,   DEFAULT_SETTLING_TIME), \
					  15 : (75,  DEFAULT_SETTLING_TIME)}
		self._run_servos(pin_lookup)
		pin_lookup.clear()

		pin_lookup = {15 : (100, DEFAULT_SETTLING_TIME)}
		self._run_servos(pin_lookup)
		pin_lookup.clear()

		pin_lookup = {11 : (120, DEFAULT_SETTLING_TIME), \
					  10 : (130, DEFAULT_SETTLING_TIME), \
					  14 : (0,   DEFAULT_SETTLING_TIME), \
					  7  : (0,   DEFAULT_SETTLING_TIME)}
					  # 8  : (160, DEFAULT_SETTLING_TIME)}
		self._run_servos(pin_lookup)
		pin_lookup.clear()

		pin_lookup = {7  : (100, DEFAULT_SETTLING_TIME), \
					  8  : (75,  DEFAULT_SETTLING_TIME), \
					  15 : (90,  DEFAULT_SETTLING_TIME)}
		self._run_servos(pin_lookup)
		pin_lookup.clear()

		pin_lookup = {14 : (180, DEFAULT_SETTLING_TIME), \
					  10 : (0,   DEFAULT_SETTLING_TIME)}
		self._run_servos(pin_lookup)
		pin_lookup.clear()

		self.deinit_all_servo_gpio()


# FUNCTIONS

# CODE
if __name__ == '__main__':
	print "Do not run page_turner.py from __main__."

# END OF FILE