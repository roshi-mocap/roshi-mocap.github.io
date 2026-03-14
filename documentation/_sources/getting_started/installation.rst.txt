Installation
============

Prerequisites
-------------

- Python 3.8+
- Project Aria glasses with MPS (Machine Perception Services) access
- iPhone or iPad running iOS 17.6+ (for calibration)

Python Environment
------------------

.. code-block:: bash

   git clone https://github.com/Jirl-upenn/RoSHI.git
   cd RoSHI
   pip install -r requirements.txt

IMU Firmware
------------

Each IMU tracker runs firmware that streams BNO085 orientation data over Wi-Fi
at 100 Hz. See the :doc:`../hardware/components` page for flashing instructions.

Calibration App
---------------

The iOS calibration app is available at
`RoSHI-App <https://github.com/Jirl-upenn/RoSHI-App>`_.

.. code-block:: bash

   git clone https://github.com/Jirl-upenn/RoSHI-App.git

Open ``ROSHI.xcodeproj`` in Xcode 15+ and build to your device.
