#!/usr/bin/env bash
set -eo pipefail

WORKSPACE="${GO2_WS:-$HOME/go2_ws}"
source /opt/ros/jazzy/setup.bash
if [[ ! -f "$WORKSPACE/install/setup.bash" ]]; then
  echo "Missing workspace install/setup.bash: $WORKSPACE" >&2
  echo "Build it first: cd $WORKSPACE && colcon build --symlink-install" >&2
  exit 1
fi
source "$WORKSPACE/install/setup.bash"

# Mesa's D3D12 GPU renderer fixes llvmpipe CPU rendering on this WSL laptop.
export GALLIUM_DRIVER=d3d12
LAUNCH="$WORKSPACE/src/unitree_go2_ros2/unitree_go2_sim/launch/unitree_go2_launch.py"
if [[ -f "$LAUNCH" ]] && ! grep -q -- '--render-engine ogre' "$LAUNCH"; then
  echo "WARNING: upstream launch file does not appear to request OGRE." >&2
  echo "          This system required '--render-engine ogre' in gz_args." >&2
  echo "          See docs/00_environment.md before launching." >&2
fi

echo "Launching Go2 with camera + 3D LiDAR disabled for performance."
echo "Wait for controllers to become active before sending /cmd_vel."
exec ros2 launch unitree_go2_sim unitree_go2_launch.py \
  rviz:=false \
  disable_camera:=true \
  disable_d455:=true \
  disable_lidar_l1:=true \
  disable_velodyne_lidar:=true \
  "$@"
