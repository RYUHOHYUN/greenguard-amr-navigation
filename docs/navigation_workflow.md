## Navigation Workflow

### 1. SLAM Map Generation

TurtleBot4 and its RPLIDAR sensor were used to create an indoor map of the test environment.

RViz2 was used to check the map generation status in real time.

The generated map was later used for AMCL localization and Nav2-based navigation.

### 2. Localization

AMCL localization was launched using the generated map.

The robot pose was monitored using the AMCL pose topic, `/robot3/amcl_pose`, in the integrated demo setup.

RViz2 was used to check whether the estimated robot pose was properly aligned with the map.

### 3. Waypoint Collection

The RViz2 `/clicked_point` topic was used to collect candidate waypoint coordinates.

Nav2 Goal and teleop commands were used to verify whether each waypoint was actually reachable by the robot.

Only waypoints that were reachable in the real test environment were included in the patrol route.

### 4. Patrol Control

The robot first checks its current pose using the AMCL pose topic, `/robot3/amcl_pose`.

The nearest waypoint is selected based on the current robot position.

The robot moves to the nearest waypoint before entering the patrol loop.

After entering the patrol loop, the robot repeatedly follows the predefined waypoint sequence.

### 5. Speed Tuning

Normal navigation linear speed was set to 0.30 m/s.

Patrol navigation linear speed was reduced to 0.15 m/s for more stable camera-based detection during patrol.

The angular velocity limit was kept at 1.00 rad/s.

Nav2 controller speed-related parameters were adjusted to apply a slower linear speed profile during the patrol section.

## ROS 2 Interfaces Used

The navigation workflow used the following ROS 2 interfaces.

* `/robot3/amcl_pose`: subscribed to AMCL pose feedback for map-based robot pose estimation in the integrated demo setup
* `/clicked_point`: subscribed to RViz2 Publish Point input for waypoint candidate logging
* Nav2 goal execution through TurtleBot4Navigator for waypoint movement
* `/robot3/controller_server/set_parameters`: used to adjust Nav2 controller speed parameters during patrol
* `/robot3/cmd_vel`: used to publish zero velocity commands for safe stop
