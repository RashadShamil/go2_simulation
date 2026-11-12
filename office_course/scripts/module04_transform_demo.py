#!/usr/bin/env python3
"""Module 04: 2D and 3D frame transforms, using only the Python stdlib.

Convention: T_A_B maps coordinates expressed in B into coordinates in A.
"""
import math


def transform_2d(p_b, yaw_rad, translation_a):
    """p_A = R_A_B p_B + t_A_B, positive yaw = counter-clockwise."""
    x, y = p_b
    tx, ty = translation_a
    c, s = math.cos(yaw_rad), math.sin(yaw_rad)
    return (c*x - s*y + tx, s*x + c*y + ty)


def inverse_transform_2d(p_a, yaw_rad, translation_a):
    """Inverse of the previous transform: p_B = R^T(p_A - t)."""
    x, y = p_a
    tx, ty = translation_a
    c, s = math.cos(yaw_rad), math.sin(yaw_rad)
    dx, dy = x - tx, y - ty
    return (c*dx + s*dy, -s*dx + c*dy)


def quat_from_yaw(yaw_rad):
    """ROS quaternion order (x,y,z,w), for a pure Z-axis rotation."""
    return (0.0, 0.0, math.sin(yaw_rad/2.0), math.cos(yaw_rad/2.0))


def rotate_vector_by_quat(v, q):
    """Rotate 3D vector v by unit quaternion q = (qx,qy,qz,qw)."""
    qx, qy, qz, qw = q
    norm = math.sqrt(qx*qx+qy*qy+qz*qz+qw*qw)
    if norm == 0:
        raise ValueError("Zero quaternion is not a rotation")
    qx, qy, qz, qw = (part/norm for part in (qx,qy,qz,qw))
    x, y, z = v
    # q * (v,0) * conjugate(q), written with cross products.
    cx, cy, cz = qy*z-qz*y, qz*x-qx*z, qx*y-qy*x
    c2x, c2y, c2z = qy*cz-qz*cy, qz*cx-qx*cz, qx*cy-qy*cx
    return (x+2*(qw*cx+c2x), y+2*(qw*cy+c2y), z+2*(qw*cz+c2z))


def close_tuple(actual, expected, tolerance=1e-9):
    assert all(abs(a-b)<tolerance for a,b in zip(actual,expected)), (actual,expected)


def main():
    p_robot = (1.0, 0.0)  # 1 m in front of robot
    yaw = math.radians(90.0)
    robot_origin_in_office = (2.0, 1.0)
    p_office = transform_2d(p_robot, yaw, robot_origin_in_office)
    recovered = inverse_transform_2d(p_office, yaw, robot_origin_in_office)
    q = quat_from_yaw(yaw)
    p3_rotated = rotate_vector_by_quat((1.0, 0.0, 0.0), q)
    close_tuple(p_office, (2.0, 2.0))
    close_tuple(recovered, p_robot)
    close_tuple(p3_rotated, (0.0, 1.0, 0.0))
    print("Robot-frame point:", p_robot)
    print("Robot origin in office:", robot_origin_in_office)
    print("Robot yaw: 90 degrees CCW")
    print("Office-frame point:", tuple(round(v,4) for v in p_office))
    print("Inverse transform (back to robot frame):",tuple(round(v,4) for v in recovered))
    print("ROS quaternion x,y,z,w:",tuple(round(v,4) for v in q))
    print("Quaternion rotation of (1,0,0):",tuple(round(v,4) for v in p3_rotated))
    print("PASS: forward, inverse and quaternion transformations agree.")


if __name__ == "__main__":
    main()
