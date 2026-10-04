#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState

JOINTS = [
	'shoulder_yaw',
	'shoulder_pitch',
	'elbow_pitch',
	'elbow_roll',
	'wrist_pitch',
	'wrist_roll',
]

class JointControl(Node):
	def __init__(self):
		super().__init__('joint_control')
		self.pub = self.create_publisher(JointState, 'joint_states', 10)
		self.positions = [1.0, 0.5, -0.5, 0.0, 0.3, 0.0]
		self.create_timer(0.1, self.publish)
		self.get_logger().info('joint_control started')

	def publish(self):
		msg = JointState()
		msg.header.stamp = self.get_clock().now().to_msg()
		msg.name = JOINTS
		msg.position = self.positions
		self.pub.publish(msg)

def main():
	rclpy.init()
	node = JointControl()
	rclpy.spin(node)
	node.destroy_node()
	rclpy.shutdown()

if __name__ == '__main__':
	main()