Guidance Parameters
===================

For calibration math, see :doc:`/calibration/math`.

Overview
--------

After the diffusion model predicts a pose sequence, a Levenberg-Marquardt
optimizer refines it to be physically plausible and consistent with sensor
readings. The optimizer runs twice: once between denoising steps (``inner``,
5 iterations) and once after sampling is complete (``post``, 20 iterations).

Shared Constraints (All Modes)
------------------------------

These constraints are applied in every guidance mode, including pure
``egoallo``:

.. list-table::
   :header-rows: 1
   :widths: 30 12 58

   * - Constraint
     - Weight
     - What it does
   * - Pose prior
     - 1.0
     - Keeps joint rotations close to the diffusion output
   * - Torso prior
     - 5.0
     - Keeps torso joint positions close to the diffusion output
   * - Delta smoothness
     - 10.0
     - Prevents large frame-to-frame changes in the optimizer correction
   * - Velocity smoothness
     - 5.0
     - Penalizes acceleration in joint rotations (reduces jitter)
   * - Foot skating
     - 30.0
     - Prevents foot joints from sliding when contact is predicted

IMU Constraints (RoSHI Modes)
------------------------------

These are added in ``roshi`` and ``roshi_ariahand`` modes:

.. list-table::
   :header-rows: 1
   :widths: 30 12 58

   * - Constraint
     - Weight
     - What it does
   * - Local joint matching
     - 5.0
     - Each IMU-equipped joint rotation should match its IMU reading
   * - Pelvis rotation matching
     - 5.0
     - Frame-to-frame pelvis rotation change should match the pelvis IMU
   * - Body prior
     - 0.1
     - Extra prior to keep IMU-guided poses near the diffusion output
   * - Body smoothness
     - 10.0
     - Extra temporal smoothing for body joints

**Local joint matching** minimizes the geodesic distance between predicted and
IMU-derived parent-relative rotations:

.. math::

   \mathcal{L}_{\text{local}} =
   \sum_{j \in \mathcal{J}_{\text{IMU}}}
   \left\lVert
   \log\!\left(
   \hat{R}_{j}^{\top} \cdot R_{j}^{\text{IMU}}
   \right)
   \right\rVert^{2}

**Pelvis rotation matching**:

.. math::

   \mathcal{L}_{\text{pelvis}} =
   \sum_{t}
   \left\lVert
   \log\!\left(
   \Delta \hat{R}_{\text{pelvis}}^{\top}(t) \cdot
   \Delta R_{\text{pelvis}}^{\text{IMU}}(t)
   \right)
   \right\rVert^{2}

**Body smoothness** penalizes large frame-to-frame rotation changes:

.. math::

   \mathcal{L}_{\text{smooth}} =
   \sum_{t} \sum_{j}
   \left\lVert
   \log\!\left(
   \hat{R}_{j}(t)^{\top} \cdot \hat{R}_{j}(t{+}1)
   \right)
   \right\rVert^{2}
