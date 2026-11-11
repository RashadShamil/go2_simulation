#!/usr/bin/env bash
set -o pipefail
LAB_DIR="$HOME/go2_simulation_lab"
mkdir -p "$LAB_DIR/experiments"
STAMP="$(date +%Y%m%d_%H%M%S)"
OUT="$LAB_DIR/experiments/snapshot_${STAMP}.txt"
source /opt/ros/jazzy/setup.bash
if [[ -f "$HOME/go2_ws/install/setup.bash" ]]; then source "$HOME/go2_ws/install/setup.bash"; fi
{
  echo "Snapshot (local): $(date --iso-8601=seconds)"
  echo "Ubuntu: $(lsb_release -ds)"
  echo "ROS: $ROS_DISTRO"
  gz sim --version
  echo "GPU rendering:"
  GALLIUM_DRIVER=d3d12 glxinfo -B | grep -E 'renderer string|Accelerated' || true
  echo "Upstream checkout:"
  git -C "$HOME/go2_ws/src/unitree_go2_ros2" rev-parse HEAD 2>/dev/null || true
  git -C "$HOME/go2_ws/src/unitree_go2_ros2" status --short 2>/dev/null || true
  echo "ROS nodes:"
  timeout 8s ros2 node list || true
  echo "ROS topics:"
  timeout 8s ros2 topic list -t || true
  echo "ROS controllers:"
  timeout 8s ros2 control list_controllers || true
  echo "cmd_vel endpoint info:"
  timeout 8s ros2 topic info /cmd_vel -v || true
} > "$OUT" 2>&1
printf 'Saved session snapshot: %s\n' "$OUT"
