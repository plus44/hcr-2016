#! /usr/bin/python
''' HTTP Server implementation that handles comms between RasPi and iPhone.
'''

# STANDARD PYTHON IMPORTS
import os
import argparse
import sys
from os import sep

# PYTHON LIBRARIES
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn

# USER LIBRARIES
import enum
from thread_mgr import ThreadManager
from state_mgr import StateManager
from devices import DeviceManager

# GLOBAL VARIABLES
DEFAULT_PORT_NUMBER = 8080
SERVER_DIR = os.path.dirname(os.path.realpath(__file__)) + sep + 'www'

# CLASSES
class RequestHandler(BaseHTTPRequestHandler):
	''' Handles HTTP requests to the server
	'''
	def __init__(self, dev_mgr, *args):
		''' Initialise handler instance variables
		'''
		self._dev_mgr = dev_mgr
		BaseHTTPRequestHandler.__init__(self, *args)

	def do_GET(self):
		''' Handler for GET requests to the server.
		'''
		if self.path == '/':
			self.path = '/index.html'
			f = open(SERVER_DIR + self.path)
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			self.wfile.write(f.read())
			f.close()

		elif self.path == '/pi':
			content = self._dev_mgr.long_poll(enum.Device.PI)
			if content == None:
				# Do nothing
				pass
			elif content == False:
				# Send 204 No Content
				self.send_response(204)
				self.end_headers()
			else:
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				self.wfile.write(content)

		elif self.path == '/phone':
			content = self._dev_mgr.long_poll(enum.Device.PHONE)
			if content == False:
				# Send 204 No Content
				self.send_response(204)
				self.end_headers()
			else:
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				self.wfile.write(content)

		elif self.path == '/laptop':
			content = self._dev_mgr.long_poll(enum.Device.LAPTOP)
			if content == False:
				# Send 204 No Content
				self.send_response(204)
				self.end_headers()
			else:
				self.send_response(200)
				self.send_header('Content-type', 'image/jpeg')
				self.end_headers()
				self.wfile.write(content)

		else:
			self.send_error(404, "Path %s does not exist." % self.path)

	def do_POST(self):
		''' Handler for POST requests to the server.
		'''
		# Fetch the body from the HTTP request
		content_len = int(self.headers.getheader('Content-length', 0))
		body = self.rfile.read(content_len)

		bad_path = False

		if self.path == '/pi':
			self._dev_mgr.handle_post(enum.Device.PI, body)
		elif self.path == '/phone':
			self._dev_mgr.handle_post(enum.Device.PHONE, body)
		elif self.path == '/laptop':
			self._dev_mgr.handle_post(enum.Device.LAPTOP, body)
		else:
			bad_path = True

		if bad_path:
			self.send_error(404, "Path %s does not exist." % self.path)
		else:
			self.send_response(200)
			self.end_headers()



class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	''' Handle requests in a separate thread
	'''

# FUNCTIONS
def main(port=DEFAULT_PORT_NUMBER):
	''' Performs the main operations of the server program on a given port.
	'''
	try:
		# Create a global thread manager for all our devices
		thread_mgr = ThreadManager()
		# Create a global state manager for handling device queues
		state_mgr = StateManager()
		# Initialise the device manager
		dev_mgr = DeviceManager(thread_mgr, state_mgr)

		def handler(*args):
			''' Initialise our custom handler with the device manager.
			'''
			RequestHandler(dev_mgr, *args)

		# Create a web server and define the handler to manage the incoming 
		# requests on separate threads.
		server = ThreadedHTTPServer(('', port), handler)
		print "Started ThreadedHTTPServer on port %d" % port

		# Wait forever for incoming HTTP requests
		server.serve_forever()

	except KeyboardInterrupt:
		print "Shutting down HTTPServer."
		server.socket.close()

def parse_port(args=None):
	''' Returns the parsed port argument from the command line
	'''
	parser = argparse.ArgumentParser(description= \
		'Starts the server on a specified port.')
	parser.add_argument('-p', '--port',
						type=int,
						help='Port to start the server on.',
						default=DEFAULT_PORT_NUMBER)
	results = parser.parse_args(args)
	return int(results.port)

# CODE
if __name__ == '__main__':
	port = parse_port(sys.argv[1:])
	main(port)
else:
	print "Run main.py from __main__."

# END OF FILE
