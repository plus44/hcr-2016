import math

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)

    def onLoad(self):
        #put initialization code here
        pass

    def onUnload(self):
        #put clean-up code here
        pass

    def onInput_onStart(self):
        #self.onStopped() #activate the output of the box
        
        motion_proxy  = ALProxy("ALMotion")
        posture_proxy = ALProxy("ALRobotPosture")
       # navigation_proxy = ALProxy("ALNavigationProxy")

    #   Wake up robot
        motion_proxy.wakeUp()

    # Send robot to Stand at a relative speed of 50%
        if posture_proxy.goToPosture("StandInit", 1):
            print "NAO has stood up."

    # Enable foot contact protection
    #    motion_proxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])

    # Walk one metre (blocking call)
       x = 1
       y=0
       theta=0
       motion_proxy.moveTo(x, y, theta)

        #if navigation_proxy.navigateTo(DISTANCE_TO_TRAVEL, 0):
         #   print "NAO has walked %s" % DISTANCE_TO_TRAVEL

    # Sit down
        if posture_proxy.goToPosture("SitRelax", 1):
            print "NAO is now relaxing."

    # Go to rest position/ turn motors off
        motion_proxy.rest()


    def onInput_onStop(self):
        self.onUnload() #it is recommended to reuse the clean-up as the box is stopped
        self.onStopped() #activate the output of the box
