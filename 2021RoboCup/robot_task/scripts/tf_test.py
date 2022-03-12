import rospy
import tf.transformations
from geometry_msgs.msg import *
import tf2_ros

rospy.init_node('tf_test')

buffer = tf2_ros.Buffer()
listener = tf2_ros.TransformListener(buffer)

dx = 1
dy = 0
dth = 0

# 新建一个相对于底盘的坐标点
ps_base_link = PointStamped()
ps_base_link.header.frame_id='/base_link'
ps_base_link.header.stamp = rospy.Time.now()
ps_base_link.point.x = dx
ps_base_link.point.y = dy
ps_base_link.point.z = 0
# 坐标变换为地图中的坐标
ps_map = PointStamped()
print(buffer.transform(ps_base_link,'/map'))
# 获取当前机器人的位姿
pose:Pose = get_current_pose()
# 更新下一步机器人应达到的坐标
pose.position = ps_map.point

# 获取当前的偏航角
_,_,current_yaw = tf.transformations.euler_from_quaternion([pose.orientation.x,
                    pose.orientation.y,pose.orientation.z,pose.orientation.w])
# 转换为四元数
tf_qut_list = tf.transformations.quaternion_from_euler(0,0,current_yaw+dth)
# 更新目标偏航角
pose.orientation.x = tf_qut_list[0]
pose.orientation.y = tf_qut_list[1]
pose.orientation.z = tf_qut_list[2]
pose.orientation.w = tf_qut_list[3]
