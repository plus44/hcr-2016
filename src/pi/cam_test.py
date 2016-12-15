""" Takes a picture using the RasPi camera, using the LED flash
"""

# STANDARD PYTHON IMPORTS
import os
import time
import picamera

# EXTERNAL LIBRARY IMPORTS
import RPi.GPIO as GPIO

# GLOBAL VARIABLES
FLASH_PIN=4
SLEEP_TIME=3 # seconds
PHOTO_DIR_REL='../photo' # Relative to this file's location

# CODE AND CLASSES
def get_photo_dir():
	''' Returns the full path of the photo directory using PHOTO_DIR_REL,
	relative to the current file's directory
	'''
	dir_path = os.path.dirname(os.path.realpath(__file__))
	return '%s/%s' % (dir_path, PHOTO_DIR_REL)

def init_gpio():
	''' Initialises the LED flash GPIO pin.

	Returns true if initialisation was successful, false otherwise.
	'''
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(FLASH_PIN, GPIO.OUT)
	return True

def deinit_gpio():
	''' Deinitialises the GPIO pins
	'''
	GPIO.cleanup()

def init_camera(camera=None):
	''' Initialises the camera settings.

	Returns true if initialisation was successful, false otherwise.
	'''
	if camera != None:
		try:
			# Set the resolution to maximum
			camera.resolution = (3280, 2464)
			return True
		except:
			pass
	return False

def deinit_camera(camera=None):
	''' Releases the camera resources.
	'''
	if camera != None:
		camera.close()

def main():
	''' Takes a photo after initialising the LED flash GPIO pin.
	The picture is stored in PHOTO_DIR_REL.
	'''
	camera = picamera.PiCamera()

	# Initialise GPIO
	if init_gpio() != False:
		print "Successfully initialised GPIO."
	else:
		print "Failed initialising camera."
		return

	# Initialise camera
	if init_camera(camera) != False:
		print "Successfully initialised camera."
	else:
		print "Failed initialising camera."
		camera.close()
		return

	time.sleep(SLEEP_TIME)
	GPIO.output(FLASH_PIN, GPIO.HIGH)
	camera.capture('%s/test.png' % get_photo_dir())
	GPIO.output(FLASH_PIN, GPIO.LOW)

	# Perform deinitialisations
	deinit_camera(camera) 	
	deinit_gpio()

if __name__ == '__main__':
	main()
else:
	print "This program is meant to be run as main."
