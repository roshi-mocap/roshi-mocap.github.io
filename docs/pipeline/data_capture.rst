Data Capture
============

This page describes how to capture motion data using RoSHI.

Setup
-----

Before capturing data, ensure:

1. All 9 IMU trackers are powered on and streaming
2. Project Aria glasses are paired and recording
3. Calibration has been completed for the current session

Recording
---------

1. Start Aria recording via the companion app
2. Start IMU streaming (all trackers auto-connect to Wi-Fi)
3. Perform the desired activities
4. Stop Aria recording and IMU streaming

The system captures:

- **IMU data**: 9 sensors × 100 Hz orientation quaternions
- **Aria data**: 6-DoF head trajectory (from onboard SLAM) + RGB video
- **Timestamps**: UTC-synchronized across all sensors

Data Synchronization
--------------------

IMU and Aria streams are aligned via UTC timestamps. The synchronization
pipeline handles clock drift correction between the two modalities.
