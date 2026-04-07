AprilTag on trackers
====================

RoSHI estimates body pose by combining **sparse IMU** data with **AprilTag**
observations from egocentric video (Project Aria). Each body tracker carries a
**printed AprilTag** on a **rigid, known face** of its enclosure so calibration
can relate tag poses to IMU frames.

Why not the stock Hyperion case?
--------------------------------

The community **SlimeVR Hyperion Lite** cases (see the `Case guide`__) are
optimized for SlimeVR’s strap layout and internal clearances. They do not
include a standardized, calibration-friendly **AprilTag mounting plane** for
RoSHI.

For RoSHI we use a **custom case** (or a modified print) that:

- Holds the **BNO085** stack and battery from the same PCB design as
  :doc:`assembly`
- Presents a **flat, stiff tag surface** with predictable offset and orientation
  relative to the IMU
- Keeps the tag **visible** to the glasses cameras without occlusion from
  straps or edges

__ https://github.com/Shine-Bright-Meow/SlimeVR-Hyperion-BMI-BNO-PCB-Case#case-guide

Tag family and size
-------------------

RoSHI documentation standardizes on:

- **Family:** Tag36h11 (common in robotics and easy to generate with standard
  tools)
- **Physical size:** **42 mm** outer square for the printed tag (match your
  generator and detection settings)

Use the **same family and ID layout** across all nine body tags as defined in
:doc:`components` (AprilTag ID ↔ body part). Mismatched IDs or sizes will break
calibration association.

Mechanical checklist
--------------------

Before capture sessions:

#. **Rigid bond:** The tag must not flex or peel; use a flat insert or printed
   pocket rather than a loose sticker on fabric.
#. **Known pose:** Document (or CAD) the transform from IMU frame to tag frame
   if you change the case; the calibration procedure assumes consistency across
   trackers of the same design.
#. **Visibility:** No clothing or strap should cover the tag in normal poses;
   matte print reduces glare from room lights.
#. **Alternatives:** If you use a different SlimeVR-class PCB or IMU module, you
   can reuse the same tag spec, but you must **redesign the case** so the tag
   still sits on a stable, visible plane suited to head-mounted cameras.

See also
--------

- Tracker build: :doc:`assembly`
- Tag ID ↔ joint mapping: :doc:`components`
- Calibration pipeline: :doc:`../calibration/index`
