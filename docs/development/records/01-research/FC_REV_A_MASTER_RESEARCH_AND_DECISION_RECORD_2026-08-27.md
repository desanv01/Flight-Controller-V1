> Historical technical record. Names and private workstation/session references were neutralized for publication. Dates and assertions describe the recorded stage, not current physical qualification. See the current validation-status page for later checks.

# Flight Controller Rev A — Master Research, Architecture, Interface & Implementation Record

**Project:** FC Drone / UAS-UAM prototype  
**Record date:** 27 August 2026  
**Status:** Current working master record  
**Scope:** Custom flight-controller PCB, companion-computer integration, modular external interfaces, and the related ESC, propulsion, camera, lidar, power, firmware and implementation decisions.

> This file is the current consolidated working record. The earlier files `FC_REV_A_DECISION_BASELINE_2026-08-27.md` and `DIY_Flight_Controller_PCB_Research_and_Preliminary_BOM_2026-08-26.md` are retained as historical/source material and are not the authority for new design decisions. This master record intentionally reorganizes the current information instead of continuing the old version-history style.

## 0. How to read this record

The user's requests and decisions are the controlling requirements. Statements copied or summarized from supplied reports, repositories, videos, forums, manufacturer pages and standards are engineering references, not instructions that override the user.

The project is a prototype. A successful bench or controlled test does not make the aircraft certified, safe for public operation, or suitable for autonomous operation around people. Propellers must be removed during electrical bring-up and early motor tests, with current limiting, physical restraint and appropriate supervision.

For layer-by-layer execution, use `FC_REV_A_STAGE_MAP_AND_WORKFLOW_2026-08-28.md`. This master record remains the technical source of truth; the stage map controls task separation, entry/exit gates and focused-chat handoffs.

Labels used below:

- **Decision:** current project direction to use unless a later explicit decision changes it.
- **Recommendation:** the presently preferred engineering choice, still subject to validation.
- **Candidate:** an option that still requires datasheet, footprint, availability, thermal and system checks.
- **Open input:** information required before freezing a schematic, PCB or purchasing BOM.
- **Reference only:** useful design evidence or learning material, not automatically production-ready.

## 1. User requirements and project context

### 1.1 Current user decisions

1. The final flight controller will use the **bare MCU chip on a custom PCB**, not a ready-made development board or off-the-shelf flight-controller board.
2. The Rev A approach is to clone or adapt a proven DIY/open hardware design because the complete project must be moving within less than one month. The cloned design must still be checked against the selected parts, interfaces, dimensions, firmware and power architecture.
3. The flight controller should be **Pixhawk-like in connectivity and modularity**: external ESC, receiver, telemetry, GNSS/compass, lidar and companion-computer connections should be serviceable and replaceable.
4. The preferred companion computer is a **Raspberry Pi Compute Module 5 (CM5)**, not a standard Raspberry Pi 5 single-board computer and not a CM5 AI HAT. The CM5 requires a carrier board.
5. The CM5 is intended for YOLO models, object detection, object tracking, camera processing, scanning-lidar processing, mapping or high-level collision-avoidance logic as the implementation matures.
6. The FC remains responsible for stabilization, sensor fusion required for flight, arming, motor outputs, radio-loss behavior and hard failsafes. The CM5 must be optional to basic manual/stabilized flight.
7. The aircraft has separate workstreams for the ESC/motors, transmitter/receiver, lidar attachment and camera attachment. Their electrical and software contracts must be included in the FC design now, even if another team member implements each subsystem.
8. The design should accommodate two sensor attachments: one camera and one lidar. They may connect to or be processed by the CM5 depending on sensor type and data rate.
9. Open-source firmware and open hardware references are important and will be revisited during implementation.
10. The two existing Markdown files should no longer be treated as the active project record; this new file is the consolidated current record.

### 1.2 Workstream ownership and integration boundary

| Workstream | Responsibility | Required FC integration contract |
|---|---|---|
| Flight controller / autopilot | Custom STM32H743 PCB, onboard sensors, firmware port, stabilization and failsafes | Power, debug, sensor, RC, telemetry, ESC-output, GNSS, CAN and companion interfaces |
| ESC and motors | ESC board, motor selection, propulsion wiring and related firmware | Motor-signal protocol, signal/ground connector, telemetry, logic voltage, current and reset behavior |
| Transmitter/receiver | Radio transmitter and receiver PCB/circuits | Receiver protocol, UART/serial levels, supply, failsafe and binding/configuration behavior |
| Lidar attachment | Sensor selection, mount, wiring and driver | FC rangefinder UART/CAN contract or CM5 USB/UART/Ethernet contract; update rate and frame definition |
| Camera attachment | Camera module, mount, lens and video/data path | CM5 CSI/USB/data contract; optional independent FPV video path |
| Companion-computer integration | CM5 carrier, Linux/ROS 2/application, perception and high-level decisions | FC serial/CAN/MAVLink link, power rail, heartbeat, command limits and failure behavior |

No workstream may silently assume that raw battery power, 5 V, 3.3 V, UART labels, CAN termination, PWM polarity or connector pin numbering are interchangeable. Those items must be written into the interface contract.

## 2. Authoritative Rev A decisions

### 2.1 Flight-controller hardware direction

| Area | Rev A decision |
|---|---|
| Main MCU | STM32H743VIT6 bare MCU, custom PCB, LQFP package |
| Primary IMU | ICM-42688-P onboard, connected over SPI and powered from a quiet sensor rail |
| Barometer | BMP390 onboard, with protected vent and appropriate mechanical placement |
| External navigation | External GNSS and compass/magnetometer; keep the magnetic sensor away from power and motor current |
| ESC outputs | External ESC board; signal and ground only on the FC connector; do not route raw battery current through the FC |
| Receiver | External, modular receiver connection; exact protocol is still an open input |
| Telemetry | External modular UART and/or CAN connection |
| Lidar | Downward scalar rangefinder may connect directly to the FC; scanning or 3D lidar should be processed by the CM5 |
| Camera | CM5-side CSI camera for perception; a dedicated analog/digital FPV camera remains a separate video system if required |
| Companion | CM5 on a separate carrier board, separately powered and connected to the FC through a controlled data link |
| Storage | Optional onboard logging, initially microSD or external flash depending on complexity and selected firmware |
| Debug | SWD, reset, boot access, USB-C and test points are required |
| Board style | Pixhawk-inspired modular connector architecture, without claiming exact Pixhawk electrical/mechanical compatibility unless the standard pinout and requirements are followed |
| Sensor modularity | Hybrid architecture: high-rate/noise-sensitive stabilization sensors onboard; selected navigation and payload sensors external |
| Firmware path | ArduPilot is the leading application recommendation; PX4 is a strong alternative; Betaflight is useful for a minimal manual/stabilized prototype |
| ESC protocol | DShot preferred when the selected ESC supports it; PWM is the bring-up fallback; DroneCAN/CAN ESCs are a separate architecture option |

### 2.2 Why the hybrid sensor architecture is selected

Three architectures were considered:

| Architecture | Benefits | Problems | Decision |
|---|---|---|---|
| Fully modular raw sensors | Every IMU, barometer, compass and navigation sensor can be replaced | Long IMU wires add vibration, EMI, ground and timing risk; connector failures affect the control loop; harder first prototype | Not selected for Rev A |
| Mostly onboard | Short deterministic IMU/barometer paths and simpler control-loop timing | Less serviceable; magnetic and vibration isolation can be difficult; payload-specific sensors still need interfaces | Not selected as the complete architecture |
| Hybrid | Fast stabilization sensors are local; magnetic, navigation and payload sensors can be physically separated and replaced | Requires explicit bus, connector, timestamp, frame and failure contracts | **Selected for Rev A** |

The primary IMU and barometer are therefore soldered on the FC. GNSS, compass, telemetry, receiver, lidar and CM5 are modular. A future smart sensor node could contain a remote IMU only if it provides deterministic timestamping, a defined update rate and a robust bus such as CAN; a raw high-rate IMU cable is not the Rev A default.

### 2.3 Functional partition

```text
                       +----------------------+
                       | Transmitter / RX     |
                       +----------+-----------+
                                  | RC protocol
                                  v
+----------------+       +--------+---------+       signal + GND       +----------------+
| GNSS + compass |------>|                  |-------------------------->| ESC board       |
+----------------+ UART  |  STM32H743 FC   |                             +-------+--------+
+----------------+       |                  |                                     |
| Downward lidar |------->| IMU + baro      |                             3-phase outputs
+----------------+ UART  | control/failsafe |                                     v
                         +--+----+-----+----+                              +-------+--------+
                            |    |     |                                   | Motors/props   |
                         USB/   |     |                                   +----------------+
                         SWD    |     |
                                |     +------ telemetry / CAN / GNSS / lidar
                                |
                    data-only UART/CAN, separate power
                                v
                       +--------+---------+
                       | CM5 carrier      |
                       | camera + scanning|
                       | lidar + YOLO     |
                       +------------------+

     Battery -> ESC/PDB and propulsion power
             -> separate regulated 5 V FC rail
             -> separate regulated 5.1 V-class CM5 rail
```

The CM5 may send high-level, bounded commands or validated obstacle information. It must not be the only source of the basic attitude loop, motor timing, arming logic or radio-loss response.

## 3. CM5 companion-computer role and integration

### 3.1 What the CM5 is for in this aircraft

The CM5 is useful as a mission/perception computer rather than as a second flight controller. In this project it can:

- capture frames from a CSI camera;
- resize, normalize and run YOLO object detection;
- track detected objects across frames;
- fuse camera detections with lidar distances;
- create a local obstacle representation or occupancy data;
- process scanning or 3D lidar point clouds that are too large for the FC;
- run visual-inertial or optical-flow experiments if the selected camera and timing are adequate;
- send high-level “slow/stop/avoid/hold position” or navigation setpoints to ArduPilot/PX4;
- log synchronized camera, lidar, telemetry and autopilot data;
- expose a local operator or test interface over Ethernet/Wi-Fi when appropriate;
- perform mission logic, target selection and non-safety-critical autonomy.

It should not be relied on for:

- the innermost attitude stabilization loop;
- direct generation of the four motor waveforms;
- the only arming or disarming path;
- the only radio-loss failsafe;
- an emergency stop that depends on Linux booting;
- safety-critical decisions when its heartbeat, timestamps or data quality are stale.

### 3.2 Camera and lidar processing split

| Sensor/data type | Preferred processing location | Reason |
|---|---|---|
| Downward single-point range for altitude/landing assist | FC UART or CAN where practical | Low data rate, simple range value, useful even if CM5 is off |
| Forward single-point range for a simple test | FC UART/CAN or CM5 depending on driver | FC can use a validated distance; CM5 can use it for perception experiments |
| 2D scanning lidar | CM5 over USB/UART/Ethernet; optionally publish a filtered result to FC | The scan is high-volume and needs obstacle-sector logic |
| 3D lidar | CM5 over Ethernet/USB | Point-cloud handling and mapping are companion-computer workloads |
| CSI camera for YOLO/tracking | CM5 CSI-2 | The FC does not have the memory, OS or accelerator path for image models |
| Independent FPV camera | Dedicated video transmitter/receiver chain | Pilot video has a different latency and link requirement from perception |

A single-point lidar is not full collision avoidance. The FC can use it for terrain/altitude or a narrow protected direction; all-direction or map-based avoidance requires a scanning/3D sensor and an explicit CM5-to-autopilot data contract.

### 3.3 CM5 hardware and carrier choices

The CM5 is a compute module, not a complete SBC. It exposes two 100-pin board-to-board connectors and requires a carrier for power, boot/storage selection, USB, Ethernet, camera, display or other desired interfaces. Use the official CM5IO board for bench evaluation and a custom carrier only when the required interfaces are known.

| CM5 decision | Current recommendation |
|---|---|
| Module | CM5 based on the Raspberry Pi 5-class platform |
| RAM | 4 GB for one small YOLO pipeline and basic tracking; 8 GB if ROS 2, multiple models, mapping or larger logs are expected |
| Storage | eMMC variant for a fixed embedded installation, or Lite + reliable microSD for rapid iteration |
| Carrier | CM5IO for bench bring-up; custom carrier later if weight, connector placement, camera and lidar interfaces justify it |
| AI accelerator | No AI HAT in current plan; benchmark CPU/GPU/Vulkan/TensorFlow-Lite/ONNX-runtime path before assuming real-time performance |
| Camera interface | CSI-2 on the carrier; keep FPV video separate when low pilot latency is required |
| FC link | 3.3 V UART with TX/RX/GND and optional CTS/RTS, or CAN if both sides have a suitable interface |
| CM5 power | Dedicated regulated rail, designed around measured peak load; do not power it from the FC's small sensor rail |
| FC dependency | None for basic stabilization, manual control and failsafe behavior |

The current electrical starting point is a dedicated 5.1 V-class, 5 A-capable CM5 regulator path with local bulk capacitance. This is a design target, not a claim that the module always consumes 25 W. A nominal 25 W CM5 load at 90% converter efficiency is approximately 27.8 W input: roughly 1.9 A from a 4S nominal pack or 1.25 A from a 6S nominal pack, before wiring and transients. Measure actual CM5, camera, lidar and USB loads.

### 3.4 CM5-to-FC communication contract

Preferred first implementation: a dedicated UART running a conservative baud rate, with a defined packet protocol or MAVLink transport and a heartbeat. Add CTS/RTS if cable length, packet rate or Linux scheduling makes it useful. Start conservatively and increase the rate only after bench validation; 921600 baud is a test target, not a guaranteed requirement.

Minimum contract requirements:

- 3.3 V logic levels; no 5 V UART is connected directly to the STM32 or CM5 GPIO.
- TX, RX and ground are mandatory; CTS/RTS are optional but recommended for higher-rate traffic.
- Every message has a type, timestamp or sequence number, source, validity and expected rate.
- The FC rejects stale, malformed, out-of-range or unacknowledged high-level commands.
- CM5 heartbeat loss must cause a defined non-catastrophic action such as ignoring companion commands and continuing the FC's configured mode/failsafe.
- FC arming and disarming cannot require CM5 availability.
- The CM5 receives telemetry, state and sensor information; it does not receive raw battery current through this link.
- If CAN is used, node IDs, message definitions, bus bitrate, termination and cable topology must be frozen separately.

Official reference roles: Raspberry Pi CM5 documentation defines module/carrier requirements; PX4 and ArduPilot documentation provide companion-computer integration patterns, telemetry and high-level command approaches.

## 4. External modular interface architecture

### 4.1 Bus selection

| Bus/interface | Rev A use | Electrical/layout rules |
|---|---|---|
| SPI | Onboard ICM-42688-P and possibly local flash | Keep short; dedicated chip-select; route clock/data over a clean reference; provide interrupt if used |
| I2C | BMP390 if the selected driver/architecture uses it; short auxiliary sensors | Keep short and low-speed; define pull-ups; calculate capacitance; do not use as the primary long external sensor cable |
| UART | Receiver, GNSS, telemetry, downward lidar, CM5 | Point-to-point; label FC TX as device RX and FC RX as device TX; specify logic level and ground return |
| CAN | Future/robust GNSS, smart lidar, DroneCAN peripherals or CAN ESC | Differential pair, controlled topology, one termination at each physical bus end, defined bitrate and node IDs |
| PWM/DShot | FC to external ESC | Signal plus ground only; no raw battery or motor phase conductors on the FC connector |
| USB | FC configuration/debug and CM5 peripherals | ESD protection, connector retention, controlled routing and clear power-source policy |
| CSI-2 / Ethernet | CM5 carrier-side camera and high-rate lidar | Keep entirely on the CM5 carrier/payload side unless a custom interconnect is deliberately designed |
| SWD | MCU programming/debug | Dedicated header/test pads, reset and reference voltage exposed |

### 4.2 Proposed logical port names

Use the following names in the schematic, silkscreen, firmware configuration and integration documents:

`POWER1`, `ESC_SIG`, `RC_IN`, `GPS1`, `GPS2/AUX_I2C`, `CAN1`, `CAN2`, `TELEM1`, `COMPANION`, `LIDAR_FC`, `AUX_UART`, `AUX_SPI`, `SWD/DEBUG`, `USB-C`.

The names describe function, not a claim that every connector is physically identical to a Pixhawk product. Connector choice and exact pin numbers are frozen only after the selected enclosure, cable, current, mating cycle and supplier are known.

### 4.3 Proposed logical pin contracts

These are the current engineering starting points. They are not yet a purchasing or fabrication freeze.

#### `POWER1` — FC regulated power and monitoring

| Pin/function | Meaning |
|---|---|
| `5V_FC` | Regulated FC input, protected and current-rated |
| `GND` | Power return |
| `VBAT_SENSE` | Scaled battery-voltage measurement from the power/ESC/PDB side |
| `CURR_SENSE` | Conditioned current-sense signal from external shunt/monitor |
| `PWR_STATUS` | Optional power-good or monitor status |
| `SPARE` | Reserved; do not assign without documentation |

Raw battery current stays on the ESC/PDB side. The FC only receives a protected low-current power input and scaled measurement signals.

#### `ESC_SIG` — four signal-only motor outputs

| Pin | Function |
|---|---|
| 1 | Motor 1 signal |
| 2 | Ground return |
| 3 | Motor 2 signal |
| 4 | Ground return |
| 5 | Motor 3 signal |
| 6 | Ground return |
| 7 | Motor 4 signal |
| 8 | Ground return |

Do not place `VBAT`, motor phase outputs, or high-current copper on this FC connector. If ESC telemetry or a BEC return is required, use a separately documented connector and voltage/current budget.

#### `RC_IN`

`5V_AUX`, `GND`, `FC_RX`, `FC_TX`.

The exact receiver protocol may be CRSF, SBUS, FPort, iBUS or another selected serial protocol. The final choice must include inversion requirements, failsafe behavior, telemetry direction and binding/configuration access.

#### `GPS1`

`5V_AUX`, `GND`, `FC_TX`, `FC_RX`, `SCL`, `SDA`; add `PPS` only if the selected GNSS/compass and firmware require it. GNSS UART and compass I2C must be mapped unambiguously.

#### `CAN1` / `CAN2`

`5V_AUX`, `CANH`, `CANL`, `GND`.

Define bus bitrate, node IDs, polarity, termination location and maximum cable length. Do not place a termination resistor at every connector; use only the two physical bus ends.

#### `TELEM1`

`5V_AUX`, `GND`, `TX`, `RX`, `CTS`, `RTS`.

The port may be populated with a 4-pin implementation if hardware flow control is not needed, but the signal naming must remain clear.

#### `COMPANION`

`3V3_REF`, `GND`, `FC_TX`, `FC_RX`, `CTS`, `RTS`.

This is a data connector only. The CM5 receives power from its own carrier/regulator and does not draw its main current through this FC port.

#### `LIDAR_FC`

`5V_AUX`, `GND`, `TX`, `RX`.

Use this for a downward or other scalar rangefinder that has been validated for the selected altitude and vibration envelope. A scan lidar should normally use the CM5-side connection.

#### `AUX_UART`, `AUX_SPI` and `SWD/DEBUG`

Each auxiliary port must document its supply, ground, direction, voltage level, maximum cable length and reserved pins. `SWD/DEBUG` exposes `SWDIO`, `SWCLK`, `NRST`, `3V3_REF`, `GND` and optional `SWO`.

### 4.4 Connector recommendation

Use small keyed locking connectors such as **JST-GH 1.25 mm or an electrically/mechanically equivalent family** for low-current modular ports when the physical constraints and supplier availability support them. Exact Pixhawk compatibility is not claimed unless the selected connector, pinout, signal allocation, dimensions, locking and power limits follow the intended standard precisely.

Connector rules:

- keyed and locking where possible;
- ground return beside fast or sensitive signals;
- silkscreen labels and pin-1 marking;
- one connector family where practical, but not at the expense of current rating or polarization clarity;
- no assumed hot-plug unless the circuit has inrush, ESD and sequencing provisions;
- document allowable voltage and current per port;
- expose test pads for UART, CAN, power and reset;
- define whether a port supplies 5 V, 3.3 V or reference-only voltage;
- add series resistors, termination or pull-ups where the interface requires them;
- provide a mating cable/pinout drawing to every team member;
- keep connector orientation and service access consistent across the board.

### 4.5 Sensor placement and physical isolation

| Item | Physical treatment |
|---|---|
| ICM-42688-P | Onboard, close to the MCU but away from regulators, USB, connectors and mounting stress; follow the datasheet orientation and land pattern |
| BMP390 | Onboard with a protected vent; keep away from prop wash, heat sources and conformal-coating blockage |
| Compass | External GNSS/compass mast or low-noise location, away from battery/ESC/motor current and magnetic fasteners |
| GNSS antenna | External top-facing location with sky view and separation from CM5 RF/noisy digital wiring |
| Downward lidar | Rigid isolated mount with an unobstructed beam; direct FC or CM5 according to function |
| Scanning/3D lidar | CM5/payload side, mechanically supported and isolated from vibration; process scan on CM5 |
| Camera | CM5 CSI carrier or independent FPV camera mount; define field of view, vibration and lens protection |
| ESC | External high-current board, physically separated from FC sensor area; keep phase/current conductors off FC |

## 5. Flight-controller electrical design baseline

### 5.1 MCU and core requirements

The core schematic must explicitly include and verify:

- every required STM32H743VIT6 power pin and local decoupling;
- VCAP capacitors and values/layout per the STM32 datasheet/reference design;
- VDDA/VREF treatment and analog ground/current-sense routing;
- HSE and optional LSE oscillator arrangement if the firmware requires them;
- NRST, BOOT0 and recovery access;
- SWDIO, SWCLK, reference voltage, ground, reset and optional SWO;
- USB D+/D−, ESD protection and connector policy;
- unused pins in a documented safe state;
- alternate-function mapping for SPI, UART, CAN, timers, ADC, SD and debug;
- a clock tree that matches the chosen firmware target;
- status LEDs, buzzer/arming indicator and reset/user controls as required.

The exact alternate-function pin map must be frozen in the KiCad schematic and firmware configuration together. A pin that works in a generic STM32 example is not automatically suitable when timers, DMA streams, interrupts and debug functions are combined.

### 5.2 Sensor circuit baseline

#### ICM-42688-P

- default bus: SPI;
- dedicated chip-select and interrupt line;
- short, clean clock/data paths;
- quiet sensor supply with local decoupling;
- correct logic voltage and power-up sequencing;
- exact package land pattern, orientation mark and exposed-pad treatment checked against the datasheet;
- mechanical placement close to the intended vehicle center of rotation;
- no long external cable for the primary stabilization sensor in Rev A.

#### BMP390

- use the selected bus and driver consistently;
- place a protected pressure vent and avoid direct prop wash;
- keep away from hot regulators and high airflow gaps;
- provide local decoupling and verify address/CS straps;
- document whether it is the primary barometer or a redundant/reference device.

#### External GNSS/compass

- separate power return and physical mounting plan from high-current propulsion wiring;
- UART direction labels and baud rate;
- compass bus pull-ups and address;
- optional PPS line if time synchronization is required;
- connector pinout and cable length;
- calibration and magnetic-interference procedure.

### 5.3 Power architecture

Recommended block structure:

```text
LiPo battery
  +--> ESC/PDB high-current path --> ESCs --> motors
  +--> protected regulated FC 5 V --> 3.3 V MCU/sensor rails
  +--> dedicated regulated CM5 5.1 V-class rail --> CM5 carrier/camera/lidar as designed
  +--> external voltage/current monitor --> scaled FC ADC signals
```

Required power features, selected after load and battery data are known:

- input fuse or resettable protection appropriate to the branch;
- reverse-polarity protection where required;
- TVS/transient strategy appropriate to the battery and wiring inductance;
- regulator thermal and peak-current analysis;
- separate noisy/high-current and quiet sensor domains;
- 5 V and 3.3 V test points;
- ADC divider for battery voltage with calculated range, tolerance and filtering;
- current-sense input with known shunt/monitor scaling, bandwidth and ground reference;
- USB power back-feed policy;
- CM5 inrush and transient handling;
- clear indication of which connector can source or sink current;
- local bulk capacitance near the MCU, sensors, connectors and CM5 carrier input.

The FC should never be selected or laid out around an assumed battery voltage before the ESC team supplies the cell count and transient conditions. The working battery candidates are 4S and 6S LiPo; a 6S pack is 22.2 V nominal and 25.2 V fully charged.

### 5.4 Current and voltage monitoring

The FC receives measurement signals, not raw propulsion current. The external ESC/PDB team must define:

- shunt location and resistance;
- current-sense amplifier or ESC telemetry source;
- output range and zero-current offset;
- voltage scale and maximum full-charge voltage;
- ADC reference and ground relationship;
- required filtering and update rate;
- calibration procedure;
- behavior when the monitor is absent or invalid.

## 6. PCB layout baseline

### 6.1 Layer stack

Default Rev A: four-layer PCB.

| Layer | Primary use |
|---|---|
| L1 | Components and critical short routes |
| L2 | Continuous ground plane |
| L3 | Power distribution and non-critical signals |
| L4 | Signals and connectors |

If the routing density, EMC risk or CM5/USB interface requires it, a six-layer stack is preferred:

`L1 signal/components`, `L2 ground`, `L3 signal`, `L4 power`, `L5 ground`, `L6 signal`.

The actual stack-up must be obtained from the PCB manufacturer. Trace widths, impedance, dielectric height and via rules depend on that stack-up.

### 6.2 Placement order

1. Confirm mounting holes, board outline, connector access and enclosure clearance.
2. Place the IMU in the intended low-vibration central region.
3. Place the MCU close to the IMU without placing the MCU or high-current switching node directly under the sensor.
4. Place the barometer with its vent and keep-out region.
5. Place regulators and power entry away from the sensor area.
6. Place USB-C, SWD, boot/reset and test points where a probe or cable can reach them.
7. Place external modular connectors with clear cable exits and pin-1 orientation.
8. Place storage, CAN transceivers and auxiliary circuitry according to the final bus topology.
9. Place LEDs/buzzer where they remain visible/audible after installation.

### 6.3 Routing priorities

1. Sensor SPI, interrupt and clock paths.
2. Ground return and MCU/sensor power distribution.
3. MCU decoupling and VCAP paths.
4. USB D+/D− and ESD path.
5. SD/SPI flash, CAN differential pair and other timing-sensitive links.
6. PWM/DShot outputs and UARTs.
7. I2C and low-speed auxiliary buses.
8. Any raw-battery conversion branch, which should remain outside the FC when possible.

Do not route high-current propulsion conductors through the flight-controller board. Keep switching regulator nodes compact, keep sensor ground references quiet, avoid unnecessary vias in critical sensor paths, and document any split/partition strategy rather than creating an accidental broken ground plane.

## 7. Firmware and open-source application direction

### 7.1 Candidate firmware comparison

| Firmware | Strengths for this project | Tradeoffs | Current role |
|---|---|---|---|
| ArduPilot | Mature autopilot, GPS/navigation modes, rangefinder support, MAVLink and companion-computer integration | Porting a custom H743 board and full parameter/driver validation takes work | **Leading recommendation** for the integrated UAS prototype |
| PX4 | Strong Pixhawk hardware conventions, DroneCAN, ROS 2 and companion-computer workflows | Custom-board port and sensor/airframe configuration still require significant validation | Strong alternative, especially if the team prioritizes PX4/DroneCAN/ROS 2 |
| Betaflight | Fastest path to a basic manual/stabilized FPV-style proof-of-life; DShot ecosystem is familiar | Less aligned with mission autonomy, mapping, companion links and general UAS functions | Minimal bring-up or backup path, not the preferred integrated autopilot |
| Custom educational firmware | Maximum learning and control over every layer | High schedule and safety risk; not appropriate as the only path in a one-month project | Use selectively for sensor/MCU experiments, not as the main aircraft firmware unless scope is reduced |

### 7.2 Firmware partition and failure rules

The FC firmware owns:

- IMU/barometer acquisition;
- attitude/rate estimation and stabilization;
- motor mixing/output timing;
- arming/disarming;
- receiver failsafe and link-loss response;
- power and sensor health monitoring;
- direct scalar rangefinder handling where selected;
- watchdog and recovery behavior.

The CM5 application owns:

- camera capture and image inference;
- object detection/tracking;
- scan/point-cloud processing;
- high-level avoidance or mission decisions;
- logging and operator interfaces.

The FC must define what happens when the CM5 is powered off, rebooting, delayed, noisy, disconnected, sending stale data or sending values outside allowed limits. The safe default is to ignore companion commands and continue the configured FC behavior.

### 7.3 Open-source and licensing rules

Relevant sources include PX4, ArduPilot, Betaflight, Pixhawk hardware standards, OpenFC, OpenESC/AM32, Shirley-FC and the Udayate educational repositories.

Before copying code, schematics, footprints or artwork:

- record the repository commit/tag used;
- read the license and preserve required notices;
- distinguish hardware license from firmware/software license;
- do not imply official Pixhawk compatibility or branding without meeting the applicable standard;
- do not treat a forum, video or repository as a certification or production guarantee;
- note that `pixhawk2.1` contains mixed licensing considerations and requires individual-file review.

## 8. Supplied design/reference comparison

The following is the consolidated comparison of all 16 supplied reference items. The first two YouTube pages were not reliably machine-readable in the earlier review; the associated repositories were used where available. The user-supplied item 10 Reddit URL was malformed; it is listed as unresolved and no unsupported technical claims are assigned to it.

### 8.1 Comparison table

| # | Reference | What it contributes | What can be reused | Limits / caution |
|---:|---|---|---|---|
| 1 | OpenDrone-hw OpenFC-Lite-Mini + YouTube | Open hardware FC architecture; RP2354A, BMI270, dedicated sensor rail, microSD, multiple UARTs, external 4-in-1 signal-level ESC concept, 3–6S class, six-layer implementation | Power separation, connector/serviceability thinking, sensor placement, manufacturing structure and review checklist | Different MCU/IMU/firmware; do not copy pin map or assume validation transfers to STM32H743 |
| 2 | HomeGliders FCV2 + YouTube | KiCad project/repository structure for a DIY FC | Inspect schematic organization, footprints, net naming and board workflow after confirming exact revision | Exact part choices and validation status must be checked from the repository; not automatically a drop-in reference |
| 3 | Jacob Thornhill flight-controller video | Educational STM32F405 build with I2C sensor, UART GPS/receiver and control-loop learning | Minimal signal flow, bring-up order and the value of proving a basic loop first | Educational implementation; filtering, timing, frame conventions and failure handling are not sufficient evidence for this project |
| 4 | Pixhawk hardware repository | Mature modular autopilot architecture, external sensor/telemetry ports, power/debug patterns | Port categories, serviceability, power monitoring, connector documentation and system partitioning | Check current hardware standards and licenses; do not claim Pixhawk compatibility by appearance alone |
| 5 | Reddit custom H743 build/review | Community lessons involving current measurement, external shunt, regulators and compass placement | Review checklist for power, magnetics, current measurement and physical layout | Community post; verify every claim against datasheets and measurements |
| 6 | Reddit custom FC from scratch | Community experiences with custom FC complexity | Scope/risk awareness and staged development | Anecdotal and not a validated design source |
| 7 | Reddit “anyone built their own FC?” | Community concepts including more advanced/AI-oriented FC ideas | Awareness of possible architectures and failure modes | Low authority; not a Rev A design basis |
| 8 | Reddit multicopter custom FC | Recommendation to prove STM32 + gyro + basic loop before adding logs/baro/lidar | Bring-up sequencing and scope control | It does not remove the need for the modular external interfaces required here |
| 9 | Bare-Metal-Foundry Shirley-FC-Dev-Board | Closest architecture reference: H743ZIT6, ICM-40609-D, MMC5983MA, BMP390, SD, 5 V mux/dual 3.3 V, four ESC outputs, GPS/RC/telemetry/USB/CAN, GH1.25 | Port partition, connector strategy, power-domain thinking and H7 implementation patterns | Different MCU/package and sensors; treat as architecture reference, not exact clone |
| 10 | User-supplied PCB review Reddit URL | Intended as a PCB review reference | Resolve the correct URL/post before assigning technical conclusions | Supplied URL appears malformed; no unsupported claims used |
| 11 | Betaflight manufacturer design guidelines | Practical FC design guidance: SPI IMU, dedicated sensor rail, H7 timer/DMA use, I2C baro/mag, ADC/SWD/blackbox considerations | IMU bus, power, timer/DMA, logging, debug and layout review requirements | Betaflight-oriented; adapt to ArduPilot/PX4 and this project's modular architecture |
| 12 | Duplicate OpenFC-Lite-Mini link | Same OpenFC reference as item 1 | Same reuse map | Duplicate source, not independent evidence |
| 13 | Reddit STM32H743 flight-controller review | H743VIT6, ICM-42688-P, BMP388, 9/5/3.3 V domains, microSD, USB-C, four UART and four-layer style | Closest part-level comparison for the selected H743/ICM family; review comments on LQFP/BGA, IMU LDO and shunt | Community review; verify footprint, power design, regulator stability and current-sense implementation |
| 14 | Udayate + Kalman-AHRS + LSM6DSL library + Quaternion Visualiser + video | Educational STM32/Firmware/sensor-driver/EKF/visualization material | Driver structure, AHRS/EKF concepts, quaternion visualization and test scaffolding | Not a drop-in autopilot, not the selected sensor and not a substitute for ArduPilot/PX4 validation |
| 15 | MRazgunas pixhawk2.1 | Schematic and architecture reference for Pixhawk 2.1-style hardware | Port and power concepts, redundant interfaces and documentation style | Mixed licenses and older hardware assumptions; review each file before reuse |
| 16 | Reddit beginner custom FC thread | Beginner-level scope and hardware-first warnings | Reinforces bench-first development and known-good component validation | Does not override the requirement for a custom modular PCB |

### 8.2 Reuse map

| Design topic | Primary references |
|---|---|
| Main MCU/board organization | Shirley-FC-Dev-Board; H743 community review |
| Primary IMU and sensor rail | Betaflight guidelines; OpenFC; H743 review |
| Barometer placement | Shirley; OpenFC; manufacturer datasheet guidance |
| External compass/GNSS | Pixhawk hardware; PX4 sensor/vehicle conventions |
| Modular ports | Pixhawk hardware; Shirley; PX4 conventions |
| ESC boundary | OpenFC; OpenESC; Betaflight DShot material |
| ESC protocol | Betaflight DShot documentation; AM32/OpenESC |
| Power/current measurement | Betaflight guidelines; H743 review; community review lessons |
| Firmware/application | ArduPilot; PX4; Betaflight; Udayate for learning only |
| CM5 integration | Official Raspberry Pi CM5 documentation; PX4/ArduPilot companion-computer documentation |
| Process and KiCad workflow | OpenFC, HomeGliders, Shirley and the supplied educational build references |

## 9. MCU, board and platform options considered

### 9.1 MCU shortlist

| MCU/platform | Why it was considered | Rev A assessment |
|---|---|---|
| STM32H743VIT6 | H7 performance, timers/DMA, SPI/UART/CAN/ADC capacity and broad autopilot precedent in an LQFP package | **Selected** |
| STM32H743ZI | More pins and memory/package options | Useful if the final port count or SD/parallel peripherals exceed the VIT6 package; not the current baseline |
| STM32H753 | H7 family performance and memory features | Candidate, but unnecessary part change unless availability or firmware requires it |
| STM32H723/H725 | H7-class performance in related packages | Candidate alternative; verify memory, peripherals, package and firmware support |
| STM32F767 | Mature flight-controller/autopilot ecosystem | Capable but less headroom than H743 for the intended integration |
| STM32G4 | Strong control/analog/timer features | Better for dedicated power/control roles than the main companion-rich FC |
| NXP i.MX RT1170 | High performance and rich peripherals | More complex ecosystem and not the fastest route for this project |
| RP2350/Pico-class | Low-cost, modern MCU and used in OpenFC-Lite-Mini | Good reference/education option, not the selected autopilot MCU |
| ESP32-S3 | Wireless and AI-adjacent features | Wireless/RTOS path adds complexity and is not the preferred deterministic FC base |
| Arduino Uno | Beginner control-loop experiments | Not appropriate for the required FC functions |

The H743VIT6 choice is a schedule-driven engineering decision. It gives enough timer, DMA, serial, ADC, storage and compute capacity for the current architecture while remaining physically hand-assemblable compared with a BGA-heavy alternative.

### 9.2 Ready-made flight-controller boards as benchmarks only

Pixhawk 6C/6X, Cube Orange+, CUAV X7, Kakute H7, Durandal and ARKV6X are useful benchmarks for:

- how ports are named and grouped;
- what redundancy and power monitoring look like;
- how autopilot firmware expects hardware to be described;
- connector/serviceability patterns;
- typical sensor and storage combinations.

They are not the Rev A final board. The project's stated requirement is a custom bare-MCU PCB.

### 9.3 Development boards for firmware de-risking

The following may be used temporarily to prove firmware ideas before the custom PCB arrives:

- STM32 NUCLEO-H723ZG;
- STM32 NUCLEO-F767ZI;
- Arduino Portenta H7;
- Arduino GIGA R1 WiFi;
- Teensy 4.1;
- Raspberry Pi Pico 2 / RP2350 board;
- Arduino Uno for very small control-loop demonstrations only.

These boards are development instruments, not substitutes for the final custom FC. Pin maps, timer assignments, sensor drivers, interrupt behavior and power noise must be revalidated on the H743 PCB.

### 9.4 Companion-computer alternatives

| Platform | Strength | Reason it is not the current selection |
|---|---|---|
| Raspberry Pi CM5 | Compact Pi 5-class compute, carrier-based integration, adequate for the intended first perception workload | Selected; requires a carrier and careful power design |
| Jetson Orin Nano Super | Stronger GPU/AI ecosystem | Higher power, thermal and integration burden for this first prototype |
| BeagleBone / NXP i.MX8M Plus class | Industrial/embedded interfaces and edge inference options | Less aligned with the team's current CM5 direction and software familiarity |
| VOXL2 / Skynode class | Purpose-built autonomy platforms | Cost and availability; not the planned custom integration path |

### 9.5 FPGA options

Kria KV260/KR260, PYNQ-Z2/Zybo Z7, DE10-Nano, Arty A7 and Microchip PolarFire were considered as possible acceleration or deterministic-I/O platforms. FPGA use is not the default for Rev A. It would expand the schedule, toolchain, power, verification and firmware burden without being necessary for the initial H743 + CM5 architecture.

## 10. ESC, motor, protocol and propulsion integration

### 10.1 FC-to-ESC protocol decision

| Protocol | Use in this project | Notes |
|---|---|---|
| DShot | Preferred first digital signal path when supported by the selected ESC | Digital command, no analog calibration in the same way as PWM; verify timer/DMA mapping, ESC support and telemetry behavior |
| Bidirectional DShot | Later option for RPM telemetry and dynamic filtering | Add after one-way command and basic motor behavior are reliable |
| PWM | Bring-up fallback | Simple to observe and widely supported; define frequency, pulse range, failsafe value and calibration |
| CAN/DroneCAN | Alternative architecture for smart ESCs/peripherals | Requires node IDs, bus termination, message definitions and firmware support; do not mix assumptions with signal-only outputs |

The FC output contract is signal-level only. A four-motor first implementation should provide one signal and one ground return per motor. If the selected ESC requires a separate telemetry line, BEC return, enable line or bidirectional signal, add it explicitly rather than modifying the generic `ESC_SIG` assumption.

### 10.2 Information required from the ESC team

Before the FC schematic and connector pinout are frozen, the ESC workstream must provide:

- number of battery cells supported and maximum full-charge voltage;
- continuous and peak current per channel;
- command protocol and logic voltage;
- command update rate, timer requirements and reset/arming behavior;
- one-way or bidirectional signal details;
- telemetry format, direction and update rate;
- FC connector family, pinout, keying and cable length;
- whether signal ground is available beside each signal;
- BEC output voltage/current and whether it may feed any FC or payload rail;
- current-sense shunt location, scaling and output behavior;
- ESC firmware, bootloader and programming access;
- motor/propeller test procedure with propellers removed;
- thermal limits and cooling/mounting assumptions.

### 10.3 OpenESC/AM32 reference boundary

The OpenDrone OpenESC/AM32 materials are useful reference points for an external 4-in-1 ESC. One referenced class uses a 2–6S, approximately 40 A/channel design and an 8-pin JST-SH-style interface carrying battery positive, battery ground, current-related signals and motor signal outputs. That high-current connector belongs to the ESC/PDB side. It must not be copied onto the FC if the FC contract is signal-only.

The exact OpenESC board is not automatically the team's ESC design. Verify the repository revision, firmware compatibility, current rating, thermal performance, connector, shunt implementation and licensing with the ESC owner.

### 10.4 Motor classes for early selection

Motor choice cannot be finalized without MTOW, propeller diameter/pitch, target flight time, battery cell count and frame geometry. The following are starting classes, not a purchase order:

| Vehicle class | Candidate motor region | Battery/ESC direction | Applicability |
|---|---|---|---|
| Light 5-inch payload quad | 2207/2207.5, roughly 1750–1950 KV on 6S or 2400–2550 KV on 4S | Approximately 35–45 A ESC class | Only if the full sensor/CM5 payload remains light |
| 7–10 inch sensor payload quad | 2810/2814 class, lower KV matched to the prop | 4S/6S and roughly 40–60 A ESC class depending on thrust/current test | More plausible for camera/lidar/CM5 payload, but must be calculated |
| Larger UAS/VTOL | Larger stator/lower KV selected from thrust data | ESC, PDB and battery sized from measured peak current | Cannot be selected until aircraft mass and geometry are known |

### 10.5 Propulsion sizing equations

For a four-motor aircraft:

```text
T_hover_each = MTOW * g / 4
```

An early engineering target is total maximum thrust of at least approximately twice aircraft weight, but the correct margin depends on the airframe, mission and test requirements. Use manufacturer thrust tables or a thrust stand for the exact motor/prop/battery combination.

The ESC continuous rating must exceed measured continuous current with thermal margin. Battery peak current capability must exceed the combined propulsion peak with margin. Approximate flight time is:

```text
usable battery energy / average aircraft power
```

This estimate must account for the usable state-of-charge window, voltage sag, efficiency, payload power and environmental conditions.

## 11. Battery and power-solution research

### 11.1 Battery direction

LiPo remains the current battery choice. 4S and 6S are the active system candidates. A 6S pack is 22.2 V nominal and 25.2 V fully charged. Do not choose a large pack simply because the CM5 needs power: pack mass increases required thrust and can reduce flight time if the propulsion system is not resized.

Representative market classes reviewed earlier included:

- 6S 1200–1400 mAh packs in roughly the 200–222 g class;
- 6S 5000 mAh, 60C-class packs in roughly the 755 g class.

These are examples, not a final selection. Confirm current availability, connector, C-rating interpretation, internal resistance, dimensions and actual mass from the selected supplier.

### 11.2 Power branch recommendations

| Branch | Source and handling |
|---|---|
| ESC/motors | Direct high-current LiPo path through the ESC/PDB design |
| FC | Protected regulated 5 V input followed by MCU/sensor regulation as required |
| GNSS/compass/receiver/lidar | 5 V or 3.3 V auxiliary rail only if the FC regulator and connector budget support it |
| CM5 | Separate converter sized for CM5, carrier, camera, lidar and USB transients; target a 5.1 V-class, 5 A-capable path until measured load allows refinement |
| Battery monitor | External shunt/monitor or ESC/PDB output scaled into FC ADC/telemetry input |

The CM5 must not be powered through a small FC sensor regulator. The CM5 carrier should have its own bulk capacitance, controlled power-on behavior and a defined ground connection to the FC data link.

### 11.3 Power checklist before freeze

- nominal, full-charge and minimum operating battery voltage;
- ESC/PDB current and transient profile;
- FC regulator input range, efficiency, thermal rise and peak current;
- CM5 peak load during boot, camera capture, inference and USB/lidar activity;
- camera and lidar supply current at startup and steady state;
- battery monitor scale and ADC protection;
- reverse polarity, fuse, TVS and inrush strategy;
- ground-current paths and voltage drop;
- connector current rating and mating cable;
- bench supply current limit and propeller-off procedure.

## 12. Lidar selection and attachment options

### 12.1 Lidar role split

The team must first choose whether the lidar is:

1. a **downward scalar rangefinder** for altitude/landing/terrain assistance; or
2. a **forward or rotating obstacle sensor** for collision avoidance; or
3. a **3D mapping sensor** for CM5-based perception and planning.

The first role can be sent directly to the FC. The second and third normally belong on the CM5 path. A single-point sensor cannot provide all-direction collision avoidance.

### 12.2 Candidate lidar modules

Specifications below are approximate selection data from the earlier research and must be confirmed against the exact revision and operating mode before purchase.

| Module/family | Approx. range/field | Approx. mass/interface | Best role | Notes |
|---|---|---|---|---|
| Benewake TF-Luna | 0.2–8 m | Under ~5 g; UART/I2C/I/O | Lightweight downward altitude sensor | Good first scalar rangefinder candidate; verify sunlight, surface and mounting performance |
| Benewake TFmini-S | 0.1–12 m | About ~5 g; UART/I2C/I/O, high update capability | Downward or single forward distance | More range/update headroom; still not a scan sensor |
| Benewake TF02-i | 0.1–40 m | About ~60 g; CAN/RS-485 and other interfaces | Robust outdoor/industrial single-point measurement | Heavier, more robust integration and power considerations |
| LightWare SF20/C | 0.2–100 m | About ~7.5 g; USB/UART/I2C | Lightweight long-range scalar | Check exact environmental performance and protocol |
| LightWare SF45/B | 320° scan, roughly 0.2–50 m | About ~59 g; USB/UART/I2C | Lightweight scanning obstacle awareness | CM5-side processing; scan data must be integrated into a frame/sector model |
| RPLIDAR A1 | 360°, approximately 12 m indoor class | About ~170 g; UART | Indoor 2D scanning experiments | Weight, power, sunlight and spinning-mechanism constraints |
| RPLIDAR S2 | 360° longer-range class | Higher-speed UART/Ethernet and heavier package | More capable 2D scan | Validate weight, power, outdoor performance and mounting |
| Livox Mid-360 | 3D, roughly 40–70 m class | About ~265 g, ~6.5 W, Ethernet | CM5 mapping/3D obstacle experiments | Probably too heavy/power-hungry for a small first aircraft; a strong payload only if MTOW allows |
| ARK DIST SR/MR class | Approximately 8–30/50 m class | DroneCAN/UART options | Autopilot-friendly scalar range | Attractive for direct autopilot integration; confirm exact model and firmware support |

### 12.3 Current lidar recommendation

For the fastest first integrated prototype:

- choose **TF-Luna** if the operating altitude and environment fit its range;
- choose **TFmini-S** if the extra range/update headroom is useful;
- connect the scalar lidar to `LIDAR_FC` or CAN only after voltage, protocol, update rate, orientation and frame are validated;
- use the CM5 for `SF45/B`, RPLIDAR or Livox-class scanning/3D processing;
- publish only validated, timestamped obstacle/sector/high-level information back to the FC.

The lidar owner must provide the exact module, supply voltage/current, connector, protocol, baud/bitrate, mounting angle, frame ID, update rate, minimum/maximum valid range, invalid-data behavior and sunlight/reflectivity limits.

## 13. Camera selection and video/perception options

### 13.1 CM5 perception cameras

| Camera | Key characteristics | Best use |
|---|---|---|
| Raspberry Pi Camera Module 3 Wide | 12 MP IMX708 class, autofocus/HDR options, approximately 120° wide field, 1080p50 or 720p120 modes depending on configuration, CSI-2 | **Default CM5 perception camera** for YOLO, detection, tracking and recording |
| Raspberry Pi Global Shutter Camera | IMX296 class, approximately 1456×1088 and up to around 60 Hz class | Visual odometry, optical flow or fast-motion scenes where rolling shutter is harmful; lower resolution |
| Raspberry Pi High Quality Camera | 12.3 MP IMX477 class with interchangeable C/CS/M12 lens options | Controlled optics, longer focal length or custom lens experiments |
| Raspberry Pi AI Camera | IMX500 class on-module inference accelerator, CSI-2 | Optional if the project later needs low-latency camera-side inference; not required for current no-AI-HAT plan |

### 13.2 Dedicated FPV cameras

| Camera/path | Approx. role | Integration boundary |
|---|---|---|
| RunCam Phoenix 2 class | Analog FPV, CVBS, roughly 1000 TVL, 5–36 V class, approximately 9 g | Dedicated analog VTX/receiver/goggles; do not send pilot video through the FC UART |
| HDZero Nano90 V2 class | Digital FPV, low-latency HD class | Separate digital VTX/goggle ecosystem and power budget |
| Caddx digital class | Digital FPV ecosystem | Separate proprietary/digital video integration; verify exact VTX, camera, power and latency |

### 13.3 Current camera recommendation

Use **Camera Module 3 Wide** as the default CM5 camera for the first YOLO/detection/tracking path. Choose the **Global Shutter Camera** instead if visual odometry, optical flow or fast-motion measurement becomes a primary requirement. If pilot FPV is required, add a separate FPV camera and video transmitter; do not confuse the perception camera with the pilot-video link.

The camera workstream must define lens/FOV, mounting angle, vibration isolation, CSI cable length and retention, frame rate, resolution, exposure mode, lighting assumptions, power path and whether raw frames or encoded frames are passed to the model.

## 14. Preliminary component and BOM direction

This is a design candidate list, not a frozen purchasing list. Exact MPNs, footprints, alternates, package availability and supplier stock must be checked before ordering.

### 14.1 Core active components

| Ref | Function | Current candidate |
|---|---|---|
| U1 | Main MCU | STM32H743VIT6 |
| U2 | Primary IMU | TDK/InvenSense ICM-42688-P |
| U3 | Barometer | Bosch BMP390 |
| U4 | CAN transceiver | TCAN332-class 3.3 V CAN transceiver, exact MPN to be frozen after bus requirements |
| U5 | 3.3 V main regulator | LMR33630/TPS62162-class regulator, exact input range and thermal choice pending |
| U6 | Quiet sensor regulator | LP5907-class low-noise regulator, exact current and enable scheme pending |
| U7 | 5 V regulator / input stage | LMR33630/TPS62162-class or equivalent sized for the FC branch |
| U8 | USB power/load switch or protection | TPS2116-class or equivalent, subject to USB power policy |
| U9 | USB ESD protection | TPD4EUSB30DQAR-class or equivalent USB ESD device |
| U10 | Optional external flash | W25Q128JV-class SPI NOR flash |
| Q1 | Reverse-polarity or load-switch FET | Exact P-channel/N-channel solution pending power topology |
| Q2 | Buzzer/indicator switch | 2N7002K-7-W-class small MOSFET candidate |

The component numbers above are placeholders for the current schematic concept. They do not supersede a datasheet review or imply that each device must be purchased.

### 14.2 Connectors and electromechanical parts

| Function | Candidate |
|---|---|
| External low-current modular ports | JST-GH 1.25 mm family or equivalent keyed locking connector |
| Example 4-position JST-style part | SM04B-GHS-TB-LF-SN candidate; verify mating housing, current rating, orientation and supplier |
| USB-C | USB4105-GF-A candidate; verify exact footprint, shell grounding and mechanical retention |
| SWD | Standard 1.27 mm or test-pad arrangement selected for the programmer/cable actually available |
| Mounting | Four-hole pattern selected from frame/enclosure, with vibration and ground-clearance considerations |

### 14.3 Passive and protection groups

Include, then calculate exact values during schematic capture:

- 100 nF, 1 µF and 4.7 µF local MCU/sensor decoupling;
- 47–100 µF bulk capacitance on appropriate regulated rails;
- VCAP capacitors exactly as required by the STM32H743 datasheet;
- crystal load capacitors if external HSE/LSE is used;
- USB-C CC resistors and any required USB power identification;
- ADC battery-voltage divider with tolerance and clamp/protection analysis;
- current-sense input filtering and protection;
- 33–100 Ω series resistors where signal integrity/ringing warrants them;
- I2C pull-ups calculated for bus voltage and capacitance;
- CAN termination provision, ideally selectable by jumper/assembly option;
- TVS/ESD parts at exposed connectors;
- reset, boot and test-point pull resistors;
- status LEDs and current-limiting resistors;
- buzzer driver and connector;
- ferrites or filters only where the measured noise problem justifies them.

### 14.4 Optional storage

Start with the least complex logging solution supported by the selected firmware. A microSD connector provides removable logs but has mechanical and signal-integrity implications. W25Q128JV-class SPI NOR flash is smaller and simpler but may require a firmware-specific logging implementation. Storage is optional for the minimal motor-control bring-up but highly useful for estimator and sensor debugging.

### 14.5 BOM freeze rules

The final BOM must contain, for every line item:

- reference designator(s);
- manufacturer and exact MPN;
- package and footprint source;
- quantity per board and planned spares;
- voltage/current/temperature rating;
- approved alternate if available;
- supplier and stock check date;
- assembly method (hand, stencil/reflow, connector hand-solder);
- datasheet and license/source note where relevant.

Earlier price and stock estimates are intentionally not treated as current purchasing data. Check live supplier information immediately before buying.

## 15. KiCad design and deliverable scope

### 15.1 What can be produced from the supplied inputs

Once the external interfaces and selected components are supplied, the design work can include:

- KiCad project setup and library organization;
- complete STM32H743VIT6 core schematic;
- power tree, protection and rail calculations;
- ICM-42688-P and BMP390 circuits;
- UART, CAN, USB, SWD, ADC, storage, LEDs and buzzer interfaces;
- modular connector symbols, pinouts and net labels;
- preliminary or complete PCB placement and routing edits;
- design-rule and net-class setup;
- manufacturer stack-up and trace-width constraints;
- fabrication outputs (Gerbers, drill files, drawings) when the design is frozen;
- BOM and component-placement files;
- connector pinout and cable tables;
- bring-up checklist, test-point map and firmware pin configuration;
- review of ERC/DRC results and likely assembly/debug issues.

This work accelerates schematic/layout and review, but every physical footprint, datasheet limit, regulator stability condition, assembly constraint, thermal assumption, connector mating part and flight-safety behavior must still be checked by the project team. A generated schematic is not evidence that a board is flight-ready.

### 15.2 Inputs required before detailed capture

The following are the minimum inputs needed to produce a real board rather than a generic template:

1. ESC schematic or exact signal/power pinout;
2. MTOW or current mass estimate, including CM5, carrier, camera, lidar, battery and mounting hardware;
3. motor and propeller choice or at least the intended motor/prop class;
4. battery cell count, capacity and connector;
5. receiver model and protocol;
6. exact CM5 variant (RAM, eMMC/Lite) and carrier approach;
7. camera module and CSI/FPV path;
8. lidar model and whether it is direct-FC altitude sensing or CM5 obstacle sensing;
9. selected autopilot firmware target (ArduPilot, PX4 or constrained Betaflight path);
10. board outline, mounting-hole pattern, maximum dimensions and connector access;
11. PCB manufacturer stack-up, minimum track/space, drill and assembly capability;
12. required ports, redundancy and physical cable lengths;
13. target test/demo behavior and acceptable bench-only scope.

### 15.3 Schematic capture checklist

Before layout, perform these checks:

- symbol pin numbers match the selected footprints and datasheets;
- all MCU power and VCAP pins are connected;
- no hidden power pins are relying on undocumented global labels;
- every external connector has pin-1, voltage, ground and direction documentation;
- UART TX/RX labels are expressed from the FC point of view;
- I2C pull-ups are present exactly once per bus domain;
- CAN transceiver supply, standby, RX/TX and termination are explicit;
- USB ESD and power/back-feed behavior are explicit;
- ADC inputs cannot exceed the MCU pin limits under any defined battery fault;
- `ESC_SIG` contains no raw battery nets;
- SWD, reset and boot recovery work with the enclosure installed;
- test points exist for every power rail and critical bus;
- ERC exceptions are reviewed individually, not blanket-suppressed;
- the firmware pin map is generated from the final net names.

### 15.4 PCB review checklist

- footprint land patterns checked against the manufacturer datasheet;
- IMU orientation and coordinate frame recorded in silkscreen/documentation;
- barometer vent and keep-out are not blocked;
- regulators have appropriate copper, vias and thermal path;
- continuous ground reference exists below critical routes;
- USB differential routing and ESD return are short and controlled;
- CANH/CANL are routed as a pair with the selected stack-up;
- no connector can be inserted backwards or into an incompatible port;
- cable exits do not interfere with mounting holes or vibration isolators;
- test points can be probed safely;
- silkscreen does not cover pads or hide polarity/keying;
- mounting-hole and board-edge clearances are checked;
- DRC is clean except for documented, reviewed exceptions;
- 3D model and actual mating hardware have been checked;
- assembly process is practical for the available tools.

## 16. Verification, bring-up and test plan

### 16.1 Staged development

#### Stage 0 — Freeze requirements

Write down the vehicle geometry, target mass, battery, motor/propeller class, ESC protocol, receiver protocol, CM5 link, camera, lidar role, board outline and firmware target. Mark anything unknown as an explicit assumption.

#### Stage 1 — Minimal FC proof of life

Bring up only the H743, clock, reset, SWD, USB, one IMU, one barometer, one receiver input and four safe output channels. Use a bench supply/current limit and no propellers.

#### Stage 2 — Communications and logging

Validate GNSS/compass UART/I2C, telemetry, CAN, selected storage, current/voltage ADCs, LEDs/buzzer and connector pinouts.

#### Stage 3 — CM5 and payload integration

Bring up CM5 carrier power independently. Test camera capture, lidar driver, inference latency, packet heartbeat, stale-data rejection and safe CM5 disconnect behavior.

#### Stage 4 — Controlled aircraft tests

Use an approved restrained test rig or similarly controlled environment. Progress from motor identification and direction to low-risk stabilized tests only after the electrical and software checks are recorded.

### 16.2 Pre-power checks

- inspect solder joints, bridges, tombstoned parts and connector orientation;
- compare PCB against schematic and BOM;
- check resistance from each rail to ground;
- check for raw battery nets on the FC;
- verify MCU pin-1 and sensor orientation;
- confirm VCAP capacitor placement;
- inspect USB, SWD, reset and boot connections;
- confirm regulator enable/power-good state;
- verify ESC connector is signal-only;
- check all external cables against the pinout drawing.

### 16.3 First-power sequence

1. Power the FC alone from a current-limited bench supply at the regulated input voltage.
2. Record inrush, steady current and every rail voltage.
3. Confirm no unexpected heating with a visual/thermal check.
4. Connect the programmer and verify SWD identification.
5. Test reset, bootloader and USB enumeration.
6. Load the smallest MCU test firmware.
7. Add the IMU and barometer one at a time.
8. Add external ports one at a time, checking their supply current and logic levels.
9. Power CM5 from its own bench-limited path, then connect only the data link.

### 16.4 Functional tests

| Test | Pass evidence |
|---|---|
| MCU clock/reset/SWD | Stable programming, reset and debug session |
| Power rails | Correct voltage, ripple and current under expected loads |
| IMU | Correct WHO_AM_I/identity, orientation, rate, interrupts and stable data |
| Barometer | Identity, pressure/temperature response and no vent blockage |
| Receiver | Correct frame/protocol, channel mapping and failsafe on cable/radio loss |
| ESC outputs | Correct channel order, protocol timing and safe zero output on boot/disarm |
| Telemetry | Bidirectional packets, correct labels and no framing errors |
| GNSS/compass | Fix, heading, calibration and magnetic-interference behavior |
| Lidar | Valid/invalid range handling, frame orientation and update rate |
| CM5 link | Heartbeat, sequence/timestamp validation and safe disconnect |
| Current/voltage | Scale, zero offset, filtering and calibration against a reference |
| Storage | Reliable write/read and log integrity if enabled |
| Thermal | No unacceptable regulator, MCU, connector or CM5 carrier temperature |

### 16.5 Required safety gates

- props removed during all electrical and firmware bring-up;
- motors physically restrained during first output tests;
- independent disarm/kill procedure verified;
- radio-loss behavior tested before powered flight;
- CM5 loss behavior tested before any companion-assisted mode;
- power polarity and battery full-charge voltage checked;
- an experienced operator/instructor approves the test environment;
- no public or people-adjacent flight is inferred from bench success.

## 17. Manufacturing and assembly plan

The likely hand-assembly approach is:

- use 0603 passives only if the team's tools and inspection can support them; use larger packages where schedule risk matters;
- use a stencil and controlled paste placement if possible;
- reflow or hot-air the MCU and small parts with microscope inspection;
- hand-solder connectors, USB-C and mechanically stressed parts as appropriate;
- inspect under magnification and clean according to the flux/process requirements;
- order spare MCUs, IMUs, barometers, regulators and connectors;
- build one bare-board/prototype first before assembling all units;
- keep a serial/revision record for each assembled board.

The release package should contain:

- KiCad project, schematic and PCB;
- symbol/footprint libraries or versioned library links;
- PDF schematic and board drawing;
- stack-up and fabrication constraints;
- Gerber and drill files;
- BOM and component-placement file;
- connector/cable pinout;
- test-point map;
- ERC/DRC report and reviewed exceptions;
- firmware target/pin map;
- bring-up and acceptance-test record;
- copied license notices and source revision list.

## 18. One-month execution plan

This is a high-risk schedule, so each day must produce a reviewable artifact.

| Time | Deliverable |
|---|---|
| Days 1–2 | Freeze interface contract, MTOW assumptions, battery cell count, ESC signal pinout, receiver, CM5 variant and sensor roles |
| Days 3–6 | Complete core schematic, create firmware scaffold, bench-test CM5 carrier, camera and candidate scalar lidar |
| Days 7–10 | Complete PCB placement/routing, run ERC/DRC, review footprints and connector drawings |
| Days 11–14 | Release fabrication package and order/assemble the first board; prepare bench fixtures and test cables |
| Days 15–21 | FC power/MCU/IMU/baro/receiver/outputs bring-up; log all failures and rework |
| Days 22–27 | Integrate ESC, GNSS/compass, telemetry, lidar and CM5 link; run loss/stale-data and power tests |
| Days 28–30 | Controlled demo gate, documentation, known-issues list and decision on whether the aircraft is ready for further testing |

If a required input is missing at the end of Days 1–2, freeze a documented interface stub rather than silently changing the board later. The safest one-month outcome may be a verified FC bench demonstrator plus a separately tested CM5 perception stack, not an uncontrolled autonomous flight.

## 19. Main risks and mitigations

| Risk | Mitigation |
|---|---|
| H743 power/VCAP/clock error | Copy only verified datasheet/reference-design patterns; inspect rails before firmware |
| Wrong footprint or package orientation | Check every critical footprint against the exact datasheet and 3D model |
| IMU vibration/EMI/noise | Onboard placement, quiet rail, ground plane, mechanical isolation and logged noise testing |
| Compass interference | External placement, calibration and current-path separation |
| Raw battery routed into FC connector | Separate net classes and schematic review; `ESC_SIG` signal/ground only |
| Connector mismatch between teams | One signed pinout drawing, keyed cables, pin-1 labels and continuity testing |
| I2C loading/long cables | Keep I2C local where possible; calculate pull-ups or use CAN/UART externally |
| CAN termination mistake | Explicit bus-end ownership and selectable termination only at physical ends |
| CM5 brownout/inrush | Dedicated regulator, bulk capacitance, current limit and boot-load testing |
| CM5 becomes a hidden flight dependency | FC owns stabilization, arming, radio-loss and basic failsafe |
| Firmware port takes longer than PCB | Start with existing ArduPilot/PX4/Betaflight target structure and use a dev board for early scaffolding |
| One-month scope overload | Minimal proof-of-life milestone before perception/autonomy features |
| LGA/hand-assembly defect | Use inspection, stencil/reflow practice and spare parts; consider assembly service for the MCU |
| Battery/motor mismatch | Use thrust stand/current data and calculate mass before purchase |
| Community design claim is wrong or stale | Treat forum/video content as a hypothesis; verify with primary datasheets and measurements |
| Stock or part changes | Select alternates and recheck supplier stock immediately before BOM freeze |
| High-level avoidance command is unsafe | Bounds, heartbeat, timestamp, mode gating and stale-command rejection in FC firmware |

## 20. Open decisions and required next inputs

The master record is not a final schematic/BOM until these are answered:

### Vehicle and propulsion

- estimated and measured MTOW;
- frame type and motor count (current architecture assumes four motors);
- maximum propeller diameter and pitch;
- target hover time and flight time;
- 4S or 6S decision;
- exact motor/propeller candidate;
- ESC board current rating, firmware and connector;
- FC-to-ESC protocol: DShot, PWM or CAN;
- ESC telemetry and current-sense details;
- BEC availability and whether the BEC is allowed to power any logic load.

### FC and interfaces

- exact board outline and mounting holes;
- desired connector family and cable lengths;
- exact number of UART, CAN, I2C, SPI and motor outputs;
- receiver model/protocol and required telemetry;
- firmware target for Rev A;
- logging method;
- exact battery-monitor source and scale;
- whether official Pixhawk pin compatibility is required or only Pixhawk-inspired modularity.

### CM5, camera and lidar

- CM5 RAM/storage variant;
- official CM5IO first, custom carrier immediately, or both;
- camera choice and lens/FOV;
- whether independent FPV video is mandatory;
- lidar model;
- lidar role: altitude, forward scalar, 2D scan or 3D mapping;
- CM5-side interface: CSI, USB, UART or Ethernet;
- CM5-to-FC transport: UART/MAVLink, CAN/DroneCAN or another defined protocol;
- YOLO model size, target frame rate and acceptable latency;
- collision-avoidance behavior when perception data is unavailable.

### Production and test

- PCB manufacturer and layer stack;
- assembly capability and smallest practical package;
- number of boards and spares;
- test equipment available (bench supply, oscilloscope, logic analyzer, programmer, thrust stand);
- controlled test rig and responsible operator;
- project demonstration definition.

## 21. Source register and links

### 21.1 Official/primary technical sources

- [Raspberry Pi Compute Module documentation](https://www.raspberrypi.com/documentation/computers/compute-module.html)
- [Raspberry Pi CM5 datasheet](https://datasheets.raspberrypi.com/cm5/cm5-datasheet.pdf)
- [Pixhawk standards](https://pixhawk.org/standards/)
- [PX4 companion computers](https://docs.px4.io/main/en/companion_computer/pixhawk_companion)
- [PX4 collision prevention](https://docs.px4.io/main/en/computer_vision/collision_prevention)
- [PX4 rangefinders](https://docs.px4.io/main/en/sensor/rangefinders)
- [ArduPilot companion computers](https://ardupilot.org/dev/docs/companion-computers.html)
- [ArduPilot rangefinder setup](https://ardupilot.org/copter/docs/common-rangefinder-setup.html)
- [Betaflight manufacturer design guidelines](https://betaflight.com/docs/development/manufacturer/manufacturer-design-guidelines)
- [Betaflight DShot documentation](https://github.com/betaflight/betaflight.com/blob/master/docs/development/API/Dshot.mdx)
- [OpenDrone-hw OpenFC-Lite-Mini](https://github.com/OpenDrone-hw/OpenFC-Lite-Mini)
- [OpenDrone-hw OpenESC-20x20](https://github.com/OpenDrone-hw/OpenESC-20x20)
- [AM32 firmware](https://github.com/am32-firmware/AM32)
- [HomeGliders FCV2](https://github.com/HomeGliders/FCV2)
- [Bare-Metal-Foundry Shirley-FC-Dev-Board](https://github.com/Bare-Metal-Foundry/Shirley-FC-Dev-Board)
- [Raspberry Pi Camera Module 3](https://www.raspberrypi.com/products/camera-module-3/)
- [Raspberry Pi Global Shutter Camera](https://www.raspberrypi.com/products/raspberry-pi-global-shutter-camera/)
- [Raspberry Pi High Quality Camera](https://www.raspberrypi.com/products/raspberry-pi-high-quality-camera/)
- [Raspberry Pi AI Camera](https://www.raspberrypi.com/products/ai-camera/)
- [Benewake TF-Luna](https://en.benewake.com/TFLuna/index_proid_328.html?proid=329)
- [Benewake TFmini-S](https://en.benewake.com/TFminiS/index.html?proid=325)
- [Benewake TF02-i](https://en.benewake.com/TF02i/index.html?proid=861)
- [LightWare SF20/C](https://lightwarelidar.com/shop/sf20-c-100-m/)
- [LightWare SF45/B](https://lightwarelidar.com/shop/sf45-b-50-m/)
- [Slamtec RPLIDAR A1 specifications](https://www.slamtec.com/en/lidar/a1spec)
- [Slamtec RPLIDAR S2 specifications](https://www.slamtec.com/en/s2/spec)
- [Livox Mid-360 specifications](https://www.livoxtech.com/de/mid-360/specs)
- [T-Motor motor reference](https://tmotorhobby.com/goods.php?id=1183)
- [EMAX ECO II 2207 motor reference](https://emaxmodel.com/products/emax-eco-ii-series-2207-3-6s-1700kv-1900kv-2400kv-2750kv-brushless-motor)
- [EMAX ECO II 2814 motor reference](https://shop.emaxmodel.com/products/emax-ecoii-2814-730kv-830kv-brushless-motor-for-rc-drone)
- [Tattu battery brochure](https://www.genstattu.com/content/instock/rc_product_brochure.pdf)
- [Tattu R-Line battery range](https://genstattu.com/tattu-r-line-version-5-0-batteries/?page=2)

### 21.2 Supplied repositories and educational references

- [Udayate](https://github.com/Ozonised/Udayate)
- [Kalman-AHRS](https://github.com/Ozonised/Kalman-AHRS)
- [LSM6DSL platform-independent library](https://github.com/Ozonised/LSM6DSL-Platform-Independent-Library)
- [Quaternion Visualiser](https://github.com/Ozonised/Quaternion-Visualiser)
- [Pixhawk 2.1 reference repository](https://github.com/MRazgunas/pixhawk2.1)

### 21.3 User-supplied videos

- [DIY FC video/reference 1](https://www.youtube.com/watch?v=XDYZoMRJFeQ)
- [DIY FC video/reference 2](https://www.youtube.com/watch?v=6n7d8Jn2brQ)
- [DIY FC video/reference 3](https://www.youtube.com/watch?v=wYC-siMWn70)
- [Udayate-related video](https://www.youtube.com/watch?v=pUdvCbNR1gM&t=43s)

The first two video pages were not reliably machine-readable in the previous review. Their associated repositories were analyzed where available; no unsupported claims were made from inaccessible video content.

### 21.4 User-supplied Reddit references

- [Custom flight controller, r/fpv](https://www.reddit.com/r/fpv/comments/1r5rvne/build_a_custom_flight_controller/)
- [Custom flight controller from scratch, r/diydrones](https://www.reddit.com/r/diydrones/comments/1q5k508/built_a_custom_flight_controller_from_scratch/)
- [Anyone built their own flight controller, r/diydrones](https://www.reddit.com/r/diydrones/comments/1oibb96/anyone_here_built_their_own_flight_controller/)
- [Custom flight controller, r/Multicopter](https://www.reddit.com/r/Multicopter/comments/1s6r7ht/building_a_custom_flight_controller_from_scratch/)
- [User-supplied PCB review link, normalized](https://www.reddit.com/r/PCB/comments/1qci8jg/review_request_drone_flight_controller_with/)
- [STM32H743 flight-controller review, r/PCB](https://www.reddit.com/r/PCB/comments/1q3kh9f/stm32h743_flight_controller_review_request/)
- [Flight-controller build, r/diydrones](https://www.reddit.com/r/diydrones/comments/1ts9v3u/building_a_flight_controller/)

The normalized PCB-review link above reflects the malformed path supplied in the original list. It must be rechecked before relying on that post for a specific claim.

## 22. Current final recommendation

Proceed with a **custom STM32H743VIT6 Rev A FC** using an onboard **ICM-42688-P + BMP390**, external GNSS/compass, external receiver/telemetry, a signal-only modular ESC interface, and a hybrid Pixhawk-inspired connector architecture. Use a separately powered **CM5 carrier** for camera/YOLO/tracking and scanning-lidar work. Use a lightweight scalar lidar only if the FC needs an independent altitude/range source. Start with DShot when the ESC supports it and retain PWM for bring-up. Keep ArduPilot as the leading integrated autopilot path while preserving PX4 as the principal alternative for a stronger DroneCAN/ROS 2/Pixhawk workflow.

The next implementation gate is not another general research pass. It is the collection and freeze of the open inputs in Section 20, followed by the KiCad schematic, pinout, PCB constraints, BOM and staged bench verification.
