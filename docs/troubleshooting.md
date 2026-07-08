# Troubleshooting

## Issue 1. False Loop Closure During SLAM

### Symptom

During initial SLAM map generation, map distortion occurred due to false loop closure.

### Actions Taken

- Increased minimum travel distance to reduce excessive scan node creation.
- Increased minimum travel heading to reduce unnecessary node creation from small rotations.
- Reduced loop search maximum distance to remove distant loop closure candidates.
- Increased loop match minimum chain size to strengthen loop closure acceptance.
- Reduced coarse matching variance threshold to remove uncertain coarse matches.
- Increased coarse and fine matching response thresholds to strengthen matching criteria.

### Parameter Changes

- minimum_travel_distance: 0.0 to 0.15
- minimum_travel_heading: 0.0 to 0.12
- loop_search_maximum_distance: 3.0 to 1.5
- loop_match_minimum_chain_size: 10 to 15
- loop_match_maximum_variance_coarse: 3.0 to 1.5
- loop_match_minimum_response_coarse: 0.35 to 0.50
- loop_match_minimum_response_fine: 0.45 to 0.60

### Lesson Learned

Even when using existing SLAM packages, map quality depends heavily on parameter tuning, robot driving behavior, and the structure of the test environment.

## Issue 2. Patrol Speed and Detection Stability

### Symptom

During patrol, the robot sometimes moved too fast for stable camera-based object detection.

### Action Taken

- Reduced Nav2 controller speed parameters during patrol sections.
- Used a slower patrol speed profile for the waypoint loop.

### Parameter Changes

- Normal max velocity: 0.30 m/s
- Patrol max velocity: 0.15 m/s
- Adjusted parameters: FollowPath.max_vel_x, FollowPath.max_speed_xy, FollowPath.max_vel_theta

