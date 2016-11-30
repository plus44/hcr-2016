#! /usr/bin/python
''' Manages the states and queues of the devices
'''

# STANDARD PYTHON IMPORTS
from collections import deque

# PYTHON LIBRARIES

# USER LIBRARIES
import enums

# GLOBAL VARIABLES

# CLASSES
class StateManager():
	''' Holds the device queues
	'''
	def __init__(self):
		''' Create empty queues for each device
		'''
		self.dev_que = {EnumDevice.PI : deque(), \
						EnumDevice.PHONE : deque(), \
						EnumDevice.LAPTOP : deque()}

# FUNCTIONS

# CODE
if __name__ == '__main__':
	print "Do not run state_mgr.py from __main__."

# END OF FILE