#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import rospy
from std_msgs.msg import String
import config
from  robot_voice.msg import *

rospy.init_node("conversation",anonymous=True)

from rospy.topics import Publisher

pub_People = rospy.Publisher("People", Person, queue_size=20)
pub_location = rospy.Publisher("Location", String, queue_size=10)
pub_Answer = rospy.Publisher("Answer",String,queue_size = 10)
pub_Name = rospy.Publisher("people_name",String,queue_size= 1)
pub_subjects = rospy.Publisher("subject", String, queue_size=1)


def ob_confirm(L:String):
    data = L.split(" ")
    for w in data:
        if w in config.objects:
            return True
def lo_confirm(L:String):
    data = L.split(" ")
    for w in data:
        if w in config.location:
            return True
# 对话匹配
def conversation(data):
    answer = String()
    Asking = data
    people = Person()
    words = Asking.split(" ")  #将输出的文本以空格分开
    for w in words:
        if(w in config.HI):
            answer = "Hi,What's your name?"
        if(w in config.Name):
            people.name = w
            answer = "ok,fine "+w+" what do you want drink"
            pub_Name.publish(w)
            rospy.loginfo("people name:"+people.name)

        if(w in config.drinking):
            people.drink = w
            answer= "Ok,I already know you like "+w
            rospy.loginfo("people want drink:"+people.drink)

        if(w in config.Myname):
            answer = "S I T Robot."

        if(w in config.room and ob_confirm(Asking)):
            room = w
            for s in words:
                if s in config.objects:
                    answer="ok i will go to "+room+" and take "+s+" for you."
                    pub_location.publish(room)
                    pub_subjects.publish(s)
                    

        if (w in config.room and not ob_confirm(Asking)):
            answer = "ok i will go to "+w  
            pub_location.publish(w)

        if(w in config.objects and lo_confirm(Asking)):
            objects = w
            for s in words:
                if s in config.location:
                    answer="ok i will go to "+s+" and take "+objects+" for you."
                    pub_location.publish(room)
                    pub_subjects.publish(s)

        if (w in config.objects and not lo_confirm(Asking)):
            answer = "ok i will go to take "+w  
            pub_location.publish(w)
        
        if(w == "out"):
            answer = "ok i will go out. "
            pub_location.publish("exit")
        if(w == "stop"):
            pub_location.publish("stop")
            answer = "OK, i wait you start again."
        if(w == "follow"):
            answer = "Ok i will follow you."
            pub_location.publish("follow")
    pub_People.publish(people)
    pub_Answer.publish(answer)


def heard_cb(heard_text:String):
    conversation(heard_text.data)

rospy.Subscriber('heard_text',String,callback=heard_cb,queue_size=1)

try:
    rospy.spin()
except KeyboardInterrupt:
    rospy.signal_shutdown()
