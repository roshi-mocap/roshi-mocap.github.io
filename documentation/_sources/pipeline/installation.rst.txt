Installation
============

Prerequisites
-------------

- Python 3.8+
- Project Aria glasses with MPS (Machine Perception Services) access
- iPhone or iPad running iOS 17.6+ (for calibration)

Python Environment
------------------

.. code-block:: bash

   git clone https://github.com/Jirl-upenn/RoSHI-MoCap.git
   cd RoSHI-MoCap

Install the Python environment needed for the parts of the RoSHI pipeline you
plan to run. The main repository README lists the core dependencies, and the
bundled projects such as ``sam-3d-body/``, ``MHR/``, and ``egoallo/`` document
their additional setup requirements.

Core Dependencies
-----------------

- Python 3.10+
- ``numpy``, ``scipy``, ``torch``, ``smplx``
- ``opencv-python``, ``viser``, ``pillow``
- ``pyserial`` for the IMU hardware interface

Additional Components
---------------------

- ``egoallo/`` additionally requires Python 3.12+, JAX with CUDA, and
  ``jaxls``. See ``egoallo/README_RoSHI_egoallo.md`` for the full setup.
- ``sam-3d-body/`` and ``MHR/`` have their own dependency instructions in
  their respective ``README.md`` files.

Model Files
-----------

SMPL body models are licensed separately and must be placed under ``model/``:

.. code-block:: text

   model/
   ├── smplh/
   │   └── neutral/model.npz
   └── smplx/
       └── SMPLX_NEUTRAL.npz

See the official SMPL-H and SMPL-X distribution sites for the required model
downloads.

IMU Firmware
------------

Each IMU tracker runs firmware that streams BNO085 orientation data over Wi-Fi
at 100 Hz. See the :doc:`../hardware/components` page for flashing instructions.

Calibration App
---------------

The iOS calibration app is available at
`RoSHI-App <https://github.com/Jirl-upenn/RoSHI-App>`_.

.. code-block:: bash

   git clone https://github.com/Jirl-upenn/RoSHI-App.git

See :doc:`../calibration/app_setup` for build and receiver setup, and
:doc:`../calibration/app_reference` for app settings, outputs, and
troubleshooting.
