# Altair Phase 3 

## Md.Tanvir Rahman Hridoy 
###240042136
####CSE(SWE)

![ROS 2](https://img.shields.io/badge/ROS_2-Humble-blue)
![Ubuntu](https://img.shields.io/badge/Ubuntu-22.04-orange)
![Python](https://img.shields.io/badge/Python-3-yellow)
![Platform](https://img.shields.io/badge/Simulator-Turtlesim-green)

## 1. Project Overview

Altair Phase 3 is a ROS 2-based autonomous navigation project developed using Python and the Turtlesim simulator.

The project implements an autonomous robot mission in which the turtle navigates through three predefined destinations in a specific order. The robot uses its current position and orientation to calculate movement commands and navigate towards each waypoint.

In addition to autonomous navigation, the system implements an obstacle detection and recovery mechanism. When an obstacle is detected, the robot immediately pauses and continuously publishes zero-velocity commands to prevent further movement.

The mission does not automatically resume when the obstacle is cleared. Instead, it requires an explicit service request to continue navigation.

### Main Features

- Autonomous waypoint navigation.
- Ordered navigation through three destinations.
- Pose-based position and orientation tracking.
- Distance-based waypoint arrival detection.
- Continuous velocity command publishing.
- Obstacle detection using a ROS 2 topic.
- Immediate pause when an obstacle is detected.
- Continuous zero-velocity publishing while paused.
- Explicit service-based mission resumption.
- Rejection of resume requests while an obstacle remains active.
- ROS 2 launch file for starting the simulator and mission together.

---

## 2. Technologies Used

| Technology | Purpose |
|---|---|
| Ubuntu 22.04 | Operating system |
| ROS 2 Humble | Robotics middleware |
| Python 3 | Mission implementation |
| Turtlesim | Robot simulation |
| rclpy | ROS 2 Python client library |
| geometry_msgs | Velocity command messages |
| std_msgs | Obstacle status messages |
| std_srvs | Mission resume service |
| colcon | ROS 2 workspace build tool |

---

## 3. Mission Route

The autonomous mission consists of three destinations that must be reached in the following order:

| Order | Destination | X Coordinate | Y Coordinate |
|---|---|---:|---:|
| 1 | Bottle | 8.0 | 5.5 |
| 2 | Mallet | 8.0 | 8.0 |
| 3 | Base | 5.5 | 5.5 |

### Route Sequence

**Bottle → Mallet → Base → DONE**

The robot navigates to each destination sequentially. Once it reaches a waypoint within the configured arrival tolerance, it records the arrival and proceeds to the next destination.

After reaching the final destination, the mission enters the DONE state and stops the robot.

---

## 4. Project Structure

```text
altair_phase3/
│
├── altair_phase3/
│   ├── __init__.py
│   ├── mission.py
│   ├── drive_menu.py
│   ├── go_to_point.py
│   ├── telemetry_pub.py
│   └── telemetry_monitor.py
│
├── launch/
│   └── mission.launch.py
│
├── resource/
│   └── altair_phase3
│
├── test/
│   ├── test_copyright.py
│   ├── test_flake8.py
│   └── test_pep257.py
│
├── package.xml
├── setup.py
├── setup.cfg
└── README.md
```

### Important Files

- `mission.py`: Implements autonomous navigation, waypoint management, obstacle handling, and mission resumption.
- `mission.launch.py`: Launches both the Turtlesim simulator and the mission node.
- `drive_menu.py`: Contains the package's driving-menu node.
- `go_to_point.py`: Contains the package's point-navigation node.
- `telemetry_pub.py`: Contains the telemetry publisher node.
- `telemetry_monitor.py`: Contains the telemetry monitoring node.
- `package.xml`: Defines package metadata and ROS 2 dependencies.
- `setup.py`: Defines Python package installation and executable entry points.

---

## 5. Installation Requirements

Before running the project, ensure the following are installed:

- Ubuntu 22.04
- ROS 2 Humble
- Python 3
- Turtlesim
- Colcon build tools

Install Turtlesim if it is not already installed:

```bash
sudo apt update
sudo apt install ros-humble-turtlesim
```

Make sure ROS 2 Humble is available:

```bash
source /opt/ros/humble/setup.bash
```

---

## 6. Building the Package

Navigate to the ROS 2 workspace:

```bash
cd ~/altair_phase3_ws
```

Source ROS 2:

```bash
source /opt/ros/humble/setup.bash