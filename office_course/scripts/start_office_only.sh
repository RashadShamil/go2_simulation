#!/usr/bin/env bash
set -eo pipefail
COURSE_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
source /opt/ros/jazzy/setup.bash
export GALLIUM_DRIVER=d3d12
if [ ! -f "$COURSE_DIR/worlds/office_lab.sdf" ]; then
  python3 "$COURSE_DIR/scripts/generate_office_world.py"
fi
exec gz sim -v 3 "$COURSE_DIR/worlds/office_lab.sdf" --render-engine ogre
