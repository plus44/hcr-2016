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
	State = enum('INIT', 'QUEUE_INIT_SPEECH', 'WAIT_FOR_INIT_SPEECH', \
		'REQUEST_IMAGE', 'QUEUE_LONG_POLL', 'WAIT_FOR_IMAGE', \
		'QUEUE_OCR', 'WAIT_FOR_OCR', 'QUEUE_TELL_STORY', \
		'WAIT_FOR_STORY')
	SpeechState = enum('INIT', 'WAIT_FOR_RESPONSE', 'RESPONSE_RECEIVED', \
		'TIMEOUT', 'DONE')
# END OF FILE
