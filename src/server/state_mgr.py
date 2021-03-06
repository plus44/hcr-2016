#! /usr/bin/python
''' Manages the states and queues of the devices
'''

# STANDARD PYTHON IMPORTS
from collections import deque
import threading

# PYTHON LIBRARIES

# USER LIBRARIES
import enum

# GLOBAL VARIABLES

# CLASSES
class StateManager():
	''' Holds the device queues
	'''
	def __init__(self):
		''' Create empty queues for each device
		'''
		self.dev_que = {enum.Device.PI : deque(), \
						enum.Device.PHONE : deque(), \
						enum.Device.LAPTOP : deque()}
		self.dev_lock = {enum.Device.PI : threading.Lock(), \
						 enum.Device.PHONE : threading.Lock(), \
						 enum.Device.LAPTOP : threading.Lock()}

	def clear_queue(self, dev):
		''' Clear the queue of the passed dev
		'''
		if dev != enum.Device.INVALID:
			self.dev_lock[dev].acquire(True)
			self.dev_que[dev].clear()
			try:
				self.dev_lock[dev].release()
			except threading.ThreadError:
				print "Lock for device queue: %s already unlocked." % \
					enum.Device.get_name[dev]
			print "Cleared queue for device %s" % enum.Device.get_name[dev]

	def push_to_queue(self, dev, item):
		''' Push an item to the end of the queue of a device.
		'''
		if dev != enum.Device.INVALID:
			self.dev_lock[dev].acquire(True)
			self.dev_que[dev].append(item)
			try:
				self.dev_lock[dev].release()
			except threading.ThreadError:
				print "Lock for device queue: %s already unlocked." % \
					enum.Device.get_name[dev]

	def pop_from_queue(self, dev):
		''' Pop an item from the top of a device's queue. FIFO ordering is 
		applied to the queues.

		Returns the popped item or None if the device is invalid or no items 
		remain on the device queue.
		'''
		if dev != enum.Device.INVALID:
			self.dev_lock[dev].acquire(True)
			item = self.dev_que[dev].popleft()
			try:
				self.dev_lock[dev].release()
			except threading.ThreadError:
				print "Lock for device queue: %s already unlocked." % \
					enum.Device.get_name[dev]
			finally:
				return item
		else:
			return None

	def get_queue_len(self, dev):
		''' Returns the current queue length of a given device queue.
		'''
		if dev != enum.Device.INVALID:
			return len(self.dev_que[dev])
		else:
			return 0

# FUNCTIONS

# CODE
if __name__ == '__main__':
	print "Do not run state_mgr.py from __main__."

# END OF FILE