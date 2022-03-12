#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import os
import sys
from robot_voice.msg import Person
from robot_voice.msg import Subjects
from rospy.topics import Subscriber
from std_msgs.msg import String

# soundplay节点初始化
from sound_play.msg import SoundRequest
from sound_play.libsoundplay import SoundClient

# 初始化ROS节点
rospy.init_node('file', anonymous=True)


soundhandle = SoundClient()
rospy.sleep(1)
soundhandle.stopAll()


pub_confirm = rospy.Publisher("Confirm", String, queue_size=10)


# 这里为获取到的人物以及物品信息存储


People_count = 0
Subject_count = 0
people1 = Person()
people2 = Person()

subject1 = Subjects()
subject2 = Subjects()


def Save_people(data):
    People_count += 1
    if(People_count == 1):
        people1 = data.data
    elif(People_count == 2):
        people2 = data.data
    pub_confirm.publish("ok")  # 给底盘发送消息，信息采集完毕

def Save_subjects(data):
    Subject_count += 1
    if(Subject_count == 1):
        subject1 = data.data
    elif(Subject_count == 2):
        subject2 = data.data
    pub_confirm.publish("ok")  # 给底盘发送消息，信息采集完毕




while not rospy.is_shutdown:
    Subscriber("People", Person, Save_people)
    Subscriber("Subject", Subjects, Save_subjects)
