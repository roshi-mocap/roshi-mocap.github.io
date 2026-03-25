Installation
============

Prerequisites
-------------

- Project Aria glasses with MPS (Machine Perception Services) access
- iPhone or iPad running iOS 17.6+ (for calibration)
- NVIDIA GPU with CUDA support

.. code-block:: bash

   git clone https://github.com/Jirl-upenn/RoSHI-MoCap.git
   cd RoSHI-MoCap

Conda Environments
------------------

RoSHI uses three separate conda environments for different pipeline components.

**roshi** — main pipeline (Python 3.12)

.. raw:: html

   <p class="todo-red">TODO @Margaret: Update this section if we merge EgoAllo into our code.</p>

Handles IMU data reception, calibration, pose reconstruction, synchronization,
and `EgoAllo <https://github.com/facebookresearch/egoallo>`_-based
diffusion pose estimation.

.. code-block:: bash

   conda create -n roshi python=3.12
   conda activate roshi
   pip install -r requirements_roshi.txt

**sam_3d_body** — 3D body estimation from video (Python 3.11)

Used by the `sam-3d-body <https://github.com/Jirl-upenn/RoSHI-MoCap/tree/main/sam-3d-body>`_
module for extracting SMPL-X body parameters from third-person video frames.
See the `installation guide <https://github.com/Jirl-upenn/RoSHI-MoCap/blob/main/sam-3d-body/INSTALL.md>`_
for detailed setup instructions and checkpoint downloads.

**mhr** — motion and hand reconstruction (Python 3.12)

Used by the `MHR <https://github.com/Jirl-upenn/RoSHI-MoCap/tree/main/MHR>`_ module to convert
MHR format to SMPL. Refer to its
`README <https://github.com/Jirl-upenn/RoSHI-MoCap/blob/main/MHR/README.md>`_
for detailed installation instructions and checkpoint downloads.

Model Files
-----------

SMPL body models are licensed separately and must be placed under ``model/``:

.. code-block:: text

   model/
   ├── smplh/
   │   └── neutral/model.npz
   └── smplx/
       └── SMPLX_NEUTRAL.npz

See the official `SMPL-H <https://mano.is.tue.mpg.de/>`_ and
`SMPL-X <https://smpl-x.is.tue.mpg.de/>`_ distribution sites for the
required model downloads.

