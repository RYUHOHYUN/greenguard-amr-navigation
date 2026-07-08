# Navigation Workflow

## 1. SLAM Map Generation

- TurtleBot4 and RPLIDAR were used to create an indoor map of the test environment.
- RViz2 was used to check the map generation status.
- The generated map was later used for AMCL localization and Nav2 navigation.

## 2. Localization

- AMCL was executed on the generated map.
- Robot pose was monitored using AMCL pose.
- RViz2 was used to check pose alignment on the map.

## 3. Waypoint Collection

- RViz2 clicked point was used to collect candidate waypoint coordinates.
- Nav2 Goal and teleop command were used to check whether each waypoint was actually reachable.

## 4. Patrol Control

- The robot first checks the current AMCL pose.
- The nearest waypoint is selected from the current robot position.
- The robot moves to the nearest waypoint before entering the patrol loop.
- The robot repeatedly follows the predefined waypoint sequence.

## 5. Speed Tuning

- Normal navigation speed was set to 0.30 m/s.
- Patrol navigation speed was reduced to 0.15 m/s for more stable camera-based detection during patrol.

