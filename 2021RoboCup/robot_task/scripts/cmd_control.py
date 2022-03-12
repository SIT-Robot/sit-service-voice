import rospy
from geometry_msgs.msg import Twist
speed_pub = rospy.Publisher('/cmd_vel',Twist)

def set_speed(vx,vy,vw):
    t = Twist()
    t.linear.x = vx
    t.linear.y = vy
    t.angular.z = vw
    speed_pub.publish(t)

def stop():
    set_speed(0,0,0)