# Lesson 09 — Kalman Filters and EKF on Unitree Go2

## Why this lesson?

Manual spawning into Gazebo worked with:
```bash
ros2 run ros_gz_sim create -world office_lab -topic robot_description -name go2 -x 0 -y 0 -z 0.375
```
This inserts the robot description into a specifically named Gazebo world. The upstream automatic spawn launch action lacks `-world`, which may explain why the robot did not initially appear. Verify rather than assume the controller manager exists. The `/cmd_vel` subscriber being present does **not** guarantee joints are actuated.

## Mental model: prediction plus correction

A robot's true position and speed are not perfectly measured. IMU values drift during integration; leg odometry can slip; LiDAR and cameras have observation errors. A Kalman filter keeps a **state estimate** and its **uncertainty** and repeatedly:

1. Predicts the next state with a motion model.
2. Predicts uncertainty.
3. Compares a new measurement with the prediction (**innovation**).
4. Weights the correction using the **Kalman gain**.

Toy scalar example, robot predicted at 2.0 m and sensor reads 2.4 m:
- Equal uncertainty: fuse to 2.2 m.
- More trust in prediction: fuse closer to 2.0 m.
- More trust in measurement: fuse closer to 2.4 m.

Run `python3 office_course/scripts/kalman_1d_demo.py`. Change `R` from `0.09` to `1.0` and rerun; then reset and increase `Q` to `0.5`.

## Equations and variable names

Linear dynamic model: `x_k = F x_(k-1) + B u_k + w_k`.
Measurement model: `z_k = H x_k + v_k`.
Here `w` (process error) has covariance `Q` and `v` (measurement error) has covariance `R`.

**Predict:** `x⁻ = F x⁺ + B u`; `P⁻ = F P⁺ Fᵀ + Q`.

**Update:** innovation `y = z - H x⁻`; `S = H P⁻ Hᵀ + R`;
`K = P⁻ Hᵀ S⁻¹`; `x⁺ = x⁻ + K y`;
`P⁺ = (I - KH)P⁻` (simplified covariance update; Joseph form may be preferable numerically).

A larger `R` generally means lower gain, so the filter puts less trust in the sensor. A larger `Q` generally increases reliance on newer measurements.

## Why EKF rather than ordinary KF?

For a mobile robot turning through heading `θ`:
```text
x_new = x + v cos(θ) dt
y_new = y + v sin(θ) dt
θ_new = θ + ω dt
```
Sine and cosine make these nonlinear. The **Extended Kalman Filter** approximates nonlinear motion and observation functions locally using Jacobian matrices, then performs a Kalman-like predict/correct cycle. This is a first-order approximation, not an exact nonlinear solution.

Common families include linear KF, EKF, UKF (sigma points), error-state EKF (error around an IMU-propagated nominal state), and iterated EKF. Particle filters are a different sample-based estimator, not a Kalman filter. There is no definitive total count of variants.

## Exactly what this Go2 repository uses

Verified from upstream [launch file](https://github.com/khaledgabr77/unitree_go2_ros2/blob/main/unitree_go2_sim/launch/unitree_go2_launch.py), [EKF configuration 1](https://github.com/khaledgabr77/unitree_go2_ros2/blob/main/champ_base/config/ekf/base_to_footprint.yaml), [EKF configuration 2](https://github.com/khaledgabr77/unitree_go2_ros2/blob/main/champ_base/config/ekf/footprint_to_odom.yaml), and [CHAMP state estimation code](https://github.com/khaledgabr77/unitree_go2_ros2/blob/main/champ_base/src/state_estimation.cpp).

**`state_estimation_node`:** uses joint states, foot contacts and (if enabled) IMU observations to produce `/odom/raw` and `/base_to_footprint_pose` (actual topic may be relative to namespace).

**`base_to_footprint_ekf`:** 50 Hz; `two_d_mode: false`. Fuses `base_to_footprint_pose` position/orientation with selected `imu/data` orientation, angular velocities and Z acceleration. Output: `/odom/local`; TF `base_footprint → base_link`. Handles body's 3D pose relative to its footprint, including vertical motion and tilt.

**`footprint_to_odom_ekf`:** 50 Hz; `two_d_mode: true`. Fuses velocity and yaw rate from `/odom/raw` with yaw/yaw rate from `/imu/data`. Output: `/odom`; TF `odom → base_footprint`. Handles travel across a mostly planar floor.

TF chain: `map → odom → base_footprint → base_link → leg links`.

The static `map → odom` edge in the launch file is **not** a SLAM correction. Do not confuse filtered odometry (`/odom`) with Gazebo's `/odom/ground_truth`.

## Practical checks — run in the SAME ROS domain as the simulator

```bash
source /opt/ros/jazzy/setup.bash
source ~/go2_ws/install/setup.bash
echo "ROS domain: ${ROS_DOMAIN_ID:-unset}"
ros2 topic list
ros2 topic info /cmd_vel -v
ros2 topic echo /odom/raw --once
ros2 topic echo /odom --once
ros2 topic echo /odom/local --once
ros2 topic echo /imu/data --once
ros2 service list | grep controller_manager
```

Only echo topics that exist and have publishers. `--once` can wait if no messages are arriving.

## Experiment record

- Which sensors feed each EKF?
- Compare numeric values and uncertainty in `/odom/raw` and `/odom`.
- Why does estimating heading influence X/Y travel?
- Does manually spawning the Go2 restore `/controller_manager` services?
- Why doesn't a static `map → odom` transform fix drift?

Record output, observations, failures and solutions in `office_course/experiments/`. 
