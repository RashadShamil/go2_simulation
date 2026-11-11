# Unitree Go2 Office Simulation Course

**Ubuntu 24.04 · ROS 2 Jazzy · Gazebo Harmonic 8.15 · WSL2 · Intel Iris Xe**

This folder contains a **fictional 8 m × 6 m office**, not the user's real working environment. Its dimensions and furniture are deliberately generic. Use the JSON config and generator to build a measured, permission-approved model of a real office when ready.

## Prerequisites

- ROS 2 Jazzy + Gazebo Harmonic
- The community [unitree_go2_ros2](https://github.com/khaledgabr77/unitree_go2_ros2) repository built at `~/go2_ws`
- Gazebo GUI verified to work using `GALLIUM_DRIVER=d3d12 gz sim --render-engine ogre`
- Go2's installed launch file patched for the OGRE renderer as described in the root lab README
- A separate ROS domain is used for this simulation (`ROS_DOMAIN_ID=71`).

These scripts do **not** require the project to be stored under `~/go2_simulation_lab`. Paths are resolved from the actual script location.

## Lab 01 — Build and view the office

Run from the Git repository root:

```bash
python3 office_course/scripts/generate_office_world.py
bash office_course/scripts/start_office_only.sh
```

The generator writes `office_course/worlds/office_lab.sdf` (Gazebo world) and `office_course/worlds/office_floorplan.svg` (2D plan). Close this standalone world before launching a second Gazebo server.

## Lab 02 — Spawn and operate Go2

In the first terminal:

```bash
bash office_course/scripts/start_office_go2.sh
```

In another terminal:

```bash
source office_course/scripts/env.sh
ros2 topic info /cmd_vel -v
ros2 control list_controllers
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

Stop keyboard teleop before running the automated motion demo:

```bash
source office_course/scripts/env.sh
python3 office_course/scripts/demo_office_motion.py
```

The motion script publishes low-speed `/cmd_vel` commands only when `ROS_DOMAIN_ID=71`. The physical robot should remain disconnected during simulated movement experiments. Always verify `/cmd_vel` actually has a subscriber before expecting motion.

## Lab 03 — Change office geometry

Edit `config/office_example.json` (room dimensions, door opening, furniture sizes/positions). Regenerate and relaunch:

```bash
python3 office_course/scripts/generate_office_world.py
```

Coordinates use metres, with origin at the room centre (+X right, +Y up on the floor plan, +Z up in 3D). The wall visuals are shortened for a cutaway view, while collision walls retain their full height.

## Lab 04 — Inspect / record ROS traffic

```bash
source office_course/scripts/env.sh
bash office_course/scripts/inspect_robot.sh
bash office_course/scripts/record_experiment.sh
```

Stop the bag recorder using Ctrl+C. ROS bag files and private office images should **not** be committed to this public repository.

## Curriculum

1. [Measure the real office](docs/00_measurements.md)
2. [Understand SDF worlds](docs/01_world_sdf.md)
3. [Go2 locomotion & Twist commands](docs/02_go2_motion.md)
4. [ROS data, TF and simulation time](docs/03_ros_data.md)
5. [Improve office geometry](docs/04_geometry_fidelity.md)
6. [Virtual sensors and rendering constraints](docs/05_sensors.md)
7. [Mapping and SLAM](docs/06_mapping.md)
8. [Autonomous navigation](docs/07_navigation.md)
9. [Sim-to-real validation](docs/08_validation.md)

Each lesson should result in a reproducible command sequence, a short note on expected vs observed behavior, and a saved experiment log in `experiments/`.

**Limitations:** Gazebo is not guaranteed to model optical reflections from glass realistically. WSL D3D12 + OGRE1 may also limit some GPU-based sensors. A complete SLAM/Nav2 solution is a separate integration task—not provided by default by the community Go2 simulator.

## Debugging

- `AMENT_TRACE_SETUP_FILES: unbound variable`: do not run `set -u` before sourcing ROS environment scripts.
- `llvmpipe` instead of D3D12: verify `GALLIUM_DRIVER=d3d12 glxinfo -B`.
- Black/crashing Gazebo GUI: verify the **OGRE** renderer is used, not OGRE2.
- Python path not found: run commands relative to your Git repo, not `~/go2_simulation_lab` unless you've created that symlink.
- Robot doesn't move: inspect `/cmd_vel` subscribers, active controllers, simulation pause state and ROS domain.

> This is a teaching prototype. World geometry, controller behavior and sensors still need validation in your particular WSL setup.
