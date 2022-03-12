import rospy
from std_msgs.msg import *
import actionlib
from robot_voice.msg import *

say_pub = rospy.Publisher('Answer', String, queue_size=5)

# 创建客户端对象
client = actionlib.SimpleActionClient("recording", recognizerAction)

rospy.loginfo('等待连接语音识别服务...')
client.wait_for_server()
rospy.loginfo('语音识别服务连接成功')

# 说话
def say(text: str):
    rospy.loginfo('say: %s',text)
    msg = String()
    msg.data = text
    say_pub.publish(msg)


# 识别一句话，识别t秒
def recognize(t) -> str:
    rospy.loginfo('recoding...')
    goal = recognizerGoal()
    goal.seconds = t
    client.send_goal_and_wait(goal)
    result: recognizerResult = client.get_result()
    heared_text = result.voice_txt
    rospy.loginfo('I heared:%s',heared_text)
    return heared_text

def recongnize_async(t):
    rospy.loginfo('recoding...')
    goal = recognizerGoal()
    goal.seconds = t
    client.send_goal(goal)

angle = 0


def angle_cb(angle_msg: Float32):
    global angle
    angle = angle_msg.data


angle_sub = rospy.Subscriber('voice_angle', Float32,)


def get_angle():
    return angle
