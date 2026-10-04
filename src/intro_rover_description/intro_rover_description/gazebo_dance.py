#!/usr/bin/env python3
import math
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64

JOINTS = [
	'shoulder_yaw',
	'shoulder_pitch',
	'elbow_pitch',
	'elbow_roll',
	'wrist_pitch',
	'wrist_roll',
]

class GazeboDance(Node):
	def __init__(self):
		super().__init__('gazebo_dance')
		self.pubs = {
			name: self.create_publisher(
				Float64, f'/{name}_cmd', 10)
			for name in JOINTS
		}
		self.t = 0.0
		self.create_timer(0.05, self.publish)
		self.get_logger().info('gazebo_dance started')

	def publish(self):
		self.t += 0.05
		values = [
			math.sin(self.t),
			0.5 * math.sin(self.t * 0.5),
			-0.6 * math.sin(self.t),
			math.sin(self.t * 2.0),
			0.4 * math.sin(self.t * 1.5),
			math.sin(self.t)
		]
		for name, value in zip(JOINTS, values):
			self.pubs[name].publish(Float64(data=value))

def main():
	rclpy.init()
	node = GazeboDance()
	rclpy.spin(node)
	node.destroy_node()
	rclpy.shutdown()

if __name__ == '__main__':
	main()