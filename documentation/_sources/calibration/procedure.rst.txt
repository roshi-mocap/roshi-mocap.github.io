Calibration Procedure
=====================

RoSHI calibration recovers the sensor-to-bone and cross-sensor heading
alignments from a short iPhone video.

Steps
-----

1. **Wear the suit** with all 9 IMU trackers attached and powered on
2. **Launch the calibration app** and ensure the receiver status (top-right) is
   green
3. **Tap Record** — a 3-second countdown starts, then recording begins
4. **Slowly rotate** to expose all 9 AprilTags to the camera — the tag
   detection tracker in the app shows progress per tag
5. **Tap Stop** when all tags reach the target detection count
6. The app automatically uploads the video and metadata to the receiver

.. tip::
   The calibration video only needs to be 20–40 seconds. Move slowly and keep
   tags facing the camera. Good lighting helps detection accuracy.

How It Works
------------

Each IMU tracker has a rigidly mounted AprilTag. The calibration pipeline:

1. Detects AprilTags in the RGB video to recover 3D tag poses
2. Runs SAM 3D Body estimation on the calibration video
3. Computes sensor-to-bone rotation offsets by aligning tag frames with the
   estimated bone frames
4. Recovers cross-sensor heading alignment

.. note::
   Calibration can be repeated at any time without removing the IMUs. Simply
   re-record a short calibration video.

Output
------

The calibration produces a JSON file containing per-sensor rotation offsets
that is used by the pose estimation pipeline.
