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
   * - Lower-body joint limits
     - 50.0
     - Soft penalty for biomechanically implausible knee/ankle rotations
       (see :ref:`lower-body-joint-limits`)

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

.. _lower-body-joint-limits:

Lower-Body Joint Angle Limits
------------------------------

The diffusion prior occasionally produces biomechanically impossible knee or
ankle poses (hyperextended knees, severely twisted ankles). Two complementary
mechanisms keep the lower body realistic:

1. A **soft penalty** inside the LM optimizer (used in every guidance mode),
   so small violations push the solution away from invalid regions while still
   respecting the IMU and prior terms.
2. A **hard clamp** applied once at inference time after the final pose has
   been recovered (see :ref:`Step 4 <joint-limit-clamp>` in
   :doc:`postprocessing`), which guarantees the saved ``body_quats`` never
   exceed the limits.

Joints and limits
~~~~~~~~~~~~~~~~~

Limits are applied per axis on the ``log`` (axis-angle) of each joint's
parent-relative rotation. Indices follow the SMPL-H 21-joint body convention
(root excluded):

.. list-table::
   :header-rows: 1
   :widths: 22 12 22 22 22

   * - Joint
     - Index
     - X (flex/ext)
     - Y (abd/add)
     - Z (int/ext rot)
   * - Left / Right knee
     - 3, 4
     - no hyperextension (X ≥ 0)
     - ±5°
     - ±10°
   * - Left / Right ankle
     - 6, 7
     - —
     - ±25° (inv/eversion)
     - ±20°

Soft penalty (optimizer)
~~~~~~~~~~~~~~~~~~~~~~~~

For each constrained joint :math:`j` and axis :math:`a` with limit
:math:`\theta^{\max}_{j,a}`, the optimizer adds a one-sided hinge residual on
the log-map components :math:`\boldsymbol{\omega}_{j} = \log \hat{R}_{j}`:

.. math::

   \mathcal{L}_{\text{limit}} =
   w_{\text{limit}} \sum_{t} \Big[
     \sum_{j \in \{\text{knee}\}} \max(-\omega_{j,x}(t),\, 0)^{2}
   + \sum_{j,\,a \in \{y,z\}}
     \max\!\big(|\omega_{j,a}(t)| - \theta^{\max}_{j,a},\, 0\big)^{2}
   \Big]

with :math:`w_{\text{limit}} = 50.0`. The knee X term penalises only negative
values (hyperextension); the abduction/rotation axes are penalised
symmetrically once the limit is exceeded, so motions that stay within the box
incur zero cost.
