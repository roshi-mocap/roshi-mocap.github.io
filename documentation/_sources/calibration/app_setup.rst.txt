Calibration App Setup
=====================

The RoSHI calibration app is an iOS application that captures RGB video with
real-time AprilTag detection to recover sensor-to-bone orientation offsets.

Source code: `RoSHI-App <https://github.com/Jirl-upenn/RoSHI-App>`_

Requirements
------------

- iPhone or iPad running **iOS 17.6+**
- **Xcode 15+** with Swift 5.0
- A computer on the same LAN to run the receiver script

Building the App
----------------

.. code-block:: bash

   git clone https://github.com/Jirl-upenn/RoSHI-App.git
   cd RoSHI-App

1. Open ``ROSHI.xcodeproj`` in Xcode
2. Select your target device
3. Build and run (Cmd+R)

No external Swift packages or CocoaPods are needed — the AprilTag library is
vendored as C source.

Setting Up the Receiver
-----------------------

On your computer (same Wi-Fi network as the iOS device):

.. code-block:: bash

   cd RoSHI-App
   pip install -r requirements.txt
   python3 receiver.py

The receiver advertises itself via Bonjour. The app discovers it automatically.

**Options:**

.. code-block:: bash

   python3 receiver.py --port 8080               # custom port (default: 50000)
   python3 receiver.py --output-dir ~/roshi_data  # custom output directory

App Settings
------------

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
     - 1x–5x
     - 1x
   * - Camera
     - Front / Back
     - Back
