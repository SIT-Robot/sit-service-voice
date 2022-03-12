from robot_voice.msg import Person, Subjects
from rospy.topics import Publisher
from .config import *
from .recognizer import recording
from sound_play.libsoundplay import SoundClient
from sound_play.msg import SoundRequest
import rospy
import os
import sys
from std_msgs.msg import String