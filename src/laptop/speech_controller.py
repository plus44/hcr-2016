import speech_recognition as sr
import argparse
import sys
import time
import base64
import enum

class SpeechController():

	def __init__(self, gestureController, state_machine=None):
		self._state_machine = state_machine
		self._gesture_controller = gestureController
		self.init_state = enum.SpeechState.INIT
		self.done_init_seq = False
		self.processed_speech = ""
		self.n = 0
		self.r = sr.Recognizer()
		self.m = sr.Microphone()
		self.listen_string = ""
		

	def start_init_seq(self):
		while not self.done_init_seq:
			self._start_init_seq()
		if self._state_machine != None:
			self._state_machine.handler_speech_done_init_seq()
		else:
			print "Done init seq"

	def _start_init_seq(self):
		if self.init_state == enum.SpeechState.INIT:
			test_initial = self.ask_user()
			self._gesture_controller.animatedSay(test_initial)
			print test_initial
			self.n = 0
			#resp = self.wait_for_response_or_until_timeout()
			resp = True
			if resp:
				self.init_state = enum.SpeechState.WAIT_FOR_RESPONSE
			else:
				self.init_state = enum.SpeechState.TIMEOUT
			return

		if self.init_state == enum.SpeechState.WAIT_FOR_RESPONSE:
			self.n += 1
			if self.n >= 4:
				self.init_state = enum.SpeechState.DONE
				return

			self.listen_string = self.listen()
			if self.listen_string == "":
				self.init_state = enum.SpeechState.WAIT_FOR_RESPONSE
				self.n = self.n - 1
			else:
				self.init_state = enum.SpeechState.RESPONSE_RECEIVED
			return

		if self.init_state == enum.SpeechState.RESPONSE_RECEIVED:
			response =  self.process_response(self.listen_string, self.n)
			print response
			self._gesture_controller.animatedSay(response)
			#call function that says response

			#gestureController.animatedSpeechProxy.say(response)
			if response == None:
				self.n = self.n - 1
				self._gesture_controller.animatedSay("Sorry, I did not catch that, could you please repeat?")

			self.init_state = enum.SpeechState.WAIT_FOR_RESPONSE
			return

		if self.init_state == enum.SpeechState.DONE:
			self.done_init_seq = True
			return

		# 	if not done:
		# 		self.init_state = enum.SpeechState.ANSWER_BACK
		# 	else:
		# 		self.init_state = enum.SpeechState.DONE
		# 	return

		# if self.init_state == enum.SpeechState.DONE:
		# 	call gesture controller and say text
		# 	self.done_init_seq = True



	def listen(self):
		# print("A moment of silence, please...")
		with self.m as source: 
			self.r.adjust_for_ambient_noise(source)
		# print("Set minimum energy threshold to {}".format(self.r.energy_threshold))
		# print("test1")
		print("Say something!")
		with self.m as source: 
			audio = self.r.listen(source)
		print("Got it! Now to recognize it...")
		var1 = ""
		try:
			# recognize speech using Google Speech Recognition
			value = self.r.recognize_google(audio)
			# we need some special handling here to correctly print unicode characters to standard output
			if str is bytes:  # this version of Python uses bytes for strings (Python 2)
				print(u"You said {}".format(value).encode("utf-8"))
				var1 = u"{}".format(value).encode("utf-8")
			else:
				print("You said {}".format(value))
				print("test3")
		except sr.UnknownValueError:
			print("Oops! Didn't catch that")
		except sr.RequestError as e:
			print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
		return var1

	def process_response(self, var1, n):
		my_dict = self.get_dictionary(n)
		#print "[n = %d] MY_DICT: %s" % (n, my_dict)
		#print "var1 = %s" % var1
		#print "n = %d"  % n
		ret = ""
		funct_dict = {}
		for keyword, funct in my_dict.iteritems():
			print "var1: %s, keyword: %s, find: %d" % (var1, keyword, var1.find(keyword))
			if var1.find(keyword) >= 0:
				funct_dict[keyword] = funct

		if 'you' in funct_dict:
			ret = funct_dict['you']
		elif len(funct_dict) > 0:
			ret = funct_dict.itervalues().next()

		return ret

	def ask_user(self):
		return("Hey! My name is NAO, how are you?")

	def get_dictionary(self, n):
		if n == 1:
			return {"you" : self.how_are_you(),\
					"fine" : self.describe_exp(),\
					"good" : self.describe_exp(),\
					"thanks" : self.describe_exp(),\
					"hi" : self.describe_exp(),\
					"hello" : self.describe_exp(),\
					"well" : self.describe_exp(),\
					}
		if n == 2:
			return {"high" : self.increase_vol(),\
					"higher" : self.increase_vol(),\
					"hi" : self.increase_vol(),\
					"hiya" : self.increase_vol(),\
					"more" : self.increase_vol(),\
					"low" : self.decrease_vol(),\
					"lower" : self.decrease_vol(),\
					"less" : self.decrease_vol(),\
					"ok" : self.ok_vol(),\
					"fine" : self.ok_vol(),\
					}
		if n == 3: 
			return {"fast" : self.increase_speed(),\
					"faster" : self.increase_speed(),\
					"hi" : self.increase_speed(),\
					"slow" : self.decrease_speed(),\
					"slower" : self.decrease_speed(),\
					"ok" : self.ok_speed(),\
					"fine" : self.ok_speed(),\
					}
		# if n == 4:
		# 	return {"ok" : self.start_read(),\
		# 			"alright" : self.start_read(),\
		# 			"fine" : self.start_read(),\
		# 			"sure" : self.start_read(),\
		# 			}
	def ask_user(self):
		return("Hey! My name is Pinaoqio, how are you?") 	
	
	def how_are_you(self):
		return("I'm fine, thanks. " + self.describe_exp())

	def describe_exp(self):
		return ("Today, I am going to be reading a passage from an eagle in the snow, by Michael Morpurgo. Let's check the volume. Could you please say more or less if you would like higher or lower volume, or OK if the volume is fine.")

	def increase_vol(self):
		self._gesture_controller.incrementVol()
		return("Great, I have increased the volume. What do you think about the speed? Please say faster, slower, or ok.")

	def decrease_vol(self):
		self._gesture_controller.decrementVol()
		return("Great, I have decreased the volume. What do you think about the speed? Please say faster, slower, or ok.")

	def ok_vol(self):
		return("I am glad you like the volume. What do you think about the speed? Please say faster, slower, or ok.")

	def increase_speed(self):
		self._gesture_controller.incrementSpeed()
		return("Alright, I have increased the speed. I am now ready to read you a story! Please say ok when you are ready!")

	def decrease_speed(self):
		self._gesture_controller.decrementSpeed()
		return("Alright, I have decreased the speed. I am now ready to read you a story! Please say ok when you are ready!")

	def ok_speed(self):
		return("Perfect. I am now ready to read the a story! I will take a picture of the book to process its text, sorry for the wait!")

	# def start_read(self):
	# 	#start reading
	# 	return("starting")

	# def listen_while_reading()
	# 	print("A moment of silence, please...")
	# 	with m as source: r.adjust_for_ambient_noise(source)
	# 	print("Set minimum energy threshold to {}".format(r.energy_threshold))
	# 	while var1 != "stop":
	# 	print("test1")
	# 		print("Say something!")
	# 		with m as source: audio = r.listen(source)
	# 		print("Got it! Now to recognize it...")
	# 		try:
	# 			# recognize speech using Google Speech Recognition
	# 			value = r.recognize_google(audio)
	# 			# we need some special handling here to correctly print unicode characters to standard output
	# 			if str is bytes:  # this version of Python uses bytes for strings (Python 2)
	# 			   print(u"You said {}".format(value).encode("utf-8"))
	# 			   var1 = u"You said {}".format(value).encode("utf-8")
	# 			else:  	# 			else:  # this version of Python uses unicode for strings (Python 3+)
# this version of Python uses unicode for strings (Python 3+)
	# 				print("You said {}".format(value))
	# 		print("test3")
	# 		except sr.UnknownValueError:
	# 			print("Oops! Didn't catch that")
	# 		except sr.RequestError as e:
	# 			print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
	# 	return var1

def main ():
	speech_controller = SpeechController()
	speech_controller.start_init_seq()

if __name__ == "__main__":
	main()
