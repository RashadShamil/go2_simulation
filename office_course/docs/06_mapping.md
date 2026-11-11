# Lesson 06 — Mapping

**Goal:** drive a repeatable path through the office, record simulated sensor data, and build a map.

Progression: verify valid point clouds and timestamps → verify sensor TF → record rosbag → reconstruct a simple odometry-based map → compare with Gazebo ground truth → integrate a selected SLAM stack.

The community Go2 package does not automatically provide a complete working SLAM and Nav2 pipeline. Integration and validation are separate experiments.

**Metrics:** map coverage, trajectory drift, missing obstacles, real-time factor and reproducibility.
