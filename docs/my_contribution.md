# My Contribution

This document clarifies my individual contribution to the GreenGuard AMR Navigation project and separates it from the team-level GreenGuard system.

## My Main Contribution

My main contribution was focused on the AMR Navigation part of the system. I worked on configuring and implementing the navigation workflow that allowed TurtleBot4 to localize itself on a generated map and repeatedly patrol predefined waypoints.

Specifically, I contributed to the following tasks:

* SLAM map generation for the test environment
* RViz2-based map generation monitoring
* AMCL localization setup and pose verification
* Nav2 Goal-based movement testing
* RViz2 clicked point and teleop-based waypoint collection
* waypoint patrol route design
* Python-based ROS 2 patrol control node implementation
* AMCL pose-based nearest waypoint selection
* Nav2 goal execution for repeated waypoint patrol
* Nav2 speed parameter tuning for slower patrol movement
* AMR-side troubleshooting related to false loop closure and map distortion
* SLAM parameter tuning to reduce unstable loop closure candidates

## Joint AMR Control Work

AMR Control was handled by two members in the team.

* Hohyun Ryu: map generation, waypoint collection, patrol route design, nearest waypoint selection, and patrol-only navigation control
* Teammate: detection-event-based behavior transition, including tracking behavior when an object was detected during patrol

My work provided the navigation foundation used by the team-level scenarios, while the detection-triggered tracking transition was mainly implemented by another teammate.

## Team-level Components Not Mainly Implemented by Me

The following components were part of the full GreenGuard team system, but they were not my main implementation responsibility:

* YOLO detection model
* laptop camera-based tomato inspection logic using a camera connected on top of the TurtleBot4
* fixed webcam-based detection trigger
* Mission Manager logic for event handling
* detection-event-based tracking behavior
* SQLite3 DB monitoring
* event logging UI
* Flask Web UI
* full system integration between detection, event handling, tracking, database, and web monitoring

These components are mentioned in the README only to explain the system context and how my AMR navigation module was used within the full team project.

## Scope of My Implementation

This project used existing ROS 2 navigation packages and tools such as Nav2, AMCL, SLAM, TurtleBot4 navigation packages, and RViz2.

I did not implement SLAM, localization, or path planning algorithms from scratch. Instead, my contribution was focused on configuring and integrating the ROS 2 navigation stack for a working TurtleBot4-based AMR patrol scenario.

My implementation scope can be summarized as follows:

* creating a usable SLAM map for the test environment
* setting up localization on the generated map
* collecting and organizing patrol waypoints
* designing a repeatable waypoint patrol route
* implementing a Python-based ROS 2 patrol control node
* executing repeated Nav2-based waypoint navigation
* selecting the nearest waypoint based on the current AMCL pose
* adjusting Nav2 speed parameters for stable patrol operation
* troubleshooting navigation-side issues such as false loop closure and unstable map generation

## Note

My main contribution was focused on the AMR Navigation part of the GreenGuard system.

This document is intended to clarify my individual contribution without overstating my role in the team-level object detection, web monitoring, database, event handling, tomato inspection, or tracking modules.
