#! /usr/bin/python
''' HTTP client, that does OCR, gesture parsing and speech recognition.
'''

# STANDARD PYTHON IMPORTS
import argparse
import sys
import time
import base64

# PYTHON LIBRARIES

# USER LIBRARIES
import enum
from client import LaptopClient
from ocr import OCRController

# GLOBAL VARIABLES

# CLASSES
class GlobalStateMachine():
	''' Describes the state machine that handles server, OCR, speech, gestures
	'''
	def __init__(self, client=None, ocr=None):
		''' Initialise the state machine

			'client' is a LaptopClient() instance
			'ocr' is an OCRController() instance
		'''
		self._client = client
		self._ocr = ocr
		self.state = enum.State.INIT
		self.image = ""
		self.extracted_string = ""
		self.error = 'None'

	def handler_done_long_polling(self, image):
		''' Handler that gets called by the client whenever long-polling has a
		result that needs servicing.
		'''
		self.image = image
		# Save the image to disk 
		with open('photo/latest.jpeg', 'wb') as fh:
			fh.write(self.image)
		fh.close()
		print "Received an image from server. Saved it to disk."

	def handler_extracted_text(self, text):
		''' Handler that gets called by the OCR whenever it has finished 
		extracting text from a string.
		'''
		self.extracted_string = text
		print "Extracted text: %s" % self.extracted_string.encode('utf-8')

	def set_client_and_ocr(self, client, ocr):
		''' Set the internal variables _client and _ocr, after they have been
		initialised with a reference to self
		'''
		self._client = client
		self._ocr = ocr

	def perform_init_sequence(self):
		''' Initialise the sub-modules of the laptop.
		'''
		start_time = time.time()
		while (time.time() - start_time < 5.0):
			pass

	def process_state(self):
		''' Step through the states as needed, queuing tasks in the process.
		'''
		if self.state == enum.State.INIT:
			self.perform_init_sequence()
			self.state = enum.State.REQUEST_IMAGE
			return

		elif self.state == enum.State.REQUEST_IMAGE:
			if self.error == 'None':
				self._client.post_success()
			else:
				self._client.post_failure(self, self.error)
			self.state = enum.State.INITIATE_LONG_POLL
			return

		elif self.state == enum.State.INITIATE_LONG_POLL:
			self._client.queue_long_poll()
			self.state = enum.State.WAIT_FOR_IMAGE
			return

		elif self.state == enum.State.WAIT_FOR_IMAGE:
			# While we're waiting, for the long-poll to finish, do nothing
			if self._client.is_long_polling:
				pass
			# Long polling has finished
			else:
				self.state = enum.State.INITIATE_OCR
			return

		elif self.state == enum.State.INITIATE_OCR:
			self._ocr.queue_extract_text('photo/latest.jpeg')
			self.state = enum.State.WAIT_FOR_OCR
			return

		elif self.state == enum.State.WAIT_FOR_OCR:
			# Do nothing while we're waiting for OCR to finish
			if self._ocr.is_extracting:
				pass
			# OCR has finished
			else:
				self.state = enum.State.PARSE_GESTURES
			return

		elif self.state == enum.State.PARSE_GESTURES:
			# TODO: actual gesture parsing
			# Go back to requesting an image
			self.state = enum.State.REQUEST_IMAGE
			return


# FUNCTIONS
def main(host, port=80):
	''' Performs the operations of the laptop client, connecting to a 
	server on host:port.
	'''

	state_machine = GlobalStateMachine()
	client = LaptopClient(host, port=port, state_machine=state_machine)
	ocr = OCRController(state_machine=state_machine)

	state_machine.set_client_and_ocr(client, ocr)

	while True:
		state_machine.process_state()

	# init()
	# print "Processing done: %s" % client.post_success()

	# picture = client.long_poll()
	# print "Picture: %s received from the server." % picture
	# with open('photo/latest.jpeg', 'wb') as fh:
	# 	fh.write(picture.decode('base64'))

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