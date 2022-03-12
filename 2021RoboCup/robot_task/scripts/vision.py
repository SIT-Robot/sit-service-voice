import rospy
from std_msgs.msg import String
import json

detected_obj = {}

def obj_cb(detected_result:String):
    global detected_obj
    # 不断更新检测到的目标
    detected_obj = json.loads(detected_result.data)


def get_detected_objs():
    rospy.loginfo(detected_obj)
    return detected_obj

rospy.Subscriber('/vision_obj',String,callback=obj_cb)



