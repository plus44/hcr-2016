import speech_recognition as sr
import argparse
import sys
import time
import base64
import enum

class SpeechController():

	r = sr.Recognizer()
	m = sr.Microphone()
	
	def __init__(self, state_machine=None):
		self._state_machine = state_machine
		self.init_state = enum.SpeechState.INIT
		self.done_init_seq = False
		self.processed_speech = ""

	def start_init_seq(self):
		while not self.done_init_seq:
			self._start_init_seq()
		if self._state_machine != None:     
			self._state_machine.handler_speech_done_init_seq()
		else:
			print "Done init seq"

	def _start_init_seq(self):
		if self.init_state == enum.SpeechState.INIT:
			self.ask_user()
			n = 0
			resp = self.wait_for_response_or_until_timeout()
			if resp:
				self.init_state = enum.SpeechState.RESPONSE_RECEIVED
			else:
				self.init_state = enum.SpeechState.TIMEOUT
			return

		if self.init_state == enum.SpeechState.RESPONSE_RECEIVED:
			n+=1            
			#done = self.process_response(string, n)
			string = self.listen()
			response =  self.process_response(string, n)
			self.init_state = enum.SpeechState.DONE

	
		# 	if not done:
		# 		self.init_state = enum.SpeechState.ANSWER_BACK
		# 	else:
		# 		self.init_state = enum.SpeechState.DONE
		# 	return

		# if self.init_state == enum.SpeechState.DONE:
		# 	call gesture controller and say text
		# 	self.done_init_seq = True


	def listen():
		print("A moment of silence, please...")
		with m as source: r.adjust_for_ambient_noise(source)
		print("Set minimum energy threshold to {}".format(r.energy_threshold))
		print("test1")
		print("Say something!")
		with m as source: audio = r.listen(source)
		print("Got it! Now to recognize it...")
		try:
			# recognize speech using Google Speech Recognition
			value = r.recognize_google(audio)
			# we need some special handling here to correctly print unicode characters to standard output
			if str is bytes:  # this version of Python uses bytes for strings (Python 2)
				print(u"You said {}".format(value).encode("utf-8"))
				var1 = u"You said {}".format(value).encode("utf-8")
			else:
				print("You said {}".format(value))
				print("test3")
		except sr.UnknownValueError:
			print("Oops! Didn't catch that")
		except sr.RequestError as e:
			print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
		return var1

	def process_response(var1, n):
		my_dict ={}
		my_dict = get_dictionary(n)
		for keyword, funct in my_dict:
			if var1.find(keyword):
				return(funct)
			else:
				if n == 1:
					return (describe_exp())
				if n == 2:
					return (ok_vol())

	def get_dictionary(n):
		if n == 1:
			return {"you" : how_are_you()}
		if n == 2:
			return {"high" : increase_vol(),\
					"higher" : increase_vol(),\
					"low" : decrease_vol(),\
					"lower" : decrease_vol(),\
					"ok" : ok_vol(),\
					"fine" : ok_vol(),\
					}
		if n == 3: 
			return {"high" : increase_speed(),\
					"higher" : increase_speed(),\
					"low" : decrease_speed(),\
					"lower" : decrease_speed(),\
					"ok" : ok_speed(),\
					"fine" : ok_speed(),\
					}
		if n == 4:
			return {"ok" : start_read(),\
					"alright" : start_read(),\
					"fine" : start_read(),\
					"sure" : start_read(),\
					}
		
	
	def how_are_you():
		return("I'm fine thanks" + describe_exp())


	def describe_exp():
		return ("we will read to you. Could you please say high or low if you'd like higher or lower volume, or OK if volume is fine")

	def increase_vol():
		# get volume
		# increment volume
		# upadte volume
		return("I have increased the volume. WHat do you think about the speed? Could say higher, lower, or okay?")

	def decrease_vol():
		# get volume
		# decrement volume
		# upadte volume
		return("I have decreased the volume. WHat do you think about the speed? Could say higher, lower, or okay?")

	def ok_vol():
		return("I am glad you like the volume. WHat do you think about the speed? Could say higher, lower, or okay?")

	def increase_speed():
		# get speed
		# increment speed
		# upadte speed
		return("I have increased the speed. I am now ready to read you a story! Could you say ok when you are ready?")

	def decrease_speed():
		# get speed
		# decrement speed
		# upadte speed
		return("I have decreased the speed. I am now ready to read you a story! Could you say ok when you are ready?")

	def ok_speed():
		return("I am glad you like the speed. I am now ready to read you a story! Could you say ok when you are ready?")

	def start_read():
		#start reading
		return("")

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
