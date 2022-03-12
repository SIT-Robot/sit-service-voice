#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rospy 
import actionlib
from robot_voice.msg import *
from std_msgs.msg import Int32

def started_cb(goal:recognizerActionGoal):
    rospy.loginfo("开始聆听您的指令")

def feedback_cb(feedback: recognizerActionFeedback):
    rospy.loginfo("正在识别：%d",feedback.feedback.n_seconds)

def result_cb(result: recognizerActionResult):
    rospy.loginfo("识别结束，%s",result.result.voice_txt)

if __name__=="__main__":
    rospy.init_node("voice_show")
    rospy.Subscriber("/recording/goal",recognizerActionGoal,started_cb)
    rospy.Subscriber("/recording/feedback",recognizerActionFeedback,feedback_cb)
    rospy.Subscriber("/recording/result",recognizerActionResult,result_cb)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        rospy.signal_shutdown()

       