# The micro-ROS_kobuki_demo repository

This repository provides a demo of micro-ROS (and in particular its client library features) based on a [Kobuki (Turtlebot 2)](http://kobuki.yujinrobot.com/about2/) and an [Olimex STM32-E407 board](https://www.olimex.com/Products/ARM/ST/STM32-E407/open-source-hardware).

The basic idea and working principle is as follows: Instead of the typical laptop running ROS, the Kobuki is equipped with a STM32 F4 microcontroller only. This STM32 F4 runs the micro-ROS stack and a port of the [thin_kobuki driver](https://github.com/Lab-RoCoCo/thin_drivers/blob/master/thin_kobuki/), which interacts with the robot's firmware (which runs on a built-in microcontroller). The STM32 F4 communicates the sensor data via DDS-XRCE to a remote laptop running a standard ROS 2 stack, the micro-ROS agent and rviz. At the same time, using the other direction of communication, the Kobuki can be remote-controlled.

![Illustration of idea and working principle](README_idea.png)

In detail, this repository contains the following ROS 2 and micro-ROS packages:

* [micro-ros_kobuki_demo_remote](micro-ros_kobuki_demo_remote/) provides launch files to start teleop_twist_joy, rviz2, robot_state_publisher and the odom_to_tf node.
* [micro-ros_kobuki_demo_robot-description](micro-ros_kobuki_demo_robot-description/) provides the URDF and meshes and textures for the Kobuki as well as the Olimex board.
* _The port of the [thin_kobuki driver](https://github.com/Lab-RoCoCo/thin_drivers/blob/master/thin_kobuki/) to micro-ROS is located in a separate repository at [https://github.com/micro-ROS/nuttx_apps/tree/demo/safe_kobuki/examples/kobuki](https://github.com/micro-ROS/nuttx_apps/tree/demo/safe_kobuki/examples/kobuki)._ Please note that it has not been ported to Foxy yet.

Technical information on these packages is given in the README.md files in the corresponding subfolders.

## Purpose of the project

The software is not ready for production use. It has neither been developed nor tested for a specific use case. However, the license conditions of the applicable Open Source licenses allow you to adapt the software to your needs. Before using it in a safety relevant setting, make sure that the software fulfills your requirements and adjust it according to any applicable safety standards (e.g. ISO 26262).

## Requirements, how to build, test, install, use, etc

Clone the repository into a ROS workspace and build it using [colcon](https://colcon.readthedocs.io/).

## License

micro-ROS_kobuki_demo is open-sourced under the Apache-2.0 license. See the [LICENSE](LICENSE) file for details.

For a list of other open source components included in micro-ROS_kobuki_demo, see the file [3rd-party-licenses.txt](3rd-party-licenses.txt).

## Quality assurance

The colcon_test tool is used for quality assurances, which includes cpplint, uncrustify, flake8, xmllint and various other tools.

## Known issues/limitations

Please notice the following issues/limitations:

* Currently, the demo does not use the standard ROS 2 odometry message types but shorter types due to issues in the middleware.
