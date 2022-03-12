import sound
from config import voice_cfg
from std_msgs.msg import *

class command:
    room:str = None
    location:str = None
    subject:str = None
    people:str = None
    Action:str = None

first_command = command()
second_comand = command()
Third_command = command()
commands[3] = command()

room:str = None
location:str = None
subject:str = None
name:str = None
dringk:str = None
Action:str = None

def c_room(data:str):
    words = data.split(" ")
    for w in words:
        if w in voice_cfg.room:
            room = w
            return True

def c_location(data:str):
    words = data.split(" ")
    for w in words:
        if w in voice_cfg.location:
            location = w
            return True

def c_subjects(data:str):
    words = data.split(" ")
    for w in words:
        if w in voice_cfg.objects:
            object = w
            return True

def c_drink(data:str):
    words = data.split(" ")
    for w in words:
        if w in voice_cfg.drinking:
            dringk=w
            return True

def c_name(data:str):
    words = data.split(" ")
    for w in words:
        if w in voice_cfg.Name:
            return True

def c_right(data:str):
    words = data.split(" ")
    for w in words:
        if w == "right" or w=="Yes":
            return True


def get_commands(data):
    count:Int32 = 0
    answer = String()
    Asking = data
    sound.say("The first command is "+Asking+" right?")
    if(c_drink):
        pass
    if(c_location(Asking) and c_subjects(Asking)):
        sound.say("Ok,I already get it,please speaker next command")
        v_confirm =sound.recognize(3)
        if(c_right(v_confirm)):
            count+1
            command[count].room=room
            command[count].location=location
            command[count].subject=subject
    if(c_name):
        pass
    if(c_room(Asking) and c_location(Asking) and c_subjects(Asking)):
        sound.say("The command is "+Asking+" right?")
        v_confirm =sound.recognize(3)
        if(c_right(v_confirm)):
            count+1
            command[count].room=room
            command[count].location=location
            command[count].subject=subject
    if(c_subjects):
        pass
       
