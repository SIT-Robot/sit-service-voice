#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import os
import sys

from actionlib.simple_action_client import SimpleActionClient
from robot_voice.msg import Person, Subjects
from rospy import client
from rospy.topics import Publisher
import config
from sound_play.libsoundplay import SoundClient
from sound_play.msg import SoundRequest
from std_msgs.msg import String
from robot_voice.msg import *
import actionlib

# 初始化ROS节点
rospy.init_node('voice_sound')
rospy.sleep(1)

heard_text_pub = rospy.Publisher('heard_text',String,queue_size=1)

# soundplay节点初始化
soundhandle = SoundClient()
rospy.sleep(1)
soundhandle.stopAll()

# 创建客户端对象
client = actionlib.SimpleActionClient("recording", recognizerAction)
client.wait_for_server()
# 发送请求：
goal_obj = recognizerGoal()
goal_obj.seconds = 4  # 发送录音时间

def done_cb(staus, voice_txt):
    if(staus == actionlib.GoalStatus.SUCCEEDED):  # 如果识别成功并且返回
        rospy.loginfo("响应结果为：%s", voice_txt.voice_txt)
        res = voice_txt.voice_txt
        rospy.loginfo("I heard::"+res)
        heard_text_pub.publish(res)

        
    else:
        rospy.loginfo("响应失败..")

    client.send_goal(goal_obj, done_cb, active_cb)


def active_cb():
    rospy.loginfo("连接已建立....")


# 建立客户端与服务端连接，#参数一：发送请求参数二：对返回最终结果进行处理，#参数三：建立action连接
client.send_goal(goal_obj, done_cb, active_cb)

try:
    rospy.spin()
except KeyboardInterrupt:
    rospy.signal_shutdown()
