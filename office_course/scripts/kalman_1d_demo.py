#!/usr/bin/env python3
"""Teaching demo: scalar Kalman filter for a stationary target. Python 3 stdlib."""
measurements = [1.30, 0.85, 1.12, 0.91, 1.05, 0.97]
estimate = 0.0    # predicted position in m
P = 1.0           # estimate variance (m^2)
Q = 0.01          # process noise variance (m^2)
R = 0.09          # measurement noise variance (m^2)
print("step   sensor   gain   fused_position   uncertainty_variance")
for i, z in enumerate(measurements, 1):
    predicted = estimate                 # model: target remains stationary
    predicted_P = P + Q                  # uncertain predictions
    gain = predicted_P / (predicted_P + R)
    estimate = predicted + gain * (z - predicted)
    P = (1 - gain) * predicted_P
    print(f"{i:>4}  {z:>7.2f}  {gain:>5.3f}  {estimate:>14.3f}  {P:>20.4f}")
print("Try R=1.0 (less trust in sensor) or Q=0.5 (less trust in model).")
