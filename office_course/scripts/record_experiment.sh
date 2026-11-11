#!/usr/bin/env bash
set -eo pipefail
COURSE_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
source "$COURSE_DIR/scripts/env.sh"
mkdir -p "$COURSE_DIR/experiments"
OUT="$COURSE_DIR/experiments/rosbag_$(date +%Y%m%d_%H%M%S)"
echo "Recording to $OUT (Ctrl+C to stop)"
exec ros2 bag record -o "$OUT" /cmd_vel /odom /joint_states /tf /tf_static /clock
