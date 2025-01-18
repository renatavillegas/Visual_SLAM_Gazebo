import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, DeclareLaunchArgument
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration

# this is the function launch  system will look for

def generate_launch_description():

    world_file_name = 'turtlebot_iscas_model.world'
    world_package_name = 'gazebo_model'
    # full  path to urdf and world file
    
    world = os.path.join(get_package_share_directory(world_package_name), 'worlds', world_file_name)

    # create and return launch description object
    return LaunchDescription([
        # start gazebo, notice we are using libgazebo_ros_factory.so instead of libgazebo_ros_init.so
        # That is because only libgazebo_ros_factory.so contains the service call to /spawn_entity
        # we don't need to spawn the robot because this .world file already have the model. 
        ExecuteProcess(
            cmd=['gazebo', '--verbose', world, '-s', 'libgazebo_ros_factory.so'],
            output='screen'),
    ])


