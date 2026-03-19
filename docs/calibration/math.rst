Calibration Math
================
This page summarizes the rotation conventions used by the RoSHI calibration pipeline and the equations used to solve both **sensor-to-bone calibration offsets** and **per-IMU world alignment**.


Coordinate Frames
-----------------

.. list-table::
   :header-rows: 1
   :widths: 15 45

   * - Frame
     - Description
   * - :math:`C`
     - Camera frame using the OpenCV convention, with :math:`x` right,
       :math:`y` down, and :math:`z` forward
   * - :math:`B`
     - Bone frame from the SMPL-X joint
   * - :math:`T`
     - AprilTag frame rigidly attached to the IMU
   * - :math:`S`
     - IMU sensor frame from the fused quaternion output
   * - :math:`W_i`
     - Per-IMU world frame, gravity aligned with arbitrary heading
   * - :math:`W_p`
     - Shared world frame using the pelvis IMU as reference

Offset Calibration
------------------

The AprilTag is rigidly attached to the body segment. At time :math:`t`:

.. math::

   {}^{C}R_{T}(t) = {}^{C}R_{B}(t) \cdot {}^{B}R_{T}

Rearranging gives a frame-wise estimate of the constant offset:

.. math::

   {}^{B}R_{T}(t) = \left({}^{C}R_{B}(t)\right)^{\top} \cdot {}^{C}R_{T}(t)

RoSHI then computes the final calibration by minimizing the geodesic distance
over all valid frames:

.. math::

   \widehat{{}^{B}R_{T}} =
   \arg\min_{R \in SO(3)}
   \sum_{t=1}^{N} \rho\left(d_g\left(R, {}^{B}R_{T}(t)\right)\right)

where the geodesic distance is:

.. math::

   d_g(R_1, R_2) = \left\lVert \log\left(R_1^{\top}R_2\right) \right\rVert

Supported Optimization Methods
------------------------------

.. list-table::
   :header-rows: 1
   :widths: 18 24 34

   * - Method
     - Loss
     - Typical use
   * - ``karcher`` (default)
     - Geodesic L2
     - Clean data with approximately Gaussian noise
   * - ``huber``
     - L2 near zero, L1 for outliers
     - Moderate outliers
   * - ``cauchy``
     - Cauchy / Lorentzian
     - Heavy outliers
   * - ``l1``
     - Geodesic L1
     - Median-like robustness
   * - ``ransac``
     - RANSAC plus Karcher refinement
     - Severely corrupted samples

.. note::
   In our tests, there is no significant difference between the performance of these solvers. ``karcher`` tended to work slightly better overall.
   ``ransac`` can potentially be stronger but typically benefited from more tuning.


IMU-Only Pose Reconstruction
----------------------------

Given the calibrated offset :math:`{}^{B}R_{S}` and a live IMU reading
:math:`{}^{W_i}R_{S}(t)`, the corresponding bone orientation is:

.. math::

   {}^{W_i}R_{B}(t) =
   {}^{W_i}R_{S}(t) \cdot \left({}^{B}R_{S}\right)^{\top}

World-frame alignment uses AprilTag observations to estimate
:math:`{}^{W_p}R_{W_i}` so the individual IMU headings can be expressed in a
shared pelvis-centric frame.

For each joint IMU, RoSHI first estimates the camera-to-IMU-world rotation:

.. math::

   {}^{C}R_{W_i}(t) =
   {}^{C}R_{T_i}(t) \cdot \left({}^{W_i}R_{T_i}(t)\right)^{\top}

These per-frame estimates are averaged over time, and the pelvis world is used
as the shared reference:

.. math::

   {}^{W_p}R_{W_i} =
   \left(\overline{{}^{C}R_{W_p}}\right)^{\top} \cdot \overline{{}^{C}R_{W_i}}

The aligned bone orientation in the pelvis world then becomes:

.. math::

   {}^{W_p}R_{B}(t) =
   {}^{W_p}R_{W_i} \cdot {}^{W_i}R_{B}(t)

Tag-to-IMU Axis Mapping
-----------------------

The rigid transform from the AprilTag frame to the IMU frame is:

.. math::

   {}^{T}R_{S} =
   \begin{bmatrix}
   0 & -1 & 0 \\
   -1 & 0 & 0 \\
   0 & 0 & -1
   \end{bmatrix}

.. note::
   We get this mapping from the **BNO085 IMU frame** and **AprilTag frame** conventions.

   - The **BNO085 IMU frame** is given in the `BNO08X datasheet <https://www.ceva-ip.com/wp-content/uploads/BNO080_085-Datasheet.pdf>`_ on page 41.
   - The **AprilTag frame** is centered on the tag with :math:`x` right, :math:`y` down, and :math:`z` into the tag. See the `AprilTag 3 documentation <https://github.com/AprilRobotics/apriltag>`_.


