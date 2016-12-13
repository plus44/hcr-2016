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
class DummyPhoneClient():
	""" Exposes a simple interface to the main program for accessing the server.
	Pretends to act like the phone client will.
	"""
	def __init__(self, host, port=80):
		''' Initialises the client on default port 80, on a provided host.
		'''
		self._host = host
		self._port = port
		self.post_req = {"doneTakingPicture" : False, 
						 "error" : "NotInitialized", 
						 "picture" : None}
		self.conn = httplib.HTTPConnection(self._host, self._port)

	def long_poll(self):
		''' Long polls the server. If code 204 is returned, the server has timed
		out and the long-poll is re-initiated.
		'''
		try:
			self.conn.request('GET', '/phone', '')
			response = self.conn.getresponse()
		
			while response.status == 204:
				self.conn.request('GET', '/phone', '')
				response = self.conn.getresponse()

			if response.status == 200:
				return response.read()
		except:
			print "Returning from phone long-polling."
			return ''

	def post_success(self):
		''' POST request to the server that sends the picture across.

		Returns True if successfully sent the request.
		Returns False if request failed sending.
		'''
		self.post_req["doneTakingPicture"] = True
		self.post_req["error"] = "None"
		self.post_req["picture"] = "somePicture"
		return self._do_post_request()

	def _do_post_request(self):
		''' Sends the POST request to the server as a JSON string with the 
		contents given by self.post_req.
		'''
		try:
			self.conn.request('POST', '/phone', json.dumps(self.post_req), \
				{"Content-type" : "application/json"})
			response = self.conn.getresponse()

			if response.status == 200:
				return True
		except:
			print "Phone failed sending POST request to server."

		return False

# FUNCTIONS

# CODE
if __name__ == '__main__':
	print "Do not run client.py from __main__."

# END OF FILE