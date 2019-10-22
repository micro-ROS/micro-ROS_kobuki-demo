# Copyright (c) 2019 - for information on the respective copyright owner
# see the NOTICE file and/or the repository https://github.com/micro-ROS/micro-ROS_kobuki_demo.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import math

import rclpy
from rclpy.clock import Clock
from rclpy.node import Node
from rclpy.qos import QoSProfile
from tf2_msgs.msg import TFMessage
from geometry_msgs.msg import Point
from geometry_msgs.msg import Point32
from geometry_msgs.msg import Vector3
from geometry_msgs.msg import Quaternion
from geometry_msgs.msg import TransformStamped
from geometry_msgs.msg import Pose2D
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist
from nav_msgs.msg import Path

from rclpy.qos import QoSReliabilityPolicy

class AttitudeToVel(Node):

    def __init__(self):
        super().__init__('attitude_to_vel')

        self.lastPose = Point32()
        self.posearray = []

        self.sub_drone_att = self.create_subscription(Point32, "/drone/robot_pose", self.drone_att_callback, QoSProfile(reliability=QoSReliabilityPolicy.RMW_QOS_POLICY_RELIABILITY_BEST_EFFORT))
        self.sub_drone_att = self.create_subscription(Point32, "/drone/odometry", self.drone_odom_callback, QoSProfile(reliability=QoSReliabilityPolicy.RMW_QOS_POLICY_RELIABILITY_BEST_EFFORT))
        self.pub_tf = self.create_publisher(TFMessage, "/tf", QoSProfile(depth=10))
        self.pub_vel = self.create_publisher(Twist, "/cmd_vel", QoSProfile(depth=10))
        self.pub_posearray = self.create_publisher(Path, "/cmd_vel", QoSProfile(depth=10))

    def euler_to_quaternion(self, roll, pitch, yaw):

        qx = math.sin(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) - math.cos(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
        qy = math.cos(roll/2) * math.sin(pitch/2) * math.cos(yaw/2) + math.sin(roll/2) * math.cos(pitch/2) * math.sin(yaw/2)
        qz = math.cos(roll/2) * math.cos(pitch/2) * math.sin(yaw/2) - math.sin(roll/2) * math.sin(pitch/2) * math.cos(yaw/2)
        qw = math.cos(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) + math.sin(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
        return [qx, qy, qz, qw]

    
    def drone_att_callback(self, rcv):
        self.lastPose = rcv

        rcv.x *= math.pi/180.0
        rcv.y *= math.pi/180.0
        rcv.z *= math.pi/180.0

        # Publish pose for rviz
        msg = TransformStamped()
        msg.header.frame_id = "/map"
        msg.header.stamp = Clock().now().to_msg()
        msg.child_frame_id = "/base_footprint_drone_attitude"

        quat = self.euler_to_quaternion(rcv.x,rcv.y,rcv.z)
        orientation = Quaternion()
        orientation.x = quat[0]
        orientation.y = quat[1]
        orientation.z = quat[2]
        orientation.w = quat[3]
        msg.transform.rotation = orientation
        tfmsg = TFMessage()
        tfmsg.transforms = [msg]
        self.pub_tf.publish(tfmsg)

        # Publish velocity
        msg = Twist()
        msg.linear.x = rcv.x
        msg.angular.z = rcv.y
        self.pub_vel.publish(msg)

    def drone_odom_callback(self, rcv):

        rcv.x *= math.pi/180.0
        rcv.y *= math.pi/180.0
        rcv.z *= math.pi/180.0

        # Publish pose for rviz
        msg = TransformStamped()
        msg.header.frame_id = "/map"
        msg.header.stamp = Clock().now().to_msg()
        msg.child_frame_id = "/base_footprint_drone"

        quat = self.euler_to_quaternion(self.lastPose.x,self.lastPose.y,self.lastPose.z)
        orientation = Quaternion()
        orientation.x = quat[0]
        orientation.y = quat[1]
        orientation.z = quat[2]
        orientation.w = quat[3]
        msg.transform.rotation = orientation

        position = Vector3()
        position.x = rcv.x
        position.y = rcv.y
        position.z = rcv.z
        msg.transform.translation = position

        tfmsg = TFMessage()
        tfmsg.transforms = [msg]
        self.pub_tf.publish(tfmsg)

        # Publish Rviz Path
        msg = Path()
        msg.header.frame_id = "/map"
        msg.header.stamp = Clock().now().to_msg()


        pose = PoseStamped()
        pose.header.frame_id = "/map"
        pose.header.stamp = Clock().now().to_msg()

        pose.point.x = rcv.x
        pose.point.y = rcv.y
        pose.point.z = rcv.z
        self.posearray.append()

        msg.poses = self.posearray
        self.pub_posearray.publish(msg)


def main(args=None):
    rclpy.init(args=args)

    node = AttitudeToVel()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()