#!/usr/bin/env bash
set -eo pipefail
source /opt/ros/jazzy/setup.bash
if [[ -f "$HOME/go2_ws/install/setup.bash" ]]; then source "$HOME/go2_ws/install/setup.bash"; fi
for _ in 1 2 3; do
  ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist \
    '{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}'
done
printf 'Sent 3 zero-velocity commands. Check robot visually.\n'
