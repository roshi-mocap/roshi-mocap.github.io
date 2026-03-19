Calibration Procedure
=====================

This page focuses on the short iPhone capture used to recover
**sensor-to-bone calibration offsets** and **per-IMU world alignment**.

Recording Steps
---------------

1. **Wear the suit** with all 9 IMU trackers attached and powered on.
2. **Start the receiver** on the computer that will receive the uploaded files, and check the IP address and port shown in the receiver terminal.
3. **Launch the calibration app** and ensure the receiver status (top-right) is green.
4. **Tap Record**. You can use either the front or back camera.
5. **Slowly rotate** until all 9 AprilTags have been seen; the tag tracker in
   the app shows progress for each tag.
6. **Once all tags are detected**, you can step out of the camera view and
   start performing the motion you want to record.
7. **Tap Stop** when you are done with the collection.
8. The app uploads the video and metadata to the receiver. You can also start
   the offline calibration process.

.. tip::
   The full take can be longer, but the calibration segment itself usually only
   needs 20-40 seconds. The app records when calibration is complete and uses
   that time to define the calibration clip automatically. Move slowly while
   exposing the tags, keep them facing the camera, and use good lighting for
   reliable detection.

.. note::
   For a quick visual walkthrough, see the demo video
   in :ref:`the demo video in App Reference <app-reference-video>`.

Post-processing Pipeline
----------------
- Run SAM 3D Body on the RGB video with camera intrinsics from the app.
- Convert the result to SMPL(X) format.
- Solve for sensor-to-bone calibration offsets and per-IMU world alignment.

.. note::
   Calibration can be repeated at any time without removing the IMUs. Simply
   re-record a short calibration video.

Output
------

The calibration output is a JSON file with per-sensor rotation offsets for the
pose estimation pipeline. The output file is named `imu_calibration.json`.
