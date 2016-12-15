#! /usr/bin/python
''' Exposes the functionalities of the devices communicating to/from the server. 
'''

# STANDARD PYTHON IMPORTS
import os
import sys
import time
import json

# PYTHON LIBRARIES
from collections import deque

# USER LIBRARIES
import enum
from thread_mgr import ThreadManager
from state_mgr import StateManager
import constants

# GLOBAL VARIABLES

# CLASSES
class Device():
	''' Generic device class. Subclass from this.
	'''
	def __init__(self, thread_mgr=None, state_mgr=None, dev=enum.Device.INVALID):
		self._thread_mgr = thread_mgr
		self._state_mgr = state_mgr
		self._dev = dev
		self.time = time.time()
		# Change this to what long-polling should return.
		self.ret_val = ""

	def long_poll(self):
		''' With the device lock and does not return until either the 
		constants.LONG_POLL_TIMEOUT has passed or the device is self.ready_to_return().

		Returns False if timed out.
		Returns self.ret_val if actually ready_to_return.
		'''
		# if self._thread_mgr.acquire_dev_lock(self._dev):
		try:
			# Store the current time
			self.time = time.time()
			# Do nothing until ready_to_return() is true or timed out
			while not self.ready_to_return() and \
				((time.time() - self.time) < constants.LONG_POLL_TIMEOUT):
				pass

			# Check to see if we are actually ready to return or just timed
			# out.
			if ((time.time() - self.time) < constants.LONG_POLL_TIMEOUT):
				return self.ret_val
			else:
				print "Long poll timed out."
				return False

		finally:
			pass
				# self._thread_mgr.release_dev_lock(self._dev)

		return None

	def ready_to_return(self):
		''' Checks the designated device's device queue inside the state 
		manager. If it's empty, it returns false. If there's something to do, 
		it returns true.
		'''
		if self._state_mgr.get_queue_len(self._dev) == 0:
			# Empty the return value
			self.ret_val = ""
			return False
		else:
			# Set the return value to the item popped from the queue
			self.ret_val = self._state_mgr.pop_from_queue(self._dev)
			return True

	def handle_post(self, body):
		''' Begin handling a post request by trying to parse the JSON string 
		from the body of the request.
		'''
		try:
			p_json = json.loads(body)
			self._handle_post(p_json)
		except:
			print "Failed parsing %s POST request body as JSON: %s" % \
				(enum.Device.get_name[self._dev], body)

	def _handle_post(self, p_json):
		''' Override this function in classes that inherit from Device.
		'''
		# Add the body of the received post request to the corresponding device
		# queue in self._state_mgr.dev_que[self._dev]
		pass

class RaspberryPi(Device):
	''' Raspberry Pi device class.
	'''
	def __init__(self, thread_mgr, state_mgr):
		Device.__init__(self, thread_mgr, state_mgr, enum.Device.PI)

	def _handle_post(self, p_json):
		''' If there was no error with turning, add a takePicture item to the
		device queue of the phone, otherwise add a turnPage item to the Pi's
		device queue.
		'''
		if p_json["doneTurning"] == True and \
			p_json["error"] == "None":
			# Tell the phone to take a picture.
			self._state_mgr.push_to_queue(enum.Device.PHONE, "takePicture")
			print "Successfully turned page on Raspberry Pi"
		elif p_json["error"] != "None":
			self._state_mgr.push_to_queue(enum.Device.PI, "turnPage")
			print "Received error: %s, from Raspberry Pi" % p_json["error"]
			print "Re-turning page."

class Phone(Device):
	''' Phone device class.
	'''
	def __init__(self, thread_mgr, state_mgr):
		Device.__init__(self, thread_mgr, state_mgr, enum.Device.PHONE)

	def _handle_post(self, p_json):
		''' If there was no error in taking a picture, add the picture content 
		to the laptop's queue. Otherwise, add a retakePicture item to the phone
		queue.
		'''
		if p_json["doneTakingPicture"] == True and \
			p_json["error"] == "None":
			# Push the actual picture to the laptop
			self._state_mgr.push_to_queue(enum.Device.LAPTOP, p_json["picture"])
			print "Successfully took a picture on the iPhone."
		elif p_json["error"] != "None":
			self._state_mgr.push_to_queue(enum.Device.PHONE, "takePicture")
			print "Received error: %s, from the iPhone. " % p_json["error"]
			print "Retaking picture."

class Laptop(Device):
	''' Laptop device class.
	'''
	def __init__(self, thread_mgr, state_mgr):
		Device.__init__(self, thread_mgr, state_mgr, enum.Device.LAPTOP)

	def _handle_post(self, p_json):
		''' If there was no error, add a turnPage item to the Pi's queue.
		'''

		# Passthrough modes from laptop to pi and phone.
		if p_json["piExtraAction"] != "doNothing":
			self._state_mgr.push_to_queue(enum.Device.PI, \
				p_json["piExtraAction"])

		if p_json["phoneExtraAction"] != "doNothing":
			self._state_mgr.push_to_queue(enum.Device.PHONE, \
				p_json["phoneExtraAction"])

		# 'State' machine mode of laptop
		if p_json["doneProcessing"] == True and \
			p_json["error"] == "None" and \
			not p_json["isFirstStart"]:
			# Tell the Raspberry Pi to turn the page.
			self._state_mgr.push_to_queue(enum.Device.PI, "turnPage")
			print "Successfully processed and spoke everything on the laptop."
		
		elif p_json["doneProcessing"] == True and \
			p_json["error"] == "None" and \
			p_json["isFirstStart"]:

			print "Clearing queues."
			# Clear all device queues:
			self._state_mgr.clear_queue(enum.Device.PHONE)
			self._state_mgr.clear_queue(enum.Device.LAPTOP)
			self._state_mgr.clear_queue(enum.Device.PI)

			# Tell the phone to take an image.
			self._state_mgr.push_to_queue(enum.Device.PHONE, "takePicture")
		
		elif p_json["error"] != "None":
			# Tell the laptop to retry.
			self._state_mgr.push_to_queue(enum.Device.LAPTOP, "retry")
			print "Received error: %s from laptop." % p_json["error"]
			print "Retrying laptop operations."
		else: 
			print "Received weird JSON combo from laptop."
			print p_json

class DeviceManager():
	''' Container/wrapper class for the trio of devices.
	'''
	def __init__(self, thread_mgr, state_mgr):
		self.devs = {enum.Device.PI : RaspberryPi(thread_mgr, state_mgr), \
					 enum.Device.PHONE : Phone(thread_mgr, state_mgr), \
					 enum.Device.LAPTOP : Laptop(thread_mgr, state_mgr)}

	def long_poll(self, dev):
		''' Activates long-polling on a device.
		'''
		if dev != enum.Device.INVALID:
			return self.devs[dev].long_poll()
		else:
			print "Invalid device to long-poll."
			return False

	def handle_post(self, dev, body):
		''' Handles a POST request on a device.
		'''
		if dev != enum.Device.INVALID:
			self.devs[dev].handle_post(body)
		else:
			print "Invalid device to handle POST request."

# FUNCTIONS

# CODE
if __name__ == '__main__':
	print "Do not run devices.py from __main__."

# END OF FILE