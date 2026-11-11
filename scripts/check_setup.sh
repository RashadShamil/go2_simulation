#!/usr/bin/env bash
set -eo pipefail
source /opt/ros/jazzy/setup.bash
printf '\n=== Ubuntu ===\n'
lsb_release -ds
printf '\n=== ROS ===\n'
echo "ROS_DISTRO=$ROS_DISTRO"
printf '\n=== Gazebo ===\n'
gz sim --version
printf '\n=== GPU: forced Mesa D3D12 ===\n'
if command -v glxinfo >/dev/null 2>&1; then
  GALLIUM_DRIVER=d3d12 glxinfo -B | grep -E 'renderer string|Accelerated|OpenGL version' || true
else
  echo 'Install GPU utility: sudo apt install mesa-utils'
fi
printf '\n=== Workspace ===\n'
if [[ -f ~/go2_ws/install/setup.bash ]]; then echo 'Built workspace found'; else echo 'Workspace not found'; fi
