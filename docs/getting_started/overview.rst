Overview
========

RoSHI is a hybrid wearable motion capture system that combines:

- **9 low-cost IMU trackers** (~$30 each, BNO085-based, wireless at 100 Hz)
- **Project Aria glasses** for egocentric SLAM and RGB video

The two modalities are complementary:

- **IMUs** provide robustness to visual occlusion and high-speed motion
- **Egocentric SLAM** anchors long-horizon global localization and stabilizes
  upper-body pose

System Output
-------------

RoSHI produces:

- Full 3D body pose (SMPL format) in a metric global coordinate frame
- Egocentric RGB video
- Globally consistent root trajectory

Key Features
------------

- **Portable**: the entire system is wearable and self-contained
- **Low-cost**: total hardware cost under $500 (excluding Aria glasses)
- **Quick calibration**: 20–40 second iPhone video is all that's needed
- **In-the-wild**: no external cameras or controlled environment required
