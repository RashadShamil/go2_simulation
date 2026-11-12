#!/usr/bin/env python3
"""Module 03: controlled simulated Go2 motion (not for physical robot)."""
import os
import time
import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node

RATE_HZ = 10.0
FORWARD_M_S = 0.10
TURN_RAD_S = 0.20

def command(forward=0.0, turn=0.0):
    msg = Twist()
    msg.linear.x = float(forward)
    msg.angular.z = float(turn)
    return msg

def publish_for(node, publisher, forward, turn, seconds):
    deadline = time.monotonic() + seconds
    while rclpy.ok() and time.monotonic() < deadline:
        publisher.publish(command(forward, turn))
        rclpy.spin_once(node, timeout_sec=0.0)
        time.sleep(1.0 / RATE_HZ)

def main():
    if os.environ.get("ROS_DOMAIN_ID") != "71":
        raise SystemExit("Refusing motion: source office_course/scripts/env.sh (domain 71).")
    rclpy.init()
    node = Node("module03_motion_lab")
    pub = node.create_publisher(Twist, "/cmd_vel", 10)
    try:
        deadline = time.monotonic() + 5.0
        while rclpy.ok() and node.count_subscribers("/cmd_vel") == 0 and time.monotonic() < deadline:
            rclpy.spin_once(node, timeout_sec=0.1)
        if node.count_subscribers("/cmd_vel") == 0:
            raise RuntimeError("No /cmd_vel subscriber. Is the Go2 controller running?")
        node.get_logger().info("Forward: 0.10 m/s for 2 seconds")
        publish_for(node, pub, FORWARD_M_S, 0.0, 2.0)
        node.get_logger().info("Stop for 1 second")
        publish_for(node, pub, 0.0, 0.0, 1.0)
        node.get_logger().info("Turn: 0.20 rad/s for 2 seconds")
        publish_for(node, pub, 0.0, TURN_RAD_S, 2.0)
    except KeyboardInterrupt:
        node.get_logger().warn("Interrupted; attempting stop")
    finally:
        if rclpy.ok():
            node.get_logger().info("Sending stop for 1 second")
            publish_for(node, pub, 0.0, 0.0, 1.0)
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == "__main__":
    main()
