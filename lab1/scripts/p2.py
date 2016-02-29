#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
import tf.transformations
import roslib
import math
import geometry_msgs.msg

def test():

    
    listener = tf.TransformListener()
    twist=Twist()

    bot2_vel = rospy.Publisher('robot_1/cmd_vel', Twist,queue_size=1)    
    rate = rospy.Rate(10.0)
    rospy.sleep(2)
    while not rospy.is_shutdown():

        try:
	    now=rospy.Time.now()
	    past=now-rospy.Duration(1.0)
	    listener.waitForTransformFull("/robot_1/odom", now,
                                      "/robot_0/odom", past,
                                      "/world", rospy.Duration(1.0))
	    #(trans,rot) = listener.lookupTransform('/robot_1/odom', '/robot_0/odom', rospy.Time())
            (trans,rot) = listener.lookupTransformFull('/robot_1/odom',now, '/robot_0/odom',past, "/world")
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue
        angular = 4.0 *math.atan2(trans[1], trans[0])
    	linear = 1.0 * math.sqrt(trans[0] ** 2 + trans[1] ** 2)
    	twist.linear.x = linear
    	twist.angular.z = angular
    	bot2_vel.publish(twist)

        rate.sleep()
      
if __name__ == '__main__':

    rospy.init_node('trans_bot',anonymous=True)
    test()


