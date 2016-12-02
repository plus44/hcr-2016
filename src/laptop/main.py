#! /usr/bin/python
''' HTTP client, that does OCR, gesture parsing and speech recognition.
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
def main(host, port=80):
	''' Performs the operations of the laptop client, connecting to a 
	server on host:port.
	'''
	client = LaptopClient(host, port)
	# action = client.long_poll()
	# print "Action: %s received from the server." % action
	print "Processing done: %s" % client.post_success()

def parse_host_and_port(args=None):
	''' Returns a tuple of the parsed address and port arguments from the 
	command line
	'''
	parser = argparse.ArgumentParser(description= \
		"Connects to the server, waits for pictures from the phone and tells " \
		"the server what to do next.")
	parser.add_argument('-H', '--host',
						help="Host IP/name",
						required='True',
						default='localhost')
	parser.add_argument('-p', '--port',
						type=int,
						help="Port of the server",
						default=80)

	results = parser.parse_args(args)
	return (results.host, int(results.port))

# CODE
if __name__ == '__main__':
	host, port = parse_host_and_port(sys.argv[1:])
	main(host, port)
else:
	print "Run main.py from __main__."

# END OF FILE