#! /usr/bin/python
''' Implements an HTTP client for the laptop
'''

# STANDARD PYTHON IMPORTS
import json

# PYTHON LIBRARIES
import httplib

# USER LIBRARIES

# GLOBAL VARIABLES

# CLASSES
class LaptopClient():
	""" Exposes a simple interface to the main program for accessing the server.
	"""
	def __init__(self, host, port=80):
		''' Initialises the client on default port 80, on a provided host.
		'''
		self._host = host
		self._port = port
		self.post_req = {"doneProcessing" : False, "error" : "NotInitialized"}
		self.conn = httplib.HTTPConnection(self._host, self._port)

	def long_poll(self):
		''' Long polls the server. If code 204 is returned, the server has timed
		out and the long-poll is re-initiated.
		'''
		try:
			self.conn.request("GET", "/laptop", "")
			response = self.conn.getresponse()
		
			while response.status == 204:
				self.conn.request("GET", "/laptop", "")
				response = self.conn.getresponse()

			if response.status == 200:
				return response.read()
		except:
			print "Returning from long-polling."
			return ""

	def post_success(self):
		''' POST request to the server that tells it we're done processing stuff
		without any errors.

		Returns True if successfully sent the request.
		Returns False if request failed sending.
		'''
		self.post_req["doneProcessing"] = True
		self.post_req["error"] = "None"
		return self._do_post_request()

	def post_failure(self, error):
		''' POST request to the server with an error code.

		Returns True if successfully sent the request.
		Returns False if request failed sending.
		'''
		self.post_req["doneProcessing"] = True
		self.post_req["error"] = error
		return self._do_post_request()

	def _do_post_request(self):
		''' Sends the POST request to the server as a JSON string with the 
		contents given by self.post_req.
		'''
		try:
			self.conn.request("POST", "/laptop", json.dumps(self.post_req), \
				{"Content-type" : "application/json"})
			response = self.conn.getresponse()

			if response.status == 200:
				return True
		except:
			print "Failed sending POST request to server."

		return False

# FUNCTIONS

# CODE
if __name__ == '__main__':
	print "Do not run client.py from __main__."

# END OF FILE