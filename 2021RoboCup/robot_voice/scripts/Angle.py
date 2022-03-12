#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import time
import wave

from tuning import Tuning

import usb.core

import usb.util


import rospy
import os
import sys
from std_msgs.msg import String,Float32

rospy.init_node("voice_angle", anonymous=True)

pub = rospy.Publisher("voice_angle", Float32, queue_size=10)


def _sum(arr, n):
    return(sum(arr))


def get_angle(T):  # 角度平均T为角度获取次数
    angle = []
    i = 0
    dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)

    if dev:

        Mic_tuning = Tuning(dev)
        while True:

            try:
                angle.append(1)
                angle[i] = Mic_tuning.direction
                time.sleep(1)
                i = i+1
                if(i >= T-1):
                    n = len(angle)
                    ans = _sum(angle, n)
                    return ans/n
            except KeyboardInterrupt:
                break


while not rospy.is_shutdown():
    ans = get_angle(2)
    print(ans)
    pub.publish(ans)