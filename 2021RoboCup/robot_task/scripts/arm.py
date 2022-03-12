import rospy
from robotic_arm.srv import *

get_addr_client = rospy.ServiceProxy('GetAddr',GetAddr)
get_status_client = rospy.ServiceProxy('GetStatus',GetStatus)
lock_m1_client = rospy.ServiceProxy('LockM1',LockM1)
unlock_m1_client = rospy.ServiceProxy('UnlockM1',UnlockM1)
handup_m1_client = rospy.ServiceProxy('HandUpM1',HandUpM1)
up_down_client = rospy.ServiceProxy('UpDown',UpDown)
scratch_client = rospy.ServiceProxy('ScratchAsync',ScratchAsync)
deliver_client = rospy.ServiceProxy('Deliver',Deliver)

# 等待服务就绪
rospy.wait_for_service()

def get_addr():
    req = GetAddrRequest()
    resp = get_addr_client.call(req)
    return resp.addr


def get_status():
    req = GetStatusRequest()
    resp:GetStatusResponse = get_status_client.call(req)
    return resp.m1,resp.m2,resp.servo
    

def lock_m1(pwm):
    req = LockM1Request()
    req.pwm = pwm
    lock_m1_client.call(req)


def unlock_m1():
    req = UnlockM1Request()
    unlock_m1_client.call(req)

def handup_m1(angle,shift):
    req = HandUpM1Request()
    req.angle = angle
    req.shift = shift
    resp:HandUpM1Response = handup_m1_client.call(req)
    return resp.finalAngle


def up_down(distance,shift):
    req = UpDownRequest()
    req.distance = distance
    req.shift = shift
    resp:UpDownResponse = up_down_client.call(req)
    return resp.finalDistance


def scratch(servo):
    req = ScratchAsyncRequest()
    req.servo = servo
    resp: ScratchAsyncResponse = scratch_client.call(req)


def deliver(x,y):
    req = DeliverRequest()
    req.x = x
    req.y = y
    deliver_client.call(req)
