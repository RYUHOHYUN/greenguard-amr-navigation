# GreenGuard AMR Navigation

SLAM-based AMR patrol system using ROS2 Humble, Nav2, TurtleBot4, RPLIDAR, and Python.

This repository summarizes the AMR navigation part of the GreenGuard project.

## Project Overview

GreenGuard is a smart-farm AMR patrol system.

The overall system includes autonomous patrol, object detection, event handling, logging, and web-based monitoring.

This repository focuses on the AMR navigation part.

## My Role

I was responsible for the AMR navigation and patrol control part.

Main contributions:

- Built and refined the indoor map using SLAM and RPLIDAR.
- Configured ROS2/Nav2-based autonomous navigation.
- Defined waypoint positions for AMR patrol.
- Implemented waypoint-based patrol logic using TurtleBot4Navigator.
- Used AMCL pose to select the nearest waypoint from the robot's current position.
- Tuned Nav2 velocity parameters for stable patrol and image detection.
- Integrated patrol-to-tracking mode transition when a detection event was received.

## Tech Stack

- ROS2 Humble
- Nav2
- TurtleBot4
- RPLIDAR
- OAK-D Pro
- Python
- AMCL
- SLAM

## Key Features

### SLAM Mapping

Created an indoor occupancy grid map for TurtleBot4 navigation.

### AMCL Localization

Used AMCL pose to estimate the robot position on the map.

### Waypoint Patrol

The robot patrols predefined waypoints repeatedly.

### Event-based Mode Transition

When a detection event is received during patrol, the current Nav2 goal is cancelled and the robot switches to tracking mode.

## Repository Structure

```text
greenguard-amr-navigation/
├── README.md
├── src/
│   └── patrol_control_node.py
├── docs/
│   └── my_contribution.md
└── config/
    └── waypoints.yaml
```

## Note

This was a team project.

My contribution was focused on SLAM mapping, AMR navigation, waypoint patrol, and Nav2-based patrol control.
