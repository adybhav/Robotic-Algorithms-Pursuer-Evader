#!/usr/bin/env python
import rospy
import random
import roslib
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
import tf


x_speed=2.0
def sub():
   pub1=rospy.Subscriber('robot_0/base_scan',LaserScan,callback)
   rospy.spin()

def turn():   
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
    while(True):
    	pub.publish(twist)
        break

def callback(data):   
   twist=Twist()
   for i in range(22,135):    
	if data.ranges[i]< 1.0:
		turn()
	else:
		walker()
       	
def broadcast(bcast,botname):
    br = tf.TransformBroadcaster()
    br.sendTransform((bcast.pose.pose.position.x, bcast.pose.pose.position.y, 0),
                     (bcast.pose.pose.orientation.x,bcast.pose.pose.orientation.y,bcast.pose.pose.orientation.z,bcast.pose.pose.orientation.w),
                     rospy.Time.now(),
                     'robot_0/odom',
                     "world")

def broadcast1(bcast,botname1):
    br = tf.TransformBroadcaster()
    br.sendTransform((bcast.pose.pose.position.x, bcast.pose.pose.position.y, 0),
                     (bcast.pose.pose.orientation.x,bcast.pose.pose.orientation.y,bcast.pose.pose.orientation.z,bcast.pose.pose.orientation.w),
                     rospy.Time.now(),
                     'robot_1/odom',
                     "world")

if __name__ == '__main__':
    try:	
	botname='robot_0'
	botname1='robot_1'
	pub = rospy.Publisher('robot_0/cmd_vel', Twist, queue_size=1)
	twist=Twist()
	bcast=Odometry()
	rospy.init_node('pursuer', anonymous=True)
	rospy.Subscriber('/robot_0/odom',
                     Odometry,
                     broadcast,
                     'robot_0/odom')
	rospy.Subscriber('/robot_1/odom',
                     Odometry,
                     broadcast1,
                     'robot_1/odom')

	sub()		
    except rospy.ROSInterruptException:
        pass	
