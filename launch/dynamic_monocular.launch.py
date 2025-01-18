import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node

def generate_launch_description():

    package_name = 'gazebo_model'
    world_file_name = 'iscas_model.world'
    urdf_file_name = 'simple_robot.urdf'
    urdf_file_name2 = 'simple_robot2.urdf'
    
    world = os.path.join(get_package_share_directory(package_name), 'worlds', world_file_name)
    urdf = os.path.join(get_package_share_directory(package_name), 'urdf', urdf_file_name)
    urdf2 =os.path.join(get_package_share_directory(package_name), 'urdf', urdf_file_name2)
    xml = open(urdf, 'r').read()
    xml = xml.replace('"', '\\"')
    xml2 = open(urdf2, 'r').read()
    xml2 = xml2.replace('"', '\\"')

    position_robot1 = "{ position : { x : 5.0, y: -3.0, z: 0.1}, orientation : { x : 0.0, y: 0.0, z: 1.0, w: 0.03} }"
    position_robot2 = "{ position : { x : -1.5, y: 1.7, z: 0.1}, orientation : { x : 0.0, y: 0.0, z: -0.7069527184574635, w: 0.7072608103450506} }"
    
    spawn_args_robot1 = '{name: "simple_robot", xml: "' + xml + '", initial_pose :' + position_robot1 + '}'
    spawn_args_robot2 = '{name: "simple_robot2", xml: "' + xml2 + '", initial_pose :' + position_robot2 + '}'

    return LaunchDescription([
        ExecuteProcess(
            cmd=['gazebo', '--verbose', world, '-s', 'libgazebo_ros_factory.so'],
            output='screen'),

        ExecuteProcess(
            cmd=['ros2', 'service', 'call', '/spawn_entity', 'gazebo_msgs/SpawnEntity', spawn_args_robot1],
            output='screen'),

        ExecuteProcess(
            cmd=['ros2', 'service', 'call', '/spawn_entity', 'gazebo_msgs/SpawnEntity', spawn_args_robot2],
            output='screen'),
    ])