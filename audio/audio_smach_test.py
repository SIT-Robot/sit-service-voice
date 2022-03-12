import rospy
import smach
import smach_ros
import sys

import actionlib
from sit_phone_audio_msgs.msg import *


class Speak(smach.State):
    """
    语音合成状态
    """

    def __init__(self):
        """
        说完的结果有如下几种
        1. 成功说完
        2. 语音合成出错
        """
        super(Speak, self).__init__(outcomes=['success', 'error'],
                                    input_keys=['text'])
        self.speak_action = actionlib.SimpleActionClient('/speak', SpeakAction)
        self.speak_action.wait_for_server()

    def execute(self, ud: smach.user_data.Remapper):
        rospy.loginfo("语音合成状态开始执行")
        speak_goal = SpeakGoal()
        speak_goal.text = ud['text']
        self.speak_action.send_goal_and_wait(speak_goal)
        result: SpeakResult = self.speak_action.get_result()
        if result.hasError:
            print(result.errorMassage)
            return 'error'
        return 'success'


class Hear(smach.State):
    def __init__(self):
        """
        听完的结果有如下几种
        1. 退出状态机程序
        2. 打印输出听到的话
        3. 重复播放听到的话
        4. 识别出错
        5. 导航
        """
        super(Hear, self).__init__(outcomes=['exit', 'print', 'speak', 'error', 'nav'],
                                   output_keys=['text', 'position'])
        self.hear_action = actionlib.SimpleActionClient('/hear', HearAction)
        self.hear_action.wait_for_server()

    def execute(self, ud):
        rospy.loginfo('语音识别状态开始执行')
        hear_goal = HearGoal()
        self.hear_action.send_goal_and_wait(hear_goal)
        result: HearResult = self.hear_action.get_result()
        if result.hasError:
            return 'error'
        hear_text = result.text
        ud['text'] = hear_text
        if '退出' in hear_text:
            return 'exit'
        if '打印' in hear_text:
            return 'print'
        if '导航' in hear_text:
            if '厨房' in hear_text:
                ud['position'] = '厨房'
            else:
                ud['position'] = '未知'
            return 'nav'
        return 'speak'


class Print(smach.State):
    def __init__(self):
        super(Print, self).__init__(outcomes=['success'],
                                    input_keys=['text'])

    def execute(self, ud):
        rospy.loginfo('打印状态开始执行')
        print(ud['text'])
        return 'success'


class Nav(smach.State):
    def __init__(self):
        super(Nav, self).__init__(outcomes=['success'],
                                  input_keys=['position'])

    def execute(self, ud):
        position = ud['position']
        rospy.loginfo('导航到目的地：%s', position)
        for i in range(0, 101):
            rospy.sleep(0.1)
            rospy.loginfo('导航进度: %d', i)
        rospy.loginfo('导航结束')
        return 'success'


def main():
    rospy.init_node('my_smach_audio_test', sys.argv)

    # 该状态机的归宿为exit或者error
    sm = smach.StateMachine(outcomes=['exit', 'error'])

    with sm:
        smach.StateMachine.add('Hear', Hear(), transitions={'exit': 'exit',
                                                            'print': 'Print',
                                                            'speak': 'Speak',
                                                            'error': 'Hear',
                                                            'nav': 'Nav'})
        smach.StateMachine.add('Speak', Speak(), transitions={'success': 'Hear',
                                                              'error': 'Hear'})

        smach.StateMachine.add('Print', Print(), transitions={'success': 'Hear'})
        smach.StateMachine.add('Nav', Nav(), transitions={'success': 'Hear'})

        sis = smach_ros.IntrospectionServer('my_smach_audio_test_server', sm, '/SM_ROOT')
        sis.start()
        rospy.signal_shutdown(sm.execute())

    rospy.spin()
    sis.stop()


if __name__ == '__main__':
    main()
