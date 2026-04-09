Installation
============

This section covers the four components you need to install and set up before
using RoSHI:

1. **Environment & Codebase** — software environments, dependencies, model files
2. **Calibration App** — iOS companion app for sensor-to-bone calibration
3. **Hardware – IMUs** — 9 body-worn IMU trackers with AprilTags
4. **Aria Glasses** — Project Aria for egocentric SLAM and hand tracking

1. Environment & Codebase
-------------------------

Prerequisites
^^^^^^^^^^^^^

- NVIDIA GPU with CUDA support
- Python 3.12+

We recommend using conda to manage the environment and dependencies.

Clone the main repository:

.. code-block:: bash

   git clone https://github.com/Jirl-upenn/RoSHI-MoCap.git
   cd RoSHI-MoCap

Conda Environments
^^^^^^^^^^^^^^^^^^

RoSHI uses 3 separate conda environments for different pipeline components.

**roshi** — main pipeline + EgoAllo inference (Python 3.12)

This environment handles IMU data reception, calibration, pose reconstruction, synchronization,
and `EgoAllo <https://github.com/brentyi/egoallo>`_-based
diffusion pose estimation with our guidance optimizer. EgoAllo is integrated directly into the codebase
under ``src/egoallo/``.

.. code-block:: bash

   conda create -n roshi python=3.12
   conda activate roshi

   # Install the package (includes egoallo and all dependencies)
   pip install -e .

   # JAX with CUDA support (required for guidance optimization)
   pip install "jax[cuda12]>=0.6"
   pip install git+https://github.com/brentyi/jaxls.git

**sam_3d_body** — 3D body estimation from video (Python 3.11)

This environment is used by the `sam-3d-body <https://github.com/Jirl-upenn/RoSHI-MoCap/tree/main/sam-3d-body>`_
module for extracting SMPL-X body parameters from third-person video frames as part of our calibration pipeline.
See the `installation guide <https://github.com/Jirl-upenn/RoSHI-MoCap/blob/main/sam-3d-body/INSTALL.md>`_
for detailed setup instructions. Model checkpoints should be placed under ``model/sam3d/``
(see `Model Files`_ below).

**mhr** — motion and hand reconstruction (Python 3.12)

This environment is used by the `MHR <https://github.com/Jirl-upenn/RoSHI-MoCap/tree/main/MHR>`_ module to convert
MHR format to SMPL-X as part of our calibration pipeline. Refer to its
`README <https://github.com/Jirl-upenn/RoSHI-MoCap/blob/main/MHR/README.md>`_
for detailed installation instructions. Model checkpoints should be placed under ``model/mhr/``
(see `Model Files`_ below).

Model Files
^^^^^^^^^^^

All model checkpoints are placed under ``model/``. Some models are licensed
separately and must be downloaded manually.

.. code-block:: text

   model/
   ├── egoallo/                           # EgoAllo diffusion checkpoint
   │   └── checkpoints_3000000/
   │       ├── model.safetensors
   │       └── ...
   ├── mhr/                               # MHR model assets (full bundle)
   │   ├── mhr_model.pt
   │   ├── lod*.fbx
   │   ├── compact_v6_1.model
   │   ├── corrective_activation.npz
   │   └── corrective_blendshapes_lod*.npz
   ├── sam3d/                             # SAM 3D Body checkpoint
   │   └── sam-3d-body-dinov3/
   │       ├── model.ckpt
   │       ├── model_config.yaml
   │       └── assets/
   │           └── mhr_model.pt
   ├── smplh/                             # SMPL-H body model
   │   └── neutral/model.npz
   └── smplx/                             # SMPL-X body model
       └── SMPLX_NEUTRAL.npz

- **SAM 3D Body**: download the ``sam-3d-body-dinov3`` checkpoint from
  `Hugging Face <https://huggingface.co/facebook/sam-3d-body-dinov3>`_
  (access request required). Place it under ``model/sam3d/``:

  .. code-block:: bash

     huggingface-cli download facebook/sam-3d-body-dinov3 \
         --local-dir model/sam3d/sam-3d-body-dinov3

- **MHR**: download the full assets bundle from the
  `MHR GitHub release <https://github.com/facebookresearch/MHR/releases/tag/v1.0.0>`_.
  The MHR→SMPL-X conversion requires the complete assets (LOD meshes,
  corrective blendshapes, etc.), not just the torchscript model:

  .. code-block:: bash

     curl -OL https://github.com/facebookresearch/MHR/releases/download/v1.0.0/assets.zip
     unzip assets.zip -d model/mhr/ && rm assets.zip
     # Flatten: move files from model/mhr/assets/ up to model/mhr/
     mv model/mhr/assets/* model/mhr/ && rmdir model/mhr/assets

- **SMPL-H** (16 shape parameters, "Extended SMPL+H model"): download from the
  `MANO project page <https://mano.is.tue.mpg.de/>`_.
  Used by EgoAllo for diffusion-based pose estimation.
- **SMPL-X**: download from the
  `SMPL-X project page <https://smpl-x.is.tue.mpg.de/>`_.
  Used by the calibration pipeline and IMU pose reconstruction.
- **EgoAllo checkpoint**: run ``bash scripts/download_checkpoint_and_data.sh``,
  or download manually from
  `Google Drive <https://drive.google.com/file/d/14bDkWixFgo3U6dgyrCRmLoXSsXkrDA2w/view?usp=drive_link>`_.

Sample Data
^^^^^^^^^^^

A sample recording is available for testing the full postprocessing pipeline.
Download from
`Google Drive <https://drive.google.com/file/d/1FT1rDZvcw7Yv5sHv-mdlsmndZcEfuSWU/view?usp=sharing>`_
and extract into ``received_recordings/``:

.. code-block:: bash

   # Download sample_data.zip from the link above, then:
   unzip sample_data.zip -d received_recordings/

This provides a complete raw session (video, metadata, IMU, Aria VRS + MPS outputs) ready for
the :doc:`postprocessing pipeline </pipeline/postprocessing>`.

Project Structure
^^^^^^^^^^^^^^^^^

After setup, the repository is organized as follows:

.. code-block:: text

   RoSHI-MoCap/
   ├── src/
   │   ├── egoallo/          # EgoAllo: diffusion model + IMU guidance optimizer
   │   ├── pipeline/         # End-to-end pipeline scripts
   │   │   ├── 01_receiver.py      # Receive calibration data from iOS app
   │   │   ├── 02_calibrate.py     # Calibrate bone-to-sensor rotation offsets
   │   │   ├── 03_sync.py          # Synchronize RGB + calibrated IMU data
   │   │   ├── 04_inference.py     # Run EgoAllo diffusion-based pose estimation
   │   │   ├── 05_visualize.py          # Visualize IMU FK and SAM results (no localization)
   │   │   ├── 05_visualize_roshi.py   # Visualize RoSHI pipeline results
   │   │   └── 06_evaluate.py          # Evaluate against OptiTrack ground truth
   │   └── utils/             # Shared utilities
   ├── sam-3d-body/            # SAM 3D Body
   ├── MHR/                   # Momentum Human Rig
   ├── hardware/              # IMU hardware driver (ESP32 serial reader)
   ├── evaluation/            # Evaluation scripts and ground truth
   ├── scripts/               # Download scripts
   ├── model/                 # All model files (checkpoints, SMPL-X, etc.)
   ├── received_recordings/   # Raw + processed session data
   │   └── <session_name>/    # One directory per recording session
   ├── pyproject.toml         # Package configuration
   └── requirements_roshi.txt # Pip requirements

2. Calibration App
------------------

The RoSHI calibration app runs on an iOS device and is used to record a
short video for sensor-to-bone calibration. See the `RoSHI-App repository <https://github.com/Jirl-upenn/RoSHI-App>`_ for
build instructions, and :doc:`/calibration/app_setup` for detailed setup and
receiver configuration.

3. Hardware -- IMUs
-------------------

We open-source our 9-IMU design. For building the assembled tracker, including
the 3D-printed IMU case, routers, and more information, please visit the
`Hardware Documentation <https://roshi-mocap.github.io/documentation/hardware/index.html>`_.

4. Aria Glasses
---------------

RoSHI has been tested with both Aria Gen 1 (recording profile 9) and
Gen 2 (recording profile 8). The current codebase is validated on **Gen 2**.

For device setup, recording profiles, and MPS submission, refer to the
official `Aria Gen 2 documentation <https://facebookresearch.github.io/projectaria_tools/gen2/>`_.
