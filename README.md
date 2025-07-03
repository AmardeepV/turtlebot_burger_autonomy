# BumperBot Autonomy

This repository contains the full stack to deploy an autonomous TurtleBot Burger-like robot using ROS2.

## 🐢 **Packages Included**

### 1. `bumperbot_description`
- Contains the URDF, meshes, and configuration files defining the BumperBot.
- Responsible for robot description and visualization.

### 2. `ldlidar_ros2`
- ROS2 driver package for LDLidar sensors.
- Added as a submodule to keep updated with upstream.

### 3. `serial_motor_demo`
- Arduino-based motor control interface.
- Bridges ROS2 topics to motor commands over serial.

## 🚀 **Setup Instructions**

```bash
# Clone the repository
git clone --recurse-submodules https://github.com/YourUsername/bumperbot_autonomy.git
cd bumperbot_autonomy

# Install dependencies
rosdep install --from-paths src --ignore-src -r -y

# Build
colcon build
