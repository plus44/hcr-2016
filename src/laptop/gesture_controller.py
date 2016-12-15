#! /usr/bin/python
''' Implements the Gesture controller using NAOqi API
'''

# STANDARD PYTHON IMPORTS
import math
import sys
from naoqi import ALProxy

# PYTHON LIBRARIES


# USER LIBRARIES

# GLOBAL VARIABLES
OVERRIDE = 6
should_set_random_gestures = True

# CLASSES
class GestureController():
	""" Implements gestures associated with specific key words/phrases.
	"""
	def __init__(self, robotIP, robotPort, state_machine=None):
	
		self._state_machine = state_machine

		#Setting up the Proxies
		try:
			self.motionProxy = ALProxy("ALMotion", robotIP, robotPort)
		except Exception, e:
			print "Could not create proxy to ALMotion"
			print "Error was: ", e

		try:
			self.postureProxy = ALProxy("ALRobotPosture", robotIP, robotPort)
		except Exception, e:
			print "Could not create proxy to ALRobotPosture"
			print "Error was: ", e

		try:    
			self.ttsProxy = ALProxy("ALTextToSpeech", robotIP, robotPort)
		except Exception, e:
			print "Could not create proxy to ALTextToSpeech"
			print "Error was: ", e
		
		try:
			self.animatedSpeechProxy = ALProxy("ALAnimatedSpeech", robotIP, robotPort)
		except Exception, e:
			print "Could not create proxy to ALAnimatedSpeech"
			print "Error was: ", e

		try:
			self.ledProxy = ALProxy("ALLeds",robotIP, robotPort)
		except Exception, e:
			print "Could not create proxy to ALLeds"
			print "Error was: ", e

		self.ttsProxy.setVolume(0.75)
		self.ttsProxy.setParameter("speed", 80)

		# Turn on the Motors
		self.motionProxy.wakeUp()
		
		# #StandUp
		self.StandUp()

	def __del__(self):
		# Turn off the Motors
		self.motionProxy.rest()

	def tell_story(self, InString):
		string_to_use = ""

		if OVERRIDE == 0:
			string_to_use = "It was at that precise moment, as their eyes met in the cinema, that Billy felt he had met this man before, not on screen, but face to face. And when Hitler raised his hand and brushed his hair back from his forehead, he knew at once who it was, and where they had met, and remembered everything that had happened between them. Christine clutched his arm, looking away from the screen, then buried her head in Billy's shoulder. Billy realised that everyone in that cinema was feeling as she did. It was fear, the kind that gripped your body and soul and wouldn't leave you. No one whistled any more, no one hooted, no one laughed. It was as if everyone in the cinema was holding their breath, waiting for what was to come, dreading the horror of it, but knowing that there was nothing that could stop it, because this man, this Hitler, was going to make it happen. But Billy knew more. All the while Billy looked up into his eyes, and could not look away. All the while he was wondering if what had come into his mind could possibly be true. The more he looked into those eyes, the more he realised that it was, that there could be no doubt about it. That man, that warmonger, was up there now, able to spew out his hatred only because Billy had spared his life all those years before, after the Battle of Marcoing."
		elif OVERRIDE == 1:
			self.StandUp()
			string_to_use = "Then, somewhere, a dog started barking. The eagle lifted off, lumbering into the air, the hare limp in his talons. A dog was bounding down through the snow towards the eagle, towards Billy, hackles up. It was a huge Alsatian, his bark and his growl fearsome, intimidating. That was when Billy looked up, and saw Hitler, in his peaked cap and his long black coat. He was still some way away. He was strolling down the road, and there were six or seven other men, all of them in black uniforms, two of them readying their rifles. Everything was happening so fast and not at all as Billy had expected it. But he kept his head. The dog would not stop him. The sight of the raised rifles would not stop him. He was going to do it. He had to. This was the opportunity he had waiting for all this time."
		else:
			string_to_use = InString

		# # Set body language mode: 0:disabled, 1:random, 2:contextual 
		if should_set_random_gestures:
			self.animatedSpeechProxy.setBodyLanguageMode(2)
		else:
			self.animatedSpeechProxy.setBodyLanguageMode(0)
	


		processedStory = self.dictSearch(string_to_use)[0]
		print processedStory

		customGestureDict = self.init_gesture_dictionary()
		#print customGestureDict[3]
		
				
				
		for i in processedStory:
			if i in customGestureDict:
				customGestureDict[i](i)
			else:
				self.animatedSpeechProxy.say(i)        

		

		# Tell the state machine we're done telling the story.
		if self._state_machine != None:
			self._state_machine.handler_told_story()
		else:
			print "Finished telling story."

	def animatedSay(self, InString):
		self.animatedSpeechProxy.setBodyLanguageMode(2)
		self.animatedSpeechProxy.say(InString)

	def say(self, InString):
		self.ttsProxy.say(InString)

	def dictSearch(self, InString):
		outList = [InString]
		gesture_mapping = { "It was at that precise moment," : "^start(animations/Stand/Gestures/You_4) It was at that, precise moment,", \
							", not on screen," : "^start(animations/Stand/Gestures/No_1) not on screen,", \
							"as their eyes met in the cinema," : "as their eyes met in the cinema,", \
							"that Billy felt he had met this man before" : "^start(animations/Stand/Gestures/Explain_4) that Billy felt he had met this man before", \
							"but face to face." : "^start(animations/Stand/Gestures/Me_2) but face to face", \
							"raised his hand and brushed his hair back from his forehead," : "raised his hand and brushed his hair back from his forehead,", \
							"he knew at once who it was, and where they had met, and remembered" : "he knew at once who it was, and where they had met, and remembered", \
							"everything that had happened between them." : "everything that had happened between them.", \
							"clutched his arm," : "clutched his arm,", \
							"looking away from the screen," : "looking away from the screen,", \
							"then buried her head in Billy's shoulder." : "then buried her head in Billy's shoulder.", \
							"Billy realised that everyone in that cinema" : "Billy realised that everyone in that cinema", \
							"was feeling as she did." : "^start(animations/Stand/Gestures/Me_1) was feeling as she did.", \
							"It was fear," : "^start(animations/Stand/Gestures/You_4) It was fear", \
							"that gripped your body and soul" : "^start(animations/Stand/Gestures/Me_1) that gripped your body and soul", \
							"no one hooted," : "^start(animations/Stand/Gestures/No_1) no one hooted, ^wait(animations/Stand/Gestures/No_1)", \
							"no one laughed." : "^start(animations/Stand/Gestures/No_1) no one laughed. ^wait(animations/Stand/Gestures/No_1)", \
							"No one whistled any more," : "^start(animations/Stand/Gestures/No_1) No one whistled any more, ^wait(animations/Stand/Gestures/No_1)", \
							"as if everyone in the cinema" : "as if everyone in the cinema", \
							"was holding their breath," : "was holding their breath,", \
							"waiting for what was to come, dreading the horror of it," : "^mode(contextual) waiting for what was to come, dreading the horror of it, ^mode(disabled)", \
							"that there was nothing " : "^start(animations/Stand/Gestures/No_1) that there was nothing ", \
							"this man, this Hitler," : "^start(animations/Stand/Gestures/You_4) this man, This Hitler,",\
							"But Billy knew more." : "But Billy knew more.",\
							"Billy looked up" : "Billy looked up",\
							"could not look away." : "could not look away.",\
							"he was wondering" : "^start(animations/Stand/Gestures/IDontKnow_1) he was wondering",\
							"if what had come into his mind" : "if what had come into his mind",\
							"could possibly be true." : "^start(animations/Stand/Gestures/Explain_4) could possibly be true.",\
							"The more he looked" : "The more he looked", \
							"into those eyes," : "into those eyes,", \
							"the more he realised that it was," : "^start(animations/Stand/Gestures/Explain_4) the more he realised that is was,", \
							"no doubt about it." : "^start(animations/Stand/Gestures/No_1) no doubt about it.",\
							"That man, that warmonger," : "^start(animations/Stand/Gestures/You_4) That man, that warmonger,",\
							"was up there now," : "was up there now,",\
							"able to spew out his hatred" : "able to spew out his hatred",\
						  }

		for keyword, gesture in gesture_mapping.iteritems():
			j=0 #Index that allows the removal and insertion at specific location
			for n in range(len(outList)):
		
				#Split the List according to keyword 
				splitList = outList.pop(j).split(keyword)
							
				#Merge splitted list with keyword
				tempList = []
				tempList.append(splitList.pop(0))
				for subst in splitList: 
					tempList.append(gesture)
					tempList.append(subst)
				
				#Insert Splitted List into Output List
				for subst2 in tempList:
					outList.insert(j, subst2)
					j+=1
		return[outList] 

	def init_gesture_dictionary(self):
		gesture_dictionary = { "as their eyes met in the cinema," : self.crazyEyes, \
                        "raised his hand and brushed his hair back from his forehead," : self.do_gesture_1_wipe_forehead, \
                        "he knew at once who it was, and where they had met, and remembered" : self.do_gesture_2_whoNwhere, \
                        "everything that had happened between them." : self.do_gesture_3_everything, \
                        "clutched his arm," : self.do_gesture_4_armclutch, \
                        "looking away from the screen," : self.do_gesture_5_lookAway, \
                        "then buried her head in Billy's shoulder." : self.do_gesture_6_burryHead,\
                        "Billy realised that everyone in that cinema" : self.do_gesture_3_everything,\
                        "as if everyone in the cinema" : self.do_gesture_3_everything,\
                        "was holding their breath," : self.do_gesture_6_burryHead,\
                        "But Billy knew more." : self.do_gesture_3_everything,\
                        "Billy looked up" : self.do_gesture_7_lookUp,\
                        "could not look away." : self.do_gesture_8_shakeHead,\
                        "if what had come into his mind" : self.do_gesture_9_think,\
                        "The more he looked" : self.do_gesture_3_everything,\
                        "into those eyes," : self.crazyEyes,\
                        "was up there now," : self.do_gesture_10_showUp,\
                        "able to spew out his hatred" : self.changeMode,\
                        }
		return gesture_dictionary
		
	def get_gesture_1_wipe_forehead(self):
		names = list()
		times = list()
		keys = list()

		names.append("HeadPitch")
		times.append([0.96, 1.68, 3.28, 3.96, 4.52, 5.08])
		keys.append([-0.0261199, 0.427944, 0.308291, 0.11194, -0.013848, 0.061318])

		names.append("HeadYaw")
		times.append([0.96, 1.68, 3.28, 3.96, 4.52, 5.08])
		keys.append([-0.234743, -0.622845, -0.113558, -0.00617796, -0.027654, -0.036858])

		names.append("LElbowRoll")
		times.append([0.8, 1.52, 3.12, 3.8, 4.36, 4.92])
		keys.append([-0.866668, -0.868202, -0.822183, -0.992455, -0.966378, -0.990923])

		names.append("LElbowYaw")
		times.append([0.8, 1.52, 3.12, 3.8, 4.36, 4.92])
		keys.append([-0.957257, -0.823801, -1.00788, -0.925044, -1.24412, -0.960325])

		names.append("LHand")
		times.append([1.52, 3.12, 3.8, 4.92])
		keys.append([0.132026, 0.132026, 0.132026, 0.132026])

		names.append("LShoulderPitch")
		times.append([0.8, 1.52, 3.12, 3.8, 4.36, 4.92])
		keys.append([0.863599, 0.858999, 0.888144, 0.929562, 1.017, 0.977116])

		names.append("LShoulderRoll")
		times.append([0.8, 1.52, 3.12, 3.8, 4.36, 4.92])
		keys.append([0.286815, 0.230059, 0.202446, 0.406468, 0.360449, 0.31903])

		names.append("LWristYaw")
		times.append([1.52, 3.12, 3.8, 4.92])
		keys.append([0.386526, 0.386526, 0.386526, 0.386526])

		names.append("RElbowRoll")
		times.append([0.64, 1.36, 2.96, 3.64, 4.2, 4.76])
		keys.append([1.28093, 1.39752, 1.57239, 1.24105, 1.22571, 0.840674])

		names.append("RElbowYaw")
		times.append([0.64, 1.36, 2.96, 3.64, 4.2, 4.76])
		keys.append([-0.128898, -0.285367, -0.15651, 0.754686, 1.17193, 0.677985])

		names.append("RHand")
		times.append([1.36, 2.96, 3.64, 4.76])
		keys.append([0.166571, 0.166208, 0.166571, 0.166208])

		names.append("RShoulderPitch")
		times.append([0.64, 1.36, 2.96, 3.64, 4.2, 4.76])
		keys.append([0.0767419, -0.59515, -0.866668, -0.613558, 0.584497, 0.882091])

		names.append("RShoulderRoll")
		times.append([0.64, 1.36, 2.96, 3.64, 4.2, 4.76])
		keys.append([-0.019984, -0.019984, -0.615176, -0.833004, -0.224006, -0.214801])

		names.append("RWristYaw")
		times.append([1.36, 2.96, 3.64, 4.76])
		keys.append([-0.058334, -0.0521979, -0.067538, -0.038392])

		return (names, times, keys)

	def do_gesture_1_wipe_forehead(self, InString):
		#(names, keys, times) = self.get_gesture_1_wipe_forehead()
		names = list()
		times = list()
		keys = list()

		names.append("HeadPitch")
		times.append([0.96, 1.68, 3.28, 3.96, 4.52, 5.08])
		keys.append([-0.0261199, 0.427944, 0.308291, 0.11194, -0.013848, 0.061318])

		names.append("HeadYaw")
		times.append([0.96, 1.68, 3.28, 3.96, 4.52, 5.08])
		keys.append([-0.234743, -0.622845, -0.113558, -0.00617796, -0.027654, -0.036858])

		names.append("LElbowRoll")
		times.append([0.8, 1.52, 3.12, 3.8, 4.36, 4.92])
		keys.append([-0.866668, -0.868202, -0.822183, -0.992455, -0.966378, -0.990923])

		names.append("LElbowYaw")
		times.append([0.8, 1.52, 3.12, 3.8, 4.36, 4.92])
		keys.append([-0.957257, -0.823801, -1.00788, -0.925044, -1.24412, -0.960325])

		names.append("LHand")
		times.append([1.52, 3.12, 3.8, 4.92])
		keys.append([0.132026, 0.132026, 0.132026, 0.132026])

		names.append("LShoulderPitch")
		times.append([0.8, 1.52, 3.12, 3.8, 4.36, 4.92])
		keys.append([0.863599, 0.858999, 0.888144, 0.929562, 1.017, 0.977116])

		names.append("LShoulderRoll")
		times.append([0.8, 1.52, 3.12, 3.8, 4.36, 4.92])
		keys.append([0.286815, 0.230059, 0.202446, 0.406468, 0.360449, 0.31903])

		names.append("LWristYaw")
		times.append([1.52, 3.12, 3.8, 4.92])
		keys.append([0.386526, 0.386526, 0.386526, 0.386526])

		names.append("RElbowRoll")
		times.append([0.64, 1.36, 2.96, 3.64, 4.2, 4.76])
		keys.append([1.28093, 1.39752, 1.57239, 1.24105, 1.22571, 0.840674])

		names.append("RElbowYaw")
		times.append([0.64, 1.36, 2.96, 3.64, 4.2, 4.76])
		keys.append([-0.128898, -0.285367, -0.15651, 0.754686, 1.17193, 0.677985])

		names.append("RHand")
		times.append([1.36, 2.96, 3.64, 4.76])
		keys.append([0.166571, 0.166208, 0.166571, 0.166208])

		names.append("RShoulderPitch")
		times.append([0.64, 1.36, 2.96, 3.64, 4.2, 4.76])
		keys.append([0.0767419, -0.59515, -0.866668, -0.613558, 0.584497, 0.882091])

		names.append("RShoulderRoll")
		times.append([0.64, 1.36, 2.96, 3.64, 4.2, 4.76])
		keys.append([-0.019984, -0.019984, -0.615176, -0.833004, -0.224006, -0.214801])

		names.append("RWristYaw")
		times.append([1.36, 2.96, 3.64, 4.76])
		keys.append([-0.058334, -0.0521979, -0.067538, -0.038392])

		self.motionProxy.post.angleInterpolation(names, keys, times, True)
		self.animatedSpeechProxy.say(InString)
		
	def get_gesture_2_whoNwhere(self):
		names = list()
		times = list()
		keys = list()

		names.append("LElbowRoll")
		times.append([1.8, 3.6, 4.8])
		keys.append([-0.998592, -1.08296, -1.05382])

		names.append("LElbowYaw")
		times.append([1.8, 3.6, 4.8])
		keys.append([-1.36837, -1.31928, -1.38831])

		names.append("LHand")
		times.append([1.8, 3.6, 4.8])
		keys.append([0.244, 0.244, 0.2392])

		names.append("LShoulderPitch")
		times.append([1.8, 3.6, 4.8])
		keys.append([1.41277, 0.43408, 0.512314])

		names.append("LShoulderRoll")
		times.append([1.8, 3.6, 4.8])
		keys.append([0.254602, -0.251618, -0.191792])

		names.append("LWristYaw")
		times.append([1.8, 3.6, 4.8])
		keys.append([0.0168321, -0.191792, -1.49723])

		names.append("RElbowRoll")
		times.append([1.8, 3.6, 4.8])
		keys.append([0.971064, 0.99254, 1.05543])

		names.append("RElbowYaw")
		times.append([1.8, 3.6, 4.8])
		keys.append([1.30539, 1.30539, 1.39743])

		names.append("RHand")
		times.append([1.8, 3.6, 4.8])
		keys.append([0.244, 0.244, 0.2468])

		names.append("RShoulderPitch")
		times.append([1.8, 3.6, 4.8])
		keys.append([0.380474, 0.380474, 0.536942])

		names.append("RShoulderRoll")
		times.append([1.8, 3.6, 4.8])
		keys.append([0.31136, 0.31136, 0.260738])

		names.append("RWristYaw")
		times.append([1.8, 3.6, 4.8])
		keys.append([0.0843279, 0.0843279, 1.51555])
	   
		return(names, keys, times)

	def do_gesture_2_whoNwhere(self, InString):
		names = list()
		times = list()
		keys = list()

		names.append("LElbowRoll")
		times.append([1.8, 3.6, 4.8])
		keys.append([-0.998592, -1.08296, -1.05382])

		names.append("LElbowYaw")
		times.append([1.8, 3.6, 4.8])
		keys.append([-1.36837, -1.31928, -1.38831])

		names.append("LHand")
		times.append([1.8, 3.6, 4.8])
		keys.append([0.244, 0.244, 0.2392])

		names.append("LShoulderPitch")
		times.append([1.8, 3.6, 4.8])
		keys.append([1.41277, 0.43408, 0.512314])

		names.append("LShoulderRoll")
		times.append([1.8, 3.6, 4.8])
		keys.append([0.254602, -0.251618, -0.191792])

		names.append("LWristYaw")
		times.append([1.8, 3.6, 4.8])
		keys.append([0.0168321, -0.191792, -1.49723])

		names.append("RElbowRoll")
		times.append([1.8, 3.6, 4.8])
		keys.append([0.971064, 0.99254, 1.05543])

		names.append("RElbowYaw")
		times.append([1.8, 3.6, 4.8])
		keys.append([1.30539, 1.30539, 1.39743])

		names.append("RHand")
		times.append([1.8, 3.6, 4.8])
		keys.append([0.244, 0.244, 0.2468])

		names.append("RShoulderPitch")
		times.append([1.8, 3.6, 4.8])
		keys.append([0.380474, 0.380474, 0.536942])

		names.append("RShoulderRoll")
		times.append([1.8, 3.6, 4.8])
		keys.append([0.31136, 0.31136, 0.260738])

		names.append("RWristYaw")
		times.append([1.8, 3.6, 4.8])
		keys.append([0.0843279, 0.0843279, 1.51555])

		self.motionProxy.post.angleInterpolation(names, keys, times, True)
		self.animatedSpeechProxy.say(InString)

	def get_gesture_3_everything(self):
		names = list()
		times = list()
		keys = list()

		names.append("HeadPitch")
		times.append([2])
		keys.append([0.0429101])

		names.append("HeadYaw")
		times.append([2])
		keys.append([-0.0322559])

		names.append("LElbowRoll")
		times.append([2])
		keys.append([-0.391128])

		names.append("LElbowYaw")
		times.append([2])
		keys.append([-2.02492])

		names.append("LHand")
		times.append([2])
		keys.append([0.2408])

		names.append("LShoulderPitch")
		times.append([2])
		keys.append([0.50311])

		names.append("LShoulderRoll")
		times.append([2])
		keys.append([0.88661])

		names.append("LWristYaw")
		times.append([2])
		keys.append([-0.150374])

		names.append("RElbowRoll")
		times.append([2])
		keys.append([0.46331])

		names.append("RElbowYaw")
		times.append([2])
		keys.append([2.03097])

		names.append("RHand")
		times.append([2])
		keys.append([0.2452])

		names.append("RShoulderPitch")
		times.append([2])
		keys.append([0.483252])

		names.append("RShoulderRoll")
		times.append([2])
		keys.append([-0.894364])

		names.append("RWristYaw")
		times.append([2])
		keys.append([0.182504])

		return(names, key, times)

	def do_gesture_3_everything(self, InString):
		names = list()
		times = list()
		keys = list()

		names.append("HeadPitch")
		times.append([2])
		keys.append([0.0429101])

		names.append("HeadYaw")
		times.append([2])
		keys.append([-0.0322559])

		names.append("LElbowRoll")
		times.append([2])
		keys.append([-0.391128])

		names.append("LElbowYaw")
		times.append([2])
		keys.append([-2.02492])

		names.append("LHand")
		times.append([2])
		keys.append([0.2408])

		names.append("LShoulderPitch")
		times.append([2])
		keys.append([0.50311])

		names.append("LShoulderRoll")
		times.append([2])
		keys.append([0.88661])

		names.append("LWristYaw")
		times.append([2])
		keys.append([-0.150374])

		names.append("RElbowRoll")
		times.append([2])
		keys.append([0.46331])

		names.append("RElbowYaw")
		times.append([2])
		keys.append([2.03097])

		names.append("RHand")
		times.append([2])
		keys.append([0.2452])

		names.append("RShoulderPitch")
		times.append([2])
		keys.append([0.483252])

		names.append("RShoulderRoll")
		times.append([2])
		keys.append([-0.894364])

		names.append("RWristYaw")
		times.append([2])
		keys.append([0.182504])

		self.motionProxy.post.angleInterpolation(names, keys, times, True)
		self.animatedSpeechProxy.say(InString)

	def get_gesture_4_armclutch(self):
		names = list()
		times = list()
		keys = list()

		names.append("LElbowRoll")
		times.append([1.2])
		keys.append([-0.51845])

		names.append("LElbowYaw")
		times.append([1.2])
		keys.append([-1.58466])

		names.append("LHand")
		times.append([1.2])
		keys.append([0.234])

		names.append("LShoulderPitch")
		times.append([1.2])
		keys.append([0.306758])

		names.append("LShoulderRoll")
		times.append([1.2])
		keys.append([-0.314159])

		names.append("LWristYaw")
		times.append([1.2])
		keys.append([-0.046062])

		names.append("RElbowRoll")
		times.append([1.2])
		keys.append([0.633584])

		names.append("RElbowYaw")
		times.append([1.2])
		keys.append([1.4097])

		names.append("RHand")
		times.append([1.2])
		keys.append([0.2416])

		names.append("RShoulderPitch")
		times.append([1.2])
		keys.append([0.374338])

		names.append("RShoulderRoll")
		times.append([1.2])
		keys.append([0.314159])

		names.append("RWristYaw")
		times.append([1.2])
		keys.append([0.098134])

		return(names, key, times)

	def do_gesture_4_armclutch(self, InString):
		names = list()
		times = list()
		keys = list()

		names.append("LElbowRoll")
		times.append([1.2])
		keys.append([-0.51845])

		names.append("LElbowYaw")
		times.append([1.2])
		keys.append([-1.58466])

		names.append("LHand")
		times.append([1.2])
		keys.append([0.234])

		names.append("LShoulderPitch")
		times.append([1.2])
		keys.append([0.306758])

		names.append("LShoulderRoll")
		times.append([1.2])
		keys.append([-0.314159])

		names.append("LWristYaw")
		times.append([1.2])
		keys.append([-0.046062])

		names.append("RElbowRoll")
		times.append([1.2])
		keys.append([0.633584])

		names.append("RElbowYaw")
		times.append([1.2])
		keys.append([1.4097])

		names.append("RHand")
		times.append([1.2])
		keys.append([0.2416])

		names.append("RShoulderPitch")
		times.append([1.2])
		keys.append([0.374338])

		names.append("RShoulderRoll")
		times.append([1.2])
		keys.append([0.314159])

		names.append("RWristYaw")
		times.append([1.2])
		keys.append([0.098134])

		self.motionProxy.post.angleInterpolation(names, keys, times, True)
		self.animatedSpeechProxy.say(InString)

	def get_gesture_5_lookAway(self):
		names = list()
		times = list()
		keys = list()

		names.append("HeadPitch")
		times.append([1.2])
		keys.append([0.235247])

		names.append("HeadYaw")
		times.append([1.2])
		keys.append([-1.19963])

		return(names, key, times)

	def do_gesture_5_lookAway(self, InString):
		names = list()
		times = list()
		keys = list()

		names.append("HeadPitch")
		times.append([1.2])
		keys.append([0.235247])

		names.append("HeadYaw")
		times.append([1.2])
		keys.append([-1.19963])

		self.motionProxy.post.angleInterpolation(names, keys, times, True)
		self.animatedSpeechProxy.say(InString)

	def get_gesture_6_burryHead(self):
		names = list()
		times = list()
		keys = list()

		names.append("LElbowRoll")
		times.append([1.16])
		keys.append([-1.52015])

		names.append("LElbowYaw")
		times.append([1.16])
		keys.append([-1.00635])

		names.append("LHand")
		times.append([1.16])
		keys.append([0.2352])

		names.append("LShoulderPitch")
		times.append([1.16])
		keys.append([0.20398])

		names.append("LShoulderRoll")
		times.append([1.16])
		keys.append([-0.311444])

		names.append("LWristYaw")
		times.append([1.16])
		keys.append([-0.658128])

		names.append("RElbowRoll")
		times.append([1.16])
		keys.append([1.54325])

		names.append("RElbowYaw")
		times.append([1.16])
		keys.append([0.872804])

		names.append("RHand")
		times.append([1.16])
		keys.append([0.2524])

		names.append("RShoulderPitch")
		times.append([1.16])
		keys.append([0.1335])

		names.append("RShoulderRoll")
		times.append([1.16])
		keys.append([0.0352399])

		names.append("RWristYaw")
		times.append([1.16])
		keys.append([1.32533])

		return(names, key, times)

	def do_gesture_6_burryHead(self, InString):
		names = list()
		times = list()
		keys = list()

		names.append("LElbowRoll")
		times.append([1.16])
		keys.append([-1.52015])

		names.append("LElbowYaw")
		times.append([1.16])
		keys.append([-1.00635])

		names.append("LHand")
		times.append([1.16])
		keys.append([0.2352])

		names.append("LShoulderPitch")
		times.append([1.16])
		keys.append([0.20398])

		names.append("LShoulderRoll")
		times.append([1.16])
		keys.append([-0.311444])

		names.append("LWristYaw")
		times.append([1.16])
		keys.append([-0.658128])

		names.append("RElbowRoll")
		times.append([1.16])
		keys.append([1.54325])

		names.append("RElbowYaw")
		times.append([1.16])
		keys.append([0.872804])

		names.append("RHand")
		times.append([1.16])
		keys.append([0.2524])

		names.append("RShoulderPitch")
		times.append([1.16])
		keys.append([0.1335])

		names.append("RShoulderRoll")
		times.append([1.16])
		keys.append([0.0352399])

		names.append("RWristYaw")
		times.append([1.16])
		keys.append([1.32533])

		self.motionProxy.post.angleInterpolation(names, keys, times, True)
		self.animatedSpeechProxy.say(InString)

	def get_gesture_7_lookUp(self):
		names = list()
		times = list()
		keys = list()

		names.append("HeadPitch")
		times.append([1.2])
		keys.append([-0.61671])

		names.append("HeadYaw")
		times.append([1.2])
		keys.append([-0.024586])

		return(names, key, times)

	def do_gesture_7_lookUp(self, InString):
		names = list()
		times = list()
		keys = list()

		names.append("HeadPitch")
		times.append([1.2])
		keys.append([-0.61671])

		names.append("HeadYaw")
		times.append([1.2])
		keys.append([-0.024586])

		self.motionProxy.post.angleInterpolation(names, keys, times, True)
		self.animatedSpeechProxy.say(InString)

	def get_gesture_8_shakeHead(self):
		names = list()
		times = list()
		keys = list()

		names.append("HeadPitch")
		times.append([0.8, 2])
		keys.append([-0.380474, -0.380474])

		names.append("HeadYaw")
		times.append([0.8, 2])
		keys.append([-0.943452, 0.992456])

		return(names, key, times)
		
	def do_gesture_8_shakeHead(self, InString):
		names = list()
		times = list()
		keys = list()

		names.append("HeadPitch")
		times.append([0.8, 2])
		keys.append([-0.380474, -0.380474])

		names.append("HeadYaw")
		times.append([0.8, 2])
		keys.append([-0.943452, 0.992456])

		self.motionProxy.post.angleInterpolation(names, keys, times, True)
		self.animatedSpeechProxy.say(InString)

	def get_gesture_9_think(self):
		names = list()
		times = list()
		keys = list()

		names.append("HeadPitch")
		times.append([1.48])
		keys.append([0.0398421])

		names.append("HeadYaw")
		times.append([1.48])
		keys.append([-0.021518])

		names.append("LElbowRoll")
		times.append([1.48])
		keys.append([-0.997058])

		names.append("LElbowYaw")
		times.append([1.48])
		keys.append([-1.36837])

		names.append("LHand")
		times.append([1.48])
		keys.append([0.2436])

		names.append("LShoulderPitch")
		times.append([1.48])
		keys.append([1.41737])

		names.append("LShoulderRoll")
		times.append([1.48])
		keys.append([0.263806])

		names.append("LWristYaw")
		times.append([1.48])
		keys.append([0.0168321])

		names.append("RElbowRoll")
		times.append([1.48])
		keys.append([1.54462])

		names.append("RElbowYaw")
		times.append([1.48])
		keys.append([0.87894])

		names.append("RHand")
		times.append([1.48])
		keys.append([0.2432])

		names.append("RShoulderPitch")
		times.append([1.48])
		keys.append([-0.409536])

		names.append("RShoulderRoll")
		times.append([1.48])
		keys.append([-0.14884])

		names.append("RWristYaw")
		times.append([1.48])
		keys.append([1.04461])

		return(names, key, times)

	def do_gesture_9_think(self, InString):
		names = list()
		times = list()
		keys = list()

		names.append("HeadPitch")
		times.append([1.48])
		keys.append([0.0398421])

		names.append("HeadYaw")
		times.append([1.48])
		keys.append([-0.021518])

		names.append("LElbowRoll")
		times.append([1.48])
		keys.append([-0.997058])

		names.append("LElbowYaw")
		times.append([1.48])
		keys.append([-1.36837])

		names.append("LHand")
		times.append([1.48])
		keys.append([0.2436])

		names.append("LShoulderPitch")
		times.append([1.48])
		keys.append([1.41737])

		names.append("LShoulderRoll")
		times.append([1.48])
		keys.append([0.263806])

		names.append("LWristYaw")
		times.append([1.48])
		keys.append([0.0168321])

		names.append("RElbowRoll")
		times.append([1.48])
		keys.append([1.54462])

		names.append("RElbowYaw")
		times.append([1.48])
		keys.append([0.87894])

		names.append("RHand")
		times.append([1.48])
		keys.append([0.2432])

		names.append("RShoulderPitch")
		times.append([1.48])
		keys.append([-0.409536])

		names.append("RShoulderRoll")
		times.append([1.48])
		keys.append([-0.14884])

		names.append("RWristYaw")
		times.append([1.48])
		keys.append([1.04461])

		self.motionProxy.post.angleInterpolation(names, keys, times, True)
		self.animatedSpeechProxy.say(InString)

	def get_gesture_10_showUp(self):
		names = list()
		times = list()
		keys = list()

		names.append("LElbowRoll")
		times.append([1.2])
		keys.append([-1.05842])

		names.append("LElbowYaw")
		times.append([1.2])
		keys.append([-0.819198])

		names.append("LHand")
		times.append([1.2])
		keys.append([0.0140001])

		names.append("LShoulderPitch")
		times.append([1.2])
		keys.append([1.42658])

		names.append("LShoulderRoll")
		times.append([1.2])
		keys.append([0.16563])

		names.append("LWristYaw")
		times.append([1.2])
		keys.append([0.128814])

		names.append("RElbowRoll")
		times.append([1.2])
		keys.append([0.2102])

		names.append("RElbowYaw")
		times.append([1.2])
		keys.append([1.12898])

		names.append("RHand")
		times.append([1.2])
		keys.append([0.6556])

		names.append("RShoulderPitch")
		times.append([1.2])
		keys.append([-0.332836])

		names.append("RShoulderRoll")
		times.append([1.2])
		keys.append([0.0935321])

		names.append("RWristYaw")
		times.append([1.2])
		keys.append([-1.06924])

		return(names, key, times)

	def do_gesture_10_showUp(self, InString):
		names = list()
		times = list()
		keys = list()

		names.append("LElbowRoll")
		times.append([1.2])
		keys.append([-1.05842])

		names.append("LElbowYaw")
		times.append([1.2])
		keys.append([-0.819198])

		names.append("LHand")
		times.append([1.2])
		keys.append([0.0140001])

		names.append("LShoulderPitch")
		times.append([1.2])
		keys.append([1.42658])

		names.append("LShoulderRoll")
		times.append([1.2])
		keys.append([0.16563])

		names.append("LWristYaw")
		times.append([1.2])
		keys.append([0.128814])

		names.append("RElbowRoll")
		times.append([1.2])
		keys.append([0.2102])

		names.append("RElbowYaw")
		times.append([1.2])
		keys.append([1.12898])

		names.append("RHand")
		times.append([1.2])
		keys.append([0.6556])

		names.append("RShoulderPitch")
		times.append([1.2])
		keys.append([-0.332836])

		names.append("RShoulderRoll")
		times.append([1.2])
		keys.append([0.0935321])

		names.append("RWristYaw")
		times.append([1.2])
		keys.append([-1.06924])

		self.motionProxy.post.angleInterpolation(names, keys, times, True)
		self.animatedSpeechProxy.say(InString)

	def changeMode(self, InString):
		self.animatedSpeechProxy.setBodyLanguageMode(2)
		self.animatedSpeechProxy.say(InString)

	def crazyEyes(self, InString):
		self.ledProxy.post.fadeRGB("FaceLeds", "red", 1)
		self.animatedSpeechProxy.say(InString)
		self.ledProxy.reset("FaceLeds")

	def StandUp(self):
		self.postureProxy.goToPosture("StandInit", 1.0)

	def SitDown(self):
		self.postureProxy.goToPosture("Sit", 1.0)

	def incrementVol(self):
		#Gain to volume [0-1]
		vol = self.ttsProxy.getVolume()
		vol += 0.1
		if vol > 1:
			vol = 1
		self.ttsProxy.setVolume(vol)
		
	def decrementVol(self):
		#Gain to volume [0-1]
		vol = self.ttsProxy.getVolume()
		vol -= 0.1
		if vol < 0:
			vol = 0
		self.ttsProxy.setVolume(vol)
	
	def incrementSpeed(self):
		speed = self.ttsProxy.getParameter("speed")	
		speed += 10
		self.ttsProxy.setParameter("speed", speed)
	
	def decrementSpeed(self):
		speed = self.ttsProxy.getParameter("speed")	
		speed -= 10
		self.ttsProxy.setParameter("speed", speed)

# FUNCTIONS
def main ():
	robotPort = 9559
	robotIP = "169.254.44.123"
	# robotPort = 35063
	# robotIP = "127.0.0.1"
	
	passage = "It was at that precise moment, as their eyes met in the cinema, that Billy felt he had met this man before, not on screen, but face to face. And when Hitler raised his hand and brushed his hair back from his forehead, he knew at once who it was, and where they had met, and remembered everything that had happened between them. Christine clutched his arm, looking away from the screen, then buried her head in Billy's shoulder. Billy realised that everyone in that cinema was feeling as she did. It was fear, the kind that gripped your body and soul and wouldn't leave you. No one whistled any more, no one hooted, no one laughed. It was as if everyone in the cinema was holding their breath, waiting for what was to come, dreading the horror of it, but knowing that there was nothing that could stop it, because this man, this Hitler, was going to make it happen. But Billy knew more. All the while Billy looked up into his eyes, and could not look away. All the while he was wondering if what had come into his mind could possibly be true. The more he looked into those eyes, the more he realised that it was, that there could be no doubt about it. That man, that warmonger, was up there now, able to spew out his hatred only because Billy had spared his life all those years before, after the Battle of Marcoing."
	#passage = "He raised his hand and brushed his hair back from his forehead, and remembered everything that had happened between them."
	#passage = ("He raised his hand and brushed his hair back from his forehead,")
	gesture_controller = GestureController(robotIP, robotPort)
	gesture_controller.tell_story(passage)
	

# CODE
if __name__ == '__main__':
	main()	
	#print "Do not run gestureController.py from __main__."

# END OF FILE