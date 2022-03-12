import rospy
from face_api import BaiduFace
from person_test import cv_image_to_base64
from cv_bridge import CvBridge, CvBridgeError
import cv2 as cv
# 保存人脸的照片
face_image= []
# cv_bridge
rgb_bridge = CvBridge()

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




# 获得这个人的基本特征  给名字
def get_person_features(name:str):
    rospy.init_node('test',anonymous=True)

    from srv.srv import Person
    client = rospy.ServiceProxy('/vision_obj',Person)
    client.wait_for_service()
    person_info =  client.call(name)
    print(person_info)
    return person_info




# 这个人是谁  当前的
def get_person_name():
    global face_image
    rgb_image_sub = rospy.Subscriber('/camera/color/image_raw/compressed', CompressedImage, process_image)
    baiduface = BaiduFace()
    b64_image = cv_image_to_base64(face_image)
    result_face = baiduface.search(b64_image)
    if result_face['erro_code']==0:
        return result_face['result']['user_list'][0]['user_id']
    else:
        return None



# 判断人脸质量


# 是否存在人脸 
def cv_face_detect():
    rgb_image_sub = rospy.Subscriber('/camera/color/image_raw/compressed', CompressedImage, process_image)
    face_detecter = cv.CascadeClassifier(r'/home/sit/code/catkin_ws/src/robot_task/scripts/haarcascade_frontalface_default.xml')
    faces = face_detecter.detectMultiScale(image=face_image,scaleFactor=1.1, minNeighbors=5)
    if faces:
        return True
    else :
        return False


