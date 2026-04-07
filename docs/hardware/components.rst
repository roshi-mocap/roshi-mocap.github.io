Components
==========

IMU Trackers
------------

Each tracker consists of:

- **BNO085** 9-axis IMU sensor
- **WeMos D1 Mini** (ESP8266) for Wi-Fi streaming
- **3D-printed enclosure** with a rigidly mounted AprilTag
- **LiPo battery** (e.g. 503759 **1200 mAh**, see BOM)

You need **9 trackers** in total, placed at the following body locations:

.. list-table::
   :header-rows: 1
   :widths: 15 30

   * - Tag ID
     - Body Location
   * - 0
     - Pelvis
   * - 1
     - Left Shoulder
   * - 2
     - Right Shoulder
   * - 3
     - Left Elbow
   * - 4
     - Right Elbow
   * - 5
     - Left Hip
   * - 6
     - Right Hip
   * - 7
     - Left Knee
   * - 8
     - Right Knee

IMU / AprilTag / Joint Mapping
------------------------------

.. list-table::
   :header-rows: 1
   :widths: 15 30 18 18

   * - IMU ID
     - Body Part
     - AprilTag ID
     - SMPL-X Joint
   * - 1
     - Pelvis
     - 0
     - 0
   * - 2
     - Left Shoulder
     - 1
     - 16
   * - 3
     - Right Shoulder
     - 2
     - 17
   * - 4
     - Left Elbow
     - 3
     - 18
   * - 5
     - Right Elbow
     - 4
     - 19
   * - 6
     - Left Hip
     - 5
     - 1
   * - 7
     - Right Hip
     - 6
     - 2
   * - 8
     - Left Knee
     - 7
     - 4
   * - 9
     - Right Knee
     - 8
     - 5

Project Aria Glasses
--------------------

RoSHI uses `Project Aria <https://www.projectaria.com/>`_ glasses for:

- 6-DoF head tracking via onboard SLAM
- Egocentric RGB video capture
- Machine Perception Services (MPS) for post-processing

Bill of Materials
-----------------

Prices below are **typical U.S. Amazon retail** (before tax/shipping) for the
listed packs; buy enough packs to cover **nine trackers** plus spares where it
helps (passives, connectors). PCB Gerbers follow the SlimeVR Hyperion design—see
:doc:`assembly`.

.. list-table::
   :header-rows: 1
   :widths: 32 14 20 28

   * - Item
     - Qty (9 trackers)
     - List / pack price
     - Source
   * - WeMos D1 Mini (ESP8266 class)
     - 9 boards (e.g. **2×** 5-packs)
     - **$14.99** / 5 boards (~$3.00 ea)
     - `D1 Mini pack`_
   * - 180 kΩ resistor (1/2 W metal film)
     - 9 (buy 100-pack)
     - **$5.99** / 100 pcs
     - `180K resistor pack`_
   * - Schottky diode 1N5817
     - 9 (buy 125-pack)
     - **$5.99** / 125 pcs
     - `1N5817 diode pack`_
   * - TP4056 charger (Type-C), dual protection
     - 9 modules (1× 10-pack)
     - **$8.99** / 10 pcs
     - `TP4056 10-pack`_
   * - BNO085 nine-axis IMU module
     - 9
     - **$17.59** each
     - `BNO085 module`_
   * - Slide switch SS12D00G3 (SPDT, 3-pin)
     - 9 (40-pack)
     - **$5.59** / 40 pcs
     - `SS12D00G3 40-pack`_
   * - LiPo 503759, 3.7 V, **1200 mAh**, JST-PH 2.0 mm
     - 9
     - **$10.19** each
     - `503759 1200mAh battery`_
   * - JST-PH 2.0 mm socket kit (side-entry / right-angle, multi-pin)
     - 9× 2P sockets from kit
     - **$9.99** kit (~40× 2P + other sizes)
     - `JST-PH socket kit`_
   * - Pin headers, strap hardware, filament, AprilTag prints
     - —
     - varies
     - (local / print lab)
   * - 3D-printed tracker case
     - 9
     - material cost varies
     - see :doc:`assembly`

.. _D1 Mini pack: https://www.amazon.com/dp/B09SPYY61L
.. _180K resistor pack: https://www.amazon.com/dp/B07QG1TG1H
.. _1N5817 diode pack: https://www.amazon.com/dp/B0FC2CTR7F
.. _TP4056 10-pack: https://www.amazon.com/dp/B0C3V1NC7T
.. _BNO085 module: https://www.amazon.com/dp/B0CDGZMLPP
.. _SS12D00G3 40-pack: https://www.amazon.com/dp/B0CFDGZ9R2
.. _503759 1200mAh battery: https://www.amazon.com/dp/B0CNLNV5ZC
.. _JST-PH socket kit: https://www.amazon.com/dp/B0BM492MMF
