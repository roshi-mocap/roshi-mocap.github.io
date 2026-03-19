Calibration Procedure
=====================

RoSHI calibration uses a short iPhone recording to recover sensor-to-bone and
cross-sensor heading alignment.

For app settings, output files, and troubleshooting, see :doc:`app_reference`.

Recording Steps
---------------

1. **Wear the suit** with all 9 IMU trackers attached and powered on
2. **Launch the calibration app** and ensure the receiver status (top-right) is
   green
3. **Tap Record** - a 3-second countdown starts, then recording begins
4. **Slowly rotate** to expose all 9 AprilTags to the camera - the tag
   detection tracker in the app shows progress per tag
5. **Tap Stop** when all tags reach the target detection count
6. The app automatically uploads the video and metadata to the receiver

.. tip::
   The calibration video only needs to be 20-40 seconds. Move slowly and keep
   tags facing the camera. Good lighting helps detection accuracy.

Pipeline Summary
----------------

- Detect AprilTags in the RGB video to recover 3D tag poses
- Run SAM 3D Body on the calibration clip
- Align tag frames with estimated bone frames to solve for calibration offsets

.. note::
   Calibration can be repeated at any time without removing the IMUs. Simply
   re-record a short calibration video.

Output
------

The calibration output is a JSON file with per-sensor rotation offsets for the
pose estimation pipeline.
