#! /usr/bin/python
''' Manages server handler threading between Raspberry Pi, laptop and iPhone.
'''

# STANDARD PYTHON IMPORTS
import threading

# PYTHON LIBRARIES

# USER LIBRARIES
import enums

# GLOBAL VARIABLES

# CLASSES
class ThreadManager:
	''' Manages the required threads for accessing devices using non-blocking 
	thread locks. Every device operation should go through the thread manager.
	'''
	def __init__(self):
		''' Initialises thread locks for the devices
		'''
		self.dev_lock = {EnumDevice.PI : threading.Lock(), \
						 EnumDevice.PHONE : threading.Lock(), \
						 EnumDevice.LAPTOP : threading.Lock()}

	def acquire_dev_lock(self, dev):
		''' Attempts to acquire the lock for a device. Returns false if already
		locked. Call from the thread you want to acquire the lock.
		'''
		if dev != EnumDevice.INVALID:
			return self.dev_lock[dev].acquire(False)
		else:
			print "Invalid device to lock from ThreadManager."
			return False

	def release_dev_lock(self, dev):
		''' Attempts to release the lock for a device. An error message will be
		printed if the lock is unlocked. Does not return any value.
		'''
		if dev != EnumDevice.INVALID:
			try:
				self.dev_lock[dev].release()
			except threading.ThreadError:
				print "Lock for device %s already unlocked" % \
					EnumDevice.get_name(dev)
		else:
			print "Invalid device to release lock from ThreadManager."

# FUNCTIONS

# CODE
if __name__ == '__main__':
	print "Do not run thread_mgr.py from __main__."

# END OF FILE