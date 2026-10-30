from glob import glob
import os

from setuptools import find_packages, setup

package_name = 'altair_phase3'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
        data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='nemetrix36',
    maintainer_email='nemetrix36@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'telemetry_pub = altair_phase3.telemetry_pub:main',
            'telemetry_monitor = altair_phase3.telemetry_monitor:main',
            'drive_menu = altair_phase3.drive_menu:main',
            'go_to_point = altair_phase3.go_to_point:main',
            'mission = altair_phase3.mission:main',
        ],},
)
