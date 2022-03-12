import rospy
import actionlib
from config import locations_cfg
from move_base_msgs.msg import *
from rospy.topics import Subscriber
import tf
import tf.transformations
from geometry_msgs.msg import PoseWithCovarianceStamped
from tf2_geometry_msgs import PointStamped
import tf2_ros

current_pose = None

# 机器人位姿的更新回调
def current_pose_cb(pose_with_cs:PoseWithCovarianceStamped):
    global current_pose
    current_pose = pose_with_cs.pose.pose
    rospy.loginfo(str(current_pose))

Subscriber('/amcl_pose',PoseWithCovarianceStamped,current_pose_cb)

move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
rospy.loginfo("Waiting for move_base action server...")  

# 60s等待时间限制  
move_base.wait_for_server(rospy.Duration(60))  
rospy.loginfo("Connected to move base server")  

from geometry_msgs.msg import Pose,Point,Quaternion

# buffer = tf2_ros.Buffer()
# listener = tf2_ros.TransformListener(buffer)

def goto_pos(x,y,yaw):
    """
    运动到指定的位姿
    """
    rospy.loginfo("Going to: [%f,%f,%f]",x,y,yaw)
    goal = MoveBaseGoal()
    goal.target_pose.pose = Pose(Point(x,y,0),tf.transformations.quaternion_from_euler(yaw))
    goal.target_pose.header.frame_id = 'map'
    goal.target_pose.header.stamp = rospy.Time.now()

    move_base.send_goal_and_wait(goal)


def goto_pose(pose:Pose):
    """
    运动到目标点
    """
    #rospy.loginfo("Going to: " + location)
    goal = MoveBaseGoal()

    goal.target_pose.header.frame_id = 'map'
    goal.target_pose.header.stamp = rospy.Time.now()

    goal.target_pose.pose = pose

    move_base.send_goal_and_wait(goal,rospy.Duration(120,0))
    rospy.loginfo('Nav Done')


def get_current_pose():
    """
    获取机器人当前的位姿
    """
    return current_pose


# def move(dx:float,dy:float,dth):
#     """
#     移动的距离
#     """
#     # 新建一个相对于底盘的坐标点
#     ps_base_link = PointStamped()
#     ps_base_link.header.frame_id='base_link'
#     ps_base_link.header.stamp = rospy.Time.now()
#     ps_base_link.point.x = dx
#     ps_base_link.point.y = dy
#     ps_base_link.point.z = 0

#     # 坐标变换为地图中的坐标
#     ps_map = PointStamped()
#     print(buffer.transform(ps_base_link,'map',rospy.Duration(1)))

#     # 获取当前机器人的位姿
#     pose:Pose = get_current_pose()

#     # 更新下一步机器人应达到的坐标
#     pose.position = ps_map.point
    
#     # 获取当前的偏航角
#     _,_,current_yaw = tf.transformations.euler_from_quaternion([pose.orientation.x,
#                         pose.orientation.y,pose.orientation.z,pose.orientation.w])
#     # 转换为四元数
#     tf_qut_list = tf.transformations.quaternion_from_euler(0,0,current_yaw+dth)

#     # 更新目标偏航角
#     pose.orientation.x = tf_qut_list[0]
#     pose.orientation.y = tf_qut_list[1]
#     pose.orientation.z = tf_qut_list[2]
#     pose.orientation.w = tf_qut_list[3]
    
#     # 现在，只需要导航机器人到目标的位姿
#     goto_pose(pose)

