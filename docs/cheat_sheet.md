# Reusable command cheat sheet

## Every new terminal

```bash
source /opt/ros/jazzy/setup.bash
source ~/go2_ws/install/setup.bash
```

## Gazebo graphics check

```bash
GALLIUM_DRIVER=d3d12 glxinfo -B | grep -E 'renderer string|Accelerated'
GALLIUM_DRIVER=d3d12 gz sim -v 3 shapes.sdf --render-engine ogre
```

## Simulated Go2 launch (sensor-light)

```bash
bash ~/go2_simulation_lab/scripts/start_go2.sh
```

## ROS diagnostics

```bash
ros2 node list
ros2 topic list -t
ros2 topic info /cmd_vel -v
ros2 topic echo /cmd_vel --once
ros2 topic hz /odom
ros2 control list_controllers
ros2 run tf2_tools view_frames
```

## Teleop or scripted movement (never at the same time)

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
python3 ~/go2_simulation_lab/scripts/demo_motion.py --forward-seconds 2 --turn-seconds 1
```

## Stop

```bash
bash ~/go2_simulation_lab/scripts/stop_robot.sh
```

## Capture an experiment snapshot

```bash
bash ~/go2_simulation_lab/scripts/snapshot_session.sh
```

## Rebuild the upstream workspace after edits

```bash
cd ~/go2_ws
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install --parallel-workers 2
source install/setup.bash
```

## See local modifications to the third-party simulator

```bash
cd ~/go2_ws/src/unitree_go2_ros2
git status --short
git diff -- unitree_go2_sim/launch/unitree_go2_launch.py
git rev-parse HEAD
```
