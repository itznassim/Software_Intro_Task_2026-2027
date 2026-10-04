#!/usr/bin/env python3
import math
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

class Dance(Node):
	def __init__(self):
		super().__init__('dance')
		self.pub = self.create_publisher(JointState, 'joint_states', 10)
		self.t = 0.0
		self.create_timer(0.05, self.publish)
		self.get_logger().info('dance started')

	def publish(self):
		self.t += 0.05
		msg = JointState()
		msg.header.stamp = self.get_clock().now().to_msg()
		msg.name = JOINTS
		msg.position = [
			math.sin(self.t),
			0.5 * math.sin(self.t * 0.5),
			-0.6 * math.sin(self.t),
			math.sin(self.t * 2.0),
			0.4 * math.sin(self.t * 1.5),
			math.sin(self.t)
		]
		self.pub.publish(msg)

def main():
	rclpy.init()
	node = Dance()
	rclpy.spin(node)
	node.destroy_node()
	rclpy.shutdown()

if __name__ == '__main__':
	main()