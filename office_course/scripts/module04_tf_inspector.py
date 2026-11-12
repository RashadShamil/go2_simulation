#!/usr/bin/env python3
"""Module 04: Query a TF2 transform and transform a 3D point.

Usage (in the same ROS domain as your simulator):
  python3 office_course/scripts/module04_tf_inspector.py base_link imu_link 1 0 0

The first frame is the TARGET, the second is the SOURCE.
Example above converts a 1 m forward point from imu_link to base_link.
"""
import argparse
import math
import time

import rclpy
from rclpy.node import Node
from rclpy.time import Time
from tf2_ros import Buffer, TransformListener, TransformException


def rotate_by_quaternion(point, quat):
    """Rotate a 3D vector by quaternion q=(x,y,z,w)."""
    qx, qy, qz, qw = quat
    norm = math.sqrt(qx*qx+qy*qy+qz*qz+qw*qw)
    if norm == 0.0:
        raise ValueError("Invalid zero quaternion")
    qx, qy, qz, qw = [v/norm for v in (qx,qy,qz,qw)]
    vx, vy, vz = point
    cx, cy, cz = qy*vz-qz*vy, qz*vx-qx*vz, qx*vy-qy*vx
    dx, dy, dz = qy*cz-qz*cy, qz*cx-qx*cz, qx*cy-qy*cx
    return (vx+2*(qw*cx+dx),vy+2*(qw*cy+dy),vz+2*(qw*cz+dz))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", help="frame to express coordinates in, e.g. base_link")
    parser.add_argument("source", help="frame in which point is initially expressed, e.g. imu_link")
    parser.add_argument("px", nargs="?", type=float, default=1.0)
    parser.add_argument("py", nargs="?", type=float, default=0.0)
    parser.add_argument("pz", nargs="?", type=float, default=0.0)
    args = parser.parse_args()

    rclpy.init()
    node = Node("module04_tf_inspector")
    # A TF listener collects /tf and /tf_static messages in the buffer.
    buffer = Buffer()
    listener = TransformListener(buffer, node)
    deadline = time.monotonic()+10.0
    transform = None
    error = None
    try:
        while rclpy.ok() and time.monotonic()<deadline:
            rclpy.spin_once(node, timeout_sec=0.1)
            try:
                # Time() == 0 asks for the most recent common available time.
                transform = buffer.lookup_transform(args.target,args.source,Time())
                break
            except TransformException as exc:
                error = exc
        if transform is None:
            raise RuntimeError(f"No transform {args.source} -> {args.target}: {error}")
        t = transform.transform.translation
        q = transform.transform.rotation
        source_point = (args.px,args.py,args.pz)
        rotated = rotate_by_quaternion(source_point, (q.x,q.y,q.z,q.w))
        destination_point = (rotated[0]+t.x,rotated[1]+t.y,rotated[2]+t.z)
        print(f"Transform: {args.source} -> {args.target}")
        print(f"Translation: ({t.x:.5f}, {t.y:.5f}, {t.z:.5f}) m")
        print(f"Quaternion (x,y,z,w): ({q.x:.5f}, {q.y:.5f}, {q.z:.5f}, {q.w:.5f})")
        print(f"Point in {args.source}: {source_point} m")
        print(f"Same point in {args.target}: {tuple(round(v,5) for v in destination_point)} m")
        print("NOTE: uses latest available transform. Real sensor processing should query at measurement timestamp.")
    finally:
        # Keep a reference to the listener until the node is destroyed.
        _ = listener
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__=="__main__":
    main()
