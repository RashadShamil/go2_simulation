# Module 04 — Coordinate Frames, Rotations, Quaternions and TF2 (complete lesson)

This is a single-sitting module: intuition → equations → code → actual Go2 frames → hands-on Gazebo checks → research pitfalls.

## Learning objectives

1. Explain positions relative to coordinate origins and axes.
2. Transform points between sensor, body, odom and map frames.
3. Use 2D and 3D rigid transforms; invert and compose them.
4. Interpret roll, pitch, yaw and quaternion orientation.
5. Interpret a ROS 2 TF tree, look up time-stamped transformations and distinguish static/dynamic frames.
6. Understand LiDAR extrinsics and motion deskewing for mapping.
7. Run the two saved scripts and diagnose missing or incorrect TF data.

## 1 — Coordinates need a frame

A point described as \`(1,0,0)\` means nothing without a frame. In the robot's body frame (ROS convention: X forward, Y left, Z up), it means 1 m ahead of the robot. In \`map\` it may represent an entirely different location. Robot frame axes rotate with the robot, while map axes do not.

See [REP-103](https://reps.openrobotics.org/rep-0103/) for units, right-handed convention, and camera optical exception (Z forward, X right, Y down).

A 6-DoF pose has position \`(x,y,z)\` and orientation (roll,pitch,yaw or quaternion).

## 2 — Translation and rotation in 2D

A pure translation: \`p_A = p_B + t_A_B\` if the two axes are aligned.

2D yaw rotation (counterclockwise):
\`\`\`
R(theta) = [ cos(theta)  -sin(theta) ]
           [ sin(theta)   cos(theta) ]
\`\`\`

General rigid transform:
\`p_A = R_A_B p_B + t_A_B\`.

**Notation:** \`T_A_B\` maps coordinates written in frame B into frame A. \`t_A_B\` is the origin of frame B expressed in A; \`R_A_B\` orients B's axes with respect to A.

Example: robot origin in office = (2,1), robot yaw = +90° relative to office, obstacle in robot coordinates = (1,0).
\`R(90°)(1,0)=(0,1)\`, so \`p_office=(2,2)\`.

Inverse:
\`p_B=R_A_B^T(p_A-t_A_B)\`.
The inverse rotation of an orthonormal rotation matrix is its transpose.

Run \`python3 office_course/scripts/module04_transform_demo.py\` for a numerical verification of the forward and inverse calculations.

## 3 — 3D rotation

Rotation about the X axis, roll:
\`\`\`
Rx = [1,   0,      0]
     [0, cos(r), -sin(r)]
     [0, sin(r),  cos(r)]
\`\`\`

Rotation about Y, pitch:
\`\`\`
Ry = [ cos(p), 0, sin(p)]
     [      0, 1,      0]
     [-sin(p), 0, cos(p)]
\`\`\`

Rotation about Z, yaw:
\`\`\`
Rz = [cos(y), -sin(y), 0]
     [sin(y),  cos(y), 0]
     [     0,       0, 1]
\`\`\`

For the common ROS fixed-axis roll-pitch-yaw convention, the composed rotation is \`R=Rz(yaw) Ry(pitch) Rx(roll)\`. Rotation order matters: generally \`Rz Ry != Ry Rz\`.

**Gimbal lock:** Euler-angle parameterizations have singularities (e.g. pitch near ±90° for this ordering), so orientation is often transmitted and composed with quaternions.

## 4 — Quaternions

ROS geometry messages store quaternion components in **(x,y,z,w)** order. A unit quaternion has \`x²+y²+z²+w²=1\`.

For rotation by angle \`theta\` around a unit axis \`(ax,ay,az)\`:
\`\`\`
q = (ax sin(theta/2), ay sin(theta/2), az sin(theta/2), cos(theta/2))
\`\`\`

For yaw +90° around Z:
\`q=(0,0,0.70710678,0.70710678)\`.

The quaternion rotates a vector using \`v_rot = q (0,v) q^{-1}\` in quaternion algebra (don't interchange order). Opposite signs q and -q represent the same spatial rotation.

Quaternions avoid Euler-angle singularities in their representation; they still require normalization and careful conventions.

## 5 — Homogeneous transformations and composition

Represent a rigid transform as a 4×4 matrix:
\`\`\`
T_A_B = [ R_A_B   t_A_B ]
        [ 0 0 0      1   ]
\`\`\`

With homogeneous point \`p_B^h=[x,y,z,1]^T\`:
\`p_A^h=T_A_B p_B^h\`.

Transform chaining:
\`T_map_lidar=T_map_odom T_odom_base_footprint T_base_footprint_base_link T_base_link_lidar\`.

The middle frames must match. Matrix multiplication is not commutative.

Inverse:
\`\`\`
inv(T_A_B) = [ R^T  -R^T t ]
             [  0      1   ]
\`\`\`

The complete pose matrix is also an element of \`SE(3)\`, the group of rigid motions in 3D. Rotation matrices belong to \`SO(3)\`. These appear throughout ICP and SLAM optimization.

## 6 — TF2: transforms that vary with time

ROS TF2 manages transformations between named frames and can retrieve the relation between two connected frames at a requested time.

- \`/tf_static\`: fixed relations (body → fixed-mounted sensor, etc.) delivered with transient-local durability.
- \`/tf\`: time-varying transforms (odom → base, joint-moving links) with timestamps.
- \`robot_state_publisher\`: uses URDF/Xacro joint/link geometry and joint states to publish fixed and moving link transforms.
- \`tf2_ros\` Buffer + TransformListener: receives and caches transforms for time-specific lookups.

ROS \`TransformStamped\` includes \`header.frame_id\` (parent), \`child_frame_id\` (child), \`header.stamp\`, and a translation + quaternion. Transform metadata defines child pose relative to parent, and maps child-frame point coordinates to parent-frame coordinates.

CLI:
\`\`\`bash
source office_course/scripts/env.sh
ros2 run tf2_ros tf2_echo odom base_link
ros2 run tf2_ros tf2_echo base_link imu_link
ros2 run tf2_tools view_frames
\`\`\`
Inspect frames.pdf (name may vary). The syntax lists reference/parent first and observed/child second. See the official [Jazzy TF2 introduction](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/Introduction-To-Tf2.html).

Python API: \`buffer.lookup_transform(target_frame, source_frame, time)\`. Use \`Time()\` to request the latest available transform; use the point cloud's actual acquisition timestamp for real sensor processing.

## 7 — Your Go2's real frame setup

From [the Go2 upstream launch](https://github.com/khaledgabr77/unitree_go2_ros2/blob/main/unitree_go2_sim/launch/unitree_go2_launch.py):

\`\`\`text
map  --static identity--> odom
odom --EKF (planar)--> base_footprint
base_footprint --EKF (body pose)--> base_link
base_link --URDF fixed--> trunk --URDF fixed--> imu_link
base_link --URDF fixed--> lidar_l1_link (if L1 enabled)
base_link --URDF fixed--> velodyne_base_link -> velodyne (if enabled)
\`\`\`

The *configured* \`map → odom\` edge is identity, **not** evidence that SLAM is working. Dynamics are estimated by separate EKFs. Some sensors may be excluded by launch flags.

The simulated L1's actual [URDF/Xacro mounting joint](https://github.com/khaledgabr77/unitree_go2_ros2/blob/main/unitree_go2_description/urdf/lidar_4D_lidar.xacro) includes:
\`\`\`xml
<joint name="lidar_l1_joint" type="fixed">
  <parent link="base_link"/>
  <child link="lidar_l1_link"/>
  <origin rpy="2.879 0.0 1.5705" xyz="0.25 -0.038 -0.03"/>
</joint>
\`\`\`
Thus the L1 frame is offset and rotated relative to the robot; it is **not** safe to assume that LiDAR +X is robot +X. The L1 flag in our low-compute launcher disables the simulated L1, so that frame might be absent until enabled.

## 8 — TF2 programming example

Run the included ROS inspector when the simulator is active:
\`\`\`bash
python3 office_course/scripts/module04_tf_inspector.py base_link imu_link 1 0 0
\`\`\`
This requests the transform mapping a 1 m point in \`imu_link\` coordinates to \`base_link\`. It prints the relative translation, quaternion, and transformed point. It also supports other connected frames:
\`\`\`bash
python3 office_course/scripts/module04_tf_inspector.py odom base_link 0 0 0
\`\`\`
That gives the robot base origin's estimated odometry-frame position at the latest available transform.

The script demonstrates the math manually once TF2 supplies the transform. Its output is not a calibrated ground-truth measurement; it is computed from the published frame graph.

## 9 — LiDAR mapping and deskew

Each point in a raw LiDAR scan is initially expressed in sensor coordinates. For mapping:
\`\`\`text
p_map = T_map_lidar(t) * p_lidar
\`\`\`
But a rotating/scanning LiDAR records points over a nonzero duration. The moving robot has different poses for early and late points.

*Deskewing* means accounting for sensor motion throughout a scan, often using per-point timing and interpolated IMU/odometry poses. Treating every point as if captured at the scan's first or last instant creates warped walls and artifacts.

A wrong sensor extrinsic (translation or rotation), wrong transform direction, inconsistent timestamps or incorrect coordinate convention may produce doubled walls and distorted registration even with a correct ICP algorithm.

When comparing simulated LiDAR with real Go2 EDU Hesai or Unitree L1 measurements, do **not** assume the simulator's mounting geometry equals the real hardware configuration. Check calibrated extrinsics, real topic frame IDs and timestamps.

## 10 — Troubleshooting

- **Unknown frame:** frame not published, misspelled, sensor disabled or wrong namespace.
- **Could not transform / disconnected trees:** missing edge or inconsistent child/parent naming.
- **Extrapolation into future/past:** requested timestamp is outside available TF buffer interval, or different clock domains.
- **RViz "No transform":** verify Fixed Frame, point cloud's \`header.frame_id\`, TF connection and time.
- **Map seems rotated/mirrored:** check handedness, rotation order, quaternion order, camera optical convention and inversion.
- **Cloud shifts with robot unexpectedly:** probably using a stale/incorrect sensor-to-world transform.
- **Wrong alignment during motion:** check timestamp synchronization and scan deskew.
- **Transform duplicates:** only one broadcaster should own a dynamic parent→child relationship.

## 11 — Single-session practical workflow

1. Verify Gazebo Go2 and both controllers.
2. Source the **same** ROS domain as the running simulation (\`71\` for the office launcher).
3. \`ros2 topic list | grep -E '^/tf$|^/tf_static$'\`.
4. \`ros2 run tf2_tools view_frames\`; inspect frame tree.
5. \`ros2 run tf2_ros tf2_echo odom base_link\` and \`... base_link imu_link\`.
6. Run \`python3 office_course/scripts/module04_transform_demo.py\` and verify the arithmetic.
7. Run \`python3 office_course/scripts/module04_tf_inspector.py base_link imu_link 1 0 0\`.
8. If convenient, observe changing odom→base_link TF while driving; DO NOT drive the real robot or enable competing publishers.
9. Write a table: frame pair, static/dynamic, transform owner, measured translation, quaternion, timestamp.
10. Save observations to a lab log. Never claim a simulated sensor's transform has been calibrated on the physical robot without validation.

## 12 — Worked checks

**A:** Robot origin (2,1), yaw 90°, a robot-frame point (1,0): result **(2,2)** in office.

**B:** Robot pose (2,1,90°), office-frame point (2,2): inverse-transformed result **(1,0)** in robot.

**C:** 90° Z-rotation quaternion (x,y,z,w): **(0,0,√2/2,√2/2)**.

**D:** Sensor-to-base fixed offset (0.25,-0.038,-0.03) with nonzero RPY: translating points without rotating them is **incorrect**.

**E:** Static \`map → odom\` edge: does it remove odometry drift? **No**. There is no localization-driven correction yet.

## 13 — Mastery questions

1. Can two different coordinate triples describe the same physical chair? Why?
2. What does \`T_A_B\` mean, and which direction does it convert points?
3. Derive the 2D rotation matrix and compute a 90° example.
4. Why can't we reverse a transform by negating only translation?
5. Why is \`R^T\` the inverse of a proper rotation matrix?
6. Why are quaternions preferred for composing 3D orientation?
7. Which TF links are static vs dynamic in the Go2?
8. Why is the \`map\` to \`odom\` relation static in this simulation?
9. What happens if you use a LiDAR scan timestamp but a TF from a later robot pose?
10. What is the difference between sensor extrinsic calibration and SLAM pose estimation?

**Completion:** Explain a full \`LiDAR → base_link → odom → map\` transform chain, implement its numerical composition, and identify source/target frames and timestamps correctly. Next module: practical state estimation and sensor fusion.
