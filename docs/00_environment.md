# Module 00 — Environment and reproducibility

## What we know from the first installation

| Component | Verified observation |
|---|---|
| Ubuntu | 24.04 (user confirmed) |
| ROS distribution | Jazzy (`echo $ROS_DISTRO`) |
| Gazebo Sim | 8.15.0 (`gz sim --version`) |
| Graphics | `D3D12 (Intel(R) Iris(R) Xe Graphics)` with `Accelerated: yes` when `GALLIUM_DRIVER=d3d12` |
| Rendering engine | `ogre` worked smoothly with the shapes world |
| Previous failure | `llvmpipe` software rendering was slow; OGRE2 session exited with code 1 and `/dev/dri` warnings |
| Robot spawn | The user has seen the Go2 in Gazebo |
| Source checkout | `~/go2_ws/src/unitree_go2_ros2` (per installation steps; verify locally) |

## Why the GPU workaround mattered

`llvmpipe` runs OpenGL rasterization on the CPU. Mesa's `d3d12` driver routes rendering to the Windows GPU stack exposed through WSLg. This machine reported Intel Iris Xe, acceleration enabled, and OpenGL 4.1 on D3D12. OGRE2 may not work reliably with this combination; the older OGRE renderer worked in the shapes world. This is an **environment-specific workaround**, not a general rule for every Gazebo installation.

## Verify anytime

```bash
source /opt/ros/jazzy/setup.bash
echo "$ROS_DISTRO"
gz sim --version
GALLIUM_DRIVER=d3d12 glxinfo -B | grep -E 'renderer string|Accelerated|OpenGL version'
lsb_release -a
```

## ROS and Gazebo separation

Gazebo **simulates** the world, contacts, motors, sensors and clock. ROS 2 supplies **messages, nodes, commands, transformations and pipelines**. `ros_gz_bridge` connects selected Gazebo messages to ROS topics. RViz **visualizes** the data; it is not the physics simulator.

## Protect the setup

- Keep ROS 2 Foxy on Ubuntu 20.04 in a separate WSL distribution, if needed for legacy mapping scripts.
- Do not source Foxy and Jazzy in the same shell.
- Do not add third-party launch-file edits without recording them (`git diff`).
- If the Go2 GUI unexpectedly uses OGRE2, inspect `~/go2_ws/src/unitree_go2_ros2/unitree_go2_sim/launch/unitree_go2_launch.py` and verify its `gz_args` includes `--render-engine ogre`. This was a local modification in the installation instructions and may be lost on an upstream reset.

## Record exact dependency versions for reproducibility

```bash
apt-cache policy ros-jazzy-desktop ros-jazzy-ros-gz gz-harmonic
cd ~/go2_ws/src/unitree_go2_ros2 && git rev-parse HEAD && git diff --stat
```
