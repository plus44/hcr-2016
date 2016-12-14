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
import enum
from client import RaspberryPiClient
from page_turner import PageTurner

# GLOBAL VARIABLES

# CLASSES
class PiStateMachine():
	''' Describes the state machine that handles the server comms and the page 
	turning class.
	'''
	def __init__(self, client=None, page_turner=None):
		''' Initialise the state machine

			'client' is a RaspberryPiClient() instance
			'page_turner' is a PageTurner() instance
		'''
		self._client = client
		self._page_turner = page_turner
		self.state = enum.PiState.QUEUE_LONG_POLL

		self.action = 'doNothing'
		self.is_done_long_polling = False
		self.turned_page = False

	def set_client(self, client):
		''' Set up the internal reference to the client.
		'''
		self._client = client

	def set_page_turner(self, page_turner):
		''' Set up the internal reference to the page_turner
		'''
		self._page_turner = page_turner

	def handler_done_long_polling(self, action):
		''' Handler that gets called when the server returns an action from long
		polling.
		'''
		self.action = action
		self.is_done_long_polling = True
		print "Action received from server: %s" % action

	def handler_turned_page(self):
		''' Handler that gets called by the page turner whenever it has finished
		turning a page.
		'''
		self.turned_page = True
		print "Finished turning a page."

	def process_state(self):
		''' Step through the states as needed, queuing tasks in the process.
		'''
		if self.state == enum.PiState.QUEUE_LONG_POLL:
			self._client.queue_long_poll()
			self.state = enum.PiState.WAIT_FOR_ACTION
			return

		elif self.state == enum.PiState.WAIT_FOR_ACTION:
			if self.is_done_long_polling:
				self.is_done_long_polling = False
				self.state = enum.PiState.PROCESS_ACTION
			return

		elif self.state == enum.PiState.PROCESS_ACTION:
			if self.action == 'turnPage':
				self.state = enum.PiState.QUEUE_TURN_PAGE

			elif 'setWheelDegrees' in self.action:
				lst = self.action.split(':', 1)
				try:
					wheel_degrees = int(lst[1])
					self._page_turner.set_wheel_degrees(wheel_degrees)
				except ValueError:
					print "Couldn't convert wheelDegrees %s to int." % lst[1]

				print "Wheel degrees are now: %d" % \
					self._page_turner.get_wheel_degrees()
				# Go back to long polling
				self.state = enum.PiState.QUEUE_LONG_POLL

			elif 'setHolderArmDegrees' in self.action:
				lst = self.action.split(':', 1)
				try:
					holder_arm_degrees = int(lst[1])
					self._page_turner.set_holder_arm_degrees(holder_arm_degrees)
				except ValueError:
					print "Couldn't convert holderArmDegrees %s to int." % \
						lst[1]

				print "Holder arm degrees are now: %d" % \
					self._page_turner.get_holder_arm_degrees()
				# Go back to long polling
				self.state = enum.PiState.QUEUE_LONG_POLL

			else:
				print "Invalid action received: %s" % self.action
				# Go back to long polling
				self.state = enum.PiState.QUEUE_LONG_POLL
			return

		elif self.state == enum.PiState.QUEUE_TURN_PAGE:
			self._page_turner.queue_turn_page()
			self.state = enum.PiState.WAIT_FOR_PAGE_TURN
			return

		elif self.state == enum.PiState.WAIT_FOR_PAGE_TURN:
			print "Got to state WAIT_FOR_PAGE_TURN"
			if self.turned_page:
				self.turned_page = False
				print "Posting success server: %s" % self._client.post_success()
				self.state = enum.PiState.QUEUE_LONG_POLL
			return

		else:
			print "Entered invalid state: %s" % self.state
			return


# FUNCTIONS
def main(host, port=80):
	''' Performs the operations of the Raspberry Pi client, connecting to a 
	server on host:port.
	'''
	state_machine = PiStateMachine()

	client = RaspberryPiClient(host, port=port, state_machine=state_machine)
	page_turner = PageTurner(state_machine=state_machine)

	# Set up the recursive references
	state_machine.set_client(client)
	state_machine.set_page_turner(page_turner)

	while True:
		state_machine.process_state()

	# action = client.long_poll()
	# print "Action: %s received from the server." % action

	# if action == "turnPage":
	# 	### Turn page ###

	# 	# Simulate page turn with a delay
	# 	start_time = time.time()
	# 	while (time.time() - start_time < 5.0):
	# 		pass

	# 	print "Page turned: %s" % client.post_success()

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
