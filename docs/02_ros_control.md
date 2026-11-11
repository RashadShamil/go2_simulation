# Module 02 — ROS 2 velocity control and your first script

## Control chain

```text
Your keyboard or Python code
          |
          |  /cmd_vel (geometry_msgs/msg/Twist)
          v
CHAMP quadruped controller
          |
          |  gait / joint trajectory requests
          v
ros2_control controllers
          |
          v
Gazebo physics + joint movement
```

The verified upstream launch remaps `/cmd_vel/smooth` to `/cmd_vel`; its controller publishes commands toward `joint_group_effort_controller/joint_trajectory`.

## Understand Twist

`geometry_msgs/msg/Twist` has two 3D vectors:

```text
linear:  x, y, z   # requested translational velocity (m/s)
angular: x, y, z   # requested rotational velocity (rad/s)
```

For basic flat-ground control, `linear.x` is forward/backward and `angular.z` is yaw/turn rate. **Twist is a request, not a guarantee that the robot reached that velocity.** The gait controller and physical interaction determine the resulting motion.

## Discover command interface

```bash
source /opt/ros/jazzy/setup.bash
source ~/go2_ws/install/setup.bash
ros2 topic list -t
ros2 topic info /cmd_vel -v
ros2 interface show geometry_msgs/msg/Twist
ros2 control list_controllers
```

Do not proceed until there is at least one `/cmd_vel` subscriber and the gait controllers are ready. The launch intentionally starts some controllers with a delay.

## Keyboard (one operator at a time)

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

Use `i` to move forward, `j/l` to rotate, `,` to reverse, and `k` to stop. Start at low speeds. Stop keyboard teleop before starting the Python script.

## One-shot stop command

```bash
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist \
'{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}'
```

## Your first original motion script

```bash
python3 ~/go2_simulation_lab/scripts/demo_motion.py \
  --forward-seconds 2 --turn-seconds 1 \
  --speed 0.10 --yaw-rate 0.25
```

The script publishes at 10 Hz. It sends several stop messages at the end, including on Ctrl+C where possible. It is for **the simulator only**. Never reuse automatic movement commands on the physical Go2 without separate safety procedures, limits and an emergency stop.

## Exercises

1. Start with the Python program's defaults and watch the Go2 move forward then turn.
2. Change `--forward-seconds` to `1.0`. Compare the travel distance using odometry.
3. Keep command duration fixed, halve the speed, and compare measured displacement.
4. Explain why integrating `speed × time` is only an approximation of robot motion.

## Troubleshooting

- Robot visible but no movement: simulation paused, wrong topic, zero subscribers, controller not active, or initialization still in progress.
- Erratic movement: two teleop/publisher processes simultaneously commanding `/cmd_vel`.
- Simulation time very slow: check Gazebo real-time factor and WSL GPU; heavy sensors can add load.
