Calibration App Reference
=========================

The calibration app records the short AprilTag video used by the RoSHI
pipeline and uploads each session to the local receiver.

For installation and receiver setup, see :doc:`app_setup`. For the recording
workflow, see :doc:`procedure`.

Core Functions
--------------

- Real-time AprilTag detection (Tag36h11) with 3D pose overlay
- Video recording with per-frame UTC timestamps and camera intrinsics
- LAN receiver connection with configurable IP and port
- Per-tag detection tracking with configurable target counts
- Front and back camera support with adjustable resolution, frame rate, and
  zoom
- One-tap upload of the recorded session to the receiver

In-App Controls
---------------

.. list-table::
   :header-rows: 1
   :widths: 30 30 15

   * - Setting
     - Options
     - Default
   * - Resolution
     - 720p / 1080p
     - 720p
   * - FPS
     - 10 / 15 / 20 / 30
     - 30
   * - Target detections per tag
     - 50 / 100 / 200
     - 100
   * - Zoom
     - 1x-5x
     - 1x
   * - Camera
     - Front / Back
     - Back

Session Output
--------------

Each recording session uploads two files to the receiver:

- ``video_YYYYMMDD_HHMMSS.mp4``: H.264-encoded calibration video at the chosen
  resolution and frame rate
- ``metadata_YYYYMMDD_HHMMSS.json``: per-frame metadata including timestamps,
  intrinsics, and AprilTag detections

The metadata contains per-frame UTC timestamps, camera intrinsics, and tag
detections used by the downstream calibration pipeline.

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
