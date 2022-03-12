#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sound_play.libsoundplay import SoundClient
from sound_play.msg import SoundRequest
import rospy
import os
import sys
from std_msgs.msg import String
pub = rospy.Publisher("voice_txt", String, queue_size=10)

# soundplay节点初始化
soundhandle = SoundClient()
rospy.sleep(1)
soundhandle.stopAll()

# 初始化ROS节点
rospy.init_node('voice_recognize', anonymous=True)

# 发布获取的语音文本voice_txt


def Pub(data):
    voice_txt = data.data
    # 此处可添加过滤无用语音的算法函数
    pub.publish(voice_txt)


# 订阅由recognize语音捕获的语音文本


def listener(data):
    command = data.data
    rospy.loginfo("Starting voice recognizer")
    if(command == 'reception' or command == 'fetch'):
        rospy.Subscriber("/recognizer/output", string, Pub)
    rospy.spin()

# 订阅由port发布的command 信息


def Confirm(data):
    soundhandle.say(
        "Hi,i'm your robot! I'm staring listering you speak.", 'voice_don_diphone', 1)
    rospy.Subscriber("command", string, listener)
    listener()
# 订阅pocketsphinx语音识别的输出字符


while not rospy.is_shutdown():
    Confirm()
