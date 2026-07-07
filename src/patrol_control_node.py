#!/usr/bin/env python3

"""
GreenGuard AMR Navigation-Only Patrol Control Node

This script contains only the AMR navigation/patrol part that I was responsible for
in the GreenGuard project.

Main responsibilities reflected in this file:
- AMCL pose subscription for map-based localization
- RViz clicked point logging for waypoint collection
- Waypoint-based patrol using TurtleBot4Navigator and Nav2
- Nearest waypoint selection from the current AMCL pose
- Dynamic Nav2 controller speed adjustment during patrol sections
- Safe stop and cleanup logic

Removed from the original integrated demo code:
- Person/object tracking mode
- RGB/depth image processing
- Detection-topic based target following
- OpenCV GUI display logic

Author: Hohyun Ryu
Project: GreenGuard AMR Navigation
"""

import math
import threading
import time

import rclpy
from rclpy.node import Node
from rclpy.executors import SingleThreadedExecutor
from rclpy.qos import (
    QoSProfile,
    ReliabilityPolicy,
    DurabilityPolicy,
    HistoryPolicy,
)

from geometry_msgs.msg import PoseWithCovarianceStamped, PointStamped, Twist

from rcl_interfaces.srv import SetParameters
from rcl_interfaces.msg import Parameter as ParameterMsg
from rcl_interfaces.msg import ParameterValue, ParameterType

from turtlebot4_navigation.turtlebot4_navigator import (
    TurtleBot4Directions,
    TurtleBot4Navigator,
)


ROBOT_NS = "/robot3"

AMCL_POSE_TOPIC = f"{ROBOT_NS}/amcl_pose"
CMD_VEL_TOPIC = f"{ROBOT_NS}/cmd_vel"
CONTROLLER_SERVER_NAME = f"{ROBOT_NS}/controller_server"

# RViz2 "Publish Point" tool normally publishes geometry_msgs/PointStamped
# to /clicked_point. This was used to record waypoint candidates on the map.
CLICKED_POINT_TOPIC = "/clicked_point"

# Normal navigation speed
NORMAL_MAX_VEL_X = 0.30
NORMAL_MAX_VEL_THETA = 1.00

# Slower patrol speed for better camera-based detection during specific patrol sections
PATROL_MAX_VEL_X = 0.15
PATROL_MAX_VEL_THETA = 1.00

STOP_PUBLISH_HZ = 50.0
STOP_PERIOD = 1.0 / STOP_PUBLISH_HZ


class NavigationControlNode(Node):
    """ROS2 node for AMCL pose monitoring, clicked-point logging, and speed control."""

    def __init__(self):
        super().__init__("greenguard_navigation_control_node")

        self.current_x = None
        self.current_y = None
        self.stop_requested = False

        self.cmd_vel_pub = self.create_publisher(Twist, CMD_VEL_TOPIC, 10)

        amcl_qos = QoSProfile(
            history=HistoryPolicy.KEEP_LAST,
            depth=1,
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
        )

        self.create_subscription(
            PoseWithCovarianceStamped,
            AMCL_POSE_TOPIC,
            self.amcl_callback,
            amcl_qos,
        )

        # Optional helper subscription:
        # Used during waypoint setup to click candidate points in RViz2 and log coordinates.
        self.create_subscription(
            PointStamped,
            CLICKED_POINT_TOPIC,
            self.clicked_point_callback,
            10,
        )

    def amcl_callback(self, msg):
        self.current_x = msg.pose.pose.position.x
        self.current_y = msg.pose.pose.position.y

    def clicked_point_callback(self, msg):
        self.get_logger().info(
            "RViz clicked point received: "
            f"x={msg.point.x:.4f}, y={msg.point.y:.4f}, z={msg.point.z:.4f}, "
            f"frame_id={msg.header.frame_id}"
        )

    def has_pose(self):
        return self.current_x is not None and self.current_y is not None

    def get_pose_xy(self):
        return self.current_x, self.current_y

    def publish_zero_cmd(self):
        self.cmd_vel_pub.publish(Twist())

    def force_stop_robot(self, duration_sec=1.0):
        count = int(duration_sec * STOP_PUBLISH_HZ)

        for _ in range(count):
            self.publish_zero_cmd()
            time.sleep(STOP_PERIOD)


def spin_node(executor, node):
    while rclpy.ok() and not node.stop_requested:
        executor.spin_once(timeout_sec=0.01)


def wait_for_amcl_pose(control_node):
    while rclpy.ok():
        if control_node.has_pose():
            return control_node.get_pose_xy()

        control_node.get_logger().info("Waiting for AMCL pose...")
        time.sleep(0.5)

    return None


def make_double_param(name, value):
    param = ParameterMsg()
    param.name = name

    param.value = ParameterValue()
    param.value.type = ParameterType.PARAMETER_DOUBLE
    param.value.double_value = float(value)

    return param


def set_nav2_speed(control_node, linear_x, angular_z):
    """Dynamically update Nav2 controller speed parameters."""

    service_name = f"{CONTROLLER_SERVER_NAME}/set_parameters"

    client = control_node.create_client(SetParameters, service_name)

    control_node.get_logger().info(
        f"Waiting for parameter service: {service_name}"
    )

    if not client.wait_for_service(timeout_sec=3.0):
        control_node.get_logger().warn(
            "controller_server set_parameters service not available. "
            "Speed change skipped."
        )
        return False

    request = SetParameters.Request()
    request.parameters = [
        make_double_param("FollowPath.max_vel_x", linear_x),
        make_double_param("FollowPath.max_speed_xy", linear_x),
        make_double_param("FollowPath.max_vel_theta", angular_z),
    ]

    future = client.call_async(request)

    while rclpy.ok() and not future.done():
        time.sleep(0.02)

    response = future.result()

    if response is None:
        control_node.get_logger().warn("Speed parameter service returned None.")
        return False

    for result in response.results:
        if not result.successful:
            control_node.get_logger().warn(
                f"Speed parameter rejected: {result.reason}"
            )
            return False

    control_node.get_logger().info(
        f"Speed changed: max_vel_x={linear_x}, "
        f"max_speed_xy={linear_x}, max_vel_theta={angular_z}"
    )

    return True


def distance_xy(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def find_nearest_point(current_x, current_y, point_positions):
    nearest_name = None
    nearest_dist = None

    for name, xy in point_positions.items():
        px, py = xy
        dist = distance_xy(current_x, current_y, px, py)

        if nearest_dist is None or dist < nearest_dist:
            nearest_name = name
            nearest_dist = dist

    return nearest_name, nearest_dist


def go_to_pose(navigator, pose, name):
    navigator.info(f"Going to {name}")
    navigator.startToPose(pose)

    while rclpy.ok():
        if navigator.isTaskComplete():
            navigator.info(f"Arrived at {name}")
            return True

        time.sleep(0.01)

    return False


def get_next_loop_index(loop_names, current_name):
    for i, name in enumerate(loop_names):
        if name == current_name:
            return (i + 1) % len(loop_names)

    return 0


def build_waypoint_poses(navigator):
    """Define waypoint coordinates and convert them to Nav2 PoseStamped goals."""

    point_positions = {
        "point1": [-2.8649349212646484, -0.10677920281887054],
        "point2": [-2.5, 1.05],
        "point3": [-4.667, 1.275],
        "point4": [-2.557, 4.094],
        "point5": [-4.740, 4.403],
        "point24_mid": [-2.434, 3.028],
        "point35_mid": [-4.700, 2.830],
    }

    poses = {
        "point1": navigator.getPoseStamped(
            point_positions["point1"],
            TurtleBot4Directions.SOUTH,
        ),
        "point2": navigator.getPoseStamped(
            point_positions["point2"],
            TurtleBot4Directions.WEST,
        ),
        "point3": navigator.getPoseStamped(
            point_positions["point3"],
            TurtleBot4Directions.WEST,
        ),
        "point4": navigator.getPoseStamped(
            point_positions["point4"],
            TurtleBot4Directions.EAST,
        ),
        "point5": navigator.getPoseStamped(
            point_positions["point5"],
            TurtleBot4Directions.NORTH,
        ),
        "point24_mid": navigator.getPoseStamped(
            point_positions["point24_mid"],
            TurtleBot4Directions.SOUTH,
        ),
        "point35_mid": navigator.getPoseStamped(
            point_positions["point35_mid"],
            TurtleBot4Directions.NORTH,
        ),
    }

    return point_positions, poses


def main():
    rclpy.init(
        args=[
            "--ros-args",
            "-r",
            "__ns:=/robot3",
            "-r",
            "/tf:=/robot3/tf",
            "-r",
            "/tf_static:=/robot3/tf_static",
        ]
    )

    navigator = TurtleBot4Navigator()
    control_node = NavigationControlNode()

    executor = SingleThreadedExecutor()
    executor.add_node(control_node)

    spin_thread = threading.Thread(
        target=spin_node,
        args=(executor, control_node),
        daemon=True,
    )
    spin_thread.start()

    navigator.info("GreenGuard navigation-only patrol node started.")

    point_positions, poses = build_waypoint_poses(navigator)

    loop_names = [
        "point2",
        "point3",
        "point35_mid",
        "point24_mid",
        "point35_mid",
        "point5",
        "point4",
    ]

    try:
        set_nav2_speed(
            control_node,
            NORMAL_MAX_VEL_X,
            NORMAL_MAX_VEL_THETA,
        )

        if navigator.getDockedStatus():
            navigator.info("Robot is docked. Undocking...")
            navigator.undock()
        else:
            navigator.info("Robot is already undocked. Continue.")

        current_pose = wait_for_amcl_pose(control_node)

        if current_pose is None:
            navigator.info("Failed to get AMCL pose.")
            return

        current_x, current_y = current_pose

        nearest_name, nearest_dist = find_nearest_point(
            current_x,
            current_y,
            point_positions,
        )

        navigator.info(f"Current pose: x={current_x:.3f}, y={current_y:.3f}")
        navigator.info(
            f"Nearest point: {nearest_name}, distance={nearest_dist:.3f} m"
        )

        # Move to the nearest waypoint first.
        if not go_to_pose(navigator, poses[nearest_name], nearest_name):
            return

        # If the robot starts near point1, move to point2 before entering the loop.
        if nearest_name == "point1":
            navigator.info("Arrived at point1. Moving to point2 before patrol loop.")

            if not go_to_pose(navigator, poses["point2"], "point2"):
                return

            next_index = get_next_loop_index(loop_names, "point2")
        else:
            next_index = get_next_loop_index(loop_names, nearest_name)

        # Reduce speed during the patrol section to improve detection stability.
        navigator.info("Entering patrol speed mode.")

        set_nav2_speed(
            control_node,
            PATROL_MAX_VEL_X,
            PATROL_MAX_VEL_THETA,
        )

        navigator.info("Starting waypoint patrol loop.")

        while rclpy.ok():
            target_name = loop_names[next_index]

            if not go_to_pose(navigator, poses[target_name], target_name):
                break

            next_index = (next_index + 1) % len(loop_names)

    except KeyboardInterrupt:
        navigator.info("KeyboardInterrupt received. Stopping patrol.")

    finally:
        navigator.info("Restoring normal speed and shutting down.")

        set_nav2_speed(
            control_node,
            NORMAL_MAX_VEL_X,
            NORMAL_MAX_VEL_THETA,
        )

        try:
            navigator.cancelTask()
        except Exception:
            pass

        control_node.force_stop_robot(1.0)
        control_node.stop_requested = True

        executor.shutdown()
        spin_thread.join(timeout=1.0)

        control_node.destroy_node()
        navigator.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
