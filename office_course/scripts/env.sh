#!/usr/bin/env bash
# Source once in each terminal. Do not enable "set -u" before sourcing ROS.
source /opt/ros/jazzy/setup.bash
source "${GO2_WS:-$HOME/go2_ws}/install/setup.bash"
export GALLIUM_DRIVER=d3d12
export ROS_DOMAIN_ID="${GO2_SIM_DOMAIN_ID:-71}"
