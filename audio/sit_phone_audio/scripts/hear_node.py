#!/usr/bin/python3
import actionlib
import rospy
import sys
from rpc_node import RpcNode
from sit_phone_audio_msgs.msg import *

rospy.init_node('audio_hear_node', sys.argv)

rospy.set_param

phone = RpcNode(self_node_name='ros',
                mqtt_address=rospy.get_param('~mqtt_address', '10.1.160.240'),
                mqtt_port=rospy.get_param('~mqtt_port', 1883))


class MyHearAction:
    def __init__(self,
                 rpc_node: RpcNode):
        self.__server = actionlib.SimpleActionServer('hear', HearAction, execute_cb=self.cb, auto_start=False)
        self.__server.start()
        self.__rpc_node = rpc_node
        rpc_node.register('on_hear_error', self.on_hear_error)
        rpc_node.register('on_hear_finished', self.on_hear_finished)
        self.__on_hear_error_flag = False
        self.__on_hear_finished_flag = False
        self.__hear_finished_msg = ''
        self.__hear_error_msg = ''

    def on_hear_finished(self, message: str):
        """
        当语音识别结束后
        :param message:识别结果
        :return:
        """
        self.__on_hear_finished_flag = True
        self.__hear_finished_msg = message

    def on_hear_error(self, error_msg: str):
        """
        当语音识别出错时
        :param error_msg:
        :return:
        """
        self.__on_hear_error_flag = True
        self.__hear_error_msg = error_msg

    def hear(self):
        """
        开始监听
        :return:
        """
        rospy.loginfo('开始语音识别...')
        self.__rpc_node.call('phone', 'hear', [])

    def cb(self, goal: HearGoal):
        rospy.loginfo('收到语音识别请求')
        self.hear()
        self.__on_hear_finished_flag = False
        self.__on_hear_error_flag = False

        listen_rate = rospy.Rate(10)

        # 当speak完成或出错时结束该循环
        while not (self.__on_hear_finished_flag or self.__on_hear_error_flag):
            listen_rate.sleep()

        if self.__on_hear_error_flag:
            rospy.logerr('语音识别出错')
            result = HearResult()
            result.hasError = True
            result.errorMassage = self.__hear_error_msg
            self.__server.set_succeeded(result)

        if self.__on_hear_finished_flag:
            rospy.loginfo('语音识别完毕: %s', self.__hear_finished_msg)
            result = HearResult()
            result.text = self.__hear_finished_msg
            result.hasError = False
            result.errorMassage = ''
            self.__server.set_succeeded(result)


MyHearAction(phone)

rate = rospy.Rate(100)

try:
    while not rospy.is_shutdown():
        rate.sleep()
        phone.loop()
except KeyboardInterrupt:
    rospy.loginfo('ROS语音节点退出')
