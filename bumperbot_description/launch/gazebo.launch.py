import os
from ament_index_python.packages import get_package_share_directory, get_package_prefix

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable
from launch.substitutions import Command, LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node
from pathlib import Path
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    bumperbot_description_dir = get_package_share_directory("bumperbot_description")
    #bumperbot_description_share = os.path.join(get_package_prefix("bumperbot_description"), "share")
    #gazebo_ros_dir = get_package_share_directory("gazebo_ros")

    model_arg = DeclareLaunchArgument(name="model", default_value=os.path.join(
                                        bumperbot_description_dir, "urdf", "bumperbot.urdf.xacro"
                                        ),
                                      description="Absolute path to robot urdf file"
    )

    gazebo_resource_path = SetEnvironmentVariable(
        name="GZ_SIM_RESOURCE_PATH",
        value=[
            str(Path(bumperbot_description_dir).parent.resolve())
        ]
    )

    robot_description = ParameterValue(Command(["xacro ", LaunchConfiguration("model")]),
                                       value_type=str)

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": robot_description}]
    )
    """
    start_gazebo_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_ros_dir, "launch", "gzserver.launch.py")
        )
    )

    start_gazebo_client = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_ros_dir, "launch", "gzclient.launch.py")
        )
    )
    """

    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory("ros_gz_sim"), "launch"), "/gz_sim.launch.py"]),
                launch_arguments=[
                    ("gz_args", [" -v 4", " -r", "empty.sdf"]
                    )
                ]
    )
    """
    spawn_robot = Node(package="gazebo_ros", executable="spawn_entity.py",
                        arguments=["-entity", "bumperbot",
                                   "-topic", "robot_description",
                                  ],
                        output="screen"
    )
    """

    gz_spawn_entity = Node(
        package="ros_gz_sim",
        executable="create",
        output="screen",
        arguments=["-topic", "robot_description",
                   "-name", "bumperbot"]
    )

    return LaunchDescription([
        model_arg,
        robot_state_publisher_node,
        gazebo_resource_path,
        gazebo,
        gz_spawn_entity
    ])