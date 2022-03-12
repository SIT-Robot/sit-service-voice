#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import pyaudio
import wave
from playsound import playsound
import rospy
import os
import sys
from rospy.core import loginfo
from std_msgs.msg import String
import actionlib
from robot_voice.msg import *

rospy.sleep(1)

# 初始化ROS节点
rospy.init_node('voice_recognize', anonymous=True)

pub = rospy.Publisher("voice_txt", String, queue_size=10)

#from .tuning import Tuning

import usb.core

import usb.util

from aip import AipSpeech

APP_ID='24105668'
API_KEY='xIBkcVKdcRPkdGpOsclwCtci'
SECRET_KEY='GFnTBaNQHIlNxPwab2oDTnWWQuyTQDVm'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

class Recoding:
    def __init__(self):
        self.server = actionlib.SimpleActionServer("recording",recognizerAction,self.cb,False)
        self.server.start()
        rospy.loginfo("服务端启动....")

    def cb(self,goal):
        #解析目标值：
        goal_num=goal.seconds
        rospy.loginfo("录音时间为：%d",goal_num)
        #发送连续反馈：
        rate=rospy.Rate(10)

        result = recognizerResult()
        result.voice_txt=self.recording(goal_num,1737)
        self.server.set_succeeded(result) 

    def recording(self,time,languge):        #time为录取时间,language为语言接口英语1737，中文1537
        RESPEAKER_RATE = 16000
        RESPEAKER_CHANNELS = 1 
        RESPEAKER_WIDTH = 2
        RESPEAKER_INDEX = 7
        CHUNK = 1024
        RECORD_SECONDS = time
        WAVE_OUTPUT_FILENAME ="output.wav"

        p = pyaudio.PyAudio()

        stream = p.open(
                rate=RESPEAKER_RATE,
                format=p.get_format_from_width(RESPEAKER_WIDTH),
                channels=RESPEAKER_CHANNELS,
                input=True,
                input_device_index=RESPEAKER_INDEX,)

        print("* recording")

        frames = []

        last_time = 0
        for i in range(0, int(RESPEAKER_RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
            curr_time = int((i/(int(RESPEAKER_RATE / CHUNK * RECORD_SECONDS)-1))*time)
            if last_time != curr_time:
                fb_obj = recognizerFeedback()
                fb_obj.n_seconds = curr_time
                self.server.publish_feedback(fb_obj)    
            last_time = curr_time

            
            



        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(RESPEAKER_CHANNELS)
        wf.setsampwidth(p.get_sample_size(p.get_format_from_width(RESPEAKER_WIDTH)))
        wf.setframerate(RESPEAKER_RATE)
        wf.writeframes(b''.join(frames))
        wf.close()


        result = client.asr(self.get_file_content('output.wav'), 'wav', 16000, {
        'dev_pid': 1737,})
        
        try:
            if result['err_no'] == 0:
                return result['result'][0]
        except KeyError as ke:
            print(result)
            print(ke)
            return ''
        return ''

    #文本转语音输出测试代码
    def get_file_content(self,a):
        with open(a, 'rb') as fp:
            return fp.read()


if __name__ == "__main__":
    server = Recoding()
    rospy.spin()