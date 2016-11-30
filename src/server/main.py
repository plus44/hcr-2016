#! /usr/bin/python
''' HTTP Server implementation that handles comms between RasPi and iPhone.
'''

# STANDARD PYTHON IMPORTS
import os
from os import sep

# PYTHON LIBRARIES
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn

# USER LIBRARIES
import enums
from thread_mgr import ThreadManager

# GLOBAL VARIABLES
PORT_NUMBER = 80
SERVER_DIR = os.path.dirname(os.path.realpath(__file__)) + sep + 'www'

# CLASSES
class RequestHandler(BaseHTTPRequestHandler):
	''' Handles HTTP requests to the server
	'''
	def __init__(self, thread_mgr, *args):
		''' Initialise handler instance variables
		'''
		self._thread_mgr = thread_mgr
		BaseHTTPRequestHandler.__init__(self, *args)

	def do_GET(self):
		''' Handler for GET requests to the server.
		'''
		if self.path == '/':
			self.path = '/index.html'

		try:
			send_reply = False
			if self.path.endswith('.html'):
				mime_type = 'text/html'
				print "Will send reply."
				send_reply = True

			if send_reply:
				print "File path: %s" % SERVER_DIR + self.path
				# Open the static file requested and send it
				f = open(SERVER_DIR + self.path)
				self.send_response(200)
				self.send_header('Content-type', mime_type)
				self.end_headers()
				self.wfile.write(f.read())
				f.close()
			return

		except IOError:
			self.send_error(404, "File not found: %s" % self.path)

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	''' Handle requests in a separate thread
	'''

# FUNCTIONS
def main():
	try:
		# Create a global thread manager for all our devices
		thread_mgr = ThreadManager()

		def handler(*args):
			''' Initialise our custom handler with the global thread manager.
			'''
			RequestHandler(thread_mgr, *args)

		# Create a web server and define the handler to manage the incoming 
		# requests on separate threads.
		server = ThreadedHTTPServer(('', PORT_NUMBER), handler)
		print "Started ThreadedHTTPServer on port %d" % PORT_NUMBER

		# Wait forever for incoming HTTP requests
		server.serve_forever()

	except KeyboardInterrupt:
		print "Shutting down HTTPServer."
		server.socket.close()

# CODE
if __name__ == '__main__':
	main()
else:
	print "This file is meant to be run as main."

# END OF FILE
