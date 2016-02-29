#!/usr/bin/env python

import rospy
import random
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import tf.transformations

x_speed=2.0
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
twist=Twist()
def sub():
   rospy.loginfo("In sub")
   pub1=rospy.Subscriber('/base_scan',LaserScan,callback)
   rospy.spin()

def turn():   
    rospy.loginfo("In turn")
    twist.linear.x=0.0;
    twist.linear.y = 0;
    twist.linear.z = 0;             
    twist.angular.y = 0;   
    twist.angular.z = random.randint(1,20);
    twist.angular.x = 0;
    pub.publish(twist)

def walker():
    twist.linear.x=x_speed;
    twist.linear.y = 0;
    twist.linear.z = 0;             
    twist.angular.y = 0;   
    twist.angular.z = 0;  
    twist.angular.x = 0;
    rospy.loginfo("In talker")
    while(True):
    	pub.publish(twist)
        break

def callback(data):   
   twist=Twist()
   rospy.loginfo("In callback")
   for i in range(40,140):    
	if data.ranges[i]< 1.0:
		turn() #return true -- call function
	else:
		walker()
       	

if __name__ == '__main__':
    try:
	rospy.init_node('talker', anonymous=True)    
		
	while(True):
		sub()		
    except rospy.ROSInterruptException:
        pass	
