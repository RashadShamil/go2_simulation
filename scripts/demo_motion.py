#!/usr/bin/env python3
"""First original Go2 simulation script: slow forward motion, then slow yaw.

Only use with the local Gazebo Go2 simulation; not intended for real hardware.
Launch simulator and wait until controllers are active before running this.
Do not run teleop_twist_keyboard at the same time.
"""

import argparse
import time

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node


class Go2Demo(Node):
    def __init__(self):
        super().__init__('go2_lab_demo_motion')
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)

    def send(self, forward: float = 0.0, yaw: float = 0.0) -> None:
        command = Twist()
        command.linear.x = forward
        command.angular.z = yaw
        self.publisher.publish(command)

    def move_for(self, seconds: float, forward: float = 0.0, yaw: float = 0.0):
        end = time.monotonic() + seconds
        # Repeated publishing is more reliable than a one-shot velocity command.
        while rclpy.ok() and time.monotonic() < end:
            self.send(forward, yaw)
            time.sleep(0.1)
        self.stop()

    def stop(self):
        # Publish a short burst of zero Twist messages to ensure it is received.
        for _ in range(5):
            self.send()
            time.sleep(0.1)


def main():
    parser = argparse.ArgumentParser(description='Move simulated Go2 forward and turn.')
    parser.add_argument('--forward-seconds', type=float, default=2.0)
    parser.add_argument('--turn-seconds', type=float, default=1.0)
    parser.add_argument('--speed', type=float, default=0.10, help='m/s')
    parser.add_argument('--yaw-rate', type=float, default=0.25, help='rad/s')
    args = parser.parse_args()

    if not (0.0 <= args.forward_seconds <= 5.0 and 0.0 <= args.turn_seconds <= 5.0):
        parser.error('Each duration must be between 0 and 5 seconds')
    if not (0.0 <= args.speed <= 0.20 and 0.0 <= args.yaw_rate <= 0.40):
        parser.error('Use low simulated speeds: speed 0-0.20 m/s, yaw 0-0.40 rad/s')

    rclpy.init()
    node = Go2Demo()
    try:
        deadline = time.monotonic() + 15.0
        while node.count_subscribers('/cmd_vel') == 0 and time.monotonic() < deadline:
            time.sleep(0.25)
        if node.count_subscribers('/cmd_vel') == 0:
            raise RuntimeError('No /cmd_vel subscriber; verify the Go2 simulation and controller')
        node.get_logger().info('Starting slow forward movement')
        node.move_for(args.forward_seconds, forward=args.speed)
        node.get_logger().info('Starting slow left turn')
        node.move_for(args.turn_seconds, yaw=args.yaw_rate)
        node.get_logger().info('Motion demonstration complete')
    except KeyboardInterrupt:
        node.get_logger().warn('Ctrl+C received — stopping')
    finally:
        node.stop()
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
