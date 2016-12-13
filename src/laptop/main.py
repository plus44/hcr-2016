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
from gesture_controller import GestureController
from speech_controller import SpeechController

# GLOBAL VARIABLES
DEFAULT_ROBOT_IP = "169.254.44.123"
DEFAULT_ROBOT_PORT = 9559

# CLASSES
class GlobalStateMachine():
	''' Describes the state machine that handles server, OCR, speech, gestures
	'''
	def __init__(self, client=None, ocr=None, gesture_controller=None, \
		speech_controller=None):
		''' Initialise the state machine

			'client' is a LaptopClient() instance
			'ocr' is an OCRController() instance
		'''
		self._client = client
		self._ocr = ocr
		self._gesture_controller = gesture_controller
		self._speech_controller = speech_controller
		self.state = enum.State.INIT
		self.image = ""
		self.is_done_long_polling = False
		self.extracted_string = ""
		self.done_extracting_text = False
		self.done_telling_story = False
		self.done_init_speech = False
		self.error = 'None'
		self.first_start = True

	def handler_done_long_polling(self, image):
		''' Handler that gets called by the client whenever long-polling has a
		result that needs servicing.
		'''
		self.image = image
		self.is_done_long_polling = True
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
		self.done_extracting_text = True
		print "Extracted text: %s" % self.extracted_string.encode('utf-8')

	def handler_told_story(self):
		''' Handler that gets called by the gesture controller whenever it has
		finished telling the story it was queued to say.
		'''
		self.done_telling_story = True
		print "Finished telling story."	

	def handler_speech_done_init_seq(self):
		''' Handler that gets called by the speech controller whenever it has 
		finished doing the initial interaction.
		'''
		self.done_init_speech = True
		print "Finished speech interaction initialisation sequence."

	def set_client(self, client):
		''' Set the internal variable _client, after it has been initialised 
		with a reference to self
		'''
		self._client = client

	def set_ocr(self, ocr):
		''' Set the internal variable _ocr, after it has been initialised with
		a reference to self
		'''
		self._ocr = ocr

	def set_gesture_controller(self, gesture_controller):
		''' Set the internal variable _gesture_controller, after it has been 
		initialised with a reference to self.
		'''
		self._gesture_controller = gesture_controller
		
	def set_speech_controller(self, speech_controller):
		''' Set the internal variable _speech_controller, after it has been 
		initialised with a reference to self.
		'''
		self._speech_controller = speech_controller

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

		elif self.state == enum.State.QUEUE_INIT_SPEECH:
			self._speech_controller.start_init_seq()
			self.state = enum.State.WAIT_FOR_INIT_SPEECH
			return

		elif self.state == enum.State.WAIT_FOR_INIT_SPEECH:
			if self.done_init_speech:
				self.done_init_speech = False
				self.state = enum.State.REQUEST_IMAGE
			return

		elif self.state == enum.State.REQUEST_IMAGE:
			self._client.set_first_start(self.first_start)

			print "Successfully set first start to: %s" % self.first_start
			if self.error == 'None':
				self._client.post_success()
			else:
				self._client.post_failure(self, self.error)
			self.state = enum.State.QUEUE_LONG_POLL

			# First start should only be true the first time we post to server
			if self.first_start:
				self.first_start = False

			return

		elif self.state == enum.State.QUEUE_LONG_POLL:
			# Queue a long poll, waiting for a picture
			self._client.queue_long_poll()
			self.state = enum.State.WAIT_FOR_IMAGE
			return

		elif self.state == enum.State.WAIT_FOR_IMAGE:
			# While we're waiting, for the long-poll to finish, do nothing...
			# Long polling has finished
			if self.is_done_long_polling:
				self.is_done_long_polling = False
				self.state = enum.State.QUEUE_OCR
			return

		elif self.state == enum.State.QUEUE_OCR:
			# Extract the text from the picture
			self._ocr.queue_extract_text('photo/latest.jpeg')
			self.state = enum.State.WAIT_FOR_OCR
			return

		elif self.state == enum.State.WAIT_FOR_OCR:
			# While we're waiting for the OCR to finish, do nothing...
			# OCR has finished
			if self.done_extracting_text:
				self.done_extracting_text = False
				self.state = enum.State.QUEUE_TELL_STORY
			return

		elif self.state == enum.State.QUEUE_TELL_STORY:
			# Tell the story
			self._gesture_controller.tell_story(self.extracted_string)
			self.state = enum.State.WAIT_FOR_STORY
			return

		elif self.state == enum.State.WAIT_FOR_STORY:
			if self.done_telling_story:
				self.done_telling_story = False
				# Go back to requesting an image
				self.state = enum.State.REQUEST_IMAGE
			return

		else:
			print "Entered invalid state: %s" % self.state
			return

# FUNCTIONS
def main(host, port, robot_ip, robot_port):
	''' Performs the operations of the laptop client, connecting to a 
	server on host:port.
	'''

	state_machine = GlobalStateMachine()
	client = LaptopClient(host, port=port, state_machine=state_machine)
	ocr = OCRController(state_machine=state_machine)
	gesture_controller = GestureController(robot_ip, robot_port, \
		state_machine=state_machine)
	speech_controller = SpeechController(gesture_controller, \
		state_machine=state_machine)

	# Set up the recursive references
	state_machine.set_client(client)
	state_machine.set_ocr(ocr)
	state_machine.set_gesture_controller(gesture_controller)
	state_machine.set_speech_controller(speech_controller)

	while True:
		state_machine.process_state()

	# init()
	# print "Processing done: %s" % client.post_success()

	# picture = client.long_poll()
	# print "Picture: %s received from the server." % picture
	# with open('photo/latest.jpeg', 'wb') as fh:
	# 	fh.write(picture.decode('base64'))

def parse_hosts_and_ports(args=None):
	''' Returns a tuple of the parsed address and port arguments from the 
	command line
	'''
	parser = argparse.ArgumentParser(description= \
		"Connects to the server, waits for pictures from the phone and tells " \
		"the server what to do next. Once a picture is received, it OCRs it " \
		"and it passes the text to the robot, which will speak it.")
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
	parser.add_argument('-ri', '--robot_ip',
						type=str,
						help="IP of the robot",
						required=False,
						default=DEFAULT_ROBOT_IP)
	parser.add_argument('-rp', '--robot_port',
						type=int,
						help="Port of the robot",
						required=False,
						default=DEFAULT_ROBOT_PORT)

	results = parser.parse_args(args)
	return (results.host, int(results.port), results.robot_ip, \
		int(results.robot_port))

# CODE
if __name__ == '__main__':
	host, port, robot_ip, robot_port = parse_hosts_and_ports(sys.argv[1:])
	main(host, port, robot_ip, robot_port)
else:
	print "Run main.py from __main__."

# END OF FILE