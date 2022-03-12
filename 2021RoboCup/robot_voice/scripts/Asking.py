#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from config import *
from robot_voice.msg import Person, Subjects

from sound_play.libsoundplay import SoundClient
from sound_play.msg import SoundRequest
import rospy
import os
import sys
from std_msgs.msg import String

# 初始化ROS节点
rospy.init_node('Asking', anonymous=True)

pub = rospy.Publisher("Asking_ok", String, queue_size=10)
pub_subjects = rospy.Publisher("Pubject", Subjects, queue_size=20)
pub_People = rospy.Publisher("People", Person, queue_size=20)


# soundplay节点初始化
soundhandle = SoundClient()     
rospy.sleep(1)
soundhandle.stopAll()


command = ''


def Speaker(data):
    global command
    command = data.data
    if(command == 'reception'):
        soundhandle.say("Hi,What's your name?", 'voice_don_diphone', 1)
        rospy.Subscriber("voice_txt", String, Ask)
    elif(command == 'fetch'):
        soundhandle.say(
            "Hi,What would  you like me to get for you?", 'voice_don_diphone', 1)
        rospy.Subscriber("voice_txt", String, Ask)


def Ask(data):
    global command
    command=rospy.Subscriber("command")
    people = Person()
    subject = Subjects()
    voice_words = data.data
    rospy.loginfo("I heard::"+voice_words)
    res = voice_words.split(" ")  # 将输出的文本以空格分开
    if(command == 'reception'):
        for w in res:
            if(w in Name):
                people.name = w
                soundhandle.say(
                    "ok,fine"+w+"what would you want to drink?", 'voice_don_diphone', 1)
            if(w in drinking):
                people.drink = w
                soundhandle.say("ok,fine.Please fllow me.")
                pub_People.publish(people)  # 发布人物信息
    elif(command == 'fetch'):
        for w in res:
            if(w in objects):
                subject.name = w
            if(w in room):
                subject.location = w
                soundhandle.say("ok,fine i get it.")
                pub_subjects(subject)  # 发送采集的物品信息


rospy.Subscriber("voice_txt", String, Ask)
#rospy.Subscriber("command", String, Speaker)
rospy.spin()
