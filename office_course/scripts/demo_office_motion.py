#!/usr/bin/env python3
"""Sim-only low-speed motion demo. Disconnect from the physical robot first."""
import os
import time

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node


class OfficeMotion(Node):
    def __init__(self):
        super().__init__('office_motion_demo')
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)

    def send_for(self, vx, yaw_rate, seconds):
        msg = Twist()
        msg.linear.x = float(vx)
        msg.angular.z = float(yaw_rate)
        start = time.monotonic()
        while time.monotonic() - start < seconds and rclpy.ok():
            self.publisher.publish(msg)
            rclpy.spin_once(self, timeout_sec=0.01)
            time.sleep(0.1)

    def stop(self):
        for _ in range(10):
            self.publisher.publish(Twist())
            time.sleep(0.1)


def main():
    if os.environ.get('ROS_DOMAIN_ID') != '71':
        raise SystemExit('Use office_course/scripts/env.sh first (ROS_DOMAIN_ID must be 71).')
    rclpy.init()
    node = OfficeMotion()
    try:
        node.get_logger().info('Low-speed forward motion, then turn, in SIMULATED office')
        node.send_for(0.10, 0.0, 2.0)
        node.stop()
        node.send_for(0.0, 0.22, 2.0)
        node.stop()
    except KeyboardInterrupt:
        pass
    finally:
        node.stop()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
