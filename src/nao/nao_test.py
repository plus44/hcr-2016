"""
Gets the NAO robot to perform a simple routine.

1) Connects to the robot
2) Turns on the motors
3) Stands up
4) Walks one metre forward
5) Sits down
6) Turns off the motors
7) Disconnects from the robot
"""
# STANDARD PYTHON IMPORTS
import argparse

# LIBRARY IMPORTS
from naoqi import ALProxy

# GLOBAL VARIABLES
DISTANCE_TO_TRAVEL = 1.0

# CODE AND CLASSES
def main(robot_ip, port=9559):
	""" Performs the basic sequence of motions required
	"""
	motion_proxy  = ALProxy("ALMotion", robot_ip, port)
	posture_proxy = ALProxy("ALRobotPosture", robot_ip, port)
	navigation_proxy = ALProxy("ALNavigationProxy", robot_ip, port)

	# Wake up robot
	motion_proxy.wakeUp()

	# Send robot to Stand at a relative speed of 50%
	if posture_proxy.goToPosture("StandInit", 0.5):
		print "NAO has stood up."

	# Enable foot contact protection
	motion_proxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])

	# Walk one metre (blocking call)
	if navigation_proxy.navigateTo(DISTANCE_TO_TRAVEL, 0):
		print "NAO has walked %s" % DISTANCE_TO_TRAVEL

	# Sit down
	if posture_proxy.goToPosture("SitRelax", 0.5):
		print "NAO is now relaxing."

	# Go to rest position
	motion_proxy.rest()

if __name__ == '__main__':
	# Fetch command line arguments
	parser = argparse.ArgumentParser()
	parser.add_argument("--ip", type=str, default="127.0.0.1",
						help="Robot IP address")
	parser.add_argument("--port", type=int, default=9559,
						help="Robot port number")

	args = parser.parse_args()
	# Run the sequence of motions
	main(args.ip, args.port)
else:
	print 'This program is meant to be run as main'
