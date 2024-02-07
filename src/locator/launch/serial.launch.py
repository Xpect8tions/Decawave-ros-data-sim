import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    config = os.path.join(
        get_package_share_directory("launchers"), "config", "serial_params.yaml"
    )
    my_package_dir = get_package_share_directory("launchers")
    return LaunchDescription(
        [
            Node(
                package="locator",
                executable="serial_sub",
                name="serial_sub",
                namespace="",
                parameters=[config],
            ),
            Node(package='rviz2',
                 executable='rviz2',
                 arguments=['-d', os.path.join(my_package_dir, "config", "rviz_config.rviz")])

        ]
    )
