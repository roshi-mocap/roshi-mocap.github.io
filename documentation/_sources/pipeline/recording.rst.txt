How to Record Data
==================

This section covers the full recording workflow: calibration capture, IMU
streaming, and Aria recording.

Calibration Recording
---------------------

Before collecting motion data you need a short calibration video to recover
**sensor-to-bone offsets** and **per-IMU world alignment**.

1. **Wear the suit** with all 9 IMU trackers attached and powered on.
2. **Wear the Aria glasses** and start the Aria recording via the companion app.
3. **Start the receiver** on the computer and note the IP address and port:

   .. code-block:: bash

      python src/pipeline/01_receiver.py --output-dir received_recordings

   The terminal will print the IP address and port (default ``8085``) that the
   iOS app needs to connect to. Make sure the phone and computer are on the
   same Wi-Fi network.
4. **Launch the calibration app** and ensure the receiver status (top-right)
   is green.
5. **Tap Record**. You can use either the front or back camera.
6. **Slowly rotate** until all 9 AprilTags have been seen; the tag tracker in
   the app shows progress for each tag.
7. **Once all tags are detected**, you can step out of the camera view and
   start performing the motion you want to record.
8. **Tap Stop** when you are done with the collection. The app will upload
   the video and metadata to the receiver automatically. You will have the
   option to start the post-processing pipeline. You can also safely stop
   the Aria recording via the companion app.

.. tip::
   The full take can be longer, but the calibration segment itself usually only
   needs 20–40 seconds. Move slowly while exposing the tags, keep them facing
   the camera, and use good lighting for reliable detection.

.. note::
   Calibration can be repeated at any time without removing the IMUs. Simply
   re-record a short calibration video.

.. raw:: html

   <p style="color: red; font-weight: bold;">TODO: Add a visual guide for the entire workflow.</p>

For a quick visual walkthrough, see the
:ref:`demo video in App Reference <app-reference-video>`.

Session Output
--------------

After recording, the iOS app uploads two files to the receiver. Together with
the IMU stream, the session directory initially contains:

.. code-block:: text

   received_recordings/<session_name>/
   ├── video.mp4                       # H.264 calibration video (uploaded from iOS app)
   ├── metadata.json                   # Per-frame timestamps, intrinsics, AprilTag detections (uploaded from iOS app)
   └── imu/
       └── imu_data.csv                # Raw IMU quaternions (utc_timestamp_ns, imu_id, qw, qx, qy, qz)

For how to add Aria data, run the calibration pipeline, and prepare
synchronized outputs for inference, see :doc:`postprocessing`.

Common Issues
-------------

- **Receiver not found**: confirm the phone and receiver machine are on the
  same Wi-Fi network and that the manually entered IP and port match the
  values shown in the receiver terminal.
- **Connection timeout**: check the receiver process, port, and any manual IP
  or port override inside the app.
- **Tags not detected**: keep the 42 mm tags flat, visible, and well lit, and
  avoid strong motion blur.
- **Low detection counts**: move more slowly and give the camera a little more
  time before stopping the recording.
