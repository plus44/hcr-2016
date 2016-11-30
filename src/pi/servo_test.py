# STANDARD PYTHON IMPORTS
import time

# EXTERNAL PYTHON LIBRARIES
import RPi.GPIO as GPIO

# USER LIBRARIES

# GLOBAL VARIABLES
SERVO_PIN = 11

# CODE AND CLASSES
def init_gpio():
	''' Initialises the Servo GPIO pin.

	Returns true if initialisation was successful, false otherwise.
	'''
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(SERVO_PIN, GPIO.OUT)
	return True

def main():
	''' Performs the initialistions and runs a basic servo testing program.
	'''
	if init_gpio():
		print "Successfully initialised GPIO"
	else:
		return

	# Create a PWM object on SERVO_PIN at 50Hz
	pwm = GPIO.PWM(SERVO_PIN, 50)

	pwm.start(0)

	for i in [float(j) / 100 for j in range(360, 1050, 1)]:
		print "Duty cycle: %f" % i
		pwm.ChangeDutyCycle(i)
		time.sleep(0.05)
	
	pwm.stop()

if __name__ == '__main__':
	main()

# END OF FILE