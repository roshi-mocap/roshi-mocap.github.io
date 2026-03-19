Calibration Procedure
=====================

RoSHI calibration uses a short iPhone recording to recover **sensor-to-bone calibration offsets** and **per-IMU world alignment**.

For app settings, output files, and troubleshooting, see :doc:`app_reference`.
For the rotation equations and robust solvers used in the calibration pipeline, see :doc:`math`.

Recording Steps
---------------

1. **Wear the suit** with all 9 IMU trackers attached and powered on.
2. **Start the receiver** on the computer that will receive the uploaded files, and check the IP address and port shown in the receiver terminal.
3. **Launch the calibration app** and ensure the receiver status (top-right) is green.
4. **Tap Record** - a 3-second countdown starts, then recording begins if you are using the front camera.
5. **Slowly rotate** to expose all 9 AprilTags to the camera; the tag detection tracker in the app shows progress per tag.
6. **Once all tags are detected**, you can step out of the camera view and start performing the motion you want to record. 
7. **Tap Stop** when you are done with the collection.
8. The app automatically uploads the video and metadata to the receiver. You will also have the option to start the offline calibration process.

.. tip::
   The full recording can be longer, but the calibration segment itself usually
   only needs 20-40 seconds. The time when calibration is completed is also recorded and used to define the clip for calibration automatically. 
   Move slowly while exposing the tags, keep them facing the camera, and use good lighting for reliable detection.

Pipeline Summary
----------------
- Run SAM 3D Body on the RGB with camera intrinsics from the app to get body reconstruction in MHR format.
- Convert MHR to SMPL(X) format.
- Solve for sensor-to-bone calibration offsets and per-IMU world alignment.

.. note::
   Calibration can be repeated at any time without removing the IMUs. Simply
   re-record a short calibration video.

Output
------

The calibration output is a JSON file with per-sensor rotation offsets for the
pose estimation pipeline. The output file is named `imu_calibration.json`.
