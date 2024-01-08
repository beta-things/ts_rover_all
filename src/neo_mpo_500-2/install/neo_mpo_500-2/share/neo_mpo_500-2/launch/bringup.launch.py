# Neobotix GmbH

import launch
import math
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import ThisLaunchFileDir, LaunchConfiguration
from launch_ros.actions import Node
import os
from pathlib import Path
from launch.launch_context import LaunchContext

def generate_launch_description():
    neo_mpo_500 = get_package_share_directory('neo_mpo_500-2')
    rpi_lidar_package = get_package_share_directory('rplidar_ros')
    laser_filter_package = get_package_share_directory('laser_filters')
    robot_namespace = LaunchConfiguration('robot_namespace', default='')
    context = LaunchContext()

    static_transform_publisher_node2 = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='link2_broadcaster',
        arguments=['0.32', '-0.53', '0', '0', '0', '0.414693242656239', '0.9099612708765432','map', 'libsurvive_world'],
        output='screen'
    )

    static_transform_publisher_node3 = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='link2_broadcaster',
        arguments=['0', '0', '0', '0', '0', '0.7071068', '0.7071068','tracker_dot', 'corrected_tracker_dot'],
        output='screen'
    )


    static_transform_publisher_node4 = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='link2_broadcaster',
        arguments=['0', '0', '0', '0', '0', '0', '1','map', 'odom'],
        output='screen'
    )

    # ros2 run tf2_ros static_transform_publisher 0.32 -0.53 1.5 0 0 0.414693242656239, 0.9099612708765432 map libsurvive_world


    # Launch can be set just once, does not matter if you set it for other launch files. 
    # The arguments should certainly have different meaning if there is a bigger launch file
    # Leaving this comment here for a clarity thereof and thereforth. 
    # https://answers.ros.org/question/306935/ros2-include-a-launch-file-from-a-launch-file/

    lidar_module = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(rpi_lidar_package, 'launch/rplidar_a1_launch.py')
            ),
            launch_arguments={
                'namespace': robot_namespace,
                'frame_id': 'lidar_1_link'
                
            }.items()
        )

    lidar_filter_module = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(laser_filter_package, 'examples/box_filter_example.launch.py')
            ),
            launch_arguments={
                'namespace': robot_namespace
            }.items()
        )

    kinematics = IncludeLaunchDescription(
             PythonLaunchDescriptionSource(
                 os.path.join(neo_mpo_500, 'configs/kinematics', 'kinematics.launch.py')
             )
         )

    urdf = os.path.join(get_package_share_directory('neo_mpo_500-2'), 'robot_model', 'mpo_500.urdf')

    with open(urdf, 'r') as infp:  
        robot_desc = infp.read()

    start_robot_state_publisher_cmd = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        namespace=robot_namespace,
        parameters=[{'robot_description': robot_desc, 'frame_prefix': robot_namespace}],
        arguments=[urdf])

    teleop = IncludeLaunchDescription(
             PythonLaunchDescriptionSource(
                 os.path.join(neo_mpo_500, 'configs/teleop', 'teleop.launch.py')
             )
         )

    motor_operator = Node(
        package='odrive_motor_op',
        executable = 'motor_op',
        name='motor_op',
        namespace =  robot_namespace,
        output='screen'
    )

    # relayboard = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource(
    #         os.path.join(neo_mpo_500, 'configs/relayboard_v2', 'relayboard_v2.launch.py')
    #     ),
    #     launch_arguments={
    #         'namespace': robot_namespace
    #     }.items()
    # )

    # laser = IncludeLaunchDescription(
    #         PythonLaunchDescriptionSource(
    #             os.path.join(neo_mpo_500, 'configs/lidar/sick/s300', 'sick_s300.launch.py')
    #         )
    #     )

    # relay_topic_lidar1 = Node(
    #         package='topic_tools',
    #         executable = 'relay',
    #         name='relay',
    #         namespace =  robot_namespace,
    #         output='screen',
    #         parameters=[{'input_topic': robot_namespace.perform(context) + "lidar_1/scan_filtered",'output_topic': robot_namespace.perform(context) + "scan"}])

    # relay_topic_lidar2 = Node(
    #         package='topic_tools',
    #         executable = 'relay',
    #         name='relay',
    #         namespace =  robot_namespace,
    #         output='screen',
    #         parameters=[{'input_topic': robot_namespace.perform(context) + "lidar_2/scan_filtered",'output_topic': robot_namespace.perform(context) + "scan"}])

    # return LaunchDescription([relayboard, start_robot_state_publisher_cmd, laser, kinematics, teleop, relay_topic_lidar1, relay_topic_lidar2])
    return LaunchDescription([start_robot_state_publisher_cmd, lidar_module, kinematics, 
    teleop, motor_operator, lidar_filter_module,
    static_transform_publisher_node2])
