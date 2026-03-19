Pose Estimation
===============

RoSHI uses a guided diffusion approach to estimate full-body 3D pose from
the fused IMU and egocentric data.

Pipeline Overview
-----------------

1. **Head trajectory**: extracted from Aria SLAM (6-DoF)
2. **Bone orientations**: derived from the calibrated IMU trackers
3. **EgoAllo diffusion**: conditioned on the head trajectory, guided by IMU
   bone orientations

IMU Guidance
------------

The diffusion process is guided using three complementary constraints:

- **Joint angle matching**: direct comparison of observable joint angles
  (elbow, hip, knee)
- **Relative orientation consistency**: between the pelvis and shoulders
- **Temporal smoothness**: of pelvis-joint rotations across consecutive frames

Output Format
-------------

The pipeline outputs per-frame SMPL body model parameters:

- **Body pose**: joint rotations in axis-angle format
- **Root translation**: in the global (Aria SLAM) coordinate frame
- **Body shape**: beta parameters estimated during calibration

The calibrated session artifacts consumed by this stage are summarized on
:doc:`session_layout`.
