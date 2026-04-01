Guidance Parameters
===================

For calibration math, see :doc:`/calibration/math`.

This page explains, in plain language, what the guidance optimizer is doing
during ``04_inference.py``.

The diffusion model first predicts a pose sequence. Then the optimizer adjusts
that prediction so the final result is:

- close to the diffusion output
- smooth over time
- consistent with the available sensors

Shared Constraints (All Modes)
------------------------------

All guidance modes use these constraints:

- **Pose prior**: keeps joint rotations close to the diffusion output.
- **Torso prior**: keeps torso positions close to the diffusion output.
- **Delta smoothness**: avoids large correction changes between nearby frames.
- **Velocity smoothness**: reduces jitter.
- **Foot skating**: keeps planted feet from sliding.

Extra IMU Constraints (RoSHI Modes)
-----------------------------------

These are only used in ``roshi`` and ``roshi_ariahand``:

- **Local joint matching**: each IMU-equipped joint should match its IMU.
- **Pelvis rotation matching**: pelvis rotation changes should match the pelvis
  IMU.
- **Body smoothness**: adds extra temporal smoothing for the body.

Common Parameters
-----------------

.. list-table::
   :header-rows: 1
   :widths: 38 12 50

   * - Parameter
     - Default
     - Meaning
   * - ``prior_quat_weight``
     - 1.0
     - Strength of the body rotation prior.
   * - ``prior_pos_weight``
     - 5.0
     - Strength of the torso position prior.
   * - ``body_quat_delta_smoothness_weight``
     - 10.0
     - Smooths changes in the optimizer correction.
   * - ``body_quat_smoothness_weight``
     - 1.0
     - Smooths frame-to-frame body rotations.
   * - ``body_quat_vel_smoothness_weight``
     - 5.0
     - Reduces acceleration-like jitter.
   * - ``skate_weight``
     - 30.0
     - Strength of the foot skating penalty.
   * - ``lambda_initial``
     - 0.1
     - Initial damping for the solver.
   * - ``max_iters`` (inner / post)
     - 5 / 20
     - Solver iterations during sampling and post-optimization.

IMU Parameters
--------------

.. list-table::
   :header-rows: 1
   :widths: 38 12 50

   * - Parameter
     - Default
     - Meaning
   * - ``imu_local_quat_weight``
     - 5.0
     - Strength of local joint-to-IMU matching.
   * - ``imu_pelvis_relative_rotation_weight``
     - 5.0
     - Strength of pelvis rotation matching.
   * - ``imu_body_prior_weight``
     - 0.1
     - Extra prior to keep IMU-guided poses near the diffusion output.
   * - ``imu_body_smoothness_weight``
     - 10.0
     - Extra temporal smoothing in IMU-guided modes.

Reference Equations
-------------------

The main IMU guidance terms are:

1. **Local joint matching**

   .. math::

      \mathcal{L}_{\text{local}} =
      \sum_{j \in \mathcal{J}_{\text{IMU}}}
      \left\lVert
      \log\!\left(
      \hat{R}_{j}^{\top} \cdot R_{j}^{\text{IMU}}
      \right)
      \right\rVert^{2}

2. **Pelvis rotation matching**

   .. math::

      \mathcal{L}_{\text{pelvis}} =
      \sum_{t}
      \left\lVert
      \log\!\left(
      \Delta \hat{R}_{\text{pelvis}}^{\top}(t) \cdot
      \Delta R_{\text{pelvis}}^{\text{IMU}}(t)
      \right)
      \right\rVert^{2}

3. **Body smoothness**

   .. math::

      \mathcal{L}_{\text{smooth}} =
      \sum_{t} \sum_{j}
      \left\lVert
      \log\!\left(
      \hat{R}_{j}(t)^{\top} \cdot \hat{R}_{j}(t{+}1)
      \right)
      \right\rVert^{2}
