#! /usr/bin/python
''' Call this from __main__ to set the holder arm degrees on the Raspberry Pi.
'''

# STANDARD PYTHON IMPORTS
import argparse
import sys

# PYTHON LIBRARIES

# USER LIBRARIES
from client import LaptopClient

# GLOBAL VARIABLES
DEFAULT_WHEEL_DEGREES = 39

# CLASSES

# FUNCTIONS
def main(host, port, degrees):
	''' Performs the operations of the laptop client, connecting to a 
	server on host:port.
	'''
	client = LaptopClient(host, port=port)
	if client.post_pi_set_holder_arm_degrees(degrees):
		print "Successfully set the degrees of the Raspberry Pi holder arm to" \
			"%d" % degrees
	

def parse_host_and_port(args=None):
	''' Returns a tuple of the parsed address and port arguments from the 
	command line
	'''
	parser = argparse.ArgumentParser(description= \
		"Connects to the server, and changes the degrees of the holder arm on" \
		"the page turner that is connected to the Raspberry Pi.")
	parser.add_argument('-H', '--host',
						type=str,
						help="Server host IP/name",
						required=True,
						default='localhost')
	parser.add_argument('-p', '--port',
						type=int,
						help="Port of the server",
						required=False,
						default=80)
	parser.add_argument('-d', '--degrees',
						type=int,
						help="Degrees to set the pi wheel to",
						required=True,
						default=DEFAULT_WHEEL_DEGREES)

	results = parser.parse_args(args)
	return (results.host, int(results.port), int(results.degrees))

# CODE
if __name__ == '__main__':
	host, port, degrees = parse_host_and_port(sys.argv[1:])
	main(host, port, degrees)
else:
	print "Run set_pi_holder_arm_degrees.py from __main__."

# END OF FILE