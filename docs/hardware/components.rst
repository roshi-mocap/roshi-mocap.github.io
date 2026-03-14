Components
==========

IMU Trackers
------------

Each tracker consists of:

- **BNO085** 9-axis IMU sensor
- **ESP32** microcontroller for Wi-Fi streaming
- **3D-printed enclosure** with a rigidly mounted AprilTag
- **LiPo battery** (500 mAh, ~4 hours runtime)

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

Project Aria Glasses
--------------------

RoSHI uses `Project Aria <https://www.projectaria.com/>`_ glasses for:

- 6-DoF head tracking via onboard SLAM
- Egocentric RGB video capture
- Machine Perception Services (MPS) for post-processing

Bill of Materials
-----------------

.. list-table::
   :header-rows: 1
   :widths: 40 20 20

   * - Item
     - Quantity
     - Approx. Cost
   * - BNO085 IMU breakout
     - 9
     - $12 each
   * - ESP32 dev board
     - 9
     - $8 each
   * - LiPo battery (500 mAh)
     - 9
     - $5 each
   * - AprilTag prints (Tag36h11)
     - 9
     - ~$2 total
   * - 3D-printed enclosures
     - 9
     - ~$15 total
   * - Velcro straps
     - 9
     - ~$10 total
