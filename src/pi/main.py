#! /usr/bin/python
''' Performs all the HTTP client functions, as well as the page turning 
functions of the Raspberry Pi.
'''

# STANDARD PYTHON IMPORTS
import argparse
import sys
import time

# PYTHON LIBRARIES

# USER LIBRARIES
from client import RaspberryPiClient

# GLOBAL VARIABLES

# CLASSES

# FUNCTIONS
def main(host, port=80):
	''' Performs the operations of the Raspberry Pi client, connecting to a 
	server on host:port.
	'''
	client = RaspberryPiClient(host, port)
	action = client.long_poll()
	print "Action: %s received from the server." % action

	if action == "turnPage":
		### Turn page ###

		# Simulate page turn with a delay
		start_time = time.time()
		while (time.time() - start_time < 5.0):
			pass

		print "Page turned: %s" % client.post_success()

def parse_host_and_port(args=None):
	''' Returns a tuple of the parsed address and port arguments from the 
	command line
	'''
	parser = argparse.ArgumentParser(description= \
		"Connects to the server and waits for page turning instructions")
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
