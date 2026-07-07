# My Contribution

## Project

GreenGuard AMR Navigation

## Main Responsibility

I was responsible for the AMR navigation and patrol control part of the project.

## Contributions

### 1. SLAM Mapping

I built and refined the indoor map using SLAM and RPLIDAR.

Tasks:

- Explored the test environment with TurtleBot4.
- Generated an occupancy grid map.
- Checked the map in RViz.
- Rebuilt the map when mapping quality was not stable.
- Used the final map for Nav2 localization and patrol testing.

### 2. Localization and Navigation

I configured map-based navigation using ROS2 Humble and Nav2.

Tasks:

- Used AMCL pose for robot localization.
- Verified the robot position in the map frame.
- Tested waypoint navigation with TurtleBot4Navigator.

### 3. Waypoint Patrol

I implemented waypoint-based patrol logic.

Tasks:

- Defined patrol points on the generated map.
- Selected the nearest waypoint based on the robot's current AMCL pose.
- Implemented cyclic patrol behavior.
- Tested repeated patrol movement.

### 4. Patrol Speed Tuning

During patrol mode, the robot speed was reduced for more stable image detection.

- Normal max linear velocity: 0.30 m/s
- Patrol max linear velocity: 0.15 m/s

### 5. Patrol-to-Tracking Transition

When a detection event was received during patrol:

1. The active Nav2 goal was cancelled.
2. The robot was stopped.
3. The system switched from patrol mode to tracking mode.

## What I Learned

- SLAM map quality directly affects AMCL localization and Nav2 navigation.
- Navigation speed should be tuned together with perception performance.
- Event-driven robot behavior requires safe cancellation and stop logic.
