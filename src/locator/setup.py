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
            "serial_pub = locator.serial_port_pub:main",
            "serial_sub = locator.serial_port_sub:main",
            "new_serial_sub = locator.new_serial_port_sub:main",
        ],
    },
)
