Overview
========

.. figure:: /_static/figure1.png
   :align: center
   :alt: RoSHI system overview

RoSHI is a low-cost, portable system for in-the-wild human motion capture. It
fuses information from **9 body-worn IMUs** and **Project Aria glasses** to
output synchronized **3D body pose (SMPL format)**, **egocentric RGB video**,
and **a globally consistent root trajectory**. The figure above shows an example
of data being collected, processed, and deployed to a real robot.

Key Features
------------

- **Low-cost**: under $500 in tracker hardware — see the :doc:`/hardware/index` section for a detailed item list
- **Quick calibration**: a 20–40 second iPhone video is enough — refer to the :doc:`/calibration/index` section for details
- **Portable** & **In-the-wild**: the entire system is easily wearable, and once calibrated you can move freely in any environment
