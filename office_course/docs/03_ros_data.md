# Lesson 03 — ROS 2 state and coordinate frames

`/clock` represents simulation time. `/odom` is a local motion estimate that may drift; Gazebo visual pose is not the same as estimated odometry. `/joint_states` provides joint positions and velocities. TF connects frames such as `map`, `odom`, and `base_link`; inspect actual frame names rather than guessing.

```bash
source office_course/scripts/env.sh
ros2 topic list
ros2 topic info /cmd_vel -v
ros2 topic echo /odom --once
ros2 topic echo /joint_states --once
bash office_course/scripts/record_experiment.sh
```

Stop the recorder with Ctrl+C; inspect it with `ros2 bag info <directory>`.

**Log:** exact topic names/types and which frames are truly published.
