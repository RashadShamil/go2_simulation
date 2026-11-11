#!/usr/bin/env bash
set -eo pipefail
COURSE_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
source "$COURSE_DIR/scripts/env.sh"
WORLD="$COURSE_DIR/worlds/office_lab.sdf"
if [ ! -f "$WORLD" ]; then
  python3 "$COURSE_DIR/scripts/generate_office_world.py"
fi
GO2_LAUNCH="${GO2_WS:-$HOME/go2_ws}/src/unitree_go2_ros2/unitree_go2_sim/launch/unitree_go2_launch.py"
if [ -f "$GO2_LAUNCH" ] && ! grep -q -- '--render-engine ogre' "$GO2_LAUNCH"; then
  echo 'WARNING: Go2 launch file does not appear to include --render-engine ogre.' >&2
  echo 'The Gazebo GUI may try OGRE2 and fail under WSL.' >&2
fi
printf 'Starting office world: %s\nROS_DOMAIN_ID=%s\n' "$WORLD" "$ROS_DOMAIN_ID"
exec ros2 launch unitree_go2_sim unitree_go2_launch.py \
  world:="$WORLD" \
  world_init_x:=0.0 world_init_y:=0.0 world_init_z:=0.375 world_init_heading:=0.0 \
  rviz:=false \
  disable_camera:=true disable_d455:=true \
  disable_lidar_l1:=true disable_velodyne_lidar:=true
