# Altair Phase 3 – Autonomous Mission

## Overview

This ROS 2 package implements an autonomous TurtleSim mission with three ordered destinations:

1. Bottle – (8.0, 5.5)
2. Mallet – (8.0, 8.0)
3. Base – (5.5, 5.5)

The robot navigates between these waypoints using its current position and orientation.

The mission supports obstacle handling. When an obstacle is detected, the robot pauses and publishes zero velocity. After the obstacle is cleared, the mission remains paused until an explicit resume request is received.

## Requirements

- Ubuntu 22.04
- ROS 2 Humble
- Python 3
- Turtlesim

## Build Instructions

```bash
source /opt/ros/humble/setup.bash
cd ~/altair_phase3_ws
colcon build --packages-select altair_phase3
source install/setup.bash
