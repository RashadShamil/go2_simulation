# Module 01 — Gazebo: your first digital robot

## Learning objectives

1. Explain the difference among a **world**, an **entity/model**, a **link**, a **joint**, and a **sensor**.
2. Find the Play/Pause control and understand that **simulation time** advances only when running.
3. Tell Gazebo (physics) apart from RViz (visualization).
4. Relaunch the *same* Go2 using the same settings.

## World and robot mental model

```text
Simulation world
  ├── environment (floor, gravity, lighting, obstacles)
  ├── Go2 robot model
  │   ├── trunk (link)
  │   ├── legs (links connected by joints)
  │   ├── motors/controllers (via ros2_control + CHAMP)
  │   └── sensors (disabled initially for performance)
  └── clock + physics + rendering
```

A *link* is a rigid body. A *joint* specifies how two links can move relative to one another. A *controller* requests motion; the physics engine decides resulting motion and forces. A robot description (URDF/Xacro) encodes most of the robot's structure; a world description (SDF) encodes the environment and simulation elements.

## Lab procedure

1. Start the simulation in Terminal A with `bash ~/go2_simulation_lab/scripts/start_go2.sh`.
2. Look for the Go2 model. Rotate the camera. Pause/play the simulation and observe what changes.
3. In Terminal B run `ros2 topic list -t`; find `/clock`, `/cmd_vel`, `/joint_states` (names may vary with launch settings).
4. Run `ros2 control list_controllers` after the controllers have had time to spawn.
5. Take screenshots of Gazebo's world and your terminal output, but do not treat a screenshot alone as a reproducible experiment.

## Questions to answer in your own words

- Does Gazebo's simulated time advance while paused?
- Why can the model show up in the GUI before the controllers become active?
- Why might a robot look realistic but still be missing valid LiDAR data?
- What is the role of `robot_state_publisher`?

## Evidence files

Store screenshots with descriptive filenames and note the command/settings used. Example: `experiments/lab01_2026-11-06/go2_spawn.png`.
