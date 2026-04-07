Assembly
========

This page walks through assembling a RoSHI body tracker based on the SlimeVR
Hyperion PCB, a **BNO085** IMU, and a **custom 3D-printed case** sized for rigid
AprilTag mounting. For why the tag matters and how we use it in calibration,
see :doc:`april_tag`. **STEP/STL files, firmware, and Python tools** are in the
`RoSHI-Hardware`_ repo; after mechanical build, flash firmware per :doc:`software`.

.. _RoSHI-Hardware: https://github.com/Jirl-upenn/RoSHI-Hardware

3D printing
-----------

Printed parts for the tracker case, receiver enclosure, strap hardware, and
related pieces are published under **`RoSHI-Hardware` → `3D Prints/`** (`see repo`_).

.. _see repo: https://github.com/Jirl-upenn/RoSHI-Hardware/tree/main/3D%20Prints

- **`Design/`** — CAD sources (STEP and design files).
- **`Print/`** — **STL** files ready for slicing.

We print our parts in **PLA matte**. Other materials (for example **PETG**)
often need **tolerance adjustments** in the slicer or CAD—the fits are tuned for
our filament and machine. The internal spacing is intended as a **firm press
fit** so the **IMU stack does not rattle or vibrate** during motion.

PCB source and ordering
-----------------------

We use the PCB and ordering workflow from the **SlimeVR Hyperion Multi-IMU BMI
BNO** project (`Case guide on GitHub`_), including Gerber ordering notes.

.. _Case guide on GitHub: https://github.com/Shine-Bright-Meow/SlimeVR-Hyperion-BMI-BNO-PCB-Case#case-guide

Use that repository for **ordering PCBs** (for example Gerbers to JLCPCB),
recommended board thickness, and reference **Hyperion Lite** case variants where
helpful.

**IMU choice.** We use the **BNO085** because it includes **on-board sensor
fusion**, so orientation is ready to use without extra fusion code on the MCU. A
lower-cost path such as **ICM-45686 + QMC6309** is possible on the same PCB
family, but you must implement **custom sensor fusion** on the **ESP8266
WeMos D1 Mini** and flash that before the tracker can transmit usable
orientation data.

**Case.** We do **not** use the stock Hyperion case as-is: RoSHI needs a **custom
case** that holds a printed AprilTag in a known pose for tag-based calibration.
See :doc:`april_tag` for tag size, family, and mounting goals.

**Other SlimeVR-style trackers.** Many DIY SlimeVR-compatible PCBs and IMUs can
stream orientation over Wi-Fi in a similar way. The practical constraint for
RoSHI is mechanical: **the enclosure must present a rigid AprilTag on a known
face**. Any alternative board or IMU module is fine in principle, but you will
need to **redesign or adapt the case** (strap mounts, clearance, tag plane) for
your PCB outline and tag size.

Tracker assembly
----------------

The photos below follow one build order: charging board first, then passives and
connectors, then the IMU and MCU, then test and switch, then the enclosure stack.

Parts layout
~~~~~~~~~~~~

.. figure:: ../_static/hardware/assembly/1_layout.jpg
   :alt: Components and PCB laid out before soldering
   :width: 85%

   Overview of parts and PCB orientation before assembly.

Charging board (TP4056)
~~~~~~~~~~~~~~~~~~~~~~~

We start with the **charging board** (TP4056 “battery charger” module in the
Hyperion design—sometimes informally called the BMS section in build guides).

#. Seat the module so **its holes line up** with the PCB pads and outline.
#. **Tack one pin:** apply solder to a single pad and solder one lead first.
#. **Align the rest:** reheat that joint and gently nudge the board until all
   pads line up, then solder the remaining pins.
#. **Inspect both sides:** joints should be shiny and complete. When you flip
   the board and look from the bottom, **each through-hole should show a filled
   annulus** (solder wicked through the barrel—not a dry hole).

.. figure:: ../_static/hardware/assembly/2_bms_place.jpg
   :alt: Charging board placed on the PCB before soldering
   :width: 85%

   Align the charging module to the PCB footprint.

.. figure:: ../_static/hardware/assembly/3_bms_solder.jpg
   :alt: Soldering the charging board pins
   :width: 85%

   Tack one pin, align, then finish all joints.

.. figure:: ../_static/hardware/assembly/4_bms_back.jpg
   :alt: View of solder joints from the back of the PCB
   :width: 85%

   From underneath, through-holes should show proper fill.

Battery connector (JST)
~~~~~~~~~~~~~~~~~~~~~~~

Insert the **through-hole JST** into the battery power footprint. Adjust it so it
sits **perpendicular** to the board and **aligned with the board edges**, then
**solder from the underside** so each joint is solid.

.. figure:: ../_static/hardware/assembly/5_jst.jpg
   :alt: JST battery connector soldered to the PCB
   :width: 85%

   JST seated square and soldered from below before taller parts go on.

Resistor and diode
~~~~~~~~~~~~~~~~~~

Use a **180 kΩ** resistor and the **diode called out in the BOM**. **Diode
polarity** matches the silkscreen on the board—orient the part to that drawing
before soldering. Fit passives flush, solder so **solder fully covers each hole**
on both sides, and trim leads.

.. figure:: ../_static/hardware/assembly/6_resistor_hole.jpg
   :alt: Resistor leads through the PCB
   :width: 85%

.. figure:: ../_static/hardware/assembly/7_resistor_soldered.jpg
   :alt: Resistor soldered on the component side
   :width: 85%

.. figure:: ../_static/hardware/assembly/8_resistor_back.jpg
   :alt: Resistor joints viewed from the solder side
   :width: 85%

Pin headers (IMU and ESP32 Wemos D1 Mini)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For both the **IMU** and **ESP32 Wemos D1 Mini**, having the **long side of the
pins facing up** makes alignment easier. After soldering, **make sure solder
fully covers each hole**—no dry or shallow barrels.

.. figure:: ../_static/hardware/assembly/9_header.jpg
   :alt: Pin headers installed on the PCB
   :width: 85%

.. figure:: ../_static/hardware/assembly/10_header_back.jpg
   :alt: Header joints from the bottom of the PCB
   :width: 85%

BNO085 IMU
~~~~~~~~~~

Slide the **BNO085** breakout onto its headers. **Solder one pin first**, then
check that the module is **almost parallel** to the lower PCB before soldering
the rest. Finish all pins so the joints are complete.

.. figure:: ../_static/hardware/assembly/11_IMU.jpg
   :alt: BNO085 IMU module mounted on the PCB
   :width: 85%

ESP32 (Wemos D1 Mini)
~~~~~~~~~~~~~~~~~~~~~

Start by **soldering one pin** on the D1 Mini. When that joint is done, **clip
the long pins on top** as needed, then **re-solder any pin** that did not take
cleanly. Use the same idea for the **IMU** if the headers are tall after seating.

.. figure:: ../_static/hardware/assembly/12_ESP.jpg
   :alt: ESP32 module seated on headers
   :width: 85%

Connectivity test
~~~~~~~~~~~~~~~~~

.. figure:: ../_static/hardware/assembly/13_Testing.jpg
   :alt: Multimeter continuity check on the tracker PCB
   :width: 85%

   **Continuity check with a multimeter** (beep mode): verify **VCC**, **GND**,
   and other nets **from the test points** (or designated pads) so power and
   ground wiring matches the design before you apply battery power.

Power switch
~~~~~~~~~~~~

Use the **switch tray** from your **print list** to hold alignment. Press the
switch down until the pins **seat in the holes**, then solder by **pressing the
iron into each pin** and **filling the hole with solder** so the joint is solid.

.. figure:: ../_static/hardware/assembly/14_switch.jpg
   :alt: Power switch before final soldering
   :width: 85%

.. figure:: ../_static/hardware/assembly/15_switch_soldered.jpg
   :alt: Power switch soldered and flush
   :width: 85%

Power on
~~~~~~~~

After the **connectivity test** looks good, apply power. If the **blue LED on the
D1 Mini** comes on, the board is ready for **firmware flashing**. (This step is
not a USB data test—just power-on confirmation.)

.. figure:: ../_static/hardware/assembly/16_power_on.jpg
   :alt: Tracker powered on with indicator visible
   :width: 85%

Enclosure and IMU stack
~~~~~~~~~~~~~~~~~~~~~~~

Follow the **3D printing** notes above for material and press-fit goals. Use the
**Design/** or **Print/** folders in `RoSHI-Hardware`_ for STEP/STL.

Route **straps** through the provided loops and tighten so the tracker stays put
without crushing the shell. If you move many units at once, you can use a
**stack tower** (optional print) to keep trackers organized for transport.

.. figure:: ../_static/hardware/assembly/17_IMU_Case.jpg
   :alt: IMU and custom case shell
   :width: 85%

.. figure:: ../_static/hardware/assembly/18_IMU_CAP.jpg
   :alt: Case lid or cap fitted over the PCB stack
   :width: 85%

.. figure:: ../_static/hardware/assembly/19_IMU_wrap.jpg
   :alt: Straps or retention around the tracker case
   :width: 85%

.. figure:: ../_static/hardware/assembly/20_IMU_Full.jpg
   :alt: Fully enclosed tracker module
   :width: 85%

.. figure:: ../_static/hardware/assembly/21_IMU_Stack.jpg
   :alt: Exploded or stacked view of case and PCB
   :width: 85%

   Rigid case closure and strap routing.

Receiver unit
~~~~~~~~~~~~~

The receiver is the **host**: it **takes in data from the trackers** over
**ESP-NOW** on a **2.4 GHz** link using an **external antenna** (the **ESP32-S3
Feather** supports external antenna). **Adafruit I²C bus multiplexers** handle
**sensor routing** on the I²C bus. The Feather connects to a **small OLED** over
**I²C**; that display shows **battery** status (and related UI). **M3 threaded
inserts** secure the **top and bottom** halves of the enclosure. The Feather
**USB-C** connection goes to a **workstation** for the capture pipeline (see
:doc:`../pipeline/index`).

.. figure:: ../_static/hardware/assembly/22_Receiver_Full.jpg
   :alt: RoSHI receiver unit exterior
   :width: 85%

.. figure:: ../_static/hardware/assembly/23_Receiver_Internal.jpg
   :alt: Receiver internal electronics
   :width: 85%

.. figure:: ../_static/hardware/assembly/24_Receiver_Back.jpg
   :alt: Receiver rear panel connectors
   :width: 85%

Next step
---------

When soldering and enclosure work are complete, continue with **firmware
flashing and host Python setup** in :doc:`software`.
