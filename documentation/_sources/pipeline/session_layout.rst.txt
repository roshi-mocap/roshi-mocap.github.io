Session Data Layout
===================

After a recording session has been processed, RoSHI organizes the outputs into
the following structure:

.. code-block:: text

   <session>/
   ├── video.mp4                         # Raw recording from the iOS app
   ├── metadata.json                     # Camera intrinsics and AprilTag detections
   ├── color/                            # Extracted third-person video frames
   ├── frames.csv                        # frame_id, utc_timestamp_ns, color_path
   ├── meta/
   │   ├── camera.json                   # Camera intrinsics for SAM-3D-Body
   │   └── calibration_segment.json      # Selected calibration window
   ├── color_apriltag/
   │   └── detection_summary.json        # Per-frame tag rotations
   ├── imu/
   │   └── imu_data.csv                  # Raw IMU packets: timestamp, quat, accel, gyro
   ├── body_data/                        # SAM-3D-Body and MHR output
   ├── smpl_output/per_frame/            # SMPL-X rotations per frame
   ├── imu_calibration.json              # Calibrated bone-to-sensor offsets
   └── sync/
       ├── frames.csv                    # UTC-aligned third-person frames
       ├── color/                        # Symlinks to the session color frames
       ├── imu_info.csv                  # Calibrated IMU rotations
       ├── imu_info.pkl                  # Same information as a pickle dict
       ├── vrs_frames.csv                # Aria first-person frames, if available
       └── vrs_color/                    # Extracted VRS RGB frames, if available

