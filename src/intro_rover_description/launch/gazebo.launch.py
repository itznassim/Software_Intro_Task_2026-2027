import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
	pkg = get_package_share_directory('intro_rover_description')
	urdf = os.path.join(pkg, 'urdf', 'intro_rover_description.urdf')
	with open(urdf, 'r') as f:
		robot_description = f.read()

	gz = IncludeLaunchDescription(
		PythonLaunchDescriptionSource(
			os.path.join(
				get_package_share_directory('ros_gz_sim'),
				'launch',
				'gz_sim.launch.py',
			)
		),
		launch_arguments={'gz_args': '-r ' + os.path.join(pkg, 'worlds', 'rover.sdf')}.items(),
	)

	robot_state = Node(
		package='robot_state_publisher',
		executable='robot_state_publisher',
		parameters=[{
			'robot_description': robot_description,
			'use_sim_time': True
		}],
	)

	spawn = Node(
		package='ros_gz_sim',
		executable='create',
		arguments=['-name', 'rover', '-topic', 'robot_description', '-z', '0.3'],
		output='screen',
	)

	set_path = SetEnvironmentVariable(
		'GZ_SIM_RESOURCE_PATH',
		os.path.dirname(pkg),
	)
	bridge = Node(
		package='ros_gz_bridge',
		executable='parameter_bridge',
		parameters=[{
			'config_file': os.path.join(pkg, 'config', 'bridge.yaml'),
		}],
		output='screen',
	)
	return LaunchDescription([set_path, gz, robot_state, spawn, bridge])
	