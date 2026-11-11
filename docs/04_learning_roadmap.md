# Structured learning roadmap

## M01 — Simulation fundamentals

**Deliverable:** a reproducible launch with correct GPU mode, screenshots, model/links/joints explanation.

## M02 — ROS 2 motion control

**Deliverable:** keyboard demo, original ROS publisher script, logs of `/cmd_vel` and observed motion.

## M03 — TF, joint states and odometry

**Deliverable:** diagram of frames and a table comparing odometry and simulated ground truth.

## M04 — Sensor simulation and rosbag

**Deliverable:** a recorded bag with IMU and one LiDAR, rates and frame IDs documented.

## M05 — Mapping and navigation

**Deliverable:** a controlled mapping experiment, explicit baseline and quantitative evaluation. Requires separate SLAM/Nav2 integration; not preinstalled in this upstream project.

## M06 — Advanced experiments

**Deliverable:** reproduce the same experiment with modified terrain, gait parameters or sensor noise, record metrics, compare runs.

## Rules for research-grade notes

1. Always write your hypothesis *before* adjusting the configuration.
2. Change one variable per experiment where practical.
3. Record simulator/ROS/source revision, seed (when applicable), topic names, frame IDs and settings.
4. Distinguish command values from actual sensor output.
5. Never claim simulated glass artifacts equal those of the real Unitree LiDAR without physical validation.
