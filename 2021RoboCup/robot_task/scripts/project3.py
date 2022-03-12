import rospy
rospy.init_node('move_test')

from std_msgs.msg import *
from config import voice_cfg
import sound
#import jimyag_interface
import movement
from config import locations_cfg
from os import name, setxattr
import threading
from sensor_msgs.msg import CompressedImage


def move(location: str):
    goal = {'living room': locations_cfg.living_room_goal,
            # 'bedroom': locations_cfg.bedroom_goal,
            # 'kitchen': locations_cfg.kitchen_goal,
            # 'dining': locations_cfg.dining_room_goal,
            # 'dining table':locations_cfg.dining_table_goal,
            #  'desk':locations_cfg.desk_goal,
            #  'side':locations_cfg.side_table_goal,
            #  'bed':locations_cfg.bed_goal,
            #  'cupboard':locations_cfg.cupboard_goal,
            #  'dishwasher':locations_cfg.dishwasher_goal,
            #  'sink':locations_cfg.sink_goal,
            #  'counter':locations_cfg.counter_goal,
            #  'storage':locations_cfg.storage_table_goal,
            #  'bookcase':locations_cfg.bookcase,
             'endtable':locations_cfg.endtable_goal,
            #  'couch':locations_cfg.couch_goal,
            #  'exit':locations_cfg.exit_goal,
             'entrance':locations_cfg.entrance_goal,
            }[location]
    #movement.goto_pose(goal)
    rospy.loginfo('导航到%s', location)
    if location == 'living room':
        return
    else:
        #move('living room')
        pass


def spin_async():
    try:
        rospy.spin()
    except KeyboardInterrupt:
        rospy.signal_shutdown()


threading.Thread(target=spin_async)

rospy.sleep(1)

import sound 

class Person:
    name: str = None
    sex: str = None
    drinking: str= None
    age: int= None
    cloth_color:str = None
    hair_color:str = None
    


guest1 = Person()
guest2 = Person()
tmp_gest = Person()
master = Person()
first_location: str = None

tmp_gest.drinking =None
tmp_gest.name =None
tmp_gest.age =None
tmp_gest.cloth_color =None
tmp_gest.hair_color =None
tmp_gest.sex =None

def c_name(data:str):
    if(not data == None):
        data = data.split(" ")
        for w in data:
            if w in voice_cfg.Name:
                tmp_gest.name = w
                return True

def c_drink(data:str):
    if(not data == None):
        data = data.split(" ")
        for w in data:
            if w in voice_cfg.drinking:
                tmp_gest.drinking = w
                return True
    

def confirm(data:str):
    if(not data == None):
        data = data.split(" ")
        for w in data:
            if(w == "right" or w == "Right" or w == "Yes" or w == "yes"):
                return True
            elif( w== "No" or w == "no"):
                return False

count:Int32 = 0
introduce_count:Int32 =0




def reception(data):
    if(cv_face_detect()): #如果检测到有人开始信息询问

        if(c_name(data)):
            sound.say("ok fine "+ name +"Right?")
        if(confirm(data)):
            sound.say("Ok,i get it. What do you want to drink?")
            if(count == 0):
                guest1 = tmp_gest
                get_person_features(guest1.name)
                count+=1
                sound.say("Ok, please follow me.")
            else:
                guest2 = tmp_gest
                get_person_features(guest2.name)
        if(c_drink(data)):
            sound.say("ok fine "+ tmp_gest.drinking +"Right?")
    move("endtable")


def Introduce(data):
    if(introduce_count == 0):
        if(not guest1.name==None):
            sound.say("ok "+ guest1.name +"sit down please")
            #转向客人
            sound.say("Hi "+ guest1.name +"this is "+get_person_name())
            #转向主人
            sound.say("hi "+ master.name +"this is "+guest1.name)
            if(guest1.sex == "femal"):
                sound.say("She like drinking "+guest1.drinking)
            else:
                sound.say("He like drinking "+guest1.drinking)
            sound.say("Ok, i will go to reception the second guest")
            move("entonce")
    else:
        if(not guest1.name== None):
            sound.say("ok "+ guest2.name +"sit down please")
            #转向客人,向客人介绍主人
            sound.say("Hi "+ guest2.name +"this is "+get_person_name())
            #转向主人，向主人介绍第二个客人
            sound.say("hi "+ master.name +"this is "+guest2.name)
            if(guest1.sex == "femal"):
                sound.say("She like drinking "+guest1.drinking)
            else:
                sound.say("He like drinking "+guest1.drinking)
            #转向第一个客人，向第一个客人介绍第二个客人
            sound.say("Hi "+ guest1.name +"this is "+guest2.name)
            if(guest1.sex == "femal"):
                sound.say("She like drinking "+guest2.drinking)
            else:
                sound.say("He like drinking "+guest2.drinking)
            #转向第二个客人，向第二个客人介绍主人
            sound.say("Hi "+ guest2.name +"this is "+master.name)
            if(guest1.sex == "femal"):
                sound.say("She like drinking "+master.drinking)
            else:
                sound.say("He like drinking "+master.drinking)
            #转向第二个客人，向第二个客人介绍第一个客人
            sound.say("Hi "+ guest2.name +"this is "+guest1.name)
            if(guest1.sex == "femal"):
                sound.say("She like drinking "+guest1.drinking)
            else:
                sound.say("He like drinking "+guest1.drinking)

import ji
while not rospy.is_shutdown():
    ji.cv_face_detect()
    sound.say("Hi,dear guest what's your name")
    heard_text = sound.recognize(4)
    reception(heard_text)
    Introduce(heard_text)