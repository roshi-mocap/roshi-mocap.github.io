Calibration App Setup
=====================

Use the RoSHI iOS app to record the short AprilTag video needed for
sensor-to-bone calibration.

For app capabilities, recorded outputs, and troubleshooting, see
:doc:`app_reference`. For the capture workflow itself, see :doc:`procedure`.

Source code: `RoSHI-App <https://github.com/Jirl-upenn/RoSHI-App>`_

Requirements
------------

- iPhone or iPad running **iOS 17.6+**
- 9 AprilTags from the **Tag36h11** family, printed at **42 mm**
- **Xcode 15+** with Swift 5.0
- A computer on the same LAN to run the receiver
- The main `RoSHI <https://github.com/Jirl-upenn/RoSHI>`_ repository for the
  receiver and downstream calibration pipeline

See :doc:`../hardware/components` for the tag ID to body-location mapping.

Build the App
-------------

.. code-block:: bash

   git clone https://github.com/Jirl-upenn/RoSHI-App.git
   cd RoSHI-App

1. Open ``ROSHI.xcodeproj`` in Xcode
2. In ``Signing & Capabilities``, select your Apple Development Team
3. Select your target device
4. Build and run (Cmd+R)

No external Swift packages or CocoaPods are needed; the AprilTag library is
vendored as C source.

Run the Receiver
----------------

On your computer (same Wi-Fi network as the iOS device):

.. code-block:: bash

   git clone https://github.com/Jirl-upenn/RoSHI.git
   cd RoSHI
   python 01_receiver.py --output-dir received_recordings

The receiver is part of the main RoSHI repository. It advertises itself via
Bonjour/mDNS, so the app usually discovers it automatically. You can also
enter the receiver IP address and port manually from the app if needed.

Useful options:

.. code-block:: bash

   python 01_receiver.py --port 8080
   python 01_receiver.py --output-dir ~/roshi_data
