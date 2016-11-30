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
	''' Manages the required threads using non-blocking thread locks.
	Every thread operation should go through the thread manager.
	'''
	def __init__(self):
		''' Initialises thread locks for 
		'''
		self.pi_lock = threading.Lock()
		self.phone_lock = threading.Lock()
		self.laptop_lock = threading.Lock()

	def acquire_dev_lock(self, dev):
		''' Attempts to acquire the lock for a device. Returns false if already
		locked. Call from the thread you want to acquire the lock.
		'''
		if dev == EnumDevice.PI:
			return self.pi_lock.acquire(False)
		else if dev == EnumDevice.PHONE:
			return self.phone_lock.acquire(False)
		else if dev == EnumDevice.LAPTOP:
			return self.laptop_lock.acquire(False)
		else:
			print "Invalid device."
			return False

	def release_dev_lock(self, dev):
		''' Attempts to release the lock for a device. An error message will be
		printed if the lock is unlocked. Does not return any value.
		'''
		try:
			if dev == EnumDevice.PI:
				return self.pi_lock.release()
			else if dev == EnumDevice.PHONE:
				return self.phone_lock.release()
			else if dev == EnumDevice.LAPTOP:
				return self.laptop_lock.release()
			else:
				print "Invalid device."

		except threading.ThreadError:
			print "Lock for device: %s unlocked." % EnumDevice.get_name(dev)

# FUNCTIONS

# CODE
if __name__ == '__main__':
	print "Do not run thread_mgr.py from __main__."

# END OF FILE