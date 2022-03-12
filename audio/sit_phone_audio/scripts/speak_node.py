#!/usr/bin/python3
import actionlib
import rospy
import sys
from rpc_node import RpcNode
from sit_phone_audio_msgs.msg import *

rospy.init_node('audio_speak_node', sys.argv)

phone = RpcNode(self_node_name='ros',
                mqtt_address=rospy.get_param('~mqtt_address', '10.1.160.240'),
                mqtt_port=rospy.get_param('~mqtt_port', 1883))


class MySpeakAction:
    def __init__(self,
                 rpc_node: RpcNode):
        self.__server = actionlib.SimpleActionServer('speak', SpeakAction, execute_cb=self.cb, auto_start=False)
        self.__server.start()
        self.__rpc_node = rpc_node
        rpc_node.register('on_speak_finished', self.on_speak_finished)
        rpc_node.register('on_speak_error', self.on_speak_error)
        self.__on_speak_finished_flag = False
        self.__on_speak_error_flag = False
        self.__speak_error_msg = ''

    def on_speak_finished(self):
        """
        当语音合成结束时
        :return:
        """
        self.__on_speak_finished_flag = True

    def on_speak_error(self, error_msg: str):
        """
        当语音合成出错时
        :return:
        """
        self.__on_speak_error_flag = True

    def speak(self, msg: str):
        """
        开始语音合成
        :param msg:
        :return:
        """
        rospy.loginfo('开始语音合成: %s', msg)
        self.__rpc_node.call('phone', 'speak', [msg])

    def cb(self, goal: SpeakGoal):
        rospy.loginfo('收到语音合成请求: %s', goal.text)
        self.speak(goal.text)
        self.__on_speak_finished_flag = False
        self.__on_speak_error_flag = False

        listen_rate = rospy.Rate(10)

        # 当speak完成或出错时结束该循环
        while not (self.__on_speak_finished_flag or self.__on_speak_error_flag):
            listen_rate.sleep()

        if self.__on_speak_finished_flag:
            rospy.loginfo('语音合成结束')
            result = SpeakResult()
            result.hasError = False
            result.errorMassage = ''
            self.__server.set_succeeded(result)

        if self.__on_speak_error_flag:
            rospy.logerr('语音合成出错: %s', self.__speak_error_msg)
            result = SpeakResult()
            result.hasError = True
            result.errorMassage = self.__speak_error_msg
            self.__server.set_succeeded(result)


MySpeakAction(phone)
rate = rospy.Rate(100)

try:
    while not rospy.is_shutdown():
        rate.sleep()
        phone.loop()
except KeyboardInterrupt:
    rospy.loginfo('ROS语音节点退出')
