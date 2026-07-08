## My Contribution

This document separates my individual contribution from the team-level GreenGuard system.

## My Main Contribution

* SLAM map generation for the test environment
* AMCL localization setup and pose verification
* RViz2 clicked point and teleop-based waypoint collection
* waypoint patrol route design
* Python-based ROS 2 patrol control node implementation
* AMCL pose-based nearest waypoint selection
* Nav2 goal execution for repeated waypoint patrol
* Nav2 speed parameter tuning for slower patrol movement
* AMR-side troubleshooting related to false loop closure and map distortion
* SLAM parameter tuning to reduce unstable loop closure candidates

## Joint AMR Control Work

AMR Control was handled by two members.

* Hohyun Ryu: map generation, waypoint collection, patrol route design, and patrol-only navigation control
* Teammate: event-based beep and tracking transition behavior when a detection event occurred during patrol

## Team-level Components Not Mainly Implemented by Me

The following components were part of the team-level GreenGuard system, but they were not my main implementation responsibility.

* YOLO detection model
* Web UI
* SQLite3 DB monitoring
* event logging UI
* detection-event-based tracking behavior
* full system integration between detection, event handling, and tracking

## Note

My main contribution was focused on the AMR Navigation part of the GreenGuard system. Specifically, I worked on SLAM map generation, AMCL localization setup, waypoint collection, waypoint patrol route design, Nav2-based patrol execution, speed parameter tuning, and navigation-side troubleshooting.

This document is intended to clarify my individual contribution without overstating my role in the team-level object detection, web monitoring, database, or tracking modules.
