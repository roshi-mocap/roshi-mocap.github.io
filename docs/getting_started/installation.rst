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

   git clone https://github.com/Jirl-upenn/RoSHI.git
   cd RoSHI

Install the Python environment needed for the parts of the RoSHI pipeline you
plan to run. The main repository README lists the core dependencies, and the
bundled projects such as ``sam-3d-body/``, ``MHR/``, and ``egoallo/`` document
their additional setup requirements.

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
