

import rospy
rospy.init_node('move_test')

from std_msgs.msg import *
from config import voice_cfg
import sound
import movement
from config import locations_cfg
from os import name, setxattr
import threading


def spin_async():
    try:
        rospy.spin()
    except KeyboardInterrupt:
        rospy.signal_shutdown()


threading.Thread(target=spin_async)

rospy.sleep(1)


#import vision


class Person:
    name: str
    sex: str
    drinking: str
    age: Int32


people1 = Person()
people2 = Person()
master = Person()
first_location: str = None


def move(location: str):
    goal = {'living room': locations_cfg.living_room_goal,
            'bedroom': locations_cfg.bedroom_goal,
            'kitchen': locations_cfg.kitchen_goal,
            'dining': locations_cfg.dining_room_goal,
            'dining table':locations_cfg.dining_table_goal,
             'desk':locations_cfg.desk_goal,
             'side':locations_cfg.side_table_goal,
             'bed':locations_cfg.bed_goal,
             'cupboard':locations_cfg.cupboard_goal,
             'dishwasher':locations_cfg.dishwasher_goal,
             'sink':locations_cfg.sink_goal,
             'counter':locations_cfg.counter_goal,
             'storage':locations_cfg.storage_table_goal,
             'bookcase':locations_cfg.bookcase,
             'endtable':locations_cfg.endtable_goal,
             'couch':locations_cfg.couch_goal,
             'exit':locations_cfg.exit_goal,
             'entrance':locations_cfg.entrance_goal,
            }[location]
    movement.goto_pose(goal)
    rospy.loginfo('导航到%s,目标位姿\n%s', location, str(goal))
    sound.say("have arrived,I will back living room")
    if location == 'living room':
        return
    else:
        move('living room')


def ob_confirm(L: str):
    data = L.split(" ")
    for w in data:
        if w in voice_cfg.objects:
            return True


def lo_confirm(L: str):

    data = L.split(" ")
    for w in data:
        if w in voice_cfg.location:
            return True


# 对话匹配
def conversation(data):
    answer = String()
    Asking = data
    words = Asking.split(" ")  # 将输出的文本以空格分开
    for w in words:
        if(w in voice_cfg.HI):
            sound.say("Hi,What's your name?")
        if(w in voice_cfg.Name):
            people1.name = w
            sound.say("ok,fine "+w+" what do you want drink")
            rospy.loginfo("people name:"+people1.name)

        if (w in voice_cfg.location and not ob_confirm(Asking)):
            if(w == "table"):
                sound.say("Ok,I will go to dining table.")
                move("dining table")
            else:
                sound.say("Ok,I will go to "+ w)
                move(w)

        if(w in voice_cfg.drinking):
            people1.drink = w
            sound.say("Ok,I already know you like "+w)
            rospy.loginfo("people want drink:"+people1.drink)

        if(w in voice_cfg.Myname):
            sound.say("S I T Robot.")

        if(w == "entrance"):
            move("entrance")
            sound.say("ok i will go to entrance")
            break

        if(w in voice_cfg.room and ob_confirm(Asking)):
            room = w
            for s in words:
                if s in voice_cfg.objects:
                    if(w ==" living" or w == "leaving"):
                        sound.say("ok i will go to  living "+room +
                              " and take "+s+" for you.")
                        move("living room")
                    else:
                        sound.say("ok i will go to "+room +
                              " and take "+s+" for you.")
                        move(room)
                    # 拿取物品  take(s)

        if (w in voice_cfg.room and not ob_confirm(Asking)):
            if(w == "living" or w =="leaving"):
                sound.say("ok i will go to  living room")
                move("living room")
            else:
                sound.say("ok i will go to "+w)
                move(w)
        if(w in voice_cfg.objects and lo_confirm(Asking)):
            objects = w
            for s in words:
                if s in voice_cfg.location:
                    sound.say("ok i will go to "+s +
                              " and take "+objects+" for you.")
                    move(s)
                    # 拿取物品  take(s)

        if (w in voice_cfg.objects and not lo_confirm(Asking)):
            sound.say("ok i will go to take "+w)
            move(room)

        if(w == "out"):
            sound.say("ok i will go out.")
            move("exit")
        # if(w == "stop"):
        #     move("stop")
        #     sound.say("OK, i wait you start again.")
        if(w in voice_cfg.location and ob_confirm(Asking)):
            lo = w
            for s in words:
                if s in voice_cfg.objects:
                    if(lo == "book"):
                        lo = "bookcase"
                        sound.say("ok i will take "+s+" for you from "+lo)
                        move(lo)
                    else:
                        sound.say("ok i will take "+s+" for you from "+lo)
                        move(lo)
                    # 拿取物品  take(lo)
        if (w in voice_cfg.objects and not objects(Asking)):
            first_location = w
            sound.say("Can you talk again What do you want to take?")
        if(w in voice_cfg.objects and not first_location == None):
            sound.say("ok i will take "+w+" for you from "+first_location)
            move(first_location)
        if(w == "follow"):
            sound.say("Ok i will follow you.")
            # 给你跟随指令



movement.goto_pose(locations_cfg.living_room_goal)

while not rospy.is_shutdown():
    heard_text = sound.recognize(4)
    rospy.loginfo(heard_text)
    conversation(heard_text)
