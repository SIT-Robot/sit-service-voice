from sit_audio_recognition_msgs.msg import *
import actionlib
import rospy


class Test:
    def __init__(self):
        self.speak_action = actionlib.SimpleActionClient('/speak', SpeakAction)
        self.speak_action.wait_for_server()

        self.hear_action = actionlib.SimpleActionClient('/hear', HearAction)
        self.hear_action.wait_for_server()

    def on_speak_finished(self,a,b):
        # 说完就听
        self.hear()

    def on_hear_finished(self, msg: str,hear_result:HearResult):
        # 听完就说
        self.speak(hear_result.text)

    def speak(self, msg: str):
        speak_goal = SpeakGoal()
        speak_goal.text = msg
        self.speak_action.send_goal(speak_goal, self.on_speak_finished)

    def hear(self):
        hear_goal = HearGoal()
        self.hear_action.send_goal(hear_goal,self.on_hear_finished)


rospy.init_node('ros_test')
test = Test()
test.hear()

rate = rospy.Rate(100)
while not rospy.is_shutdown():
    rate.sleep()
