# Lesson 02 — Go2 motion and /cmd_vel

The simulated Go2 uses a robot description (URDF/Xacro), controllers, and locomotion software. A `geometry_msgs/msg/Twist` command specifies linear (m/s) and angular (rad/s) velocity; the leg controller translates a velocity request into joint motions.

**Terminal 1**
```bash
bash office_course/scripts/start_office_go2.sh
```

**Terminal 2**
```bash
source office_course/scripts/env.sh
ros2 topic info /cmd_vel -v
ros2 control list_controllers
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

Stop keyboard teleop before starting the automated publisher:
```bash
python3 office_course/scripts/demo_office_motion.py
```

If Go2 does not move, verify a subscriber on `/cmd_vel`, the controller state and whether simulation time is advancing. Always disconnect from the physical robot during simulator experiments.
