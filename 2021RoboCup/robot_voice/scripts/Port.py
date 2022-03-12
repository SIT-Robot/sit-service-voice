#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rospy
import os
import sys
from std_msgs.msg import String

pub = rospy.Publisher("command", String, queue_size=10)

# 初始化ROS节点
rospy.init_node('Port', anonymous=True)


def Port(data):
    action = data.data
    # 在此添加对底盘信息处理算法
    pub.publish(action)
    rospy.loginfo("底盘信息成功接收并发布")


def listen():
    rospy.loginfo("Starting recognize command from robot")
    rospy.Subscriber("start", String, Port)
    rospy.spin()


while not rospy.is_shutdown:
    listen()
