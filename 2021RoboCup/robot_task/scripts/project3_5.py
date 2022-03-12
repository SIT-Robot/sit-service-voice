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

def spin_async():
    try:
        rospy.spin()
    except KeyboardInterrupt:
        rospy.signal_shutdown()


threading.Thread(target=spin_async)

rospy.sleep(1)

import sound 

movement.goto_pose(locations_cfg.entrance_goal)

class Person:
    name: str = None
    drinking: str= None
    sex: str = 'male'
    age: int = 21
    cloth_color: str = 'green'
    hair_color: str = 'black'

co:bool=True
guest1 = Person()
guest2 = Person()
tmp_gest = Person()
master = Person()
master.name = "Alex"
master.drinking ="sprite"
first_location: str = None

tmp_gest.drinking =None
tmp_gest.name =None
tmp_gest.age =None
tmp_gest.cloth_color =None
tmp_gest.hair_color =None
tmp_gest.sex =None

def c_name(data:str):
    global tmp_gest
    Asking = data
    if(not data == None):
        data = data.split(" ")
        for w in data:
            if w in voice_cfg.Name:
                tmp_gest.name = w
                return True

def c_drink(data:str):
    global tmp_gest
    Asking = data
    if(not data == None):
        data = Asking.split(" ")
        for w in data:
            if w in voice_cfg.drinking:
                tmp_gest.drinking = w
                return True

def confirm(data:str):
    global tmp_gest
    Asking = data
    if(not data == None):
        data = Asking.split(" ")
        for w in data:
            if(w == "right" or w == "Right" or w == "Yes" or w == "yes"):
                return True
            elif( w== "No" or w == "no"):
                return False


count:int = 0
introduce_count:int =0

def get_person_features(name:str):
    pass


def conversation(data:str):
    global count,co
    answer = String()
    Asking = data
    if(Asking is not None):
        rospy.loginfo("ok")
        words = Asking.split(" ")  # 将输出的文本以空格分开
        for w in words:
            if(w in voice_cfg.HI):
                sound.say("Hi,What's your name?")
            if(w in voice_cfg.Name):
                guest1.name = w
                sound.say("ok,fine "+w+" what do you want drink")
                rospy.loginfo("people name:"+guest1.name)
                if(count>=1):
                    guest2.name=w
                    rospy.loginfo("people name:"+guest2.name)

            if(w in voice_cfg.drinking):
                guest1.drink = w
                sound.say("Ok,I already know you like "+w)
                rospy.loginfo("people want drink:"+guest1.drink)
                co=False
                if(count>=1):
                    guest2.name=w
                    rospy.loginfo("people want drink:"+guest2.drink)
                count+1
        



def Introduce(data):
    if(introduce_count == 1):
        if(not guest1.name==None):
            sound.say("ok "+ guest1.name +"sit down please")
            #转向客人
            sound.say("Hi "+ guest1.name +"this is "+'Alex she like drink sprite')
            #转向主人
            sound.say("hi "+ master.name +"this is "+guest1.name)
            if(guest1.sex == "female"):
                sound.say("She like drinking "+guest1.drinking)
            else:
                sound.say("He like drinking "+guest1.drinking)
            sound.say("Ok, i will go to reception the second guest")
    else:
        if(not guest1.name== None):
            sound.say("ok "+ guest2.name +"sit down please")
            #转向客人,向客人介绍主人
            sound.say("Hi "+ guest2.name +"this is "+master.name)
            #转向主人，向主人介绍第二个客人
            sound.say("hi "+ master.name +"this is "+guest2.name)
            if(guest1.sex == "femal"):
                sound.say("She like drinking "+guest1.drinking)
            else:
                sound.say("He like drinking "+guest1.drinking)
            #转向第一个客人，向第一个客人介绍第二个客人
            sound.say("Hi "+ guest1.name +"this is "+guest2.name)
            if(guest1.sex == "female"):
                sound.say("She like drinking "+guest2.drinking)
            else:
                sound.say("He like drinking "+guest2.drinking)
            #转向第二个客人，向第二个客人介绍主人
            sound.say("Hi "+ guest2.name +"this is "+master.name)
            if(guest1.sex == "female"):
                sound.say("She like drinking "+master.drinking)
            else:
                sound.say("He like drinking "+master.drinking)
            #转向第二个客人，向第二个客人介绍第一个客人
            sound.say("Hi "+ guest2.name +"this is "+guest1.name)
            if(guest1.sex == "female"):
                sound.say("She like drinking "+guest1.drinking)
            else:
                sound.say("He like drinking "+guest1.drinking)



movement.goto_pose(locations_cfg.entrance_goal)
sound.say("I will go to entrance to recipetion the first guest.")
rospy.loginfo("去入口")

while not rospy.is_shutdown():
    sound.say("Hi,dear guest what's your name")
    while True:
        heard = sound.recognize(4)
        conversation(heard)
        if not co:
            introduce_count+=1
            break
    rospy.loginfo("去桌子")
    sound.say("I will go to livingroom") 
    movement.goto_pose(locations_cfg.endtable_goal)
    Introduce()
    co =False