# Unitree Go2 Simulation Lab

**A reproducible, beginner-to-research learning notebook for Gazebo Harmonic + ROS 2 Jazzy**

This repository contains **your** learning notes and original scripts, not a copy of the upstream Unitree source code.

**Current machine (observed):** Ubuntu 24.04 in WSL, ROS 2 Jazzy, Gazebo Sim 8.15.0, Intel Iris Xe via Mesa D3D12. Gazebo's OGRE renderer worked smoothly after llvmpipe/OGRE2 problems. The Unitree Go2 has spawned successfully.

**Upstream simulation:** https://github.com/khaledgabr77/unitree_go2_ros2

## Learning principle

Every experiment gets a record of: **why**, **commands**, **expected observation**, **actual observation**, **evidence**, **failure + fix**, **next question**. Keep experiments reproducible with a commit ID and configuration changes.

## One-minute quick start

**Terminal A (launch):**

```bash
cd ~/go2_ws
bash ~/go2_simulation_lab/scripts/start_go2.sh
```

**Terminal B (inspect):**

```bash
source /opt/ros/jazzy/setup.bash
source ~/go2_ws/install/setup.bash
ros2 topic list -t
ros2 control list_controllers
```

**Terminal C (control):**

```bash
source /opt/ros/jazzy/setup.bash
source ~/go2_ws/install/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

**Terminal C (instead of keyboard, one scripted movement):**

```bash
python3 ~/go2_simulation_lab/scripts/demo_motion.py --forward-seconds 2 --turn-seconds 1
```

**Important:** Do **not** run keyboard teleop and the scripted publisher at the same time; they both publish to `/cmd_vel` and will conflict. Keep the robot in the simulator (not connected to real hardware). Wait until the Go2 controllers are active before sending motion commands; this upstream launch starts controllers after a delay.

## Set up your documentation workspace

Unzip this archive in your Ubuntu home directory so its path is `~/go2_simulation_lab`. If downloaded on Windows, access it via `/mnt/c/Users/<YourWindowsUser>/Downloads` and extract into your home directory:

```bash
# Replace the ZIP path with your real location:
mkdir -p ~/go2_simulation_lab
unzip /mnt/c/Users/<YourWindowsUser>/Downloads/go2_simulation_lab.zip -d ~/
chmod +x ~/go2_simulation_lab/scripts/*.sh
```

To open/edit the notes in VS Code from Ubuntu:

```bash
cd ~/go2_simulation_lab && code .
```

If `code` is unavailable, use any Markdown/text editor.

## Directory guide

```text
go2_simulation_lab/
├── README.md                       # entry point
├── docs/
│   ├── 00_environment.md           # what you installed and why it works
│   ├── 01_gazebo_basics.md         # initial simulation and UI concepts
│   ├── 02_ros_control.md           # topics, Twist and controls
│   ├── 03_sensors_and_data.md      # odom, IMU, lidar, bags, TF
│   ├── 04_learning_roadmap.md      # modules and project progression
│   └── cheat_sheet.md             # reusable commands
├── logs/
│   ├── 2026-11-06_lab01.md         # first lab; known observations
│   └── session_template.md        # duplicate for future experiments
├── scripts/
│   ├── start_go2.sh               # launch the working sensor-light Go2
│   ├── check_setup.sh             # versions, ROS and GPU
│   ├── snapshot_session.sh        # save environment/topic/controller status
│   ├── demo_motion.py             # original timed Twist publisher
│   └── stop_robot.sh              # publish stop command
└── experiments/                   # generated run logs; do not commit enormous bags
```

## Suggested Git workflow

Create a *new* repository for lab notes, separate from the external controller project:

```bash
cd ~/go2_simulation_lab
git init
git add README.md docs scripts logs .gitignore
git commit -m "lab01: document working Gazebo Go2 setup"
```

Do not commit bags, cached files, large screenshots, or upstream copied sources. Use a separate project or GitHub repo for the lab notebook.

## Current success criteria

- [x] ROS 2 Jazzy identified
- [x] Gazebo 8.15.0 identified
- [x] WSL GPU acceleration enabled with `GALLIUM_DRIVER=d3d12`
- [x] OGRE renderer launches without noticeable lag
- [x] Simulated Go2 visually appears
- [ ] Robot walks with keyboard control
- [ ] `/cmd_vel` type and subscribers verified
- [ ] First original Python ROS 2 script moves robot
- [ ] Odometry vs ground-truth comparison
- [ ] First sensor bag recorded

## Attribution and limitations

The Go2 simulation itself is an external community project with a CHAMP controller. Its README says SLAM and Nav2 integration are not complete; they need separate implementation and validation. Sensor readings are simulated and should not be treated as validated physical sensor behavior—especially for glass and reflections.


## Office simulation course

The [office-based Go2 simulation course](office_course/README.md) adds a configurable example office, SDF + floorplan generator, WSL-compatible Gazebo launch scripts, ROS 2 teleoperation, a safe low-speed Python movement demo, experiment recording and nine progressively structured teaching notes.

Quick start (from this repository's root, with Jazzy, Harmonic and Go2 already installed):

```bash
python3 office_course/scripts/generate_office_world.py
bash office_course/scripts/start_office_only.sh
# Close Gazebo, then:
bash office_course/scripts/start_office_go2.sh
```

The example layout is **fictional**. Check privacy/permission before adding photographs or measured dimensions of a real office to this public repo. Read [office course documentation](office_course/README.md) before enabling sensors or automated motion.
