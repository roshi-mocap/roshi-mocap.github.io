How to Postprocess the Data
===========================

This section covers the offline processing pipeline that turns raw recordings
into full-body SMPL pose estimates.

.. tip::

   A sample recording is available for testing the full pipeline. Download
   `sample_data.zip <https://drive.google.com/file/d/1FT1rDZvcw7Yv5sHv-mdlsmndZcEfuSWU/view?usp=sharing>`_
   and extract into ``received_recordings/``:

   .. code-block:: bash

      unzip sample_data.zip -d received_recordings/

   This provides a complete raw session (video, metadata, IMU, Aria VRS + MPS
   outputs) that you can use to follow along with every step below.

Step 1: Add Aria Data
---------------------

The Aria VRS recording and MPS outputs must be added to the session directory
manually after the recording is complete:

1. Download the ``.vrs`` file and its JSON sidecar from the Aria companion app.
2. Submit the VRS to `Aria MPS <https://facebookresearch.github.io/projectaria_tools/docs/data_utilities/core_code_snippets/mps>`_
   for SLAM and hand tracking processing.
3. Place the outputs into the session directory:

.. code-block:: text

   received_recordings/<session_name>/
   ├── ...                              # (existing files from recording)
   ├── <recording>.vrs                  # Aria VRS recording
   ├── <recording>.vrs.json             # VRS metadata sidecar
   └── mps_<recording>_vrs/             # Aria MPS outputs
       ├── slam/
       │   ├── closed_loop_trajectory.csv
       │   └── semidense_points.csv.gz
       └── hand_tracking/
           └── hand_tracking_results.csv

Step 2: Calibration Pipeline
-----------------------------

The calibration pipeline can run automatically when the receiver finishes
uploading, or be triggered manually on an existing session:

.. code-block:: bash

   # Run the full calibration pipeline (steps 1–4 below) on an existing session
   python src/pipeline/01_receiver.py --session <session_dir>

This runs four sub-steps:

1. **Prepare session** — extract video frames, camera intrinsics, AprilTag summary.
2. **SAM-3D-Body** — estimate 3D body parameters from third-person RGB frames.
3. **MHR → SMPL-X** — convert MHR outputs to SMPL-X format.
4. **Calibration solve** — compute bone-to-sensor rotation offsets (``imu_calibration.json``).
   Can also be re-run independently via ``python src/pipeline/02_calibrate.py <session_dir>``.

.. note::

   The calibration pipeline automatically detects which sub-steps have already
   been completed and skips them. If you need to re-run a specific step (e.g.
   after updating a model checkpoint), delete its output directory first.

After this step, the session directory contains:

.. code-block:: text

   received_recordings/<session_name>/
   ├── ...                              # (existing files)
   ├── meta/
   │   ├── camera.json                  # Camera intrinsics extracted from metadata
   │   └── calibration_segment.json     # Auto-detected calibration time window
   ├── color/                           # Extracted video frames (PNG)
   ├── frames.csv                       # Frame index, UTC timestamp, image path
   ├── color_apriltag/
   │   └── detection_summary.json       # Per-frame AprilTag detection counts
   ├── body_data/                       # SAM-3D-Body MHR outputs (*.npz per frame)
   ├── smpl_output/                     # SMPL-X conversion results
   │   ├── smpl_parameters.npz          # Joints, rotations, betas across all frames
   │   ├── smpl_vertices.npy            # Mesh vertices (memory-mapped)
   │   └── per_frame/                   # Individual SMPL-X fits
   └── imu_calibration.json             # Bone-to-sensor rotation offsets (B_R_S per joint)

Step 3: Synchronization
------------------------

The sync pipeline aligns IMU, third-person RGB, and (optionally) Aria
egocentric data to a shared UTC timeline:

.. code-block:: bash

   python src/pipeline/03_sync.py <session_dir>

This produces a ``sync/`` folder with calibrated, UTC-aligned data ready for
inference:

.. code-block:: text

   received_recordings/<session_name>/
   ├── ...                              # (existing files)
   └── sync/
       ├── frames.csv                   # UTC-mapped third-person RGB
       ├── color/                       # Symlinked RGB images
       ├── imu_info.csv                 # Calibrated IMU rotations (9 rows per timestamp)
       ├── imu_info.pkl                 # Same data as pickle: {utc_ns: {imu_id: 3x3 rotation matrix}}
       ├── vrs_frames.csv               # (optional) UTC-mapped Aria RGB
       └── vrs_color/                   # (optional) Extracted Aria RGB frames

Step 4: Pose Estimation
------------------------

Run EgoAllo diffusion-based pose estimation conditioned on head trajectory.
The ``--guidance-mode`` flag selects which signals guide the diffusion process:

.. code-block:: bash

   # Default: RoSHI (diffusion + IMU guidance)
   python src/pipeline/04_inference.py --traj-root <session_dir>

   # Or specify a different mode
   python src/pipeline/04_inference.py --traj-root <session_dir> --guidance-mode egoallo

Available guidance modes:

.. list-table::
   :header-rows: 1
   :widths: 20 10 10 10 50

   * - Mode
     - Diffusion
     - IMU
     - Aria Hand
     - Description
   * - ``egoallo``
     - yes
     - no
     - no
     - Pure EgoAllo baseline (foot skating constraint only)
   * - ``egoallo_ariawrist``
     - yes
     - no
     - wrist only
     - EgoAllo + Aria wrist pose guidance (no full hand, no IMU)
   * - ``roshi`` **(default)**
     - yes
     - yes
     - no
     - RoSHI: diffusion guided by IMU bone orientations
   * - ``roshi_ariahand``
     - yes
     - yes
     - yes
     - RoSHI + Aria hand tracking

For details on the IMU guidance constraints and optimizer parameters, see
:doc:`math`.

Results are saved to ``<session_dir>/egoallo_outputs/`` as NPZ files containing:

.. list-table::
   :header-rows: 1
   :widths: 28 72

   * - Key
     - Description
   * - ``Ts_world_cpf``
     - CPF (central pupil frame) poses in world frame (T, 7)
   * - ``Ts_world_root``
     - Root joint (pelvis) pose in world frame (T, 7)
   * - ``body_quats``
     - Local body joint quaternions, wxyz (samples, T, 21, 4)
   * - ``left_hand_quats``
     - Left hand joint quaternions, wxyz (samples, T, 15, 4)
   * - ``right_hand_quats``
     - Right hand joint quaternions, wxyz (samples, T, 15, 4)
   * - ``contacts``
     - Foot contact predictions per body joint (samples, T, 21)
   * - ``betas``
     - SMPL-H body shape parameters (samples, T, 16)
   * - ``timestamps_ns``
     - Tracking timestamps in nanoseconds (T,)

Step 5: Visualization
----------------------

Compare methods side-by-side with third-person RGB:

- **SAM-3D** — third-person video body estimation from the calibration pipeline
- **IMU FK** — pure forward kinematics from calibrated IMUs, no diffusion model, assume missing joints are at the identity
- **RoSHI** — diffusion + IMU guidance (from ``04_inference.py``)
- **EgoAllo** — diffusion baseline outputs (from ``04_inference.py --guidance-mode egoallo``)

.. code-block:: bash

   python src/pipeline/05_visualize.py <session_dir>

For evaluation against OptiTrack ground truth, see :doc:`evaluation`.

