Evaluation
==========

RoSHI is evaluated against OptiTrack motion capture ground truth across 11
activities.

Metrics
-------

- **MPJPE** (cm): mean per-joint position error in world coordinates
- **JAE** (deg): geodesic joint angle error (root-invariant)
- **Recall**: percentage of GT frames with a valid prediction

Methods
-------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Method
     - Description
   * - IMU-only
     - Forward kinematics from calibrated IMUs with naive global positioning
   * - IMU + EgoAllo root
     - IMU joint rotations with EgoAllo-estimated root position
   * - EgoAllo
     - EgoAllo egocentric pose estimation (no IMU)
   * - RoSHI (Ours)
     - IMU + diffusion test-time optimization
   * - SAM3D
     - SAM-3D-Body single-image reconstruction

Overall Results
---------------

.. list-table::
   :header-rows: 1
   :widths: 25 15 15 15

   * - Method
     - MPJPE (cm)
     - JAE (deg)
     - Recall
   * - IMU-only
     - 17.3
     - 11.4
     - ---
   * - IMU + EgoAllo root
     - 12.3
     - 11.4
     - ---
   * - EgoAllo
     - 10.7
     - 15.6
     - ---
   * - **RoSHI (Ours)**
     - **9.9**
     - **12.6**
     - ---
   * - SAM3D
     - 13.5
     - 10.8
     - 92.3%

Per-Activity Results
--------------------

.. list-table::
   :header-rows: 1
   :widths: 28 12 12 12 12 12 12 12 12 12 12

   * - Method
     - Walk
     - Stretch
     - Jump-jack
     - Pick-up
     - Walk-hi
     - Pickup-walk
     - Jog
     - Jump
     - Slide
     - Tennis
   * - IMU-only
     - 9.6
     - 15.7
     - 14.8
     - 26.7
     - 18.1
     - 27.3
     - 14.4
     - 15.2
     - 9.2
     - 23.0
   * - EgoAllo
     - 10.9
     - 8.9
     - 11.7
     - 10.7
     - 9.3
     - 11.1
     - 8.4
     - 11.3
     - 9.8
     - 15.5
   * - **RoSHI**
     - 11.6
     - **8.2**
     - **8.4**
     - **10.3**
     - **9.0**
     - 11.3
     - 9.2
     - **10.3**
     - **9.1**
     - 12.9
   * - SAM3D
     - **9.9**
     - 10.6
     - 10.1
     - 10.7
     - 9.7
     - **11.1**
     - **10.2**
     - 10.9
     - 18.6
     - 21.9

*(MPJPE in cm. Ball-throwing-catching omitted for space.)*

Running Evaluation
------------------

The OptiTrack ground truth and the pre-computed predictions for every method
(27 MB) are hosted on
`Google Drive <https://drive.google.com/file/d/1I0FfBCEsV5LmAtGimnHunU5VQih4-LVQ/view?usp=sharing>`_.
Download and extract them into ``evaluation/data/``:

.. code-block:: bash

   gdown 1I0FfBCEsV5LmAtGimnHunU5VQih4-LVQ
   unzip evaluation_data.zip -d evaluation/data/ && rm evaluation_data.zip

Then recompute the metrics:

.. code-block:: bash

   conda activate roshi
   python evaluation/compute_metrics.py

Data is organized by activity under ``evaluation/data/``:

.. code-block:: text

   evaluation/data/
   ├── 01_walk_march_jog_run/
   │   ├── optitrack_gt.npz      # Ground truth
   │   ├── roshi.npz             # RoSHI (Ours)
   │   ├── egoallo.npz           # EgoAllo baseline
   │   ├── imu_only.npz          # IMU FK baseline
   │   ├── imu_egoallo.npz       # IMU + EgoAllo root baseline
   │   └── sam3d.npz             # SAM-3D baseline
   ├── 02_stretch_boxing_bow_wave/
   ├── ...
   └── 11_ball-throwing-catching/

Every NPZ contains:

- ``joints_opti``: joint positions in the OptiTrack Z-up world frame ``(T, 22, 3)``
- ``timestamps_ns``: UTC timestamps in nanoseconds ``(T,)``

``optitrack_gt.npz`` additionally stores ``n_camera_frames``, the number of
third-person camera frames in the activity, which is the denominator of the
SAM3D recall.

An activity is one continuous motion, which may span two recordings: each
session was captured as a sequence of takes and split at the point where the
subject changed activity, so adjacent takes contributing to the same activity
are concatenated here. Predictions are scored against the nearest ground-truth
frame in time.
