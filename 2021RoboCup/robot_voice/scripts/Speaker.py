#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import rospy
from std_msgs.msg import String

rospy.init_node("Speaker",anonymous = True)

from sound_play.libsoundplay import SoundClient
from sound_play.msg import SoundRequest

# soundplay节点初始化
soundhandle = SoundClient()
rospy.sleep(1)
soundhandle.stopAll()

def Speaker(data:String):
    soundhandle.say(data.data,'voice_don_diphone',1)
    rospy.loginfo("I said: "+ data.data)

rospy.Subscriber("Answer",String,Speaker)

if __name__ =="__main__":
    try:
        rospy.spin()
    except KeyboardInterrupt:
        rospy.signal_shutdown()
    
