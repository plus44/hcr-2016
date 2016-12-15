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

# CLASSES

# FUNCTIONS
def main(host, port):
	''' Performs the operations of the laptop client, connecting to a 
	server on host:port.
	'''
	client = LaptopClient(host, port=port)
	client.set_first_start(False)
	if client.post_success():
		print "Successfully told Raspberry Pi to turn page."
	

def parse_host_and_port(args=None):
	''' Returns a tuple of the parsed address and port arguments from the 
	command line
	'''
	parser = argparse.ArgumentParser(description= \
		"Connects to the server, and posts a 'turnPage' action to the " \
		"Raspberry Pi.")
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

	results = parser.parse_args(args)
	return (results.host, int(results.port))

# CODE
if __name__ == '__main__':
	host, port = parse_host_and_port(sys.argv[1:])
	main(host, port)
else:
	print "Run set_pi_holder_arm_degrees.py from __main__."

# END OF FILE