# My Contribution

This document separates my individual contribution from the team-level GreenGuard system.

## My Main Contribution

- SLAM map generation for the test environment
- AMCL localization setup and pose check
- RViz2 clicked point and teleop-based waypoint collection
- waypoint patrol route design
- Python-based ROS 2 patrol control node implementation
- AMCL pose-based nearest waypoint selection
- Nav2 goal execution for repeated patrol
- Nav2 speed parameter tuning for slower patrol movement
- AMR-side troubleshooting related to false loop closure and map distortion

## Joint AMR Control Work

AMR Control was handled by two members.

- Hohyun Ryu: map generation, waypoint collection, patrol route, and patrol-only navigation control
- Teammate: event-based beep and tracking behavior when an object or person was detected during patrol

## Team-level Components Not Mainly Implemented by Me

- YOLO detection model
- Web UI
- SQLite3 DB monitoring
- event logging UI
- integrated detection-to-tracking behavior

