import argparse

from naoqi import ALProxy

def main(robot_ip, port=9559):

motion_proxy = ALProxy("ALMotion" , robot_ip, port)

motion_proxy.wakeup()
motion_proxy.openHand('LHand')
 
 if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot ip address")
    parser.add_argument("--port", type=int, default=9559,
                        help="Robot port number")

    args = parser.parse_args()
    main(args.ip, args.port)
else:
	print 'This program is meant to be run as main'