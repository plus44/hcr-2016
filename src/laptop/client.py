#! /usr/bin/python
''' Implements an HTTP client for the laptop
'''

# STANDARD PYTHON IMPORTS
import json
import base64
import httplib

# PYTHON LIBRARIES

# USER LIBRARIES

# GLOBAL VARIABLES

# CLASSES
class LaptopClient():
	""" Exposes a simple interface to the main program for accessing the server.
	"""
	def __init__(self, host, port=80, state_machine=None):
		''' Initialises the network client on the laptop.

			'host' is the server address
			'port' is the server port (80 for HTTP)
			'state_machine' is a reference to the state_machine that contains a 
				function 'handler_done_long_polling(image)' to handle the end of 
				long-polls.
		'''
		self._host = host
		self._port = port
		self._state_machine = state_machine
		self.post_req = {"doneProcessing" : False, "error" : "NotInitialized"}
		self.conn = httplib.HTTPConnection(self._host, self._port)
		self.is_long_polling = False
		self.decoded_image = ""

	def queue_long_poll(self):
		''' Queues a long-poll to the server on a background thread. When the 
		long-polling is complete, self.is_long_polling will be deasserted and
		the result of the request will be in self.decoded_image. 

		Additionally, the state_machine's handler_done_long_polling() method 
		will be called with the decoded image as the single parameter.

		TODO: BACKGROUND THREAD
		'''
		self.decoded_image = self.long_poll()
		self._state_machine.handler_done_long_polling(self.decoded_image)

	def long_poll(self):
		''' Long polls the server. If code 204 is returned, the server has timed
		out and the long-poll is re-initiated. 
	
		A valid return of the laptop's long-poll will contain a base64 decoded 
			picture, as per the server's specification.
		'''
		try:
			self.is_long_polling = True
			self.conn.request("GET", "/laptop", "")
			response = self.conn.getresponse()
		
			while response.status == 204:
				self.conn.request("GET", "/laptop", "")
				response = self.conn.getresponse()

			if response.status == 200:
				self.is_long_polling = False
				return response.read().decode('base64')
		except:
			self.is_long_polling = False
			print "Returning from laptop long-polling."
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
			print "Laptop failed sending POST request to server."

		return False

# FUNCTIONS

# CODE
if __name__ == '__main__':
	print "Do not run client.py from __main__."

# END OF FILE