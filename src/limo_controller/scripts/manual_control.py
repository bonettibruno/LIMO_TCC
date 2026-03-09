#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
import sys, select, termios, tty

# Standard key map for teleoperation
msg = """
Control Your Limo!
---------------------------
Moving around:
   w
a  s  d

w/s : increase/decrease linear velocity
a/d : increase/decrease angular velocity

space key, k : force stop
CTRL-C to quit
"""

def get_key():
    """ Reads a single keypress from the terminal """
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

if __name__=="__main__":
    settings = termios.tcgetattr(sys.stdin)
    
    rospy.init_node('manual_control_node')
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    # Initial velocities
    linear_vel = 0.0
    angular_vel = 0.0
    status = 0

    try:
        print(msg)
        while not rospy.is_shutdown():
            key = get_key()
            
            # Movement logic
            if key == 'w':
                linear_vel = 0.2
                angular_vel = 0.0
            elif key == 's':
                linear_vel = -0.2
                angular_vel = 0.0
            elif key == 'a':
                linear_vel = 0.0
                angular_vel = 0.5
            elif key == 'd':
                linear_vel = 0.0
                angular_vel = -0.5
            elif key == ' ' or key == 'k':
                linear_vel = 0.0
                angular_vel = 0.0
            else:
                if (key == '\x03'): # CTRL-C
                    break
            
            # Create and publish the message
            twist = Twist()
            twist.linear.x = linear_vel
            twist.angular.z = angular_vel
            pub.publish(twist)

    except Exception as e:
        print(e)

    finally:
        # Final stop for safety
        twist = Twist()
        twist.linear.x = 0.0
        twist.angular.z = 0.0
        pub.publish(twist)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)