#! /usr/bin/python
''' Exposes the functionalities of the devices communicating to/from the server. 
'''

# STANDARD PYTHON IMPORTS
import os
import sys
import time
import json
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../common'))

# PYTHON LIBRARIES
from collections import deque

# USER LIBRARIES
import enums
from thread_mgr import ThreadManager
from common import constants

# GLOBAL VARIABLES

# CLASSES
class Device():
	''' Generic device class. Subclass from this.
	'''
	def __init__(self, thread_mgr=None, state_mgr=None, dev=Device.INVALID):
		self._thread_mgr = thread_mgr
		self._state_mgr = state_mgr
		self._dev = dev
		self.time = time.time()
		# Change this to what long-polling should return.
		self.ret_val = ""

	def long_poll(self):
		''' With the device lock and does not return until either the 
		LONG_POLL_TIMEOUT has passed (returning False) or the device is
		self.ready_to_return() (returning the recorded self.ret_val).
		'''
		if self._thread_mgr.acquire_dev_lock(self._dev):
			try:
				# Do nothing until ready_to_return() is true
				while not self.ready_to_return() and \
					((time.time() - self.time) < LONG_POLL_TIMEOUT):
					pass

				# Check to see if we are actually ready to return or just timed
				# out.
				if ((time.time() - self.time) < LONG_POLL_TIMEOUT):
					return self.ret_val
				else:
					return False

			finally:
				self._thread_mgr.release_dev_lock(self._dev)

	def ready_to_return(self):
		''' Checks the designated device's device queue inside the state 
		manager. If it's empty, it returns false. If there's something to do, 
		it returns true.
		'''
		if (len(self._state_mgr.dev_que[self._dev]) == 0):
			return False
		else:
			self.ret_val = self._state_mgr.dev_que[self._dev].popleft()
			return True

	def handle_post(self, body):
		''' Override this function in classes that inherit from Device.
		'''
		# Add the body of the received post request to the corresponding device
		# queue in self._state_mgr.dev_que[self._dev]
		pass

class RaspberryPi(Device):
	''' Raspberry Pi device class.
	'''
	def __init__(self, thread_mgr, state_mgr):
		Device.__init__(self, thread_mgr, state_mgr, EnumDevice.PI)


	def handle_post(self, body):
		''' If there was no error with turning, add a takePicture item to the
		device queue of the phone, otherwise add a turnPage item to the Pi's
		device queue.
		'''
		try:
			parsed = json.loads(body)
			if parsed["doneTurning"] == True and \
				parsed["error"] == "None":

				self.

		except:
			"Failed parsing Raspberry Pi body as JSON: %s" % body
			return



# FUNCTIONS

# CODE
if __name__ == '__main__':
	print "Do not run devices.py from __main__."

# END OF FILE