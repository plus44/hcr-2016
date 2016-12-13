#! /usr/bin/python
''' Describes enumerated variable types for use in the server
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
	print "Do not run enums.py from __main__."
else:
	Device = enum('INVALID', 'PI', 'PHONE', 'LAPTOP')

# END OF FILE