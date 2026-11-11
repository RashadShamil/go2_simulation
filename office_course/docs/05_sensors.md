# Lesson 05 — Virtual sensors

A simulated LiDAR returns distances or point clouds based on its ray/geometry model. An IMU reports inertial measurements, while cameras render images. Gazebo Transport topics must be bridged to ROS 2 where needed with `ros_gz_bridge`.

**Hardware note:** Intel Iris Xe via WSL D3D12 works for your GUI with OGRE1. Some GPU LiDAR/depth camera features expect OGRE2. Enable one sensor at a time, measure runtime, and verify actual ROS topics.

Start by verifying `/odom` and any IMU data. Then enable a LiDAR flag in the Go2 launch command and inspect PointCloud2 output. Record any missing output instead of assuming it exists.

**Research caution:** default ray casting does not reproduce all real glass reflections, missing returns, and ghost points.
