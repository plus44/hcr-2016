#! /usr/bin/python
''' Provides enumerated variable types to the laptop
'''

# STANDARD PYTHON IMPORTS

# PYTHON LIBRARIES

# USER LIBRARIES

# GLOBAL VARIABLES

# CLASSES

# FUNCTIONS
def enum(*sequential, **named):
	''' Enables the use of enumerated types in python. Returns an Enum() type, 
	the lookup of which returns entries from the enums dictionary. Reverse 
	mapping available as MyEnum.get_name(my_enum_value).
	'''
	enums = dict(zip(sequential, range(len(sequential))), **named)
	reverse = dict((value, key) for key, value in enums.iteritems())
	enums['get_name'] = reverse
	return type('Enum', (), enums)

# CODE
if __name__ == '__main__':
	print "Do not run enum.py from __main__."
else:
	PiState = enum('QUEUE_LONG_POLL', 'WAIT_FOR_ACTION', 'PROCESS_ACTION', \
		'QUEUE_TURN_PAGE', 'WAIT_FOR_PAGE_TURN')

# END OF FILE