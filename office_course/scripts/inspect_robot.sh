#!/usr/bin/env bash
set -eo pipefail
COURSE_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
source "$COURSE_DIR/scripts/env.sh"
echo "ROS_DISTRO=$ROS_DISTRO ROS_DOMAIN_ID=$ROS_DOMAIN_ID"
ros2 topic list
ros2 topic info /cmd_vel -v || true
ros2 control list_controllers || true
