Software (firmware and host tools)
==================================

Firmware sketches and Python helpers live in the `RoSHI-Hardware`_ repo under
`Firmware/ <https://github.com/Jirl-upenn/RoSHI-Hardware/tree/main/Firmware>`__;
the repo README has the full layout and Arduino board settings.

.. _RoSHI-Hardware: https://github.com/Jirl-upenn/RoSHI-Hardware

Flashing order (Arduino IDE)
----------------------------

After the trackers are built and closed (see :doc:`assembly`), connect each
board over USB-C and flash from the Arduino IDE in this order:

#. **Receiver first** — ``Firmware/IMU_Receiver/HostRead/`` onto the ESP32-S3
   Feather.
#. **Each IMU tracker** — ``Firmware/IMU_Tracker/``. In ``IMU_Tracker.ino`` set
   a **unique** ``TRACKER_ID`` from **1–9** per module (the host OLED reserves
   index 0 for auxiliary button state).

``peerMAC`` and ESP-NOW
~~~~~~~~~~~~~~~~~~~~~~~

Every tracker registers a single ESP-NOW peer: the **Wi-Fi (STA) MAC address
of the receiver Feather**. Before shipping any tracker, replace the placeholder
``peerMAC`` byte array in the sketch with your receiver's real MAC—read it from
the receiver Serial log or a one-off ``WiFi.macAddress()`` sketch. A mismatch
silently breaks delivery and the OLED will show no battery for those trackers.

Verification
~~~~~~~~~~~~

Power up the receiver and trackers. With the RF link healthy, the receiver
**OLED** shows battery percentage per tracker ID, and the receiver **Serial**
monitor prints decoded IMU lines.

Python environment (USB serial reader)
--------------------------------------

Scripts under ``Firmware/python/`` (``imu_reader.py``, ``sample.py``,
``visualize.py``) talk to the receiver over USB serial. Minimal deps:

.. code-block:: text

   pip install pyserial numpy matplotlib

See also
--------

- Mechanical build: :doc:`assembly`
- Bill of materials: :doc:`components`
- Pipeline overview: :doc:`../pipeline/index`
