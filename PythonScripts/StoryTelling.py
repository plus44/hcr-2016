# -*- encoding: UTF-8 -*- 

import math
# import almath as m # python's wrapping of almath
import sys
from naoqi import ALProxy


def StandUp(proxy):
    proxy.goToPosture("StandInit", 1.0)

def SitDown(proxy):
    proxy.goToPosture("Sit", 1.0)

def gesture_1_shout(motionProxy, ttsProxy, robotIP) :

    # Choregraphe simplified export in Python.
    names = list()
    times = list()
    keys = list()

    names.append("LElbowRoll")
    times.append([1.64])
    keys.append([-1.54316])

    names.append("LElbowYaw")
    times.append([1.64])
    keys.append([-0.719487])

    names.append("LHand")
    times.append([1.64])
    keys.append([0.314])

    names.append("LShoulderPitch")
    times.append([1.64])
    keys.append([-0.0123138])

    names.append("LShoulderRoll")
    times.append([1.64])
    keys.append([0.260738])

    names.append("LWristYaw")
    times.append([1.64])
    keys.append([-0.515466])

    names.append("RElbowRoll")
    times.append([1.64])
    keys.append([1.54462])

    names.append("RElbowYaw")
    times.append([1.64])
    keys.append([0.619695])

    names.append("RHand")
    times.append([1.64])
    keys.append([0.3848])

    names.append("RShoulderPitch")
    times.append([1.64])
    keys.append([-0.0966001])

    names.append("RShoulderRoll")
    times.append([1.64])
    keys.append([-0.265424])

    names.append("RWristYaw")
    times.append([1.64])
    keys.append([0.602821])

    try:
      # uncomment the following line and modify the IP if you use this script outside Choregraphe.
      motion = ALProxy("ALMotion", robotIP, 9559)
        #motion = ALProxy("ALMotion")
      motionProxy.post.angleInterpolation(names, keys, times, True)
      ttsProxy.say("Can you see me shouting?")
    except BaseException, err:
      print err

def gesture_2(robotIP):

    # Choregraphe simplified export in Python.
    names = list()
    times = list()
    keys = list()

    

    try:
      # uncomment the following line and modify the IP if you use this script outside Choregraphe.
      motion = ALProxy("ALMotion", robotIP, 9559)
        #motion = ALProxy("ALMotion")
      motion.angleInterpolation(names, keys, times, True)
    except BaseException, err:
      print err

def knees(robotIP):

    # Choregraphe simplified export in Python.
    names = list()
    times = list()
    keys = list()

    names.append("HeadPitch")
    times.append([0.88])
    keys.append([0.0720561])

    names.append("HeadYaw")
    times.append([0.88])
    keys.append([-0.0307219])

    names.append("LAnklePitch")
    times.append([0.88])
    keys.append([-1.18944])

    names.append("LAnkleRoll")
    times.append([0.88])
    keys.append([0.073674])

    names.append("LElbowRoll")
    times.append([0.88])
    keys.append([-1.05688])

    names.append("LElbowYaw")
    times.append([0.88])
    keys.append([-0.796188])

    names.append("LHand")
    times.append([0.88])
    keys.append([0.0196])

    names.append("LHipPitch")
    times.append([0.88])
    keys.append([-0.691792])

    names.append("LHipRoll")
    times.append([0.88])
    keys.append([-0.078192])

    names.append("LHipYawPitch")
    times.append([0.88])
    keys.append([-0.251534])

    names.append("LKneePitch")
    times.append([0.88])
    keys.append([2.11228])

    names.append("LShoulderPitch")
    times.append([0.88])
    keys.append([1.41431])

    names.append("LShoulderRoll")
    times.append([0.88])
    keys.append([0.161028])

    names.append("LWristYaw")
    times.append([0.88])
    keys.append([0.118076])

    names.append("RAnklePitch")
    times.append([0.88])
    keys.append([-1.18114])

    names.append("RAnkleRoll")
    times.append([0.88])
    keys.append([-0.0758697])

    names.append("RElbowRoll")
    times.append([0.88])
    keys.append([1.0539])

    names.append("RElbowYaw")
    times.append([0.88])
    keys.append([0.762356])

    names.append("RHand")
    times.append([0.88])
    keys.append([0.0232])

    names.append("RHipPitch")
    times.append([0.88])
    keys.append([-0.710284])

    names.append("RHipRoll")
    times.append([0.88])
    keys.append([0.0782759])

    names.append("RHipYawPitch")
    times.append([0.88])
    keys.append([-0.251534])

    names.append("RKneePitch")
    times.append([0.88])
    keys.append([2.11083])

    names.append("RShoulderPitch")
    times.append([0.88])
    keys.append([1.38678])

    names.append("RShoulderRoll")
    times.append([0.88])
    keys.append([-0.1335])

    names.append("RWristYaw")
    times.append([0.88])
    keys.append([-0.182588])



    try:
      # uncomment the following line and modify the IP if you use this script outside Choregraphe.
      motion = ALProxy("ALMotion", robotIP, 9559)
        #motion = ALProxy("ALMotion")
      motion.angleInterpolation(names, keys, times, True)
    except BaseException, err:
      print err

def LookOut(ttsProxy, animatedSpeechProxy):
    ttsProxy.setParameter("emph", 1)
    ttsProxy.setParameter("volume", 2)
    animatedSpeechProxy.say("^start(animations/Stand/Gestures/You_4) Look out!")

def gesture_1_wipe_forehead(InString, motionProxy, ttsProxy, ledProxy):
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

    motionProxy.post.angleInterpolation(names, keys, times, True)
    ttsProxy.say(InString)

def gesture_2_whoNwhere(InString, motionProxy, ttsProxy, ledProxy):
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
    # names.append("LElbowRoll")
    # times.append([1.8, 3.6])
    # keys.append([-0.998592, -1.08296])

    # names.append("LElbowYaw")
    # times.append([1.8, 3.6])
    # keys.append([-1.36837, -1.31928])

    # names.append("LHand")
    # times.append([1.8, 3.6])
    # keys.append([0.244, 0.244])

    # names.append("LShoulderPitch")
    # times.append([1.8, 3.6])
    # keys.append([1.41277, 0.43408])

    # names.append("LShoulderRoll")
    # times.append([1.8, 3.6])
    # keys.append([0.254602, -0.251618])

    # names.append("LWristYaw")
    # times.append([1.8, 3.6])
    # keys.append([0.0168321, -0.191792])

    # names.append("RElbowRoll")
    # times.append([1.8, 3.6])
    # keys.append([0.971064, 0.99254])

    # names.append("RElbowYaw")
    # times.append([1.8, 3.6])
    # keys.append([1.30539, 1.30539])

    # names.append("RHand")
    # times.append([1.8, 3.6])
    # keys.append([0.244, 0.244])

    # names.append("RShoulderPitch")
    # times.append([1.8, 3.6])
    # keys.append([0.380474, 0.380474])

    # names.append("RShoulderRoll")
    # times.append([1.8, 3.6])
    # keys.append([0.31136, 0.31136])

    # names.append("RWristYaw")
    # times.append([1.8, 3.6])
    # keys.append([0.0843279, 0.0843279])


    motionProxy.post.angleInterpolation(names, keys, times, True)
    ttsProxy.say(InString)

def gesture_3_everything(InString, motionProxy, ttsProxy, ledProxy):
    names = list()
    times = list()
    keys = list()

    # names.append("LElbowRoll")
    # times.append([2])
    # keys.append([-0.406468])

    # names.append("LElbowYaw")
    # times.append([2])
    # keys.append([-2.04947])

    # names.append("LHand")
    # times.append([2])
    # keys.append([0.2384])

    # names.append("LShoulderPitch")
    # times.append([2])
    # keys.append([0.424876])

    # names.append("LShoulderRoll")
    # times.append([2])
    # keys.append([0.952572])

    # names.append("LWristYaw")
    # times.append([2])
    # keys.append([-0.17185])

    # names.append("RElbowRoll")
    # times.append([2])
    # keys.append([0.467912])

    # names.append("RElbowYaw")
    # times.append([2])
    # keys.append([2.05705])

    # names.append("RHand")
    # times.append([2])
    # keys.append([0.2444])

    # names.append("RShoulderPitch")
    # times.append([2])
    # keys.append([0.400416])

    # names.append("RShoulderRoll")
    # times.append([2])
    # keys.append([-0.960326])

    # names.append("RWristYaw")
    # times.append([2])
    # keys.append([0.223922])
    names.append("HeadPitch")
    times.append([2])
    keys.append([0.0429101])

    names.append("HeadYaw")
    times.append([2])
    keys.append([-0.0322559])

    # names.append("LAnklePitch")
    # times.append([2])
    # keys.append([-0.352862])

    # names.append("LAnkleRoll")
    # times.append([2])
    # keys.append([4.19617e-05])

    names.append("LElbowRoll")
    times.append([2])
    keys.append([-0.391128])

    names.append("LElbowYaw")
    times.append([2])
    keys.append([-2.02492])

    names.append("LHand")
    times.append([2])
    keys.append([0.2408])

    # names.append("LHipPitch")
    # times.append([2])
    # keys.append([-0.455556])

    # names.append("LHipRoll")
    # times.append([2])
    # keys.append([4.19617e-05])

    # names.append("LHipYawPitch")
    # times.append([2])
    # keys.append([4.19617e-05])

    # names.append("LKneePitch")
    # times.append([2])
    # keys.append([0.693326])

    names.append("LShoulderPitch")
    times.append([2])
    keys.append([0.50311])

    names.append("LShoulderRoll")
    times.append([2])
    keys.append([0.88661])

    names.append("LWristYaw")
    times.append([2])
    keys.append([-0.150374])

    # names.append("RAnklePitch")
    # times.append([2])
    # keys.append([-0.358914])

    # names.append("RAnkleRoll")
    # times.append([2])
    # keys.append([-0.00762796])

    names.append("RElbowRoll")
    times.append([2])
    keys.append([0.46331])

    names.append("RElbowYaw")
    times.append([2])
    keys.append([2.03097])

    names.append("RHand")
    times.append([2])
    keys.append([0.2452])

    # names.append("RHipPitch")
    # times.append([2])
    # keys.append([-0.451038])

    # names.append("RHipRoll")
    # times.append([2])
    # keys.append([0.00771189])

    # names.append("RHipYawPitch")
    # times.append([2])
    # keys.append([4.19617e-05])

    # names.append("RKneePitch")
    # times.append([2])
    # keys.append([0.70108])

    names.append("RShoulderPitch")
    times.append([2])
    keys.append([0.483252])

    names.append("RShoulderRoll")
    times.append([2])
    keys.append([-0.894364])

    names.append("RWristYaw")
    times.append([2])
    keys.append([0.182504])


    motionProxy.post.angleInterpolation(names, keys, times, True)
    ttsProxy.say(InString)

def gesture_4_armclutch(InString, motionProxy, ttsProxy, ledProxy):
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

    motionProxy.post.angleInterpolation(names, keys, times, True)
    ttsProxy.say(InString)

def gesture_5_lookAway(InString, motionProxy, ttsProxy, ledProxy):
    names = list()
    times = list()
    keys = list()

    names.append("HeadPitch")
    times.append([1.2])
    keys.append([0.235247])

    names.append("HeadYaw")
    times.append([1.2])
    keys.append([-1.19963])


    motionProxy.post.angleInterpolation(names, keys, times, True)
    ttsProxy.say(InString)

def gesture_6_burryHead(InString, motionProxy, ttsProxy, ledProxy):
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


    motionProxy.post.angleInterpolation(names, keys, times, True)
    ttsProxy.say(InString)

def gesture_7_lookUp(InString, motionProxy, ttsProxy, ledProxy):
    names = list()
    times = list()
    keys = list()

    names.append("HeadPitch")
    times.append([1.2])
    keys.append([-0.61671])

    names.append("HeadYaw")
    times.append([1.2])
    keys.append([-0.024586])

    motionProxy.post.angleInterpolation(names, keys, times, True)
    ttsProxy.say(InString)

def gesture_8_shakeHead(InString, motionProxy, ttsProxy, ledProxy):
    names = list()
    times = list()
    keys = list()

    names.append("HeadPitch")
    times.append([0.8, 2])
    keys.append([-0.380474, -0.380474])

    names.append("HeadYaw")
    times.append([0.8, 2])
    keys.append([-0.943452, 0.992456])
    
    motionProxy.post.angleInterpolation(names, keys, times, True)
    ttsProxy.say(InString)

def gesture_9_think(InString, motionProxy, ttsProxy, ledProxy):
    names = list()
    times = list()
    keys = list()

    names.append("HeadPitch")
    times.append([1.48])
    keys.append([0.0398421])

    names.append("HeadYaw")
    times.append([1.48])
    keys.append([-0.021518])

    # names.append("LAnklePitch")
    # times.append([1.48])
    # keys.append([-0.34826])

    # names.append("LAnkleRoll")
    # times.append([1.48])
    # keys.append([0.00464392])

    names.append("LElbowRoll")
    times.append([1.48])
    keys.append([-0.997058])

    names.append("LElbowYaw")
    times.append([1.48])
    keys.append([-1.36837])

    names.append("LHand")
    times.append([1.48])
    keys.append([0.2436])

    # names.append("LHipPitch")
    # times.append([1.48])
    # keys.append([-0.446352])

    # names.append("LHipRoll")
    # times.append([1.48])
    # keys.append([-0.00302601])

    # names.append("LHipYawPitch")
    # times.append([1.48])
    # keys.append([-0.00302601])

    # names.append("LKneePitch")
    # times.append([1.48])
    # keys.append([0.700996])

    names.append("LShoulderPitch")
    times.append([1.48])
    keys.append([1.41737])

    names.append("LShoulderRoll")
    times.append([1.48])
    keys.append([0.263806])

    names.append("LWristYaw")
    times.append([1.48])
    keys.append([0.0168321])

    # names.append("RAnklePitch")
    # times.append([1.48])
    # keys.append([-0.345108])

    # names.append("RAnkleRoll")
    # times.append([1.48])
    # keys.append([0.00157595])

    names.append("RElbowRoll")
    times.append([1.48])
    keys.append([1.54462])

    names.append("RElbowYaw")
    times.append([1.48])
    keys.append([0.87894])

    names.append("RHand")
    times.append([1.48])
    keys.append([0.2432])

    # names.append("RHipPitch")
    # times.append([1.48])
    # keys.append([-0.451038])

    # names.append("RHipRoll")
    # times.append([1.48])
    # keys.append([0.00464392])

    # names.append("RHipYawPitch")
    # times.append([1.48])
    # keys.append([-0.00302601])

    # names.append("RKneePitch")
    # times.append([1.48])
    # keys.append([0.704148])

    names.append("RShoulderPitch")
    times.append([1.48])
    keys.append([-0.409536])

    names.append("RShoulderRoll")
    times.append([1.48])
    keys.append([-0.14884])

    names.append("RWristYaw")
    times.append([1.48])
    keys.append([1.04461])

    motionProxy.post.angleInterpolation(names, keys, times, True)
    ttsProxy.say(InString)

def gesture_10_showUp(InString, motionProxy, ttsProxy, ledProxy):
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

    motionProxy.post.angleInterpolation(names, keys, times, True)
    ttsProxy.say(InString)

def changeMode(InString, motionProxy, ttsProxy, ledProxy):
    ttsProxy.setBodyLanguageMode(2)
    ttsProxy.say(InString)

def crazyEyes(InString, motionProxy, ttsProxy, ledProxy):
    id = ledProxy.post.fadeRGB("FaceLeds", "red", 1)
    ttsProxy.say(InString)
    ledProxy.reset("FaceLeds")

def dictSearch(InString):
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

def main(robotIP,robotPort):

    #Setting the Proxies
    try:
        motionProxy = ALProxy("ALMotion", robotIP, robotPort)
    except Exception, e:
        print "Could not create proxy to ALMotion"
        print "Error was: ", e

    try:
        postureProxy = ALProxy("ALRobotPosture", robotIP, robotPort)
    except Exception, e:
        print "Could not create proxy to ALRobotPosture"
        print "Error was: ", e

    try:    
        ttsProxy = ALProxy("ALTextToSpeech", robotIP, robotPort)
    except Exception, e:
        print "Could not create proxy to ALTextToSpeech"
        print "Error was: ", e
    
    try:
        animatedSpeechProxy = ALProxy("ALAnimatedSpeech", robotIP, robotPort)
    except Exception, e:
        print "Could not create proxy to ALAnimatedSpeech"
        print "Error was: ", e

    try:
        ledProxy = ALProxy("ALLeds",robotIP, robotPort)
    except Exception, e:
        print "Could not create proxy to ALLeds"
        print "Error was: ", e


    custom_gesture_map = { "as their eyes met in the cinema," : crazyEyes, \
                        "raised his hand and brushed his hair back from his forehead," : gesture_1_wipe_forehead, \
                        "he knew at once who it was, and where they had met, and remembered" : gesture_2_whoNwhere, \
                        "everything that had happened between them." : gesture_3_everything, \
                        "clutched his arm," : gesture_4_armclutch, \
                        "looking away from the screen," : gesture_5_lookAway, \
                        "then buried her head in Billy's shoulder." : gesture_6_burryHead,\
                        "Billy realised that everyone in that cinema" : gesture_3_everything,\
                        "as if everyone in the cinema" : gesture_3_everything,\
                        "was holding their breath," : gesture_6_burryHead,\
                        "But Billy knew more." : gesture_3_everything,\
                        "Billy looked up" : gesture_7_lookUp,\
                        "could not look away." : gesture_8_shakeHead,\
                        "if what had come into his mind" : gesture_9_think,\
                        "The more he looked" : gesture_3_everything,\
                        "into those eyes," : crazyEyes,\
                        "was up there now," : gesture_10_showUp,\
                        "able to spew out his hatred" : changeMode,\
                        }
    passage = "It was at that precise moment, as their eyes met in the cinema, that Billy felt he had met this man before, not on screen, but face to face. And when Hitler raised his hand and brushed his hair back from his forehead, he knew at once who it was, and where they had met, and remembered everything that had happened between them. Christine clutched his arm, looking away from the screen, then buried her head in Billy's shoulder. Billy realised that everyone in that cinema was feeling as she did.           It was fear, the kind that gripped your body and soul and wouldn't leave you. No one whistled any more, no one hooted, no one laughed. It was as if everyone in the cinema was holding their breath, waiting for what was to come, dreading the horror of it, but knowing that there was nothing that could stop it, because this man, this Hitler, was going to make it happen. But Billy knew more. All the while Billy looked up into his eyes, and could not look away. All the while he was wondering if what had come into his mind could possibly be true. The more he looked into those eyes, the more he realised that it was, that there could be no doubt about it. That man, that warmonger, was up there now, able to spew out his hatred only because Billy had spared his life all those years before, after the Battle of Marcoing."
    #passage =  "It was at that precise moment, as their eyes met in the cinema, that Billy felt he had met this man before, not on screen, but face to face. And when Hitler raised his hand and brushed his hair back from his forehead, he knew at once who it was, and where they had met, and remembered everything that had happened between them. Christine clutched his arm, looking away from the screen, then buried her head in Billy's shoulder.  Billy realised that everyone in that cinema was feeling as she did. It was fear, the kind that gripped your body and soul and wouldn't leave you. No one whistled any more, no one hooted, no one laughed."
    # passage = " That man, that warmonger, was up there now, able to spew out his hatred only because Billy had spared his life all those years before, after the Battle of Marcoing."
    rePassage = dictSearch(passage)[0]
    # print(rePassage)
    #ALProxy("ALTextToSpeech", robotIP, robotPort).setParameter("pitchShift", 1)

     # Set Voice Parameters
    ttsProxy.setParameter("speed", 80)
    #ttsProxy.setParameter("pitchShift", 1.0)
    # ttsProxy.setParameter("doubleVoice", 1)
    #ttsProxy.setVolume(1)
    #ttsProxy.setParameter("doubleVoiceTimeShift", 0.5)
    # Voices = ttsProxy.getAvailableVoices()
    # print(Voices)
    # ttsProxy.setVoice("naoenu")
    
    # Turn on the Motors
    motionProxy.wakeUp()
    
    #StandUp
    StandUp(postureProxy)
    


    # Set I have no ideaed, 1:random, 2:contextual 
    animatedSpeechProxy.setBodyLanguageMode(0)
    for i in rePassage:
        if i in custom_gesture_map:
            custom_gesture_map[i](i, motionProxy, animatedSpeechProxy, ledProxy)
        else:
            animatedSpeechProxy.say(i)        
    #animatedSpeechProxy.say("^start(animations\Stand\Gestures\No_1) I am doing a gesture ^wait(animations\Stand\Gestures\No_1)")


    # # # Turn off the Motors
    motionProxy.rest()


if __name__ == "__main__":
    # robotIp = "169.254.44.123" #Set a default IP here
    # robotPort = 9559           #Set default POort here
    robotPort = 42804
    robotIp = "127.0.0.1"




    # if len(sys.argv) < 2:
    #     print "Usage python robotIP please"
    # else:
    #     robotIp = sys.argv[1]

    # if len(sys.argv) > 2:
    #     print "Usage python robotPort please"
    # else:
    #     robotPort = int(sys.argv[2])

    main(robotIp, robotPort)