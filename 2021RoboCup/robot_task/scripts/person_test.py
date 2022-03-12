from std_msgs.msg import String


import threading
import rospy
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import CompressedImage # 压缩后的图像的消息类型
import time
import pyrealsense2 as rs
import numpy as np 
import cv2 as cv
import base64
import json
from face_api import BaiduFace
from srv.srv import Person
from hair_cloths import *


# 保存人脸的照片
face_image= []
# 百度云人脸识别
baiduface = BaiduFace()
# cv_bridge
rgb_bridge = CvBridge()
depth_intrinsics:rs.intrinsics = rs.intrinsics()


rospy.init_node("vision_obj")
rospy.loginfo("vision_person的测试")






def set_depth_intrinsics():
    depth_intrinsics.fx = 919.51123046875
    depth_intrinsics.fy = 919.9594116210938
    depth_intrinsics.ppx = 641.1727294921875
    depth_intrinsics.ppy = 373.4692687988281
    depth_intrinsics.model:rs.pyrealsense2.distortion = rs.pyrealsense2.distortion.inverse_brown_conrady
    depth_intrinsics.coeffs = [0.0, 0.0, 0.0, 0.0, 0.0]
    depth_intrinsics.height = 720
    depth_intrinsics.width = 1280

# 更新相机内参
set_depth_intrinsics()


# opencv格式图片转base64
def cv_image_to_base64(cv_image:np.ndarray):
    base64_image = base64.b64decode(cv_image)
    return base64_image


# base64图片转opencv格式
def base64_to_cv_image(base64_image:base64):
    image_b64decode = base64.b64decode(base64_image)
    img_arr = np.fromstring(image_b64decode,np.uint8)
    img_cv = cv.imdecode(img_arr, cv2.COLOR_BGR2RGB)
    return img_cv


def cv_face_detect(image):
    face_detecter = cv.CascadeClassifier(r'/home/jimyag/Code/ros/demo01_ws/src/vision/scripts/data/haarcascades/haarcascade_frontalface_default.xml')
    faces = face_detecter.detectMultiScale(image=image,scaleFactor=1.1, minNeighbors=5)
    if faces:
        return True
    else :
        return False


# 处理获取到的彩色压缩图
def process_image(compressed_image:CompressedImage):
    global face_image
    try:
        # 使用cvBridge转为cv2可以使用的数据格式 
        rgb_img = rgb_bridge.compressed_imgmsg_to_cv2(compressed_image, 'bgr8')
        rgb_img = rgb_img[:,400:880]
        face_image = rgb_img
    # 捕获异常退出的异常
    except CvBridgeError as e:
        print(e)
        rospy.loginfo(type(compressed_image))

def g_area(points: np.array):
    point_num = len(points)
    if point_num < 3:
        return 0.0
    s = points[0][1] * (points[point_num - 1][0] - points[1][0])
    # for i in range(point_num): # (int i = 1 i < point_num ++i):
    for i in range(1, point_num): 
        s += points[i][1] * (points[i - 1][0] - points[(i + 1) % point_num][0])
    return abs(s / 2.0)


color_dist = {'red': {'Lower': np.array([0, 60, 60]), 'Upper': np.array([6, 255, 255])},
              'blue': {'Lower': np.array([100, 80, 46]), 'Upper': np.array([124, 255, 255])},
              'green': {'Lower': np.array([35, 43, 35]), 'Upper': np.array([90, 255, 255])},
              'black': {'Lower': np.array([0, 0, 0]), 'Upper': np.array([180, 255, 46])},
              'white': {'Lower': np.array([0, 0, 221]), 'Upper': np.array([180, 30, 255])},
              'orange': {'Lower': np.array([11, 43, 46]), 'Upper': np.array([25, 255, 255])},
              'yellow': {'Lower': np.array([26, 43, 46]), 'Upper': np.array([34, 255, 255])},
              'cyan': {'Lower': np.array([78, 43, 46]), 'Upper': np.array([99, 255, 255])},
              'purple': {'Lower': np.array([125, 43, 46]), 'Upper': np.array([155, 255, 255])}
              }


def get_hair_image(x: int, y: int, w: int, h: int, image: np.array):
    return image[y - 5:y, x:x + w]


def get_clothes_image(x: int, y: int, w: int, h: int, image: np.array):
    return image[y:y+20, x:x + w]


def get_color(image: np.array):
    frame = image
    gs_frame = cv.GaussianBlur(frame, (5, 5), 0)  # 高斯模糊
    hsv = cv.cvtColor(gs_frame, cv.COLOR_BGR2HSV)  # 转化成HSV图像
    erode_hsv = cv.erode(hsv, None, iterations=2)  # 腐蚀 粗的变细
    max_color = ''
    max_area = 0.0
    for key, value in color_dist.items():
        inRange_hsv = cv.inRange(erode_hsv, color_dist[key]['Lower'], color_dist[key]['Upper'])
        cnts = cv.findContours(inRange_hsv.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        if cnts:
            c = max(cnts, key=cv.contourArea)
            rect = cv.minAreaRect(c)
            box = cv.boxPoints(rect)
            # cv2.drawContours(frame, [np.int0(box)], -1, (0, 255, 255), 2)
            # cv2.imshow('camera', frame)
            # cv2.waitKey(0)
            if g_area(box) > max_area:
                max_color = key
                max_area = g_area(box)
    return max_color




def shoot(name:String):
    global face_image
    save_images_path = name+time.strftime("%m-%d-%H-%M-%S", time.localtime())+'.jpg'
    print(save_images_path)
    cv.imwrite(save_images_path, face_image)



def process_call(name:String):
    person_info = {}
    person_info['name'] = name
    global face_image
    flag = True
    shoot()
    while flag:
        user_image = face_image
        b64_user_image = cv_image_to_base64(user_image)
        result= baiduface.add_user(b64_user_image,name)
        if result['error_code']==0:
            flag =False
            user_image_info = baiduface.image_info(b64_user_image)
            if user_image_info['error_code']==0:
                person_info['age'] = user_image_info['result']['face_kist'][0]['age']
                person_info['gender'] = user_image_info['result']['face_kist'][0]['gender']
                x= int(user_image_info['result']['face_kist'][0]['location']['left'])
                y= int(user_image_info['result']['face_kist'][0]['location']['top'])
                w= int(user_image_info['result']['face_kist'][0]['location']['width'])
                h= int(user_image_info['result']['face_kist'][0]['location']['height'])
                clothes_image = get_clothes_image(x,y,w,h,base64_to_cv_image(base64_to_cv_image))
                hair_image = get_hair_image(x,y,w,h,base64_to_cv_image(base64_to_cv_image))
                person_info['hair_color'] = get_color(hair_image)
                person_info['clothes_color'] = get_color(clothes_image)
                person_info_json = json.dumps(person_info)
                response = Person()
                response.person = person_info_json
                return response



# 发布人信息
# person_pub = rospy.Publisher('vision_person', Person,queue_size=1)
server = rospy.Service("vision_obj",Person,process_call)
rgb_image_sub = rospy.Subscriber('/camera/color/image_raw/compressed', CompressedImage, process_image)


# threading.Thread(target=ros_spin)
rospy.spin()

