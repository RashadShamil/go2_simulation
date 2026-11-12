# Module 03 — Robot Control and Locomotion: Complete Lesson

**Prerequisites:** Module 01 (Gazebo), Module 02 (ROS 2 fundamentals/intro EKF), an office world containing the Go2, and both ROS 2 controllers active.

**Verified checkpoint, November 2026:** `joint_states_controller` (JointStateBroadcaster) and `joint_group_effort_controller` (JointTrajectoryController) were reported ACTIVE in ROS domain 71. Motion itself has not been confirmed.

## 1 — Learning goals

Understand the command pipeline; define links, joints, actuators, control interfaces, ROS controllers and Gazebo dynamics; study gaits and kinematics; operate the robot with Twist commands and a complete Python publisher; compare commands with odometry; record and troubleshoot repeatable experiments.

## 2 — Control pipeline

`Python/teleop` → ROS topic `/cmd_vel` (Twist) → CHAMP `quadruped_controller_node` → planned foot trajectories → inverse kinematics → 12-joint JointTrajectory → `joint_group_effort_controller` → 12 effort interfaces via `gz_ros2_control` → Gazebo dynamics → joint states/foot contacts/odometry.

This comes from upstream [quadruped_controller.cpp](https://github.com/khaledgabr77/unitree_go2_ros2/blob/main/champ_base/src/quadruped_controller.cpp) and [launch file](https://github.com/khaledgabr77/unitree_go2_ros2/blob/main/unitree_go2_sim/launch/unitree_go2_launch.py).

## 3 — Robot structure and coordinates

Each leg has three actuated joints (hip abduction/adduction, hip pitch, knee). Four legs → 12 actuators. Upstream uses names `lf/rf/lh/rh_{hip,upper_leg,lower_leg}_joint`. Joint rotations are in radians, angular rates rad/s, effort generally torque in N·m.

For ROS Twist commands, `linear.x` requests forward movement (m/s), `linear.y` sideways movement (m/s), and `angular.z` heading rate (rad/s). Only those fields are used by this CHAMP controller's `cmdVelCallback_`. A Twist is a requested speed, not a goal position or a guarantee of displacement.

## 4 — Gaits

A gait coordinates phases of feet. Each foot alternates between *stance* (supporting/pushing against the ground) and *swing* (lift/reposition). Typical families include walk, trot (diagonal pairs), pace (same-side pairs) and bound (front/rear pairs). This package's motion is generated through CHAMP's leg controller. Changing the gait parameters is not equivalent to supplying a named gait-switching interface.

The checked-in [gait YAML](https://github.com/khaledgabr77/unitree_go2_ros2/blob/main/unitree_go2_sim/config/gait/gait.yaml) sets:
- max x speed 0.3 m/s; max y speed 0.25 m/s; max yaw rate 0.5 rad/s
- swing height 0.04 m, stance depth 0.01 m, stance duration 0.25 s, nominal height 0.225 m
- odom_scaler 0.9

These are configuration values, **not measured guarantees**.

## 5 — Kinematics

**Forward kinematics (FK)**: given joint angles, compute foot location. Simplified 2-link planar model (not the complete Go2 3-DoF leg):
`x=L1 cos(q1)+L2 cos(q1+q2)`
`z=L1 sin(q1)+L2 sin(q1+q2)`.

**Inverse kinematics (IK)**: given desired foot position, solve required joint angles:
`D=(x²+z²-L1²-L2²)/(2 L1 L2)`;
`q2=acos(D)`;
`q1=atan2(z,x)-atan2(L2 sin q2, L1+L2 cos q2)`.
Reachable targets require `|D|<=1`. Actual CHAMP accounts for hip abduction/adduction, robot-specific geometry, and knee conventions.

## 6 — Joint control and feedback

A `joint_state_broadcaster` exposes measured positions/velocities. The `joint_trajectory_controller` consumes desired angles and times, computes tracking error, and uses configured effort command interfaces. The upstream configuration includes per-joint PID gains (P=100, I=0.2, D=1). Conceptually a PID controller computes `u=Kp e + Ki integral(e) + Kd derivative(e)`; real implementation includes controller-specific protections/limits.

CHAMP's code runs a nominal 200 Hz gait loop, publishing a `JointTrajectory` containing twelve target positions with a point at 1/60 s. The ROS 2 controller manager is configured for 250 Hz. Those are code/configuration targets; real-time performance may be lower under WSL.

Inspect:
```bash
source office_course/scripts/env.sh
ros2 control list_controllers
ros2 topic info /cmd_vel -v
ros2 topic list | grep -E 'joint|odom|clock'
ros2 topic echo /joint_states --once
ros2 topic info /joint_group_effort_controller/joint_trajectory -v
```

## 7 — Run the experiment

Terminal 1:
```bash
cd /mnt/c/Users/shami/OneDrive/Documents/GitHub/go2_simulation_lab
bash office_course/scripts/start_office_go2.sh
```

Terminal 2:
```bash
cd /mnt/c/Users/shami/OneDrive/Documents/GitHub/go2_simulation_lab
source office_course/scripts/env.sh
ros2 control list_controllers
python3 office_course/scripts/module03_motion_lab.py
```

**Important:** Close other `/cmd_vel` publishers, disconnect the physical robot and verify Gazebo is not paused. The code requests forward 0.1 m/s for 2 s; then zero velocity for 1 s; then yaw +0.2 rad/s for 2 s; and publishes a final stop. Timeouts/safety stops are best-effort and not emergency stops.

Theoretical no-slip displacement `d=v·t=0.2 m`; theoretical yaw `Δθ=ωt=0.4 rad ≈ 22.9°`. These are command integrals, **not** measured motion.

## 8 — Compare requested motion with estimated motion

Observe `/cmd_vel`, `/odom/raw`, `/odom` and `/odom/ground_truth` when available. `/cmd_vel` is desired motion; `/odom` is fused estimated motion; `/odom/ground_truth` is Gazebo model-based reference, not a perfect sensor.

For 2D pose `(x0,y0)→(x1,y1)`, displacement `d=sqrt((x1-x0)^2+(y1-y0)^2)`. Tracking error is `d_measured - d_commanded`; heading error is the wrapped difference between actual and requested angle. Compare traces over time, not just end positions; account for simulation pause, drift and timestamps.

Optional recorder:
```bash
bash office_course/scripts/record_experiment.sh
```
The existing recorder captures `/cmd_vel /odom /joint_states /tf /tf_static /clock`; to compare Gazebo ground truth add `/odom/ground_truth` when present. Store run metadata and controller parameters.

## 9 — Troubleshooting

- No robot: verify the office world and Gazebo model list; spawning manually with `-world office_lab` was a known working fallback.
- No controller manager: verify the correct ROS domain and Gazebo `gz_ros2_control` plugin logs.
- Controller inactive: inspect configured controllers and spawner output before sending commands.
- Zero subscribers on `/cmd_vel`: verify CHAMP node, namespace and remapping.
- Legs move but body does not: inspect ground contacts, leg trajectories, stance/swing, friction, joint efforts.
- Robot falls or shakes: inspect gains, initial pose, gravity, contact parameters and WSL physics step performance.
- Odometry absent: inspect `/clock`, joint states, IMU and contact data; EKFs depend on valid inputs.

## 10 — Completion criteria

- Automatically spawn Go2 in office.
- Both joint controllers ACTIVE.
- Send velocity command from Python and achieve observable movement.
- Measure joints, pose and odometry.
- Explain CHAMP gait, inverse kinematics, PID tracking and physics feedback.
- Record a reproducible experiment and explain any mismatch between command and actual movement.

**Next:** Module 04 — TF, coordinate transforms, rotation matrices, quaternions and frame consistency.
