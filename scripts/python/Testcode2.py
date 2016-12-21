# -*- encoding: UTF-8 -*- 

import math
# import almath as m # python's wrapping of almath
import sys
from naoqi import ALProxy


def StiffnessOn(proxy):
    # We use the "Body" name to signify the collection of all joints
    pNames = "Body"
    pStiffnessLists = 1.0
    pTimeLists = 1.0
    proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)

def StiffnessOff(proxy):
    # We use the "Body" name to signify the collection of all joints
    pNames = "Body"
    pStiffnessLists = 0.0
    pTimeLists = 1.0
    proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)

def StandUp(proxy):
    proxy.goToPosture("StandInit", 1.0)

def SitDown(proxy):
    proxy.goToPosture("Sit", 1.0)

def Walk(proxy,x,y,theta):
    proxy.moveTo(x, y, theta)
    self.onStopped()


def gesture_1_handwave(robotIP) :

    # Choregraphe simplified export in Python.
    names = list()
    times = list()
    keys = list()

    names.append("HeadPitch")
    times.append([0.6])
    keys.append([0.0459781])

    names.append("HeadYaw")
    times.append([0.6])
    keys.append([-0.0322559])

    names.append("LAnklePitch")
    times.append([0.6])
    keys.append([-0.352862])

    names.append("LAnkleRoll")
    times.append([0.6])
    keys.append([-0.00149202])

    names.append("LElbowRoll")
    times.append([0.6])
    keys.append([-0.492372])

    names.append("LElbowYaw")
    times.append([0.6])
    keys.append([-0.09515])

    names.append("LHand")
    times.append([0.6])
    keys.append([0.2372])

    names.append("LHipPitch")
    times.append([0.6])
    keys.append([-0.443284])

    names.append("LHipRoll")
    times.append([0.6])
    keys.append([-0.00609398])

    names.append("LHipYawPitch")
    times.append([0.6])
    keys.append([0.00310993])

    names.append("LKneePitch")
    times.append([0.6])
    keys.append([0.699462])

    names.append("LShoulderPitch")
    times.append([0.6])
    keys.append([-0.921976])

    names.append("LShoulderRoll")
    times.append([0.6])
    keys.append([0.25])

    names.append("LWristYaw")
    times.append([0.6])
    keys.append([0.11194])

    names.append("RAnklePitch")
    times.append([0.6])
    keys.append([-0.348176])

    names.append("RAnkleRoll")
    times.append([0.6])
    keys.append([0.00157595])

    names.append("RElbowRoll")
    times.append([0.6])
    keys.append([0.925044])

    names.append("RElbowYaw")
    times.append([0.6])
    keys.append([1.39897])

    names.append("RHand")
    times.append([0.6])
    keys.append([0.2448])

    names.append("RHipPitch")
    times.append([0.6])
    keys.append([-0.451038])

    names.append("RHipRoll")
    times.append([0.6])
    keys.append([-0.00302601])

    names.append("RHipYawPitch")
    times.append([0.6])
    keys.append([0.00310993])

    names.append("RKneePitch")
    times.append([0.6])
    keys.append([0.696478])

    names.append("RShoulderPitch")
    times.append([0.6])
    keys.append([1.40212])

    names.append("RShoulderRoll")
    times.append([0.6])
    keys.append([-0.069072])

    names.append("RWristYaw")
    times.append([0.6])
    keys.append([0.0597839])

    try:
      # uncomment the following line and modify the IP if you use this script outside Choregraphe.
      motion = ALProxy("ALMotion", robotIP, 9559)
        #motion = ALProxy("ALMotion")
      motion.angleInterpolation(names, keys, times, True)
    except BaseException, err:
      print err


def gesture_2(robotIP):

    # Choregraphe simplified export in Python.
    names = list()
    times = list()
    keys = list()

    names.append("HeadPitch")
    times.append([0.6])
    keys.append([0.0459781])

    names.append("HeadYaw")
    times.append([0.6])
    keys.append([-0.0322559])

    names.append("LAnklePitch")
    times.append([0.6])
    keys.append([-0.348176])

    names.append("LAnkleRoll")
    times.append([0.6])
    keys.append([-0.00157595])

    names.append("LElbowRoll")
    times.append([0.6])
    keys.append([-0.925044])

    names.append("LElbowYaw")
    times.append([0.6])
    keys.append([-1.39897])

    names.append("LHand")
    times.append([0.6])
    keys.append([0.2448])

    names.append("LHipPitch")
    times.append([0.6])
    keys.append([-0.451038])

    names.append("LHipRoll")
    times.append([0.6])
    keys.append([0.00302601])

    names.append("LHipYawPitch")
    times.append([0.6])
    keys.append([0.00310993])

    names.append("LKneePitch")
    times.append([0.6])
    keys.append([0.696478])

    names.append("LShoulderPitch")
    times.append([0.6])
    keys.append([1.40212])

    names.append("LShoulderRoll")
    times.append([0.6])
    keys.append([0.069072])

    names.append("LWristYaw")
    times.append([0.6])
    keys.append([-0.0597839])

    names.append("RAnklePitch")
    times.append([0.6])
    keys.append([-0.348176])

    names.append("RAnkleRoll")
    times.append([0.6])
    keys.append([0.00157595])

    names.append("RElbowRoll")
    times.append([0.6])
    keys.append([0.925044])

    names.append("RElbowYaw")
    times.append([0.6])
    keys.append([1.39897])

    names.append("RHand")
    times.append([0.6])
    keys.append([0.2448])

    names.append("RHipPitch")
    times.append([0.6])
    keys.append([-0.451038])

    names.append("RHipRoll")
    times.append([0.6])
    keys.append([-0.00302601])

    names.append("RHipYawPitch")
    times.append([0.6])
    keys.append([0.00310993])

    names.append("RKneePitch")
    times.append([0.6])
    keys.append([0.696478])

    names.append("RShoulderPitch")
    times.append([0.6])
    keys.append([1.40212])

    names.append("RShoulderRoll")
    times.append([0.6])
    keys.append([-0.069072])

    names.append("RWristYaw")
    times.append([0.6])
    keys.append([0.0597839])


    try:
      # uncomment the following line and modify the IP if you use this script outside Choregraphe.
      motion = ALProxy("ALMotion", robotIP, 9559)
        #motion = ALProxy("ALMotion")
      motion.angleInterpolation(names, keys, times, True)
    except BaseException, err:
      print err



def squat(robotIP):

    # Choregraphe simplified export in Python.
    names = list()
    times = list()
    keys = list()

    names.append("HeadPitch")
    times.append([0.6])
    keys.append([0.0674541])

    names.append("HeadYaw")
    times.append([0.6])
    keys.append([-0.0276539])

    names.append("LAnklePitch")
    times.append([0.6])
    keys.append([-1.18276])

    names.append("LAnkleRoll")
    times.append([0.6])
    keys.append([0.070606])

    names.append("LElbowRoll")
    times.append([0.6])
    keys.append([-1.03848])

    names.append("LElbowYaw")
    times.append([0.6])
    keys.append([-0.794654])

    names.append("LHand")
    times.append([0.6])
    keys.append([0.0192])

    names.append("LHipPitch")
    times.append([0.6])
    keys.append([-0.700996])

    names.append("LHipRoll")
    times.append([0.6])
    keys.append([-0.076658])

    names.append("LHipYawPitch")
    times.append([0.6])
    keys.append([-0.237728])

    names.append("LKneePitch")
    times.append([0.6])
    keys.append([2.10767])

    names.append("LShoulderPitch")
    times.append([0.6])
    keys.append([1.44959])

    names.append("LShoulderRoll")
    times.append([0.6])
    keys.append([0.0873961])

    names.append("LWristYaw")
    times.append([0.6])
    keys.append([0.0843279])

    names.append("RAnklePitch")
    times.append([0.6])
    keys.append([-1.1863])

    names.append("RAnkleRoll")
    times.append([0.6])
    keys.append([-0.078192])

    names.append("RElbowRoll")
    times.append([0.6])
    keys.append([1.02782])

    names.append("RElbowYaw")
    times.append([0.6])
    keys.append([0.823716])

    names.append("RHand")
    times.append([0.6])
    keys.append([0.0172])

    names.append("RHipPitch")
    times.append([0.6])
    keys.append([-0.698012])

    names.append("RHipRoll")
    times.append([0.6])
    keys.append([0.07214])

    names.append("RHipYawPitch")
    times.append([0.6])
    keys.append([-0.237728])

    names.append("RKneePitch")
    times.append([0.6])
    keys.append([2.10622])

    names.append("RShoulderPitch")
    times.append([0.6])
    keys.append([1.44967])

    names.append("RShoulderRoll")
    times.append([0.6])
    keys.append([-0.0844119])

    names.append("RWristYaw")
    times.append([0.6])
    keys.append([-0.0583339])


    try:
      # uncomment the following line and modify the IP if you use this script outside Choregraphe.
      motion = ALProxy("ALMotion", robotIP, 9559)
        #motion = ALProxy("ALMotion")
      motion.angleInterpolation(names, keys, times, True)
    except BaseException, err:
      print err


def main(robotIP,robotPort):

    #Setting the Proxies
    try:
        motionProxy = ALProxy("ALMotion", robotIP, robotPort)
    except Exception, e:
        print "Could not create proxy to ALMotion"
        print "Error was: ", e

    try:
        ttsProxy = ALProxy("ALTextToSpeech", robotIP, robotPort)
    except Exception, e:
        print "Could not create proxy to ALTextToSpeech"
        print "Error was: ", e

    try:
        postureProxy = ALProxy("ALRobotPosture", robotIP, robotPort)
    except Exception, e:
        print "Could not create proxy to ALRobotPosture"
        print "Error was: ", e


    # Turn on the Motors
    StiffnessOn(motionProxy)

    #StandUp
    StandUp(postureProxy)

    # #Walk 1 Meter
    # Walk(motionProxy,1,0,0)


    # gesture_1_handwave(robotIP)
    # StandUp(postureProxy)
    # gesture_2(robotIP)


    # #StandUp
    # StandUp(postureProxy)

    # # #Sit Down
    # squat(robotIP)


    # # SitDown(postureProxy)

    # # # Turn off the Motors
    # StiffnessOff(motionProxy)



if __name__ == "__main__":
    robotIp = "169.254.44.123" #Set a default IP here
    robotPort = 9559 #Set default POort here


    # if len(sys.argv) < 2:
    #     print "Usage python robotIP please"
    # else:
    #     robotIp = sys.argv[1]

    # if len(sys.argv) > 2:
    #     print "Usage python robotPort please"
    # else:
    #     robotPort = int(sys.argv[2])

    main(robotIp, robotPort)