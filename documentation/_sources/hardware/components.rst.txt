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
