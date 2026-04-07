Software (firmware and host tools)
==================================

Firmware, flashing scripts, and Python helpers live in the `RoSHI-Hardware`_
repository on GitHub.

.. _RoSHI-Hardware: https://github.com/Jirl-upenn/RoSHI-Hardware

See the repo **README** for layout; tracker and receiver sketches are under
`Firmware/ <https://github.com/Jirl-upenn/RoSHI-Hardware/tree/main/Firmware>`__.

Flashing order (Arduino IDE)
----------------------------

#. **Build and close** each tracker per :doc:`assembly` (electronics + printed
   case).
#. **Flash the receiver first** (`Firmware/IMU_Receiver/HostRead/`). Connect the
   **ESP32-S3 Feather** to your laptop with **USB-C** and upload from the
   Arduino IDE.
#. **Flash each IMU tracker** (`Firmware/IMU_Tracker/`). Use the same IDE and
   board settings as in the repo README.

Per-tracker settings
~~~~~~~~~~~~~~~~~~~~

In ``IMU_Tracker.ino`` set a **unique** ``TRACKER_ID`` for each module (**1**
through **9**). The host OLED layout reserves index **0** for auxiliary button
state; tracker IDs **1–9** map to the nine body trackers.

``peerMAC`` and ESP-NOW
~~~~~~~~~~~~~~~~~~~~~~~

Each tracker registers **one ESP-NOW peer**: the **Wi-Fi (STA) MAC address of
the receiver ESP32-S3**. In code, ``esp_now_add_peer(peerMAC, …)`` and
``esp_now_send(peerMAC, …)`` use that address as the destination for every
packet.

The **byte array printed in the repository is a placeholder**. It only works on
your bench if it **exactly matches** the receiver’s real STA MAC. Before
shipping trackers, **replace** ``peerMAC`` with your board’s address (read from
the receiver’s Serial log, a small sketch that prints ``WiFi.macAddress()`` on
the Feather, or the Wi-Fi details screen in your router).

If ``peerMAC`` does not match the receiver, **ESP-NOW will not deliver packets**
and the OLED will not show those trackers’ battery percentages.

Verification
~~~~~~~~~~~~

After flashing, power trackers and the receiver. With RF link OK, the **OLED**
on the receiver should show **battery percentage** per tracker ID (see the
receiver’s grid layout in the firmware). You can also confirm traffic on the
receiver **Serial** monitor (it prints decoded IMU lines per ID).

Python environment (USB serial reader)
--------------------------------------

The repo README lists minimal dependencies for the scripts under
``Firmware/python/`` (for example ``pyserial``, ``numpy``, ``matplotlib``).
Install them with ``pip``, then run the reader or examples from that folder with
the **host Feather** connected over **USB-C**:

.. code-block:: text

   pip install pyserial numpy matplotlib

Use the project’s ``imu_reader.py`` / ``sample.py`` / ``visualize.py`` as
documented in **`RoSHI-Hardware`** README.

See also
--------

- Mechanical build: :doc:`assembly`
- Bill of materials: :doc:`components`
- Pipeline overview: :doc:`../pipeline/index`
