import speech_recognition as sr

r = sr.Recognizer()
m = sr.Microphone()
   
#def listen()
try:
    print("A moment of silence, please...")
    with m as source: r.adjust_for_ambient_noise(source)
    print("Set minimum energy threshold to {}".format(r.energy_threshold))
    print("test1")
    print("Say something!")
    with m as source: audio = r.listen(source)
    print("Recognizing...")
    try:
        # recognize speech using Google Speech Recognition
        value = r.recognize_google(audio)
        # we need some special handling here to correctly print unicode characters to standard output
        if str is bytes:  # this version of Python uses bytes for strings (Python 2)
            print(u"You said {}".format(value).encode("utf-8"))
	    var1 = u"You said {}".format(value).encode("utf-8")
        else:  # this version of Python uses unicode for strings (Python 3+)
            print("You said {}".format(value))
            print("test3")
    except sr.UnknownValueError:
        print("Oops! Didn't catch that")
    except sr.RequestError as e:
        print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
#    return var1

#def listen_while_reading()
#    print("A moment of silence, please...")
#    with m as source: r.adjust_for_ambient_noise(source)
#    print("Set minimum energy threshold to {}".format(r.energy_threshold))
#    while var1 != "stop":
#	print("test1")
#        print("Say something!")
#        with m as source: audio = r.listen(source)
#        print("Got it! Now to recognize it...")
#        try:
#            # recognize speech using Google Speech Recognition
#            value = r.recognize_google(audio)
#            # we need some special handling here to correctly print unicode characters to standard output
#            if str is bytes:  # this version of Python uses bytes for strings (Python 2)
#               print(u"You said {}".format(value).encode("utf-8"))
#		var1 = u"You said {}".format(value).encode("utf-8")
#            else:  # this version of Python uses unicode for strings (Python 3+)
#                print("You said {}".format(value))
#		print("test3")
#        except sr.UnknownValueError:
#            print("Oops! Didn't catch that")
#        except sr.RequestError as e:
#            print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
#	return var1

#listen
#process
#output
#listen 
#process
#output

except KeyboardInterrupt:
    print("testfinal")
    pass