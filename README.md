Ros2 Humble package to test orbSLAM3 on gazebo.

Tested on: 
Ubuntu 22.04
Opencv 4.5.4
 
How to install: 

mkdir ~/workspace

cd ~/workspace

mkdir src

-- Clone repositories:

clone this project: 

clone orbslam3 project and follow the installation process: https://github.com/zang09/ORB_SLAM3_ROS2.git

-- Build the project:

colcon build

source install/setup.sh

--To test: 

1) launch gazebo: 
ros2 launch article world.launch.py
2) run keyboard control 
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r __ns:=/article
3) run orbslam3 
ros2 run orbslam3 mono orbslam3_ros2/vocabulary/ORBvoc.txt orbslam3_ros2/config/monocular/EuRoC.yaml

To plot the trajectory and save in a file: 

python3 plot_trajectory.py KeyFrameTrajectory.txt
