#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math

class LimoSimpleMove:
    def __init__(self):
        # Initialize the ROS node
        rospy.init_node('move_distance_node', anonymous=True)
        
        # Publisher for velocity commands
        self.vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        
        # Subscriber for odometry data
        self.odom_sub = rospy.Subscriber('/odom', Odometry, self.odom_callback)
        
        # Current position variable
        self.current_x = 0.0
        self.rate = rospy.Rate(10) # 10Hz frequency

    def odom_callback(self, msg):
        """ Get the current X position from odometry """
        self.current_x = msg.pose.pose.position.x

    def run_mission(self, target_distance):
        """ Move forward until target_distance is reached """
        rospy.sleep(1) # Wait for odom to initialize
        start_x = self.current_x
        vel_msg = Twist()
        
        rospy.loginfo(f"Starting mission. Target: {target_distance}m")

        while not rospy.is_shutdown():
            # Calculate how much we have moved
            distance_moved = abs(self.current_x - start_x)
            
            if distance_moved >= target_distance:
                rospy.loginfo("Target reached!")
                break
            
            # Set speed (0.1 m/s is a safe speed for indoors)
            vel_msg.linear.x = 0.1
            self.vel_pub.publish(vel_msg)
            self.rate.sleep()

        # Stop the robot after the loop
        self.vel_pub.publish(Twist()) 

if __name__ == '__main__':
    try:
        mover = LimoSimpleMove()
        # Change '1.0' to the distance you want in meters
        mover.run_mission(target_distance=1.0)
    except rospy.ROSInterruptException:
        pass