import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, DeclareLaunchArgument
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration

# this is the function launch  system will look for

def generate_launch_description():

    robot_name = 'rgbd_robot'
    package_name = 'gazebo_model'
    world_file_name = 'iscas_model.world'
    urdf_file_name = 'rgbd_robot.urdf'

    position = "{ position : { x : 5.0, y: -3.0, z: 0.1}, orientation : { x : 0.0, y: 0.0, z: 1.0, w: 0.03} }"
    orientation = "{ orientation : { x : 0.0, y: 0.0, z: 1.0, w: 0.03} }"

    # full  path to urdf and world file
    
    world = os.path.join(get_package_share_directory(package_name), 'worlds', world_file_name)

    urdf = os.path.join(get_package_share_directory(package_name), 'urdf', urdf_file_name)
    
    # read urdf contents because to spawn an entity in 
    # gazebo we need to provide entire urdf as string on  command line

    xml = open(urdf, 'r').read()

    # double quotes need to be with escape sequence
    xml = xml.replace('"', '\\"')

    # this is argument format for spwan_entity service 
    spwan_args = '{name: "rgbd_robot", xml: "' + xml + '", initial_pose :' + position +'}'

    urdf_description = open(urdf, 'r').read()
    parameters = {'robot_description': urdf_description}

    # create and return launch description object
    return LaunchDescription([
        
        # start gazebo, notice we are using libgazebo_ros_factory.so instead of libgazebo_ros_init.so
        # That is because only libgazebo_ros_factory.so contains the service call to /spawn_entity
        ExecuteProcess(
            cmd=['gazebo', '--verbose', world, '-s', 'libgazebo_ros_factory.so'],
            output='screen'),

        # tell gazebo to spwan your robot in the world by calling service
        ExecuteProcess(
            cmd=['ros2', 'service', 'call', '/spawn_entity', 'gazebo_msgs/SpawnEntity', spwan_args],
            output='screen'),
        # publish robot_description:
        DeclareLaunchArgument('robot_description', default_value=urdf_description),
        #use the ROS timestamp
        DeclareLaunchArgument('use_sim_time', default_value='true'),
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            namespace=package_name,
            output='screen',
            parameters=[parameters],
            ),
    ])


