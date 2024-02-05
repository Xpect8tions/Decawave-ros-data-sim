import os
from glob import glob

from setuptools import find_packages, setup

package_name = "locator"

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    
        (
            os.path.join("share", package_name, "config"),
            glob(os.path.join("config", "*.yaml")),
        ),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="adriel",
    maintainer_email="xpect8tions@gmail.com",
    description="TODO: Package description",
    license="TODO: License declaration",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "uwb_logs = logging.uwb_logs",
            "DWranging = logging.DWranging",
            "dwm_locator = locator.dwm_locator_node:main",
            "file_writer = locator.file_writer:main",
            "math_pub = locator.math_multi_pub:main",
            "math_sub = locator.math_multi_sub:main",
            "multi_pub = locator.multi_pub:main",
            "yaml_multi_pub = locator.yaml_multi_pub:main",
            "yaml_multi_sub = locator.yaml_multi_sub:main",
            "yaml_rand_multi_pub = locator.yaml_rand_multi_pub:main",
            "subprocess = locator.subprocess:main",
            "client = locator.client_template:main",
            "service = locator.service_template:main",
            "trilaterate = locator.trilateration",
            "one_topic_sub = locator.one_topic_sub:main",
            "serial_pub = locator.serial_port_pub:main",
            "serial_sub = locator.serial_port_sub:main",
            "new_serial_sub = locator.new_serial_port_sub:main",
        ],
    },
)
