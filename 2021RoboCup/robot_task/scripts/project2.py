# 项目2 跟随

import rospy
import threading

rospy.init_node('project2')

import cmd_control

# #import sound
# import vision

rospy.loginfo('init finish')

rospy.sleep(1)

person_x = 0
person_distance = 0
person_empty = False

from std_msgs.msg import String
import json

def obj_cb(data:String):    #上位机
    global person_x,person_distance,person_empty
    # 不断更新检测到的目标
    detected_obj = json.loads(data.data)
    if 'person' in detected_obj.keys():
        rospy.loginfo(detected_obj['person'])
        person_x = detected_obj['person'][0]
        person_distance = detected_obj['person'][2]
        person_empty = True
    person_empty = False

rospy.Subscriber('/vision_obj',String,callback=obj_cb)


# 获取机器人旋转方向
def get_dir()->int: #下位机
    # -1 左转
    #  0 不转
    #  1 右转
    # 将x坐标区域划分为三块
    # (0,x1),(x1,x2),(x2,1280)
#    rospy.loginfo('%f %f',get_person_x(),get_person_distance())
    min_x = 0
    max_x = 1280

    x1 = 428
    x2 = 653

    if min_x < person_x and person_x < x1:
        return -1

    if x1 < person_x and person_x < x2:
        return 0

    if x2 < person_x and person_x < max_x:
        return 1


# 获取机器人是否应该前进
def get_go()->bool:
    # true 前进

    # 如果人的距离大于一米，那就前进
    rospy.loginfo('%f',person_distance)
    return person_distance > 1


# 机器人旋转
def go_dir(dir:int):
    if dir == -1:
        # 左转
        cmd_control.set_speed(0,0,0.3)
        rospy.loginfo('左转')
    elif dir == 0:
        # 停止
        cmd_control.stop()
        rospy.loginfo('停止')
    else:
        # 右转
        cmd_control.set_speed(0,0, -0.3)
        rospy.loginfo('右转')


# 机器人前进
def go_next():
    cmd_control.set_speed(0.1,0,0)

def stop():
    cmd_control.set_speed(0,0,0)

stop_flag = False


# heard_text = sound.recognize(4)

# # 语音识别线程
# def listen_thread():
#     global stop_flag
#     while not rospy.is_shutdown():
#         heard_text = sound.recognize(4)
#         if 'begin' in heard_text.lower():
#             stop_flag = False

#         if 'end' in heard_text.lower():
#             stop_flag = True

# threading.Thread(target=listen_thread)

def find_person():
    while not person_empty:
        cmd_control.set_speed(0,0,0.1)

    cmd_control.stop()

#sound.say('has arrived')



def timer1(t):
    rospy.loginfo('timer1')
    if not stop_flag and not rospy.is_shutdown():
        rospy.loginfo('running')
        if person_empty:  # 如果没人
            stop()
            return
            
        if get_go(): # 获取是否前进
            rospy.loginfo('前进')
            go_next() # 前进
        else:
            rospy.loginfo('前进停止')
            stop()
            return

        dir = get_dir() # 获取方向
        go_dir(dir) # 旋转

        rospy.sleep(0.5)


            
    if stop_flag:
        # 最后看运气能否导航回living room
        import movement
        from config import locations_cfg
        movement.goto_pose(locations_cfg.living_room_goal)

        sound.say('Has finished')

rospy.Timer(rospy.Duration(0.2),timer1)

try:
    rospy.spin()
except KeyboardInterrupt:
    rospy.signal_shutdown()