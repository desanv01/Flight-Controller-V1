> Historical technical record. Names and private workstation/session references were neutralized for publication. Dates and assertions describe the recorded stage, not current physical qualification. See the current validation-status page for later checks.

# DIY Flight-Controller PCB Research for the UAS/UAM Prototype

## Preliminary engineering report, open-hardware study, and sourcing plan

**Prepared for:** Desan’s autopilot / flight-controller work package
**Project context:** Phase 1 Malaysian UAS/UAM technology and prototype project
**Research date:** 26 August 2026
**Document status:** Preliminary engineering research — not a fabrication release
**Intended output:** A defensible starting point for a custom flight-controller PCB, component selection, and prototype plan

**Update:** 27 August 2026 — added the Pixhawk-style modular-connectivity analysis, external-port contract, bus-selection guidance, hybrid sensor-boundary decision, and the CM5/propulsion/sensor integration addendum.

> **Important scope and safety note:** This report is for a non-weaponized student research prototype intended for learning, inspection, mapping, or a simple demonstrator. It does not provide weapon guidance, targeting, or payload-control design. It is not an aircraft certification basis, a production autopilot, or a recommendation to fly an unverified custom board. All first tests should be performed without propellers, with current limiting and instructor approval.

---

## Executive conclusion

The lecturer’s feedback points to a **custom flight-controller PCB**, not merely the purchase of an Arduino, Raspberry Pi, or commercial Pixhawk. The practical interpretation is:

1. Choose a processor and interfaces.
2. Design the schematic and PCB from first principles.
3. Buy the MCU, sensors, regulators, memory, connectors, and passive SMD parts separately.
4. Fabricate the board and assemble it.
5. Flash and bring up the processor.
6. Verify the board on the bench before considering a tethered or flight demonstration.

For a first revision, the most defensible architecture is a **single STM32H743-based FMU-Lite board**:

| Recommended element | Preliminary choice | Why |
|---|---|---|
| Main processor | **STM32H743VIT6**, LQFP-100 | 480 MHz Arm Cortex-M7, up to 2 MB Flash and 1 MB RAM, many timers/SPI/UART/CAN/USB peripherals, and a relatively hand-assembly-friendly package |
| Primary inertial sensor | **ICM-42688-P** as the Rev A default; BMI088 only as a verified availability fallback | Fast SPI six-axis IMU; use a second footprint only if the firmware and board budget justify it |
| Barometer | **BMP390** | Small, low-power pressure sensor with SPI/I2C |
| Magnetometer | Prefer an **external GPS/compass module**; optionally provide an IST8310 or MMC5983MA footprint | Motor currents, battery wiring, and switching regulators can disturb an onboard compass |
| Power input | External regulated 5 V from a power module for Rev A; optional raw-battery buck only after power analysis | Reduces first-revision heat, EMI, and high-energy failure risk |
| Digital rail | 3.3 V buck regulator, with a separate low-noise sensor rail | Keeps the MCU and sensors within their voltage limits and reduces noise coupling |
| Output capability | Eight timer/PWM/DShot logic outputs | Supports a quadrotor plus spare channels; ESC power remains external |
| Communications | USB-C for setup, SWD for debug, 4–6 UARTs, one CAN interface, I2C and spare SPI | Sufficient for GNSS, telemetry, receiver, debug, and expansion |
| Logging | microSD footprint plus optional W25Q128JV flash | Supports flight/bench logs and configuration recovery |
| PCB | Four-layer Rev A; six layers only if the selected stack-up and signal-integrity need justify it | Four layers are more achievable for a student prototype; six layers help with planes and routing but increase cost and fabrication dependence |

The first flight-worthy-looking board should **not** be the first test article. A safer development sequence is:

~~~text
Schematic and pin map
        ↓
ERC / datasheet review / footprint review
        ↓
PCB layout / DRC / manufacturing files
        ↓
Unpowered inspection
        ↓
Current-limited power-up
        ↓
SWD + clock + USB + regulator bring-up
        ↓
IMU/barometer/ADC/CAN/PWM tests
        ↓
Estimator + PID bench tests
        ↓
Tethered or rig test with instructor approval
        ↓
Only then consider a controlled flight demonstration
~~~

The recommended report does **not** claim that the board will immediately run stock PX4 or ArduPilot. A custom board needs its own firmware target, bootloader/configuration, pin definitions, sensor drivers, and verification. The fastest credible early milestone is a custom board that boots, reads sensors, generates safe PWM, logs data, and passes bench tests. PX4/ArduPilot integration is a second stage.

The confirmed connectivity requirement changes the physical architecture to a **hybrid Pixhawk-style modular FC**. The FC will expose keyed external ports for the ESC board, receiver, GNSS/compass, telemetry, Raspberry Pi Compute Module 5 (CM5), CAN peripherals and appropriate lidar. The primary high-rate IMU and barometer remain on the FC PCB for timing, mechanical-reference and bring-up reliability. This provides modular vehicle integration without making the most timing-sensitive sensors dependent on long external cables.

### Abbreviation key

| Abbreviation | Meaning |
|---|---|
| FC / FMU | Flight controller / flight-management unit |
| MCU | Microcontroller unit |
| SBC | Single-board computer |
| FPGA | Field-programmable gate array |
| IMU | Inertial measurement unit |
| GNSS | Global navigation satellite system |
| ESC | Electronic speed controller |
| PWM | Pulse-width modulation |
| DShot | Digital ESC command protocol |
| UART | Universal asynchronous receiver/transmitter |
| SPI | Serial peripheral interface |
| I2C | Inter-integrated circuit bus |
| CAN | Controller Area Network |
| USB | Universal Serial Bus |
| SWD | Serial wire debug |
| ADC | Analog-to-digital converter |
| LDO | Low-dropout linear regulator |
| TVS | Transient-voltage suppressor |
| ESD | Electrostatic discharge |
| BOM | Bill of materials |
| ERC / DRC | Electrical rules check / design rules check |
| DNP | Do not populate |
| HIL | Hardware-in-the-loop |
| UAS / UAM | Unmanned aircraft system / urban air mobility |

---

## 1. What the attached material actually requires

### 1.1 The user’s request versus instructions inside the attachments

The attached meeting screenshots and transcript contain instructions and opinions from the lecturer. They are **context**, not a replacement for the current request. The current request is to research and propose possible processors/boards/MCUs for a prototype and then expand that into a from-scratch custom flight-controller PCB research package.

The deliverable in this report is therefore:

- an interpretation of the lecturer’s requirements;
- a research-backed shortlist of MCU, SBC, FPGA, and commercial-board options;
- a recommended custom flight-controller architecture;
- a preliminary logical BOM including SMD parts and purchase links;
- pricing with clear uncertainty labels;
- open-source hardware and firmware resources;
- tutorials and practical build references;
- schematic, PCB, assembly, firmware, and verification steps.

This report is **not**:

- a final production BOM;
- a guaranteed current-stock quotation;
- a certified UAS/UAM flight-control design;
- proof that any community board is safe to fly;
- permission to copy a third-party design without reading its license.

### 1.2 Requirements extracted from the meeting evidence

The meeting material consistently points to the following:

| Evidence from the meeting material | Engineering meaning |
|---|---|
| “Own autopilot” / build something yourselves | The project should demonstrate original design work, not only a purchased flight controller |
| Choose a processor and decide what the board can do | Start with requirements, pin/peripheral allocation, and a block diagram |
| Use STM parts, sensors, memory, and SMD devices bought separately | The board must have an actual schematic and BOM |
| Make the PCB, route it, fabricate layers, and solder/assemble it | Include manufacturability, footprints, assembly, inspection, and bring-up |
| Look at Pixhawk and other commercial products | Use commercial/open designs as references and benchmarks, not automatically as the project’s own design |
| Discuss firmware flashing and bench testing | Include SWD programming, bootloader, firmware bring-up, and test gates |
| Discuss PID, cascade, sensor fusion, and control allocation | Explain how measurements become motor commands, but keep the first PCB scope achievable |
| Mention DO-178 / DO-254 and standards | Treat them as future assurance context; do not claim compliance for a student prototype |
| Mention board layers, routing, air soldering, magnification, and tools | The design must be manufacturable by the team and compatible with available lab equipment |
| Demonstration is a simple prototype, not a full commercial product | Prioritize a testable educational demonstrator over redundant UAM certification features |

### 1.3 Scope boundary

The broad word **UAM** can imply passenger-carrying aircraft, detect-and-avoid, redundant flight computers, certified development processes, and airworthiness evidence. That is far beyond a first student PCB. For this work package, “UAS/UAM autopilot” should be presented as:

> A small-vehicle flight-control computer concept, developed as a non-certified prototype, showing the same basic control-chain principles used in larger UAS/UAM systems.

The report therefore includes certification and commercial references only to explain the design gap. It does not imply that a custom student board can be installed on a passenger eVTOL or used as a safety-critical primary flight computer.

### 1.4 Files and evidence used

The analysis used the supplied meeting screenshots, the supplied pasted text, and the existing project files in the shared folder:

| Supplied item | How it was used |
|---|---|
| Meeting screenshots | Primary evidence for the lecturer’s expectations: own board, processor choice, schematic, PCB layers/routing, SMD assembly, firmware flashing, testing, standards context, and prototype scope |
| Pasted meeting/transcription text | Used to identify Desan’s autopilot/PCB discussion; names and unrelated team discussions were intentionally excluded from this work package |
| Existing autopilot_uas_uam_research.md | Used as the earlier technical background on autopilot purpose, closed-loop control, sensor fusion, PX4/ArduPilot, and UAS/UAM terminology |
| Existing presentation decks and scripts | Used only to preserve continuity with the previously researched autopilot architecture; they are not treated as engineering approval |
| Earlier product/board shortlist | Expanded and corrected here into a custom-board decision, with a distinction between development aids, commercial references, and the final custom PCB |

The pasted text is an earlier research/answer document rather than a complete verbatim lecturer transcript. Where a point comes only from a community source or the previous shortlist, it is labelled accordingly rather than treated as a requirement.

### 1.5 Assessment of the previous board/solution shortlist

The earlier shortlist was directionally correct but answered a different question: “what is the lowest-risk way to make a prototype fly?” The current project asks, “what can Desan design and assemble from scratch?” The corrected interpretation is:

| Earlier conclusion | Assessment for the current project |
|---|---|
| Pixhawk 6C/6X is lower risk for a first flight | Technically true, but it is a benchmark or fallback flight controller, not the custom PCB deliverable |
| STM32H743/H753 is the strongest custom MCU family | Still the best starting point; the report narrows this to H743VIT6 for Rev A |
| Raspberry Pi/Jetson is useful for vision and mission logic | Correct; keep it as a companion computer rather than the deterministic inner-loop controller |
| FPGA is useful for parallel hardware and research | Correct; keep it optional unless the project has a defined FPGA contribution |
| Arduino Uno is accessible | Correct for teaching and bench I/O, but not suitable as the full FC |
| Portenta H7 / NUCLEO / Teensy are useful development platforms | Correct; use them to de-risk firmware and interfaces before fabricating the custom board |
| A commercial board can be used immediately | Only as an interim risk-control or comparison platform; it would not demonstrate the requested from-scratch design |

The report therefore preserves the earlier solution categories but changes the recommendation from “buy a Pixhawk” to “design an H743 custom board, while retaining a ready-made FC only as a safe fallback for software or vehicle testing.”

### 1.6 Meeting-screenshot topic map

The 49 supplied screenshots were treated as one meeting record. The following map records the relevant topics and prevents unrelated team-member discussions from being silently mixed into Desan’s work package:

| Screenshot range | Main topic observed | Relevance to this report |
|---|---|---|
| Images 1–8 | Passive/active sensors, FPGA, EO/IR/multispectral payload direction, and selecting technology based on the application | Establishes the lecturer’s preference for application-driven component selection and a realistic prototype scope |
| Images 9–17 | FPGA versus processor, RISC-V/Verilog, open-source hardware/software, and sensor processing | Supports the MCU/SBC/FPGA role separation; FPGA is optional rather than automatically the primary FC |
| Images 18–32 | Other subsystem discussions including sensors, radar/LiDAR, H-bridge, BLDC, PWM, ESC/motor-related material | Not treated as Desan’s primary deliverable; only the FC’s electrical interfaces are carried into this report |
| Images 33–39 | Own autopilot, processor choice, board capability, outputs, market/reference players, PCB design, routing, layers, and fabrication | Defines the custom FC PCB requirements |
| Images 40–44 | SMD assembly, hot air/air soldering, magnification, tools, and testing | Defines manufacturability and bring-up requirements |
| Images 45–49 | Pixhawk/commercial references, PID/cascade/sensor fusion/control allocation, firmware flashing, standards, and prototype demonstration | Defines the software path, reference-board use, assurance boundary, and non-certified demonstrator scope |

This topic map is an interpretation of the supplied images; it is not a claim that every product or standard mentioned in a meeting was formally selected.

---

## 2. What an autopilot board has to do

An autopilot is a real-time embedded control system. It repeatedly:

1. samples inertial and environmental sensors;
2. estimates attitude, position, velocity, and system health;
3. compares the estimate with pilot or mission commands;
4. computes control corrections;
5. allocates the requested thrust/torque to motors or actuators;
6. exchanges telemetry and logs the result;
7. detects faults and moves to a predefined safe state.

The board is only one part of the system. A complete prototype also needs a vehicle model, motors, ESCs, propellers, power system, radio/telemetry link, GNSS if required, firmware, calibration, and a controlled test method.

### 2.1 Closed-loop control

~~~text
Pilot / mission command
          ↓
 Position / velocity controller
          ↓
 Attitude controller
          ↓
 Rate controller
          ↓
 Mixer / control allocator
          ↓
 PWM or DShot commands
          ↓
 ESCs → motors → vehicle motion
          ↑                         ↓
          └── IMU, barometer, GNSS, compass, air-data feedback
~~~

The loop only works if the time relationship between sensor samples and actuator commands is controlled. That is why a small real-time MCU is normally the primary flight-control processor. A Linux single-board computer can add high-level processing, but it is not automatically a replacement for the deterministic inner loop.

### 2.2 Sensor fusion in one sentence

Sensor fusion combines complementary measurements:

- gyroscopes respond quickly but drift;
- accelerometers provide gravity information but are disturbed by vibration and linear acceleration;
- a magnetometer can provide heading information but is sensitive to magnetic interference;
- a barometer estimates relative altitude but is affected by airflow and pressure changes;
- GNSS provides global position/velocity but is slower, intermittent, and environment-dependent.

The estimator uses models and measurement updates to produce a better state estimate than any single sensor. A custom board must therefore provide clean sensor interfaces, timestamps, stable power, vibration-aware placement, and a firmware driver path.

---

## 3. Design target for the first custom PCB

The following target is intentionally modest. It is enough to demonstrate a serious flight-controller design while avoiding an unbounded “build a certified UAM computer” project.

### 3.1 Assumed vehicle and electrical envelope

| Parameter | Rev A design target | Reason |
|---|---:|---|
| Vehicle | Small quadrotor or VTOL research demonstrator | Matches the prototype context |
| Battery | 2S–6S Li-ion/LiPo; exact battery to be confirmed | Drives input protection and voltage measurement |
| Logic | 3.3 V | Matches STM32H7 and most modern sensors |
| Motor outputs | 8 timer/PWM/DShot-capable channels | Four motors plus expansion/spares |
| IMU | One populated high-rate SPI IMU; second optional | Keeps Rev A testable while leaving a reliability path |
| Barometer | One | Basic altitude/pressure measurement |
| Magnetometer | External preferred; optional onboard footprint | Reduces magnetic interference |
| GNSS | External module over UART/I2C/CAN as applicable | Antenna and compass should be physically separated from the power stage |
| Telemetry | At least one spare UART; one CAN bus | Supports radio and future peripherals |
| Logging | microSD and/or SPI flash | Required for debugging and presentation evidence |
| Debug | SWD, reset, boot selection, test points | Essential for first-board bring-up |
| USB | USB-C device port | Firmware loading, parameter setup, and logs |
| PCB | Four-layer default; six-layer option | Balances student fabrication and signal/power integrity |
| Operating goal | Bench, rig, and later controlled prototype demonstration | Not certified operational flight |

### 3.2 Interfaces and pin-budget checklist

Before drawing the schematic, create an explicit pin map. A candidate pin map should allocate:

- SPI1 or SPI2 for the primary IMU, with a dedicated chip-select;
- a separate SPI bus or chip-select strategy for the optional second IMU;
- I2C for barometer, external compass, and low-speed peripherals;
- one or more UARTs for GNSS, telemetry, receiver, and debug;
- CAN TX/RX for a CAN transceiver;
- eight timer outputs for motor/servo channels;
- ADC channels for battery voltage, current, and analog health signals;
- SDMMC or SPI for the microSD socket;
- USB D+ and D−;
- SWDIO, SWCLK, optional SWO, NRST, and BOOT0;
- status LEDs, buzzer, safety switch, and spare GPIO.

Do not assign pins only by the symbol name. Check the STM32 alternate-function table, DMA availability, timer channels, interrupt routing, and conflicts between USB, SDMMC, SPI, and timers.

### 3.3 Pixhawk-style modular connectivity decision

The newly confirmed mechanical/system requirement is a **fully connectable flight-control system**: the ESC board, receiver, GNSS/compass, telemetry, CM5 carrier, lidar, and other replaceable peripherals should attach through defined connectors. The important engineering distinction is that system-level modularity does not require every sensor IC to be remote.

Pixhawk is useful here as an **interface and architecture model**. The official Pixhawk standards cover pinouts, architecture, PCB guidance, and connector specifications. A board is not Pixhawk-compatible merely because it uses a similar JST connector; compatibility requires the exact selected standard pinout, electrical levels, power rules, mechanical details, and firmware mapping.

#### Options compared

| Architecture | What remains on the FC | What becomes external | Benefits | Problems | Decision |
|---|---|---|---|---|---|
| Fully modular raw-sensor FC | MCU, power and interfaces only | IMU, barometer, compass, GNSS, lidar and other sensors | Maximum replacement/serviceability and clear module boundaries | Remote SPI/I2C signal integrity, cable capacitance, EMI, connector failure, timing/latency, sensor-frame alignment, more firmware, and no local sensor for first bring-up | Reject for Rev A |
| Hybrid Pixhawk-style FC | MCU, primary high-rate IMU and barometer | ESC, receiver, GNSS/compass, telemetry, CM5, CAN peripherals and suitable lidar | Deterministic inner loop, external compass placement, strong team integration and manageable one-month scope | More connectors, protection and wiring documentation than a compact FPV FC | **Adopt for Rev A** |
| Mostly onboard FC | MCU and most sensors | ESC, receiver and CM5 mainly | Smallest harness and lowest connector cost | Compass remains near noisy power/motor hardware; less serviceable; poor fit for separate sensor workstreams | Not selected |

The resulting rule is:

> **Rev A is externally modular but internally deterministic.** Keep the primary ICM-42688-P and BMP390 on the FC PCB. Make the ESC, RC receiver, GNSS/compass, telemetry, CM5 carrier, CAN peripherals and appropriate lidar externally connectable.

#### Sensor-by-sensor boundary

| Subsystem | Rev A decision | Connection and reason |
|---|---|---|
| Primary IMU | Onboard | Short dedicated SPI traces, local interrupt/timestamp path, known mechanical reference and clean sensor supply. A future remote IMU must be a smart MCU/CAN node, not a bare IMU on a long cable. |
| Barometer | Onboard | Local low-speed bus is simpler for Rev A. Use a protected vent and isolate it from prop wash. A remote pressure location requires a purpose-designed sensor node and airflow arrangement. |
| Compass | External | Place it away from battery leads, motor phases, ESC switching currents, inductors and ferromagnetic hardware. Use an external GPS/compass module over UART+I2C or DroneCAN. |
| GNSS | External | Antenna sky view, physical separation and serviceability are better outside the FC enclosure. Provide UART and PPS, with I2C or CAN as required by the module. |
| Downward rangefinder | Direct to FC where practical | A scalar low-latency altitude measurement is most useful to the FC. UART, I2C or CAN may be used according to the selected sensor and flight-stack driver. |
| Scanning/3-D lidar | CM5 or smart CAN node | CM5 can handle USB/UART/Ethernet data, filtering, obstacle sectors, maps and logging. The FC should receive only a validated low-bandwidth result. |
| Camera | CM5-side only | Connect CSI-2 or USB camera hardware to CM5. The FC should not carry raw video frames. It may receive a trigger, timestamp, visual-odometry result or high-level command. |
| ESC/motor stage | External | The FC exposes logic-level output and optional telemetry/CAN. Battery current, motor phases, switching heat and high-current copper stay on the separate ESC/power board. |

#### Bus choice for modular connections

| Interface | Best use | Rev A cable rule |
|---|---|---|
| SPI | Primary IMU, local memory and SD | Keep on the FC PCB or a very short retained daughterboard. Do not expose the high-rate IMU bus as an arbitrary flight harness. |
| I2C | BMP390 and short external compass/low-speed accessories | Use only after calculating total bus capacitance, pull-up values, connector loading and rise time. Make external pull-ups selectable to avoid duplicate strong pull-ups. |
| UART | Receiver, GNSS, telemetry, simple lidar and FC↔CM5 link | Point-to-point, labeled by function, with a ground return and verified 3.3 V compatibility. |
| CAN/DroneCAN | Remote sensor nodes, GNSS/compass, lidar nodes, power modules and CAN ESCs | Preferred remote-module bus. Use a differential pair, line topology, short stubs and 120 Ω termination only at the two physical ends. |
| PWM/DShot | FC-to-ESC board | One defined signal and ground return per output. Do not carry motor power through the FC harness. |
| USB/CSI-2/Ethernet | CM5-side camera and high-volume data | Keep camera and scanning-lidar traffic on the CM5 side; send processed results to the FC. |

NXP’s I2C specification counts wire, connector and pin capacitance as part of the bus load and gives 400 pF as the common Standard/Fast-mode limit. TI documents the use of buffers/extenders when long cables exceed normal I2C loading. CAN is more appropriate for a robust remote sensor network; CAN in Automation recommends a line topology with 120 Ω termination at both bus ends. These constraints are the main reason the recommended design is hybrid rather than “every sensor on a long cable.”

#### Proposed modular port set

The following are **logical ports**, not yet frozen connector part numbers:

| Port | Signals/function | External owner |
|---|---|---|
| `POWER1` | Regulated 5 V, GND, scaled battery-voltage sense and protected current-sense input | ESC/power board |
| `ESC_OUT` | M1–M4 signal plus signal grounds; optional telemetry or a separate CAN path | ESC board |
| `RC_IN` | Receiver supply, GND, UART RX and optional TX | Transmitter/receiver workstream |
| `GPS1` | Module supply, GND, GNSS UART TX/RX, PPS and optional I2C compass lines | GNSS/compass module |
| `GPS2/AUX_I2C` | Supply, GND, SDA/SCL and optional interrupt | Second or short low-speed sensor module |
| `CAN1/CAN2` | Supply, GND, CANH and CANL | DroneCAN sensors, lidar, power node or CAN ESC |
| `TELEM1` | UART TX/RX/GND, optional CTS/RTS | Ground telemetry radio |
| `COMPANION` | UART TX/RX/GND, optional CTS/RTS | Raspberry Pi CM5 on a separate carrier; CM5 power is separate |
| `LIDAR_FC` | UART, I2C or CAN, supply and GND | Downward/simple rangefinder |
| `AUX_UART` | Labeled spare point-to-point serial port | Future peripheral |
| `AUX_SPI` | Short local SPI/CS/INT/GND expansion | Engineering daughterboard only |
| `SWD/DEBUG` | SWDIO, SWCLK, NRST, 3V3 reference, GND and BOOT0 access | ST-LINK and bring-up |

Connector rules:

- Use keyed, locking, vibration-tolerant connectors and documented mating cables; do not use loose Dupont jumpers for the flight harness.
- Put ground returns next to fast/noise-sensitive signals. Keep CANH/CANL together and minimize untwisted length at the connector.
- Print port names, pin 1 and signal names. `UART1` alone is not a sufficient field-service label; use `RC_IN`, `GPS1`, `COMPANION`, and so on.
- Define an electrical budget for each port. A module supply may be 5 V while its signal I/O is 3.3 V; never expose STM32 pins to 5 V without checking level compatibility or adding translation.
- Add connector-side ESD/overvoltage protection where justified, especially for USB, CAN, exposed power and long external UARTs. Verify protection capacitance against the interface speed.
- Do not assume hot-plugging. Rev A modules are changed with power removed unless the port has a deliberate load-switch/current-limit/hot-swap design and has been tested.
- Keep external sensor orientation, position relative to the FC, cable length, node ID/address, update rate and timeout in the wiring and firmware documentation.

Modular hardware also creates firmware work. PX4 and ArduPilot need board-specific definitions for the physical UARTs, buses, timers, ADCs, CAN nodes and sensor drivers. A standard connector makes wiring clearer; it does not make a new H743 board automatically supported by either flight stack. If external GPS/compass, lidar and MAVLink companion integration are central assessment features, ArduPilot or PX4 is a more natural long-term fit than a Betaflight-only target. Betaflight remains the shortest path to a manual/stabilized quad demonstration.

References for this decision: [Pixhawk Reference Standards](https://pixhawk.org/standards/), [PX4 GNSS/GPS setup](https://docs.px4.io/main/en/gps_compass/), [PX4 magnetometer guidance](https://docs.px4.io/main/en/gps_compass/magnetometer), [PX4 ARK CANnode](https://docs.px4.io/main/en/dronecan/ark_cannode), [NXP UM10204 I2C specification](https://community.nxp.com/pwmxy87654/attachments/pwmxy87654/nxp-designs/931/1/UM10204.pdf), [TI long-cable I2C guidance](https://www.ti.com/kr/lit/pdf/sdaa306), and [CAN in Automation high-speed CAN guidance](https://www.can-cia.org/can-knowledge/can-hs-transmission).

---

## 4. Options investigated: boards, MCUs, SBCs, and FPGAs

### 4.1 Main processor / MCU candidates

| Candidate | Class | Useful characteristics | Strengths | Limitations | Suitability for this custom FC |
|---|---|---|---|---|---|
| **STM32H743VIT6 / H743ZI** | Cortex-M7 MCU | Up to 480 MHz, up to 2 MB Flash and 1 MB RAM, many timers, SPI/UART/CAN/USB, DSP/FPU | Strong PX4/ArduPilot ecosystem; good real-time capability; LQFP packages available | Requires careful power, clock, VCAP, decoupling, and high-speed layout; stock prices vary | **Best Rev A main MCU** |
| **STM32H753** | Cortex-M7 MCU | Similar high-performance H7 family; extra security/crypto features in relevant variants | Suitable when security or more advanced processing is required | More expensive/complex than necessary for a first student board | Good Rev B or security-focused design |
| **STM32H723/H725** | Cortex-M7 MCU | High performance with slightly different memory/peripheral mix | Can reduce cost and still support a capable FC | Verify exact RAM/Flash/peripheral needs and community firmware support | Good alternate if supply is better |
| **STM32F767** | Cortex-M7 MCU | Mature 216 MHz-class MCU family with broad tool support | Easier historical references; capable for basic stabilization | Less headroom and memory than H7; older family | Viable lower-cost experiment |
| **STM32G4** | Cortex-M4 MCU | Fast control-oriented peripherals and ADCs | Very useful for motor control, power electronics, or an I/O coprocessor | Less suited than H7 as a feature-rich autopilot main processor | Excellent optional companion/ESC-control MCU |
| **NXP i.MX RT1170** | Crossover MCU | Very high-performance real-time MCU family | Powerful and interesting research platform | More complex ecosystem and custom firmware work; less direct PX4/ArduPilot path | Research alternate, not first choice |
| **Teensy 4.1** | MCU development board | Fast NXP MCU on a convenient module | Rapid algorithm experiments and bench work | Not a custom bare-metal board; board-level interfaces/EMC are not the project result | Useful proof-of-concept, not final PCB |
| **Arduino Portenta H7** | MCU module | Dual-core STM32H747-based development platform | Rapid prototyping and software exploration | Cost, module dependence, and less control over the custom PCB | Good software prototype; not the custom-board deliverable |
| **Raspberry Pi Pico 2 / RP2350** | MCU board/chip | Low-cost and accessible | Good for simple I/O or education | Not a direct PX4/ArduPilot flight-controller path; fewer autopilot references | Auxiliary experiment only |
| **ESP32-S3** | MCU/SoC | Wi-Fi/Bluetooth and inexpensive | Connectivity and rapid IoT experiments | Wireless stack and timing are not ideal as the first primary FC; ecosystem mismatch | Companion/telemetry experiment only |
| **Arduino Uno R3/R4** | Educational development board | Very accessible | Excellent for learning basic PWM and sensors | Insufficient memory/performance/architecture for a modern multicopter autopilot | Demonstration or sensor bench only |

**Selection:** STM32H743VIT6 is the default recommendation. Use H753 only if the project has a specific need for the added security/feature set. Do not select the MCU by clock frequency alone; pin count, timer/DMA layout, sensor-bus support, boot/debug path, firmware porting cost, package availability, and supply continuity matter more.

### 4.2 Ready-made flight-controller boards used as reference benchmarks

These are useful for studying functional partitioning, connectors, power domains, and firmware support. They are not substitutes for the requested custom design.

| Board/family | Typical role | Reference value | Caution |
|---|---|---|---|
| Pixhawk 6C / 6X | Open-ecosystem autopilot hardware | Shows modern H7 architecture, IMUs, barometers, CAN, power, and Pixhawk connector conventions | Commercial board; exact layout/firmware target and license must be respected |
| Cube Orange+ | Mature autopilot module | Useful comparison for redundancy and enclosure/module design | Not a simple first custom-board reference |
| CUAV X7 | Commercial H7 autopilot | Useful for interface and redundancy comparison | Proprietary manufacturing and exact implementation |
| Holybro Kakute H7 | Compact multicopter FC | Useful for high-density sensor/power layout ideas | FPV-centric integration differs from a Pixhawk-style research board |
| Durandal / ARKV6X | Commercial/open-ecosystem references | Show alternative connector and sensor arrangements | Use only as a benchmark, not a copy |

The key lesson from these boards is not “copy a Pixhawk.” It is “understand why the board has separated power rails, multiple sensor paths, debug access, robust connectors, and a defined firmware target.”

### 4.3 Companion computers and SBCs

| Candidate | Use | What it adds | Why it should not replace the Rev A inner-loop MCU |
|---|---|---|---|
| Raspberry Pi Compute Module 5 (CM5) | High-level autonomy, video, telemetry, logging | Linux ecosystem, CSI-2/USB camera and AI software, networking, carrier-board integration | Linux scheduling and boot time are not deterministic enough for the inner rate loop by themselves; CM5 requires a separate carrier |
| NVIDIA Jetson Orin Nano Super | Vision/AI and perception | GPU acceleration and computer-vision frameworks | Higher power, thermal, and software complexity |
| BeagleBone / NXP i.MX 8M Plus | Industrial/embedded Linux | Real-time expansion options and vision/edge processing | More integration work than needed for first prototype |
| ModalAI VOXL 2 / Auterion Skynode S | Commercial autonomy platform | Integrated compute, sensors, and robotics software | Excellent reference, but contrary to a from-scratch low-cost board objective |

Recommended split if the team later adds autonomy:

~~~text
STM32H743 custom FC  ←→  MAVLink / CAN / UART  ←→  Raspberry Pi or Jetson
real-time stabilization                              vision / mapping / mission logic
~~~

The companion computer should send high-level setpoints, not directly replace the tested real-time stabilization loop.

### 4.4 FPGA candidates

| Candidate | Useful role | Why it is interesting | Why it is not the default FC processor |
|---|---|---|---|
| AMD Kria KV260 / KR260 | Vision, FPGA acceleration, robotics I/O | Strong programmable-logic and Linux integration | Cost, power, toolchain, and real-time firmware burden |
| PYNQ-Z2 / Zybo Z7 | FPGA learning and custom hardware blocks | Accessible Zynq teaching platforms | Development board is not a finished flight-controller PCB |
| Terasic DE10-Nano | FPGA + ARM SoC research | Good for hardware/software co-design | Larger, higher-power, less direct autopilot ecosystem |
| Digilent Arty A7 | FPGA education and timing experiments | Low barrier for Verilog/VHDL exercises | Needs a separate processor and vehicle I/O architecture for a practical FC |
| Microchip PolarFire | Low-power/industrial FPGA research | Interesting for deterministic hardware and security | Toolchain, cost, and avionics assurance work are substantial |

An FPGA may be valuable for a separate sensor-processing or deterministic accelerator experiment. For Rev A flight control, an STM32 MCU is more realistic because the team needs a known firmware path, ADC/timer/PWM support, SWD debugging, and an achievable PCB.

### 4.5 Development boards for early software and interface experiments

These boards are useful before committing the custom PCB. They allow the team to prove sensor drivers, timing, PWM, and estimator code while the schematic is being reviewed. They do not replace the custom-board deliverable.

| Development board | Processor | Best use before custom PCB | Why it is not the final answer |
|---|---|---|---|
| **NUCLEO-H723ZG** | STM32H723 | STM32H7 peripheral, timer, UART, CAN, and SWD experiments | Board routing and power architecture are already done; the project still needs its own PCB |
| **NUCLEO-F767ZI** | STM32F767 | Lower-cost H7/F7 firmware and peripheral bring-up | Older/lower-performance target and not the final sensor/power integration |
| **Arduino Portenta H7** | STM32H747 dual-core module | Rapid high-level software and sensor experiments | Module cost and fixed interfaces reduce custom hardware learning |
| **Arduino GIGA R1 WiFi** | STM32H747 | General embedded/vision/networking experiments | Development board is not a flight-controller layout and adds features that are not needed in Rev A |
| **Teensy 4.1** | NXP i.MX RT1062 | Fast control-loop algorithm and PWM bench tests | Different MCU ecosystem and no direct custom STM32 board path |
| **Raspberry Pi Pico 2** | RP2350 | Basic sensor, GPIO, and educational timing experiments | Not a direct PX4/ArduPilot flight-controller target |
| **Arduino Uno R3/R4** | AVR/RA4M1 | Introductory PWM, serial, and sensor exercises | Too constrained or mismatched for a modern feature-rich FC |

The useful pattern is: use a development board to de-risk firmware, then reproduce only the required processor, power, sensor, and connector functions on the custom PCB.

---

## 5. Recommended Rev A architecture

### 5.1 Logical block diagram

~~~text
             External regulated 5 V
                      │
        USB-C 5 V ────┼──> Power mux / protection ───> 5 V_SYS
                      │                                  │
                      │                                  ├──> 3V3_DIG buck ──> STM32H743
                      │                                  │                     │
                      │                                  │                     ├─ SWD / USB
                      │                                  │                     ├─ UARTs
                      │                                  │                     ├─ CAN
                      │                                  │                     ├─ PWM/DShot ×8
                      │                                  │                     ├─ ADC V/I
                      │                                  │                     └─ SDMMC/SPI flash
                      │                                  │
                      │                                  └──> low-noise 3V3_SENSOR LDO
                      │                                                        │
                      │                                                        ├─ IMU (SPI)
                      │                                                        ├─ barometer (SPI/I2C)
                      │                                                        └─ optional mag (I2C)
                      │
Battery / power module ──> external 5 V and analog voltage/current sense

External GNSS + compass ── `GPS1` UART/I2C or `CAN1` ──> STM32
Telemetry / receiver     ── `TELEM1` / `RC_IN` UART/CAN ──> STM32
Raspberry Pi CM5 + carrier ── `COMPANION` UART/CAN ──> STM32; camera/lidar remain CM5-side
Downward rangefinder     ── `LIDAR_FC` UART/I2C/CAN ──> STM32 when low latency is required
STM32 outputs            ── `ESC_OUT` logic only ──> external ESC signal inputs
ESCs and motors          ── high current  ──> remain outside Rev A PCB
~~~

### 5.2 Why a single H743 MCU first?

A single H743 reduces:

- bootloader and firmware coordination;
- inter-processor protocols;
- reset and power sequencing;
- duplicated clocks and decoupling;
- debugging time;
- the number of unverified failure paths.

An optional I/O coprocessor can be added in Rev B if the team needs independent servo/PWM failsafe behavior. Adding a second MCU merely because commercial autopilots have one is not automatically an improvement for a first prototype.

### 5.3 Power architecture

The power system is the highest-risk part of a DIY board because a wiring or component-rating error can destroy the board or create a fire hazard. For Rev A:

1. Prefer an **external, known-good regulated 5 V power module**.
2. Provide a clearly labeled 5 V input and ground.
3. Add reverse-polarity and overvoltage protection appropriate to the actual source.
4. Use a 3.3 V buck for the main logic rail.
5. Use a low-noise 3.3 V LDO or filtered branch for sensors.
6. Add test points for input, 5 V, 3.3 V, sensor 3.3 V, and ground.
7. Do not power motors or ESCs through the flight-controller PCB.

If raw battery input is later required, use a buck regulator with an input rating, transient rating, inductor current rating, thermal design, and layout that all cover the selected battery. A 6S nominal battery can exceed 25 V when fully charged; the exact maximum and transient environment must be calculated before choosing a TVS or regulator.

### 5.4 Sensor layout

- Place the primary IMU near the mechanical center of the PCB.
- Keep the IMU away from switching inductors, high-current traces, crystals, speakers, and vibrating connectors.
- Use the IMU vendor’s land pattern, stencil, reflow, and assembly guidance.
- Route its SPI clock/data over a quiet return path.
- Put the barometer where its pressure port is not blocked; use a vent/opening strategy and protect it from prop wash and direct airflow.
- Put the magnetometer off-board or on a detachable GPS/compass mast.
- Keep battery wires, motor phases, high-current copper, and ferromagnetic hardware away from the compass.

The sensor boundary is intentionally hybrid. The primary IMU and barometer are board-mounted to keep the fastest measurement path local and repeatable. GNSS and compass are external because antenna visibility and magnetic separation matter more than keeping those devices on the FC. A remote high-rate IMU is only a future option if it is implemented as a timestamped smart sensor node with a robust bus such as DroneCAN; it is not a bare IMU connected by an unverified long SPI/I2C cable.

### 5.5 Outputs and actuator boundary

The FC board generates low-voltage logic signals. It does not need to carry motor current. Provide:

- at least four motor/ESC signal channels for the quadrotor;
- four spare timer channels;
- ground adjacent to signal pins;
- optional 5 V servo/receiver supply only if the external power budget is verified;
- series resistors (start with 33–100 ohm footprints) near the MCU or connector;
- a defined logic-high/logic-low behavior during reset;
- a safe output state before firmware enables timers.

The exact output protocol (ordinary PWM, OneShot, DShot, or another protocol) belongs in firmware and must be checked against the selected ESC.

### 5.6 Modular port contract

The FC shall be assembled as a connected system rather than a board with permanently soldered peripheral boards. Use logical, keyed and labeled ports:

| Port | Minimum signal contract | Module |
|---|---|---|
| `POWER1` | Regulated 5 V, GND, scaled battery-voltage sense, protected current-sense input | External ESC/power board |
| `ESC_OUT` | M1–M4 signals with adjacent grounds; optional telemetry/CAN as separately agreed | External ESC board |
| `RC_IN` | Receiver supply, GND, UART RX and optional TX | External receiver |
| `GPS1` | GNSS UART TX/RX, PPS, supply/GND; optional I2C compass | External GNSS/compass |
| `CAN1/CAN2` | CANH, CANL, supply and GND | Remote DroneCAN sensors, lidar, power or ESC nodes |
| `TELEM1` | UART TX/RX/GND, optional CTS/RTS | Ground telemetry radio |
| `COMPANION` | UART TX/RX/GND, optional CTS/RTS | Raspberry Pi CM5 on a separate carrier; separate CM5 power |
| `LIDAR_FC` | UART/I2C/CAN, supply and GND | Downward/simple rangefinder |
| `SWD/DEBUG` | SWDIO, SWCLK, NRST, 3V3 reference, GND and BOOT0 access | Programmer and bring-up |

Raw SPI is a local-board interface, and raw I2C is a short low-speed accessory interface. For remote sensor modules, use UART where the device supports it or use a local sensor MCU/CAN node. This boundary keeps the FC physically modular without placing the inner-loop sensors on an uncontrolled flight harness.

---

## 6. Staged development plan

### Stage 0 — Requirements and feasibility

Deliverables:

- one-page vehicle and electrical requirements;
- pin map;
- power tree;
- interface list;
- selected MCU and sensor part numbers;
- selected PCB stack-up and manufacturer capability;
- safety/test plan.

Gate: no schematic until every external signal and power source has an owner.

### Stage 1 — Minimal custom board

Populate:

- STM32H743;
- one IMU;
- one barometer;
- power rails;
- SWD;
- USB;
- four to eight outputs;
- one telemetry UART;
- ADC voltage/current input;
- LEDs and reset.

Do not add every possible feature to the first spin. A board that boots and measures correctly is more useful than a board with many untested interfaces.

### Stage 2 — Logging and communications

Add and verify:

- microSD or SPI flash;
- CAN transceiver;
- external GNSS/compass connector;
- telemetry connector;
- more output channels;
- optional external sensor connectors.

### Stage 3 — Firmware integration

Options:

- **Minimal custom firmware first:** STM32CubeIDE/HAL or LL, sensor driver, timestamping, filtering, attitude estimator, PWM output, USB telemetry, and logging.
- **PX4 later:** create a board target, bootloader configuration, board ID, pin definitions, drivers, and build/flash process.
- **ArduPilot later:** create the appropriate hardware definition, board target, bootloader path, sensor definitions, and parameter/port configuration.

### Stage 4 — Verification and controlled demonstration

Evidence:

- power-rail measurements;
- clock and reset traces;
- SWD programming log;
- sensor register readout;
- calibration results;
- PWM timing captures;
- USB/CAN/UART communication;
- log files;
- vibration and thermal observations;
- tethered/rig test results.

---

## 7. Preliminary parts list — how to read it

This is a **logical BOM**, not yet a purchase-ready manufacturing BOM. It identifies the functions and candidate manufacturer part numbers. Before ordering:

- lock each exact MPN and package;
- download the current datasheet and land pattern;
- verify component lifecycle and stock;
- assign a footprint from the manufacturer drawing;
- calculate ratings for the actual battery and interfaces;
- run ERC/DRC;
- export a real BOM with quantities, designators, and approved alternates;
- order spare sensors, MCUs, connectors, and small passives.

The quantities below are for **one populated Rev A PCB**, excluding normal assembly spares. For first builds, order approximately 20–30% extra passives and at least one spare of each expensive IC/sensor.

---

## 8. Preliminary BOM — semiconductors and sensors

| Ref. | Candidate MPN / part | Function | Package / assembly note | Qty | Indicative price observed | Example source / technical reference | Selection note |
|---|---|---|---|---:|---:|---|---|
| U1 | **STM32H743VIT6** | Main flight-control MCU | LQFP-100; practical for hand inspection/rework compared with BGA | 1 | About **US$6.48** at one LCSC listing; about **US$16.67** at a DigiKey listing; availability and seller context differ | [ST product page](https://www.st.com/en/microcontrollers-microprocessors/stm32h743zi.html), [ST datasheet](https://www.st.com/resource/en/datasheet/stm32h743zi.pdf), [LCSC example](https://www.lcsc.com/product-detail/Microcontrollers-MCU-MPU-SOC_STMicroelectronics-STM32H743VIT6_C114409.html), [DigiKey example](https://www.digikey.com/en/products/detail/stmicroelectronics/STM32H743VIT6/7809237) | Main recommendation. Verify package suffix, genuine source, Flash/RAM variant, and current stock before ordering |
| U1 alternate | STM32H743ZI / H753 variant | Main MCU alternate | Larger package; pin map changes | 0–1 | N/A — quote/verify | [STM32H7 documentation](https://www.st.com/en/microcontrollers-microprocessors/stm32h7-series/documentation.html) | Select only after a pin-map review |
| U2 | **ICM-42688-P** | Six-axis accelerometer + gyroscope | LGA-14; use vendor land pattern and MEMS assembly guidance | 1 | Distributor/search results around **US$4.67–4.91**; other marketplace pages were much higher | [TDK product page](https://www.invensense.tdk.com/en-us/products/6-axis/icm-42688-p), [datasheet](https://product.tdk.com/system/files/dam/doc/product/sensor/mortion-inertial/imu/data_sheet/ds-000347-icm-42688-p-v1.6.pdf), [PCB/MEMS assembly note](https://invensense.tdk.com/wp-content/uploads/2023/05/an-000393_imu-pcb-design-and-mems-assembly-guidelines.pdf) | Good high-rate primary IMU. Buy from an authorized source where possible |
| U3 optional | ICM-42688-P second footprint | Sensor diversity/redundancy experiment | Same as U2; may use another SPI bus/chip-select | 0–1 | Same uncertainty as U2 | Same as U2 | Do not populate until firmware and placement strategy are defined |
| U2 alternate | **Bosch BMI088** | Six-axis drone/robotics IMU | Compact package; accelerometer and gyro are separate dies in one module | 0–1 | Quote/verify current distributor price | [Bosch BMI088 page](https://www.bosch-sensortec.com/en/products/motion-sensors/imus/bmi088), [datasheet](https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bmi088-ds001.pdf) | Excellent alternate; follow Bosch placement, vibration, and SPI guidance |
| U4 | **BMP390** | Barometric pressure / relative altitude | LGA-10; protect pressure port and avoid prop wash | 1 | Around **US$3.11–3.30** in distributor results | [Bosch BMP390 page](https://www.bosch-sensortec.com/en/products/environmental-sensors/pressure-sensors/bmp390) | Preferred current barometer candidate |
| U4 alternate | DPS368 / equivalent current pressure sensor | Barometer alternate | Package and availability dependent | 0–1 | Quote/verify | Use the current manufacturer datasheet and authorized distributor | Do not start a new design around DPS310 without checking lifecycle; one distributor page labels it discontinued/not recommended for new designs |
| U5 optional | **IST8310** | Three-axis magnetometer | Confirm exact package drawing before footprint creation | 0–1 | About **US$3.19** at one LCSC listing | [LCSC example](https://www.lcsc.com/product-detail/C2683055.html) | Prefer external compass placement for real vehicle use |
| U5 alternate | **MMC5983MA** | High-resolution magnetometer | Small LGA; I2C/SPI; external placement preferred | 0–1 | About **US$2.27** at one LCSC listing | [LCSC example](https://www.lcsc.com/product-detail/Magnetic-Sensors_MEMSIC-MMC5983MA_C404329.html) | Strong alternate; verify magnetic environment before relying on it |
| U6 | **TPS62162DSGT** | 5 V to 3.3 V digital rail | 8-WSON; fixed 3.3 V, 1 A, 3–17 V input | 1 | **US$2.22** quantity one at the current DigiKey listing; lower at volume | [TI part details](https://www.ti.com/product/TPS62162/part-details/TPS62162DSGT), [DigiKey exact listing](https://www.digikey.com/en/products/detail/texas-instruments/TPS62162DSGT/2782703) | Confirm input source, thermal path, inductor, and output capacitance before layout |
| U7 | **LP5907MFX-3.3/NOPB** | Low-noise sensor LDO | SOT-23-5; fixed 3.3 V, 250 mA | 1 | **US$0.66** quantity one at the current DigiKey listing | [TI LP5907](https://www.ti.com/product/LP5907), [DigiKey exact listing](https://www.digikey.com/en/products/detail/texas-instruments/LP5907MFX-3-3-NOPB/3906441) | Use after a 5 V or clean upstream rail; do not feed it raw 6S |
| U8 | **TCAN332GDCNT** (preferred current listing) | CAN physical-layer transceiver | SOT-23-8; 3.3 V; CAN-FD-capable variant | 1 | The GDCNR listing was out of stock; the GDCNT substitute showed about **US$3.72** quantity one | [TI TCAN332](https://www.ti.com/product/TCAN332), [DigiKey GDCNR listing](https://www.digikey.com/en/products/detail/texas-instruments/TCAN332GDCNR/6572320), [LCSC example](https://www.lcsc.com/product-detail/CAN-Transceivers_Texas-Instruments-TCAN332DCNT_C2671325.html) | One CAN bus for Rev A; check pin/package differences before approving the substitute |
| U9 | **TPS2116** | USB 5 V / external 5 V power mux | Small power-path package; verify current/thermal layout | 1 | Quote/verify | [TI TPS2116](https://www.ti.com/product/TPS2116) | It is a low-voltage power mux, not a raw-battery regulator |
| U10 | **TPD4EUSB30DQAR** or suitable USB ESD array | USB D+/D− and connector ESD | 10-USON; four-channel USB protection | 1 | About **US$1.52** quantity one at the current DigiKey filter result | [TI USB ESD datasheet](https://www.ti.com/lit/ds/symlink/tpd4eusb30.pdf), [DigiKey search/result](https://www.digikey.com/en/products/filter/transient-voltage-suppressors-tvs/tvs-diodes/144) | Choose a device with appropriate capacitance and USB speed rating |
| U11 | **W25Q128JVSIQ-TR** | Optional SPI NOR flash for parameters/logging | 8-SOIC; 128 Mbit, 2.7–3.6 V | 1 | About **US$3.94** quantity one at the current DigiKey listing; one LCSC listing showed a lower marketplace price | [Winbond/DigiKey exact listing](https://www.digikey.com/en/products/detail/winbond-electronics/W25Q128JVSIQ-TR/5803944), [LCSC example](https://www.lcsc.com/product-detail/C97521.html) | Optional if microSD logging is sufficient; verify genuine source and constrained-supply status |
| U12 | **M24C64-RMN6TP** | Optional I2C EEPROM | SOIC-8 | 1 | About **US$0.60** at one LCSC listing | [LCSC example](https://www.lcsc.com/product-detail/C222104.html) | Optional; avoid duplicating storage without a use case |
| U13 optional | **STM32G0B1CET6** | Optional I/O/failsafe coprocessor | LQFP/QFN variant; choose package deliberately | 0–1 | Quote/verify | [STM32G0 family](https://www.st.com/en/microcontrollers-microprocessors/stm32g0-series.html) | Prefer this family for a new coprocessor over obsolete F103 |
| U13 legacy alternate | STM32F103C8T6 | Historical I/O coprocessor | LQFP-48 | 0–1 | About **US$1.73** at one LCSC listing; about **US$8.24** at one DigiKey listing with supply uncertainty | [LCSC example](https://www.lcsc.com/product-detail/C8734.html), [DigiKey example](https://www.digikey.com/en/products/detail/stmicroelectronics/STM32F103C8T6/1646338) | Familiar but old; do not add just because it is cheap |
| U14 optional | **TPS386000** | Multi-rail supervisor/watchdog | VQFN; Rev B feature | 0–1 | Quote/verify | [TI TPS386000](https://www.ti.com/product/TPS386000) | Use the H743 watchdog first; add only after the basic board works |
| U15 optional | INA230 / INA226 | Digital current/voltage monitor | Package and shunt design dependent | 0–1 | Quote/verify | Use current TI datasheet and distributor listing | Power module analog V/I is simpler for Rev A |
| Q1/Q2 | Reverse-polarity MOSFET or ideal-diode stage | Input protection | Choose voltage/current-rated FETs | 1–2 | Quote/verify | Select from current distributor based on actual battery | Do not choose a FET by voltage rating alone; check RDS(on), surge, heat, and body-diode direction |
| D1 | SMBJ33A or correctly sized TVS | Input transient protection | SMB; voltage depends on actual input | 1 | Around **US$0.45** in one distributor example | [DigiKey example](https://www.digikey.com/en/products/detail/littelfuse-inc/SMBJ33A/286006), [LCSC example](https://www.lcsc.com/product-detail/C320242.html) | **Not a blind recommendation.** Recalculate standoff/clamp for the final 2S–6S input and regulator |
| D2+ | USB/CAN/connector ESD arrays | Interface protection | Package depends on line count | As needed | Quote/verify | Use manufacturer application notes | Add where cable exposure warrants it; do not load high-speed lines with unsuitable capacitance |

### 8.1 Main MCU support parts

| Function | Preliminary choice | Quantity guidance | Notes |
|---|---|---:|---|
| MCU VDD decoupling | 100 nF X7R, 0402/0603, 10–16 V | One per relevant VDD supply pin; commonly 8–12 total | Exact count comes from the selected package pinout and datasheet |
| MCU bulk decoupling | 4.7 µF or 10 µF X7R, 0603/0805 | 2–3 | Place close to power-entry clusters |
| VCAP | 2.2 µF low-ESR capacitor, per H743 datasheet | 1 or exact datasheet requirement | Do not substitute a random value |
| VDDA/VREF | 100 nF + 1 µF, optionally ferrite-filtered | 1 set | Keep analog supply clean |
| HSE crystal | 8/16/25 MHz candidate chosen for firmware/USB plan | 1 | The frequency and load capacitance must match the selected design |
| HSE load capacitors | C0G/NP0, value from crystal CL calculation | 2 | Use short symmetrical traces |
| LSE crystal | 32.768 kHz, optional | 1 | Useful for RTC/timekeeping; not essential for the first control loop |
| LSE load capacitors | C0G/NP0 | 2 | Optional |
| BOOT0 pulldown | 10 kΩ | 1 | Add a jumper/test pad for recovery |
| NRST pull-up | 10 kΩ | 1 | Add a reset switch and debug access |
| NRST capacitor | 100 nF, if supported by the reset design | 1 | Follow ST guidance; do not create an excessively slow reset |
| SWD connector | 1×5 or 2×5, 1.27 mm, or Tag-Connect/test pads | 1 | SWDIO, SWCLK, NRST, 3V3, GND; optional SWO |
| Status LEDs | Green/red/blue LEDs | 3 | Use visible status codes |
| LED resistors | 1 kΩ–2.2 kΩ | 3 | Verify MCU sink/source current |
| Buzzer driver | BSS138/2N7002, 100 Ω gate resistor, 100 kΩ pulldown | 1 set | Optional; use a connector for external buzzer |

---

## 9. Preliminary BOM — power, protection, passives, and connectors

### 9.1 Power and protection

| Ref. | Part/function | Preliminary value or rule | Qty | Notes |
|---|---|---|---:|---|
| F1 | Input fuse or resettable fuse | Rated for the external 5 V source and expected fault current | 1 | For raw battery, calculate fault energy; a small PTC is not automatically enough |
| J1 | External regulated 5 V input | Keyed connector, ground adjacent to 5 V | 1 | Label polarity and maximum input |
| D1 | Input TVS | Select standoff and clamp after actual battery/source calculation | 1 | SMBJ33A is only an example; do not copy its value blindly |
| Q1/Q2 | Reverse-polarity protection | PFET/NFET/ideal-diode circuit | 1–2 | Add only after a real current/thermal calculation |
| C1 | Bulk input capacitor | 47–100 µF, 10–35 V as applicable | 1–2 | Voltage rating must exceed the real source/transients |
| C2 | Ceramic input capacitor | 1 µF–10 µF | 1–2 | Follow regulator layout guidance |
| L1 | 3.3 V buck inductor | Exact value and saturation/current rating from U6 datasheet | 1 | Do not choose by nominal inductance only |
| C3/C4 | Buck input/output capacitors | Exact value/ESR from U6 datasheet | 2–4 | Place in the recommended loop geometry |
| FB1 | Sensor-rail ferrite bead | Select impedance/current for 3.3 V sensor branch | 1 | Avoid excessive DC resistance |
| C5/C6 | Sensor-rail bulk/decoupling | 1 µF + 100 nF per sensor/reference design | 2+ | Use sensor manufacturer values |
| U9 | Power mux | TPS2116 or selected equivalent | 1 | USB 5 V and external 5 V only; not raw battery |
| D_USB | USB ESD | TPD4EUSB30 or suitable array | 1 | Keep near connector and return to ground correctly |

### 9.2 Interface passives

| Function | Initial value / quantity | Engineering reason |
|---|---|---|
| PWM/DShot output series resistors | 33–100 Ω × 8 footprints | Reduces ringing/EMI; tune or populate after scope review |
| I2C pull-ups | 2.2 kΩ–4.7 kΩ on SDA/SCL | Final value depends on bus speed, capacitance, and whether external devices already have pull-ups |
| CAN termination | 120 Ω plus jumper/switch | Terminate only when the node is at the end of the bus |
| Split CAN termination | 60 Ω + 60 Ω + optional 4.7 nF to ground | Optional topology; use only if compatible with the network |
| USB-C CC resistors | 5.1 kΩ from CC1/CC2 to ground for a USB device | Required for correct device-role advertisement |
| USB D+/D− series resistors | 22 Ω footprints if ST design recommends them | Populate only according to the selected USB design/reference |
| SDMMC series resistors | 22–33 Ω optional on clock/CMD/DATA | Tune for ringing and trace length |
| UART protection | ESD or 22–100 Ω series where cable exposure requires | Avoid unnecessary capacitance on high-speed lines |
| ADC voltage divider | Example 100 kΩ / 20 kΩ plus 1 kΩ + 100 nF filter | Must be recalculated for the maximum voltage and ADC range |
| ADC current filter | Example 1 kΩ + 100 nF | Filters the power module’s analog current signal |
| Test points | 5 V, 3V3, 3V3_SENSOR, GND, SWD, USB, IMU SPI, CAN | Make measurements possible without probing tiny pads |

### 9.3 Storage and connectors

| Function | Preliminary part/style | Qty | Notes |
|---|---|---:|---|
| microSD socket | Push-push or hinged 3.3 V socket | 1 | Keep the card away from high vibration and provide ESD/decoupling |
| GNSS/compass | JST GH 1.25 mm or a keyed connector | 1 | Put compass on a remote module if possible |
| Telemetry UART | JST GH 1.25 mm or equivalent | 1 | Include signal ground and defined voltage |
| CAN | Keyed two/three/four-pin connector | 1 | Include CANH, CANL, ground; power only if the system requires it |
| Receiver | UART/CRSF/S.BUS connector as required | 1 | Do not assume all receiver voltage levels are 3.3 V-safe |
| Motor outputs | 1×8/1×10 header or keyed harness | 1 | Put ground beside signal where possible |
| USB-C | GCT USB4105-GF-A or equivalent | 1 | Example page indicates roughly US$0.80 class; verify current stock |
| M2/M3 mounting hardware | Nonmagnetic hardware near magnetometer | 4+ | Keep mounting holes and keepouts in the mechanical drawing |
| JST GH example | SM04B-GHS-TB-LF-SN | As needed | [LCSC example](https://www.lcsc.com/product-detail/Wire-To-Board-Wire-To-Wire-Connector_JST-Sales-America_SM04B-GHS-TB-LF-SN_JST-Sales-America-SM04B-GHS-TB-LF-SN_C189895.html) |
| USB-C example | USB4105-GF-A | 1 | [DigiKey example](https://www.digikey.com/en/products/detail/gct/USB4105-GF-A/11198441) |

### 9.4 Passive value matrix for purchasing

The final quantity is generated from the schematic. The matrix below is a sensible first-order purchase list for one or a few boards, with spares:

| Passive | Package | Suggested stock for prototype batch | Typical unit/pack range | Use |
|---|---|---:|---:|---|
| 0 Ω | 0603 | 20–50 | US$0.005–0.05 | Configuration links, power isolation, debug options |
| 22 Ω | 0603 | 20–50 | US$0.005–0.05 | USB/SD/series damping options |
| 33 Ω | 0603 | 20–50 | US$0.005–0.05 | PWM/SD series options |
| 47 Ω | 0603 | 20–50 | US$0.005–0.05 | Signal damping options |
| 100 Ω | 0603 | 20–50 | US$0.005–0.05 | Gate/signal resistors |
| 1 kΩ | 0603 | 50–100 | US$0.005–0.05 | LED/current filters |
| 2.2 kΩ | 0603 | 20–50 | US$0.005–0.05 | I2C pull-up or gate networks |
| 4.7 kΩ | 0603 | 20–50 | US$0.005–0.05 | I2C/pull-up options |
| 10 kΩ | 0603 | 50–100 | US$0.005–0.05 | BOOT0, NRST, biasing |
| 20 kΩ | 0603 | 20–50 | US$0.005–0.05 | ADC divider example; recalculate |
| 100 kΩ | 0603 | 20–50 | US$0.005–0.05 | ADC/filter/gate pull-down |
| 100 nF | 0603 X7R | 100–200 | US$0.01–0.05 | MCU/sensor decoupling |
| 1 µF | 0603 X7R | 20–50 | US$0.02–0.08 | Rail/sensor decoupling |
| 2.2 µF | 0603/0805 X7R | 10–30 | US$0.03–0.15 | VCAP/rail decoupling; verify dielectric/rating |
| 4.7 µF | 0603/0805 X7R | 20–50 | US$0.05–0.20 | MCU/regulator bulk |
| 10 µF | 0805/1206 X7R | 20–50 | US$0.05–0.25 | Power rail bulk |
| 47–100 µF | 1210/polymer/electrolytic | 2–6 | US$0.20–2.00 | Input bulk; voltage rating dominates |
| Crystal load caps | 0603 C0G | 10–20 | US$0.02–0.10 | HSE/LSE clock |
| Ferrite bead | 0603 | 5–20 | US$0.05–0.50 | Sensor rail / USB power filtering |
| 120 Ω | 0603 | 5–10 | US$0.005–0.05 | CAN termination |
| 60 Ω | 0603 | 5–10 | US$0.005–0.05 | Split termination option |

For the first hand-assembled board, **0603** is a reasonable compromise between density and reworkability. Use 0402 only where the selected sensor/reference design or space constraint requires it. Tiny LGA sensors are the main assembly risk; plan for stencil, controlled hot-air/reflow, magnification, and inspection.

### 9.5 Purchase entry points for generic SMD parts

Generic passives should be locked by exact MPN after the schematic and voltage/current calculations are complete. These are live distributor search links rather than claims that one particular search result is approved:

| Part group | LCSC search | DigiKey search | Approval rule |
|---|---|---|---|
| 0603 10 kΩ resistors | [LCSC search](https://www.lcsc.com/search?q=0603%2010k%20resistor) | [DigiKey search](https://www.digikey.com/en/products/result?keywords=0603%2010k%20resistor) | Select tolerance/power rating and a current, traceable MPN |
| 0603 100 nF X7R capacitors | [LCSC search](https://www.lcsc.com/search?q=0603%20100nF%20X7R%2016V) | [DigiKey search](https://www.digikey.com/en/products/result?keywords=0603%20100nF%20X7R%2016V) | Check DC-bias derating, voltage, dielectric, and package |
| 0805 10 µF X7R capacitors | [LCSC search](https://www.lcsc.com/search?q=0805%2010uF%20X7R%2016V) | [DigiKey search](https://www.digikey.com/en/products/result?keywords=0805%2010uF%20X7R%2016V) | Check effective capacitance under rail voltage |
| 0603 ferrite beads | [LCSC search](https://www.lcsc.com/search?q=0603%20ferrite%20bead%20600%20ohm) | [DigiKey search](https://www.digikey.com/en/products/result?keywords=0603%20ferrite%20bead%20600%20ohm) | Check rated current and DC resistance |
| 0603 0 Ω links | [LCSC search](https://www.lcsc.com/search?q=0603%200%20ohm%20resistor) | [DigiKey search](https://www.digikey.com/en/products/result?keywords=0603%200%20ohm%20resistor) | Use as configuration links, not as a substitute for a fuse |
| 120 Ω CAN termination | [LCSC search](https://www.lcsc.com/search?q=0603%20120%20ohm%20resistor) | [DigiKey search](https://www.digikey.com/en/products/result?keywords=0603%20120%20ohm%20resistor) | Use a precision resistor and a jumper/switch if termination is selectable |
| C0G crystal capacitors | [LCSC search](https://www.lcsc.com/search?q=0603%20C0G%20capacitor) | [DigiKey search](https://www.digikey.com/en/products/result?keywords=0603%20C0G%20capacitor) | Calculate from the selected crystal load capacitance |

For the final manufacturing BOM, replace every search link with the exact distributor SKU, manufacturer part number, package, approved alternate, stock state, and date checked.

### 9.6 Exact orderable examples from the current spot check

The following entries turn the value matrix into an initial purchasing list. They are **candidate parts**, not automatic approvals. The prices and stock states were observed during the 26 August 2026 research pass and can change.

| Function | Candidate exact MPN | Package / rating | Observed low-quantity price and state | Purchase / datasheet link | Important caveat |
|---|---|---|---|---|---|
| 3.3 V buck | TPS62162DSGT | 8-WSON, fixed 3.3 V, 1 A, 3–17 V input | US$2.22, 5,666 in stock in the observed DigiKey listing | [DigiKey](https://www.digikey.com/en/products/detail/texas-instruments/TPS62162DSGT/2782703) | TI datasheet recommends a specific power-loop layout, inductor, and approximately 22 µF output capacitance |
| Buck inductor candidate | 744029003 | Shielded 3.3 µH-class substitute for the TI-recommended family | US$1.53, 5,823 in stock in the observed substitute listing | [DigiKey search/result](https://www.digikey.com/en/products/detail/wurth-elektronik/744029003/7321088) | Validate saturation/current/footprint against the final TPS62162 operating point |
| Buck inductor alternate | SPM3012T-3R3M-LR | Shielded 3.3 µH-class alternate | US$1.06, 264 in stock in the observed substitute listing | [DigiKey search/result](https://www.digikey.com/en/products/detail/tdk-corporation/SPM3012T-3R3M-LR/445174444) | This is an alternate, not a drop-in approval; compare DCR, Isat, dimensions, and land pattern |
| Sensor LDO | LP5907MFX-3.3/NOPB | SOT-23-5, 3.3 V, 250 mA | US$0.66, active and 199,263 in stock in the observed DigiKey listing | [DigiKey](https://www.digikey.com/en/products/detail/texas-instruments/LP5907MFX-3-3-NOPB/3906441) | The 5.5 V maximum input requires a clean 5 V or lower upstream rail |
| CAN transceiver | TCAN332GDCNT | SOT-23-8, 3.0–3.6 V | About US$3.72 for the observed available substitute; GDCNR was out of stock | [DigiKey GDCNR page](https://www.digikey.com/en/products/detail/texas-instruments/TCAN332GDCNR/6572320) | Confirm whether the chosen package/variant is CAN-FD and verify pin compatibility |
| USB ESD | TPD4EUSB30DQAR | 10-USON, four-channel | About US$1.52 in the observed DigiKey filter result; 141,096 in stock | [DigiKey TVS/ESD result](https://www.digikey.com/en/products/filter/transient-voltage-suppressors-tvs/tvs-diodes/144) | Select the exact product from the filter and verify capacitance/USB suitability |
| SPI flash | W25Q128JVSIQ-TR | 8-SOIC, 128 Mbit, 2.7–3.6 V | US$3.94 quantity one, 77,997 in stock; maximum purchase limit noted | [DigiKey](https://www.digikey.com/en/products/detail/winbond-electronics/W25Q128JVSIQ-TR/5803944) | DigiKey noted temporary constrained supply; keep microSD as an alternate |
| 100 nF decoupler | GRM188R72A104KA35D | 0603, 100 nF, 100 V, X7R | US$0.15, more than 2.5 million in stock in the observed substitute listing | [DigiKey substitute/result](https://www.digikey.com/en/products/detail/murata-electronics/GRM188R72A104KA35D/4903285) | The earlier 16 V Murata example was marked obsolete; 100 V is electrically conservative but not necessarily the smallest/cheapest choice |
| 4.7 µF rail capacitor | GRM21BR71C475KE51L | 0805, 4.7 µF, 16 V, X7R | US$0.12, 1,588 in stock in the observed listing | [DigiKey](https://www.digikey.com/en/products/detail/murata-electronics/GRM21BR71C475KE51L/6606095) | Check DC-bias derating and effective capacitance; the similar KA73L example was obsolete |
| 10 µF rail capacitor | GRM21BR61C106KE15L | 0805, 10 µF, 16 V, X5R | About US$0.12, active, with large observed stock | [DigiKey](https://www.digikey.com/en/products/detail/murata-electronics/GRM21BR61C106KE15L/965900) | Use only on rails whose maximum voltage and bias derating are appropriate |
| 10 kΩ bias resistor | RC0603FR-0710KL | 0603, 10 kΩ, 1%, 0.1 W | US$0.10 quantity one; US$0.025 at quantity ten; more than 2 million in stock | [DigiKey](https://www.digikey.com/en/products/detail/yageo/RC0603FR-0710KL/729827) | Use the same Yageo RC0603FR-07 family for 1 kΩ, 2.2 kΩ, 4.7 kΩ, 20 kΩ, and 100 kΩ after checking each exact suffix |
| Sensor-rail ferrite | BLM18AG601SN1D | 0603, 600 Ω at 100 MHz, 500 mA maximum | US$0.10 quantity one; more than 1.7 million in the observed listing | [DigiKey](https://www.digikey.com/en/products/detail/murata-electronics/BLM18AG601SN1D/584225) | Verify DC resistance and rail current; do not place it in a path that exceeds its rating |
| HSE crystal candidate | ABM3B-8.000MHZ-B2-T | 5 × 3.2 mm, 8 MHz, 18 pF, ±20 ppm | US$0.69 quantity one; 73,483 in stock in the observed listing | [DigiKey](https://www.digikey.com/en/products/detail/abracon-llc/ABM3B-8-000MHZ-B2-T/1873166) | Confirm H743 clock configuration, crystal load capacitance, drive level, and USB/firmware plan |
| Buzzer/LED driver MOSFET | 2N7002K-7-W | SOT-23, 60 V, 380 mA class | US$0.24 quantity one in the observed listing | [DigiKey](https://www.digikey.com/en/products/detail/diodes-incorporated/2N7002K-7-W/27803631) | Suitable as a small signal/buzzer driver, not as a motor or battery switch |
| Input TVS candidate | SMBJ33A family | SMB, 33 V reverse standoff, 600 W class | Equivalent listings around US$0.45–0.63; original Littelfuse listing out of stock | [DigiKey](https://www.digikey.com/en/products/detail/littelfuse-inc/SMBJ33A/286006) | **Do not approve without calculating the actual source maximum and required clamp voltage**; 33 V is not automatically right for every 6S input architecture |
| USB-C receptacle | USB4105-GF-A | USB 2.0 Type-C, right-angle SMT plus through-hole retention | US$0.80 quantity one; more than 153,000 in stock in the observed listing | [DigiKey](https://www.digikey.com/en/products/detail/gct-emea-ltd/USB4105-GF-A/11198509) | Confirm mechanical outline and place ESD/CC resistors close to the connector |
| JST-style external connector | SM04B-GHS-TB-LF-SN | 1.25 mm, keyed family connector | Quote/verify current local price | [LCSC example](https://www.lcsc.com/product-detail/Wire-To-Board-Wire-To-Wire-Connector_JST-Sales-America_SM04B-GHS-TB-LF-SN_JST-Sales-America-SM04B-GHS-TB-LF-SN_C189895.html) | Verify mating housing, pin count, current rating, and exact footprint |
| microSD socket | 1040310811 | Molex 104031 series, right-angle SMT, switch | US$2.04 quantity one; 22,387 in stock in the observed direct-substitute listing | [DigiKey](https://www.digikey.com/en/products/detail/molex/1040310811/9694134) | The closely related 1040310831 listing was obsolete; verify the socket, card-detect switch, and footprint |
| Green status LED | LTST-C190KGKT | 0603, green, clear lens | US$0.15 quantity one; more than 1.8 million in stock in the observed listing | [DigiKey](https://www.digikey.com/en/products/detail/lite-on-inc/LTST-C190KGKT/386815) | Use an appropriate series resistor and keep LED current within the H743 GPIO limits |
| Red status LED | LTST-C191KRKT | 0603, red, clear lens | About US$0.15 quantity one in the observed DigiKey LED listing | [DigiKey LED search](https://www.digikey.com/en/products/filter/led-indication-discrete/lite-on-inc/105) | Confirm the exact red part number and forward voltage before finalizing the resistor |
| Reset pushbutton | B3U-1000P | SMD top-actuated SPST-NO, 3.0 × 2.5 mm | US$1.17 quantity one; 42,102 in stock in the observed listing | [DigiKey](https://www.digikey.com/en/products/detail/omron-electronics-inc-emc-div/B3U-1000P/1859107) | Optional if BOOT0/SWD test pads are sufficient, but useful for bring-up |

The exact examples above deliberately include several “verify” gates. The component should not move from candidate to **approved for fabrication** until its datasheet, package, voltage/current rating, lifecycle, and actual supplier stock have been checked against the final schematic.

### 9.7 Provisional Rev A assembly quantities

This is the quantity skeleton to use when turning the logical design into a KiCad BOM. It assumes one STM32H743VIT6, one populated IMU, one BMP390, one CAN bus, one USB-C port, one microSD socket, one optional SPI flash, eight output channels, three status LEDs, and an external regulated 5 V input.

| Group | Provisional populated quantity | Design rule |
|---|---:|---|
| STM32H743VIT6 | 1 | Add one spare for assembly risk |
| Primary IMU | 1 | Add one spare; second footprint may remain DNP |
| BMP390 | 1 | Add one spare |
| 3.3 V buck | 1 | Add one spare if the first board is hand-built |
| Sensor LDO | 1 | Add one spare |
| CAN transceiver | 1 | Add one if CAN is in Rev A |
| USB ESD array | 1 | Add one if USB is in Rev A |
| SPI flash | 0 or 1 | DNP if microSD is the only logging path |
| EEPROM | 0 or 1 | DNP unless a defined parameter/calibration use exists |
| 100 nF local decouplers | Approximately 12–16 | One at every MCU/sensor/regulator IC supply cluster; final count follows datasheets and package pins |
| 1 µF rail/sensor capacitors | Approximately 3–5 | Regulator input/output and sensor reference requirements |
| 2.2 µF VCAP capacitor | 1 | Exact H743 datasheet requirement |
| 4.7 µF bulk capacitors | Approximately 3–5 | MCU/power/sensor rail; check effective capacitance |
| 10 µF bulk capacitors | Approximately 3–6 | Power input and 3.3 V branches; check DC-bias derating |
| 22 µF buck output capacitor | 1–2 | Use the final TPS62162 datasheet/reference design; do not rely on the generic 10 µF placeholder alone |
| 47–100 µF input bulk capacitor | 1–2 | Choose voltage rating for the actual external 5 V or raw-battery architecture |
| Ferrite beads | 1–3 | Sensor rail, VDDA, and optional USB/power filtering |
| 0 Ω links | 4–10 | Rail isolation, optional bus paths, and debug configuration |
| 1 kΩ LED/filter resistors | 3–5 | Three LEDs plus optional RC/filter paths |
| 2.2 kΩ resistors | 0–4 | I2C pull-ups or optional bias networks |
| 4.7 kΩ resistors | 2–6 | I2C pull-ups, bus bias, or expansion |
| 5.1 kΩ resistors | 2 | USB-C CC1/CC2 device pull-downs |
| 10 kΩ resistors | 3–8 | BOOT0, NRST, enable/bias, and optional failsafe inputs |
| 20 kΩ resistors | 1 | Example lower leg of battery/5 V ADC divider; recalculate |
| 100 kΩ resistors | 1–4 | Example upper ADC leg and pulldowns; recalculate |
| 22 Ω USB resistors | 0–2 | Optional; populate only if the selected STM32 USB design calls for them |
| 33–100 Ω output resistors | 8 | One per PWM/DShot signal, initially DNP or populated after signal review |
| CAN termination resistors | 1 × 120 Ω, optional split network | Make selectable if the board may be at an end or in the middle of the bus |
| HSE crystal + load capacitors | 1 + 2 | Exact capacitance from the selected crystal and H743 oscillator design |
| LSE crystal + load capacitors | 0–1 + 0–2 | Optional for Rev A |
| LEDs | 3 | Green/red/blue or project-selected colors |
| Reset switch | 1 | Add only if the mechanical layout permits |
| Buzzer MOSFET + gate parts | 0–1 set | Optional external buzzer driver |
| USB-C connector | 1 | Add mechanical clearance/retention |
| SWD connector/test pads | 1 | Do not omit, even if test pads are used instead of a header |
| microSD socket | 0–1 | DNP only if SPI flash is the selected logging path |
| External GNSS/compass connector | 1 | Keyed; compass should normally be physically remote |
| Telemetry/receiver connectors | 2–3 | Exact count follows the team’s radio architecture |
| CAN connector | 1 | Keyed and ground-referenced |
| Motor-output connector | 1 | Eight signal channels with adjacent grounds where possible |
| Mounting holes/test points | 4+ / 10+ | Mechanical and electrical verification features, not optional decoration |

The final BOM generator must replace “approximately” with actual designators and exact quantities. The table is intended to prevent the team from forgetting small but essential items such as USB CC resistors, VCAP, BOOT0, SWD, sensor decoupling, output series links, test points, and connector grounds.

---

## 10. Pricing and procurement view

### 10.1 How to interpret the prices

- Prices below are indicative observations on or around **26 August 2026**.
- They are generally quantity-one or low-quantity web prices.
- They exclude shipping, tax, customs, marketplace markup, minimum-order charges, and exchange-rate movement.
- LCSC, DigiKey, Mouser, and local Malaysian distributor prices can differ significantly.
- A live product page can change without notice; use the linked page to re-check the exact MPN and package before purchase.
- Where a reliable current price was not visible, the table says **N/A — quote/verify** rather than inventing one.
- For budgeting, use approximately **RM 4.04 per US$1** as an indicative USD/MYR conversion observed from the [Bank Negara Malaysia exchange-rate page](https://financialmarkets.bnm.gov.my/data-download-exchange-rates); use the actual bank/card rate at purchase.

### 10.2 Indicative electronics cost

| Cost group | Indicative USD | Indicative MYR | What it includes |
|---|---:|---:|---|
| H743 + primary IMU + BMP390 + power ICs + CAN/USB parts | 25–55 | 100–222 | Depends heavily on distributor and sensor source |
| Connectors, passives, protection, storage | 15–35 | 61–141 | Small-order shipping can exceed the component subtotal |
| One custom PCB run | 10–50+ | 40–202+ | Layer count, board size, finish, shipping, and quantity |
| Stencil / assembly aids | 3–20+ | 12–81+ | Frameless stencil is useful even for hand assembly |
| One populated Rev A prototype, excluding ESC/motors/GNSS/radio | **50–120+** | **202–485+** | Conservative range; treat as a planning budget, not a quote |
| Three-board batch with spares | **120–300+** | **485–1,212+** | More realistic once shipping and failed parts are included |

### 10.3 Fabrication and stencil references

| Item | Public reference | Planning value |
|---|---|---|
| JLCPCB PCB assembly | [JLCPCB PCBA price page](https://jlcpcb.com/help/article/pcb-assembly-price) | Public page lists setup, stencil, joint, and labor items; use the uploaded design for a real quote |
| JLCPCB stencil | [JLCPCB stencil page](https://jlcpcb.com/pcb-stencil) | Frameless stencil starts around the low-US$3 range depending size/spec |
| Basic PCB run | [JLCPCB ordering guide](https://jlcpcb.com/help/article/how-do-i-place-an-order) | Two-layer small boards can be very cheap; four/six-layer pricing requires an actual quote |
| PCBWay | [PCBWay online calculator](https://www.pcbway.com/HighQualityOrderOnline.aspx?h=1) | Upload Gerbers for the actual layer/finish/quantity quote |

The lecturer mentioned hand assembly and SMD soldering. A practical compromise is:

1. use a stencil and solder paste;
2. place components with tweezers;
3. reflow on an approved hot plate/reflow method or use controlled hot air;
4. inspect every solder joint under magnification;
5. hand-solder connectors, large capacitors, and through-hole test headers;
6. use an external assembly house for a second revision if the team needs repeatability.

### 10.4 Tools and test equipment

| Tool | Example | Indicative local/reference price | Priority |
|---|---|---:|---|
| SWD debugger | ST-LINK/V3SET | About **RM172** in a DigiKey Malaysia listing | Essential |
| Soldering iron | 60 W class | About **RM29** in a Cytron example listing | Essential, but tip quality matters |
| Solder paste | Small syringe/tub | About **RM11.90** in a Cytron example listing | Useful for stencil/rework |
| Multimeter | Basic digital meter | About **RM39–65** in Cytron examples | Essential |
| Helping hands | PCB holder | About **RM22.90** in Cytron examples | Useful |
| Hot-air tool | Small hot-air gun/rework tool | About **RM27.50** in a basic listing | Check temperature control; a proper rework station is safer |
| Oscilloscope | University lab scope | N/A | Strongly recommended for clocks, PWM, power transients |
| Logic analyzer | Saleae Logic 8 class | Saleae page lists around **US$499**; low-cost clones exist but have different trustworthiness | Useful, not essential if lab scope is available |
| Spectrum analyzer | Borrow/department lab | Malaysia listings show several thousand RM for Rigol units | Do not purchase for Rev A; use university equipment |

---

## 11. Open-source hardware and firmware resources

### 11.1 Highest-value repositories

| Resource | What it provides | How to use it safely |
|---|---|---|
| [Pixhawk Hardware repository](https://github.com/pixhawk/Hardware) | Open autopilot hardware designs, schematics, pin maps, BOMs, and reference layouts | Study architecture and license. Do not call an independently designed board “Pixhawk” without the required permission; describe it as Pixhawk-compatible only if it actually follows the relevant standard |
| [Pixhawk Standards](https://github.com/pixhawk/Pixhawk-Standards) | Mechanical/electrical connector and bus standards such as DS-009, DS-010, DS-012, and DS-018 | Use the standard as an interface reference, then create an original schematic and layout |
| [PX4 Autopilot](https://github.com/PX4/PX4-Autopilot) | Open flight-control firmware | Read board-support structure, drivers, build targets, and licensing before porting |
| [PX4 hardware reference design](https://github.com/PX4/PX4-Devguide/blob/master/en/hardware/reference_design.md) | Reference-design explanation and historical Pixhawk context | Use to understand the FMU/IO split and reference-design process |
| [PX4 porting guide](https://docs.px4.io/main/en/hardware/porting_guide) | Board support, NuttX, drivers, and porting cost | Treat porting as a real software work package, not a pin-name edit |
| [PX4 manufacturer board support guide](https://docs.px4.io/main/en/hardware/board_support_guide) | Own firmware target and bootloader expectations | A new board should have its own target even if it resembles another board |
| [ArduPilot](https://github.com/ArduPilot/ardupilot) | Open autopilot firmware for multiple vehicle types | Read licensing and board-port requirements |
| [ArduPilot Schematics](https://github.com/ArduPilot/Schematics) | Schematics for common autopilot hardware | Useful for power, connector, and sensor comparisons; check each folder’s license |
| [ArduPilot OEM/custom hardware guide](https://ardupilot.org/dev/docs/common-oem-customizations.html) | Custom hardware definitions and porting context | Use the board hardware-definition route and bootloader documentation rather than copying a commercial target |
| [ArduPilot ChibiOS hardware definitions](https://github.com/ArduPilot/ardupilot/tree/master/libraries/AP_HAL_ChibiOS/hwdef) | Board pin/peripheral definitions | Compare how MCU pins map to firmware functions |

### 11.2 Closest open designs to the proposed board

| Design | Why it matters | Recommended use |
|---|---|---|
| [LEVIA-H7](https://github.com/piecol/LEVIA-H7) | Open KiCad STM32H743 FC; six layers; eight motor outputs; dual ICM-42688-P; DPS368; IST8310; microSD; CAN; USB-C ESD; separate regulator rails; up to 6S; complete CAD/BOM/manufacturing files; CERN-OHL-S-2.0 | **Best architecture study** for this project. Inspect every sheet, but do not assume its validation or license permits a direct copy |
| [Shirley-FC-Dev-Board](https://github.com/Bare-Metal-Foundry/Shirley-FC-Dev-Board) | Community STM32H7 FC with multiple sensors and Pixhawk-style interfaces | Layout/review reference; verify files and license |
| [pixeagle](https://github.com/mkeyno/pixeagle) | STM32H743VIT6, BMI088, ICM-42688-P, BMP388/BMP390, IST8310 | Compare sensor redundancy and bus arrangement |
| [FPV Flight Controller PCB](https://github.com/fpv-chicken-nugget/FPV-Flight-Controller-PCB) | STM32 FC/PDB, IMU, INA230 current sense, OSD, PWM outputs, power architecture | Study power and signal partitioning; FPV assumptions differ |
| [STM32H743 Betaflight devboard](https://github.com/DpooL2000/STM32h743-devboard-betaflight) | Four-layer STM32H743 board and firmware target | Useful for MCU support, target configuration, and practical board iteration |
| [FPV-Drone-STM32F411 DroneController](https://github.com/FPV-Drone-STM32F411/DroneController) | Custom STM32F411 FC/PDB boards with KiCad and firmware | Simpler historical reference; not a performance target |
| [Kestrel](https://ahmedbadwy.com/projects/proj-kestrel) | Open FMUv6C-compatible H743 board with a smaller processor and generated design | Good example of a more ambitious custom architecture; too large for first Rev A |
| [HADES open-source flight-control system](https://www.pcbway.com/project/shareproject/HADES_Open_Source_Flight_Control_System.html) | STM32/FreeRTOS fixed-wing controller project | Compare fixed-wing assumptions and project documentation |
| [Berkeley HOPE drone controller](https://sites.google.com/berkeley.edu/hope-sp24/drone-controller) | Student custom STM32 controller project | Useful educational process reference |
| [Ethan Suttor custom drone FC project](https://ethansuttor.com/projects/custom-drone-flight-controller) | Practical write-up including BMI270, TPS5450, and KiCad | Use for design narrative and bring-up lessons |

### 11.3 License and naming rules

- Read the repository license before copying schematic blocks, footprints, CAD, or firmware.
- Separate “inspired by” from “derived from.”
- Keep a source file and license record in the project folder.
- If using Pixhawk standards, say “designed to follow the relevant Pixhawk interface standard” only after checking the exact electrical/mechanical requirements.
- Do not label an independently designed board as an official Pixhawk product.
- If the team modifies CERN-OHL or another open-hardware design, preserve the required notices and disclose the required source files.

---

## 12. Tutorials, videos, and practical learning sequence

### 12.1 Recommended sequence

1. Draw a simple STM32H7 power/clock/SWD/USB schematic.
2. Build and test a minimal STM32H7 board or development-board equivalent.
3. Read one sensor over SPI.
4. Generate one PWM output and capture it with a scope/logic analyzer.
5. Add the barometer and a logging path.
6. Create the full FC schematic and only then route the PCB.

### 12.2 Resources

| Resource | What to learn |
|---|---|
| [Phil’s Lab KiCad STM32 full design tutorial](https://www.youtube.com/watch?v=aVUqaB0IMh4) | STM32 decoupling, clocks, configuration pins, USB, power, ERC, footprints, PCB layout, routing, DRC, Gerbers, BOM, and CPL |
| [Phil’s Lab six-layer mixed-signal PCB tutorial](https://www.youtube.com/watch?v=AxEL3eESL9I) | Layer stack-up thinking, planes, high-speed/mixed-signal routing, and STM32H7-class layout |
| [Phil’s Lab flight-control system design / PCB series](https://www.fedevel.com/blog/flight-control-system-design-hardware-and-pcb-design-with-kicad-phils-lab-1) | Flight-control-specific hardware partitioning and KiCad workflow |
| [Ethan Suttor custom drone FC project](https://ethansuttor.com/projects/custom-drone-flight-controller) | A practical custom-FC design narrative |
| [LEVIA-H7 repository](https://github.com/piecol/LEVIA-H7) | Inspect a complete KiCad folder, schematic sheets, BOM, manufacturing outputs, and layer strategy |
| [Pixhawk Hardware](https://github.com/pixhawk/Hardware) | Compare mature autopilot schematics and reference layouts |

### 12.3 Community sources

Reddit reviews and build discussions can reveal practical problems that formal documentation does not show:

- [Custom H7 FC review request](https://www.reddit.com/r/PrintedCircuitBoard/comments/1qci8jg/review_request_drone_flight_controller_with/)
- [Custom F405 FC review](https://www.reddit.com/r/PrintedCircuitBoard/comments/1vwpzuz/review_request_stm32f405_flight_controller_v11/)
- [Custom FC built from scratch](https://www.reddit.com/r/diydrones/comments/1q5k508/built_a_custom_flight_controller_from_scratch/)
- [Flight-controller PCB design review](https://www.reddit.com/r/PCB/comments/1poshof/day-42-of-designing-a-flight-controller-review/)
- [STM32H743 flight-controller discussion](https://www.reddit.com/r/ardupilot/comments/1o59tul/flight-controller-design-using-stm32h743vit6/)
- [UAV PCB / ArduPilot schematic review](https://www.reddit.com/r/PrintedCircuitBoard/comments/1un6jmf/schematics_review_uav_flight_controller_that_runs_ardupilot/)

Treat these as **engineering-review material**, not certification evidence. Community claims about flight performance, reliability, or safety require independent verification.

---

## 13. Schematic design requirements

### 13.1 MCU sheet

Include:

- all STM32 power pins;
- VCAP capacitors;
- VDDA/VREF filtering;
- HSE and optional LSE;
- NRST;
- BOOT0 selection and recovery pad;
- SWDIO/SWCLK/NRST/3V3/GND;
- USB D+/D− and ESD;
- unused pins tied or marked according to ST recommendations;
- clearly labeled alternate-function net names;
- test points for core rails and reset.

### 13.2 Sensor sheet

For each sensor:

- exact voltage rail;
- local decoupling;
- SPI/I2C pull-ups if needed;
- chip-select and interrupt;
- address-selection pins;
- orientation arrow and board-axis convention;
- footprint from the current manufacturer drawing;
- keepout/placement note;
- mechanical and airflow note for the barometer.

Do not leave sensor orientation as an informal note. The firmware axis convention and PCB reference orientation must agree.

### 13.3 Power sheet

Show:

- source connector and polarity;
- fuse/current-limiting element;
- reverse-polarity stage;
- TVS;
- USB/external 5 V power mux;
- 5 V and 3.3 V rails;
- sensor rail filter/LDO;
- test points;
- maximum current and voltage annotation;
- thermal dissipation assumptions.

### 13.4 IO and communications

Show:

- all eight motor outputs with exact timer channel;
- labeled external ports: `GPS1`, `TELEM1`, `RC_IN`, `COMPANION`, `LIDAR_FC`, and `AUX_UART`;
- exact connector pin order, pin-1 marking, signal voltage, allowable supply voltage/current, and mating cable drawing;
- CAN transceiver and termination option;
- `CAN1/CAN2` topology, termination placement, node power budget, and whether the FC is a bus-end node;
- microSD;
- external compass/GNSS connector with UART/PPS/I2C/CAN ownership clearly shown;
- ADC voltage/current scaling;
- buzzer and status LEDs;
- safety switch and any external arming input.

The schematic must distinguish **board-mounted devices** (primary IMU and barometer) from **external modular devices** (ESC, receiver, GNSS/compass, CM5 carrier, telemetry and lidar). Do not present a connector as compatible with a Pixhawk standard until the exact standard revision and pinout have been checked.

---

## 14. PCB layout guidance

### 14.1 Layer choice

**Rev A default:** four-layer stack-up:

~~~text
L1: components + short high-speed / sensitive signals
L2: continuous ground plane
L3: power distribution + selected signals
L4: signals / connectors / secondary routing
~~~

**Six-layer option:**

~~~text
L1: components + signals
L2: ground plane
L3: signals
L4: power plane / power distribution
L5: ground plane
L6: signals
~~~

The exact stack-up, dielectric thickness, copper weight, controlled impedance, and via rules must come from the selected manufacturer. Do not draw a six-layer stack-up from a generic internet diagram and assume it matches the fab.

### 14.2 Placement order

1. Mounting holes and mechanical outline.
2. Primary IMU and optional second IMU.
3. MCU and its decoupling/clock/reset.
4. Sensor power filter and barometer.
5. Power regulators and inductors.
6. USB-C, SWD, connectors, microSD.
7. CAN and external interfaces.
8. LEDs, buzzer, test points, and optional footprints.

### 14.3 Routing order

1. Critical sensor and clock connections.
2. Ground plane and power return paths.
3. MCU power/VCAP/VDDA.
4. USB differential pair according to ST guidance.
5. SDMMC/SPI and CAN.
6. PWM/UART/I2C.
7. High-current power only if raw-battery conversion is included.

### 14.4 Review checklist

- Does every high-speed signal have a continuous return path?
- Are switching-current loops small?
- Is the IMU isolated from the power inductor?
- Is the magnetometer outside the high-current field?
- Are USB ESD parts close to the connector?
- Is there a clear test point for each rail?
- Can a probe reach the SWD and reset pins?
- Are connectors keyed and labeled?
- Are connector-side ESD/overvoltage parts present where required, and are their capacitance and voltage ratings compatible with the bus?
- Are fast signals given adjacent ground returns, and are CANH/CANL routed as a pair with switchable 120 ohm termination only at a bus end?
- Are I2C pull-ups selectable so external modules do not create excessive parallel pull-up strength?
- Is every external port’s voltage/current budget and hot-plug policy documented?
- Are mounting-hole keepouts and component heights checked?
- Are copper pours not silently connecting analog and noisy returns?
- Are footprints checked against 3D and datasheet drawings?
- Does the fab’s minimum drill/trace/space capability match the layout?

---

## 15. Firmware and board-support plan

### 15.1 Fastest bring-up path

Start with a small custom firmware application:

1. configure clocks and GPIO;
2. prove SWD flashing and reset;
3. enumerate USB;
4. read the IMU identification register;
5. stream raw accelerometer and gyro values;
6. read the barometer;
7. capture battery voltage/current ADC values;
8. generate one safe PWM output;
9. test all output channels;
10. write a timestamped log;
11. add a simple attitude estimator;
12. add a bench-only PID loop.

This sequence creates evidence that the custom PCB works before the complexity of a full autopilot stack is introduced.

### 15.2 PX4 route

For PX4:

- create a board-specific target under the supported board structure;
- define the MCU, clock, pins, timers, serial ports, buses, and storage;
- map the logical modular ports (`RC_IN`, `GPS1`, `COMPANION`, `CAN1/CAN2`, `LIDAR_FC`) to the actual UART/CAN/timer/ADC resources;
- add the selected sensor drivers and bus configuration;
- build and flash the board bootloader;
- define board ID and safety configuration;
- follow the PX4 porting and board-support guidance;
- test on hardware-in-the-loop or a rig before flight.

The PX4 documentation explicitly treats a new board as a real board-support task. Reusing a similar board target without checking every pin, bus, timer, and sensor can produce a dangerous mismatch.

### 15.3 ArduPilot route

For ArduPilot:

- create or adapt the board hardware definition;
- map all timers, UARTs, SPI/I2C buses, ADCs, and storage;
- map the external modular ports and document the expected GPS/compass, receiver, telemetry, companion and rangefinder functions;
- implement bootloader/board configuration;
- ensure the selected sensors are supported or add drivers;
- build and test a dedicated target;
- compare parameter, calibration, logging, and failsafe behavior with the project’s requirements.

The hardware-definition route is powerful, but it does not remove the need to verify the electrical design and sensor orientation.

### 15.4 What not to promise in the initial presentation

Avoid saying:

- “the board is military grade”;
- “the board is DO-254 compliant”;
- “the board is certified for UAM”;
- “it will run PX4 immediately”;
- “it is flight safe because it uses an STM32.”

Use:

> “This is a custom, non-certified prototype architecture informed by open autopilot hardware and firmware practices. The first milestone is controlled bench and rig verification.”

---

## 16. Verification and bring-up plan

### 16.1 Before power

- visually inspect for solder bridges and rotated ICs;
- use continuity mode to check 5 V-to-ground and 3.3 V-to-ground for shorts;
- verify diode/MOSFET orientation;
- verify regulator feedback networks;
- check capacitor voltage ratings;
- confirm no raw-battery trace accidentally connects to a logic rail;
- verify connector polarity and pin numbering;
- photograph the assembled board for the project record.

### 16.2 First power

- use a current-limited bench supply;
- begin with external regulated 5 V, not a battery;
- observe inrush and steady current;
- measure 5 V, 3.3 V, and sensor 3.3 V;
- check regulator temperature;
- power down if current is unexpectedly high;
- do not connect motors or propellers.

### 16.3 MCU and communication tests

| Test | Evidence |
|---|---|
| SWD attach | Debugger log, device ID, read/write test |
| Reset/BOOT0 | Correct boot path and recovery behavior |
| Clock | Firmware clock test or scope measurement |
| USB | Enumeration and serial/log transfer |
| UART | Loopback or known peripheral response |
| CAN | Two-node bench test with correct line topology and termination |
| External modular ports | Cable pinout/continuity, supply-current test, signal-level check, UART loopback, I2C rise-time/loading check, CAN termination and node test |
| SD/SPI flash | Write/read/CRC test |

### 16.4 Sensor tests

- read identification registers;
- verify accelerometer/gyro axis directions;
- rotate the board by hand and confirm expected sign;
- compare measured bias with a stationary dataset;
- check sample rate and timestamp jitter;
- heat-soak briefly and observe drift;
- test barometer response to controlled pressure/altitude changes;
- test magnetometer only in the final vehicle magnetic environment.

### 16.5 Output and control tests

- measure PWM frequency, pulse width, polarity, and reset state;
- test one channel at a time with a logic analyzer or scope;
- use dummy loads or ESC signal input without propellers;
- verify a failsafe/disable state when firmware stops;
- verify no output spike occurs during reset, bootloader, USB attach, or brownout.

### 16.6 Rig/tether tests

Before any free-flight test:

- mount the vehicle securely;
- use a physical propeller exclusion zone;
- use a current-limited or protected power arrangement;
- keep a manual power cutoff;
- log every sensor and actuator signal;
- perform low-throttle tests first;
- obtain lecturer/instructor approval.

---

## 17. Manufacturing and hand-assembly plan

### 17.1 Recommended Rev A assembly strategy

- use 0603 passives where practical;
- order a stencil;
- use solder paste rather than trying to hand-solder every LGA pad;
- place the H743 and sensors under magnification;
- reflow with a characterized profile where possible;
- hand-solder through-hole headers/connectors after reflow;
- clean and inspect the board;
- use X-ray or external inspection for hidden/underside joints if available;
- record failed joints and rework in a build log.

### 17.2 Assembly order

1. bare-board inspection;
2. small passives on the first side;
3. regulators and protection;
4. MCU;
5. IMU/barometer/memory;
6. reflow and inspection;
7. connectors, headers, and large capacitors;
8. continuity and resistance checks;
9. current-limited power-up.

If the team cannot reliably inspect the LGA IMU joints, build the first board with a sensor module or use an assembly service while retaining the custom PCB design. That still allows the team to learn the complete board-design process without risking all results on an invisible solder joint.

### 17.3 Documentation package

Save:

- KiCad project;
- schematic PDF;
- PCB file;
- stack-up and design rules;
- 3D render;
- Gerbers;
- drill files;
- BOM;
- component-placement/CPL file if assembled;
- assembly drawing;
- test-point drawing;
- firmware target/configuration;
- license/source register;
- revision history.

---

## 18. Main risks and mitigations

| Risk | Likely consequence | Mitigation |
|---|---|---|
| Incorrect MCU power/VCAP/clock design | Board does not boot or is unstable | Follow ST reference guidance; review with a second person; make a minimal bring-up sheet |
| Wrong sensor footprint or orientation | Bad data or impossible calibration | Use manufacturer land pattern; add an orientation arrow; verify with a physical 3D model |
| Onboard compass interference | Heading errors | Use an external GPS/compass module and keep high-current wiring away |
| Remote raw IMU/SPI/I2C cable | Timing errors, EMI, intermittent sensor data or unstable estimation | Keep primary IMU onboard; use a short local daughterboard or a timestamped smart CAN sensor node for future expansion |
| Connector/pinout mismatch | Damaged module, silent sensor failure or wrong data on a bus | Use keyed connectors, printed labels, pin-1 drawings, continuity-tested harnesses and an interface sign-off between teams |
| Excessive I2C loading | Slow edges, bus lockups or corrupted compass/barometer data | Keep the bus short, calculate capacitance and pull-ups, reduce speed or use a purpose-designed buffer/node |
| Incorrect CAN termination/topology | Reflections, intermittent node loss or failed discovery | Use a linear backbone, short stubs and 120 ohm termination only at the two physical ends |
| External-module power overload | FC reset, regulator damage or cable heating | Derive each port budget from module datasheets, add margin/current limiting, and keep CM5 power on its own 5 V regulator |
| Accidental live hot-plug | Brownout, ESD damage or corrupted bus state | Power down before module changes unless hot-swap protection is explicitly designed and tested |
| Raw battery overvoltage/transients | Regulator/PCB damage or fire | Use external 5 V for Rev A; calculate TVS/regulator ratings before adding battery input |
| No accessible debug path | First failed board becomes difficult to diagnose | SWD header, reset, BOOT0, test points, and LEDs |
| Porting firmware too early | Team cannot tell whether hardware or software is broken | Bring up peripherals with minimal firmware first |
| Copying a design without license review | Legal/reproducibility problem | Record licenses and create an original design where required |
| Too many features in Rev A | Delayed fabrication and poor testing | Freeze a minimal feature set; reserve optional footprints for Rev B |
| Hand-soldered LGA failure | Sensor appears dead | Stencil, controlled reflow, magnification, spare sensors, or assembly service |
| Inadequate ground return / noisy power | Sensor noise and estimator instability | Four-layer plane strategy, short power loops, sensor rail filtering, scope review |
| Believing community claims | Unsafe or incorrect design decisions | Use community material for ideas; verify against datasheets and measurements |
| Exact component price/stock changes | Procurement delay | Approve alternates and buy critical parts early |

---

## 19. Decisions to take to the lecturer

Present these as decisions requiring confirmation:

1. **Vehicle scope:** small quadrotor/VTOL demonstrator; exact battery and motor/ESC set.
2. **Prototype boundary:** custom FC board will initially be bench/rig demonstrated; any flight test requires approval.
3. **Rev A MCU:** STM32H743VIT6 in LQFP-100.
4. **Sensor choice:** ICM-42688-P as the Rev A default, with BMI088 only as a verified availability fallback; external magnetometer preferred.
5. **Power strategy:** external regulated 5 V for Rev A, rather than raw-battery conversion on the first board.
6. **PCB layers:** four layers as baseline; six layers only if board size, routing, and budget justify it.
7. **Firmware milestone:** minimal custom bring-up first; PX4/ArduPilot board port afterward.
8. **Assembly method:** stencil + solder paste + reflow/hot air, with inspection and spare components.
9. **Testing equipment:** access to ST-LINK, oscilloscope, current-limited supply, logic analyzer, and lab safety equipment.
10. **Modular architecture:** hybrid Pixhawk-style system; primary IMU/barometer onboard, ESC/receiver/GNSS-compass/telemetry/CM5/lidar externally connectable.
11. **Connector standard:** exact Pixhawk connector/pinout compliance or a clearly labeled Pixhawk-inspired contract; do not claim compatibility from connector shape alone.
12. **Evidence expected:** schematic, PCB, BOM, modular-port pinout and harness drawing, manufactured board, bring-up measurements, and controlled demonstration.

---

## 20. Short procurement checklist

### Critical parts to source first

- STM32H743VIT6, plus at least one spare;
- ICM-42688-P, plus at least one spare; BMI088 only if the fallback is formally selected;
- BMP390, plus one spare;
- selected 3.3 V buck and sensor LDO;
- USB-C connector and ESD array;
- CAN transceiver;
- W25Q128JV or microSD socket;
- SWD debugger;
- correct crystals and capacitors;
- input protection parts;
- selected JST/keyed connectors;
- keyed, locking connector housings/contacts and cable assemblies for `POWER1`, `ESC_OUT`, `RC_IN`, `GPS1`, `CAN`, `TELEM1`, `COMPANION` and `LIDAR_FC`;
- stencil and solder paste.

### Do not order until these are frozen

- TVS part number and voltage;
- raw-battery buck regulator;
- exact ADC-divider values;
- crystal load capacitors;
- sensor footprint;
- connector family, exact pinout, voltage/current budget, cable length and hot-plug policy;
- PCB stack-up;
- any “compatible” alternate MCU.

---

## 21. Source quality and research method

The research used four source levels:

### Tier A — primary technical sources

- ST, Bosch Sensortec, TDK/InvenSense, Texas Instruments, Winbond, MEMSIC, and other manufacturer datasheets/product pages;
- PX4 and ArduPilot official documentation and repositories;
- Pixhawk standards and official hardware repository;
- PCB manufacturer pricing/help pages.

Use Tier A sources for:

- electrical ratings;
- pin functions;
- package dimensions;
- layout rules;
- power and timing;
- firmware porting requirements;
- standards and licensing.

### Tier B — open hardware and project repositories

Use complete KiCad/Gerber/BOM repositories to understand:

- real schematic partitioning;
- component placement;
- connector strategies;
- sensor redundancy;
- board stack-ups;
- manufacturing file preparation.

Do not assume that a repository’s “working” status means flight qualification.

### Tier C — videos and build write-ups

Use tutorials to learn workflow:

- schematic capture;
- footprint assignment;
- ERC/DRC;
- PCB routing;
- Gerber/BOM/CPL export;
- soldering and inspection.

### Tier D — Reddit/community discussions

Use community reviews to identify common mistakes and practical concerns. Do not use them as the sole evidence for a safety-critical decision.

---

## 22. Selected references

### Flight-controller standards and firmware

- [Pixhawk Hardware repository](https://github.com/pixhawk/Hardware)
- [Pixhawk Standards repository](https://github.com/pixhawk/Pixhawk-Standards)
- [Pixhawk Reference Standards overview](https://pixhawk.org/standards/)
- [PX4 Autopilot repository](https://github.com/PX4/PX4-Autopilot)
- [PX4 hardware reference design](https://github.com/PX4/PX4-Devguide/blob/master/en/hardware/reference_design.md)
- [PX4 porting guide](https://docs.px4.io/main/en/hardware/porting_guide)
- [PX4 manufacturer board support guide](https://docs.px4.io/main/en/hardware/board_support_guide)
- [ArduPilot repository](https://github.com/ArduPilot/ardupilot)
- [ArduPilot schematics](https://github.com/ArduPilot/Schematics)
- [ArduPilot OEM/custom hardware guide](https://ardupilot.org/dev/docs/common-oem-customizations.html)
- [PX4 GNSS/GPS setup and external-module connections](https://docs.px4.io/main/en/gps_compass/)
- [PX4 magnetometer guidance](https://docs.px4.io/main/en/gps_compass/magnetometer)
- [PX4 DroneCAN ARK CANnode example](https://docs.px4.io/main/en/dronecan/ark_cannode)
- [PX4 Pixhawk companion-computer serial connection](https://docs.px4.io/main/en/companion_computer/pixhawk_companion)
- [ArduPilot companion computers](https://ardupilot.org/dev/docs/companion-computers.html)
- [ArduPilot rangefinder setup](https://ardupilot.org/plane/docs/common-rangefinder-setup.html)

### MCU, sensors, and power

- [STM32H743ZI product page](https://www.st.com/en/microcontrollers-microprocessors/stm32h743zi.html)
- [STM32H743 datasheet](https://www.st.com/resource/en/datasheet/stm32h743zi.pdf)
- [STM32H7 documentation](https://www.st.com/en/microcontrollers-microprocessors/stm32h7-series/documentation.html)
- [Bosch BMI088](https://www.bosch-sensortec.com/en/products/motion-sensors/imus/bmi088)
- [Bosch BMI088 datasheet](https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bmi088-ds001.pdf)
- [Bosch BMP390](https://www.bosch-sensortec.com/en/products/environmental-sensors/pressure-sensors/bmp390)
- [TDK ICM-42688-P](https://www.invensense.tdk.com/en-us/products/6-axis/icm-42688-p)
- [ICM-42688-P datasheet](https://product.tdk.com/system/files/dam/doc/product/sensor/mortion-inertial/imu/data_sheet/ds-000347-icm-42688-p-v1.6.pdf)
- [ICM-42688-P PCB/MEMS assembly guidelines](https://invensense.tdk.com/wp-content/uploads/2023/05/an-000393_imu-pcb-design-and-mems-assembly-guidelines.pdf)
- [TI LMR33630](https://www.ti.com/product/LMR33630)
- [TI TPS62162](https://www.ti.com/product/TPS62162-Q1)
- [TI LP5907](https://www.ti.com/product/LP5907)
- [TI TCAN332](https://www.ti.com/product/TCAN332)
- [TI TPS2116](https://www.ti.com/product/TPS2116)
- [TI TPS386000](https://www.ti.com/product/TPS386000)
- [ST USB hardware/PCB guidelines](https://www.st.com/resource/en/application_note/an4879-usb-hardware-and-pcb-guidelines-using-stm32-mcus-stmicroelectronics.pdf)
- [ST STM32H7 hardware development note](https://www.st.com/resource/en/application_note/an5307-getting-started-with-stm32h7a37b3-line-and-stm32h7b0-value-line-microcontroller-hardware-development-stmicroelectronics.pdf)
- [NXP UM10204 I2C-bus specification](https://community.nxp.com/pwmxy87654/attachments/pwmxy87654/nxp-designs/931/1/UM10204.pdf)
- [TI I2C long-cable/extender guidance](https://www.ti.com/kr/lit/pdf/sdaa306)
- [CAN in Automation high-speed CAN transmission guidance](https://www.can-cia.org/can-knowledge/can-hs-transmission)

### Manufacturing and tools

- [JLCPCB PCBA pricing](https://jlcpcb.com/help/article/pcb-assembly-price)
- [JLCPCB stencil](https://jlcpcb.com/pcb-stencil)
- [JLCPCB ordering guide](https://jlcpcb.com/help/article/how-do-i-place-an-order)
- [PCBWay online calculator](https://www.pcbway.com/HighQualityOrderOnline.aspx?h=1)
- [ST-LINK/V3 distributor listing](https://www.digikey.my/en/products/filter/programmers-emulators-and-debuggers/799)
- [Cytron development tools](https://my.cytron.io/c-development-tools/c-tools-and-equipments)

### Open custom-board references

- [LEVIA-H7](https://github.com/piecol/LEVIA-H7)
- [Shirley-FC-Dev-Board](https://github.com/Bare-Metal-Foundry/Shirley-FC-Dev-Board)
- [pixeagle](https://github.com/mkeyno/pixeagle)
- [FPV Flight Controller PCB](https://github.com/fpv-chicken-nugget/FPV-Flight-Controller-PCB)
- [STM32H743 Betaflight development board](https://github.com/DpooL2000/STM32h743-devboard-betaflight)
- [STM32F411 DroneController](https://github.com/FPV-Drone-STM32F411/DroneController)
- [Kestrel custom autopilot](https://ahmedbadwy.com/projects/proj-kestrel)
- [HADES open-source flight-control system](https://www.pcbway.com/project/shareproject/HADES_Open_Source_Flight_Control_System.html)
- [Berkeley HOPE drone controller](https://sites.google.com/berkeley.edu/hope-sp24/drone-controller)
- [Ethan Suttor custom flight controller](https://ethansuttor.com/projects/custom-drone-flight-controller)

### Tutorials and community

- [Phil’s Lab STM32/KiCad tutorial](https://www.youtube.com/watch?v=aVUqaB0IMh4)
- [Phil’s Lab six-layer mixed-signal tutorial](https://www.youtube.com/watch?v=AxEL3eESL9I)
- [Phil’s Lab flight-control PCB series](https://www.fedevel.com/blog/flight-control-system-design-hardware-and-pcb-design-with-kicad-phils-lab-1)
- [Reddit custom H7 FC review](https://www.reddit.com/r/PrintedCircuitBoard/comments/1qci8jg/review_request_drone_flight_controller_with/)
- [Reddit custom F405 FC review](https://www.reddit.com/r/PrintedCircuitBoard/comments/1vwpzuz/review_request_stm32f405_flight_controller_v11/)
- [Reddit from-scratch flight controller](https://www.reddit.com/r/diydrones/comments/1q5k508/built_a_custom_flight_controller_from_scratch/)

---

## Final engineering recommendation

Freeze the first prototype around **STM32H743VIT6 + one onboard SPI ICM-42688-P + onboard BMP390 + external compass/GNSS + external regulated 5 V input + 3.3 V rails + SWD/USB/CAN/UART/PWM + logging**, with a **hybrid Pixhawk-style modular port architecture**. The ESC board, receiver, GNSS/compass, telemetry, Raspberry Pi CM5 carrier and applicable lidar must attach through keyed, labeled connectors. Keep the primary IMU and barometer on the FC PCB; use CAN/DroneCAN or a local smart sensor node for future remote high-rate sensors instead of extending raw SPI/I2C arbitrarily.

Build the schematic, logical port map, cable pinout, power budget and power tree first. Use LEVIA-H7, Pixhawk, PX4, and ArduPilot as references, but preserve the project’s own design identity and license trail. The standard connector family can be borrowed only with a verified pinout and firmware mapping; connector appearance alone is not compatibility.

The strongest presentation claim is:

> “We designed and will verify a small custom real-time flight-controller PCB, using an STM32H7 MCU and discrete sensors/power/interface components. The initial milestone is a safe, non-certified bench/rig demonstrator; integration with a full autopilot stack and any flight test will follow only after board and firmware verification.”

That statement is technically credible, achievable, and aligned with the lecturer’s request to move from general autopilot research toward a real prototype.

---

## 23. Integrated-system research addendum — 27 August 2026

This addendum incorporates the user’s latest decisions and the supplied FC, companion-computer, lidar, camera, ESC, motor and battery requirements. The earlier sections remain useful background; where this addendum is more specific, it is the current Rev A direction.

### 23.1 Scope and evidence boundary

The user’s direct request is the controlling requirement. The attached reports and pasted text are reference material. The supplied YouTube videos and Reddit posts are useful for workflow, design-review warnings and project-scope evidence, but their claims are not treated as electrical specifications. Datasheets, official firmware documentation, official Pixhawk standards and complete open-hardware repositories are the evidence used for ratings, protocols, pin functions, connector standards and licensing.

The deliverable remains a **non-certified student prototype**. “Collision avoidance,” “object tracking,” “autonomy” and “UAM” in this report describe intended research functions, not a guarantee of safe autonomous flight or airworthiness.

### 23.2 Complete comparison of the supplied references

| # | Supplied reference | What it contributes | What should be reused or learned | What must not be copied blindly |
|---:|---|---|---|---|
| 1 | [OpenFC-Lite-Mini repository](https://github.com/OpenDrone-hw/OpenFC-Lite-Mini) and [linked video](https://www.youtube.com/watch?v=XDYZoMRJFeQ) | Compact open Betaflight FC using RP2354A, BMI270, dedicated sensor rail, microSD, multiple UARTs and signal-level external 4-in-1 ESC connection; 3–6S input and six-layer manufacturing approach are documented in the project family | Study the separation of logic from motor power, dedicated IMU rail, local KiCad libraries, production export flow and explicit limitations | RP2354/BMI270/Betaflight is not the selected H743/ArduPilot-or-PX4 path; no onboard barometer and no direct reason to copy its exact pinout |
| 2 | [HomeGliders FCV2 repository](https://github.com/HomeGliders/FCV2) and [linked video](https://www.youtube.com/watch?v=6n7d8Jn2brQ) | A small KiCad flight-controller project packaged as KiCad files; useful as a schematic/PCB organization example | Inspect the project archive for hierarchy, net naming, connector placement, ERC/DRC and manufacturing workflow | The repository page alone does not establish exact part ratings, flight validation or compatibility with our H743 system; extract and verify every value before reuse |
| 3 | [Jacob Thornhill DIY FC video](https://www.youtube.com/watch?v=wYC-siMWn70) | Video metadata describes an STM32F405 controller for RC drones/planes, I2C sensor collection, UART GPS/receiver links and a project failure caused by frame flexibility/filtering issues | Learn the end-to-end design narrative, basic system partitioning and the importance of mechanical stiffness and filtering | The I2C-centric F405 sensor approach is not the Rev A high-rate IMU recommendation; a video demonstration is not a flight qualification |
| 4 | [Official Pixhawk hardware repository](https://github.com/pixhawk/hardware) | Mature open autopilot architecture, FMU/IO history, power/sensor/debug organization and reference hardware | Use it for system partitioning, port naming, power-domain separation, redundancy concepts and design-document structure | Do not copy a board or call the custom PCB an official Pixhawk; check each design’s license and the exact selected standard |
| 5 | [r/fpv H743 custom-FC discussion](https://www.reddit.com/r/fpv/comments/1r5rvne/build_a_custom_flight_controller/) | Community review raises reverse-current protection, external-shunt/current-sense, regulator capability, magnetometer placement and output-series-resistor issues | Add these items to the design-review checklist; keep current shunts and noisy magnetics off the FC | Reddit comments are not a substitute for regulator calculations, thermal measurements or the actual schematic |
| 6 | [Udayate build discussion](https://www.reddit.com/r/diydrones/comments/1q5k508/built_a_custom_flight_controller_from_scratch/) | An STM32F411/FreeRTOS/HAL educational build with custom drivers and estimator work; the author reports that schematic/PCB, drivers and EKF each took substantial time | Reuse the project as a learning path for drivers, task structure, estimator testing and serial visualization; use its schedule as a realistic warning | Do not assume its F411 hardware or custom firmware is a drop-in autopilot for this H743 board |
| 7 | [“Anyone here built their own FC?” discussion](https://www.reddit.com/r/diydrones/comments/1oibb96/anyone_here_built_their_own_flight_controller/) | Discussion of AI-enabled FC concepts and the distinction between board hardware, firmware and companion processing | Reinforces the need to define the application and not confuse an AI computer with a deterministic flight controller | Community claims about AI TOPS or compatibility must be checked against vendor and firmware documentation |
| 8 | [Custom FC from-scratch feature discussion](https://www.reddit.com/r/Multicopter/comments/1s6r7ht/building_a_custom_flight_controller_from_scratch/) | Community advice strongly favours an STM32 + gyro + basic loop before adding logging, baro, lidar and autonomy; other comments request first-class lidar/camera/avoidance | Use the staged architecture: prove the inner loop, then add perception; keep the modular interfaces on the PCB even if their software is staged | Do not interpret the scope warning as permission to omit required external connectors; make connectors present but bring them up in phases |
| 9 | [Shirley-FC-Dev-Board](https://github.com/Bare-Metal-Foundry/Shirley-FC-Dev-Board) | H743ZIT6 board with ICM-40609-D, MMC5983MA, BMP390, SD, 5 V MUX, dual 3.3 V rails, four ESC outputs, GPS/RC/telemetry/USB/CAN and GH1.25 connectors | Closest architecture study for a Pixhawk-style H7 board: power tree, connector naming, CAN, debug access and sensor placement | It is not our exact MCU package or sensor set; do not substitute its ICM-40609-D/MMC5983MA choices without a firmware and availability review |
| 10 | [User-supplied PrintedCircuitBoard review link](https://www.reddit.com/r/PrintedCircuitBoard/comments/1qci8jg/review_request_drone_flight_controller_with/and) | The supplied URL is malformed/unreliably retrievable as written; it cannot be used as a verified design source until the exact post or images are provided | Preserve it as a lead and ask for the corrected link if its schematic/layout is important | No component, layout or design claim is taken from this entry |
| 11 | [Betaflight manufacturer design guidelines](https://betaflight.com/docs/development/manufacturer/manufacturer-design-guidelines) | Current practical guidance on SPI IMUs, dedicated ICM-42688-P rail, H7 timer/DMA, I2C baro/mag, ADC protection, SWD, blackbox and output grouping | Use its IMU rail, layout, output grouping, resistor, test-point and bring-up rules even if the final firmware is not Betaflight | Betaflight-specific loop-rate and target rules do not automatically define an ArduPilot/PX4 board |
| 12 | [OpenFC-Lite-Mini readme duplicate](https://github.com/OpenDrone-hw/OpenFC-Lite-Mini?tab=readme-ov-file) | Duplicate entry for reference 1; confirms the project’s documented open-hardware/readme material | Use the repository as the authoritative version of this reference | Do not count the duplicate as a second independent design |
| 13 | [STM32H743 FC review request](https://www.reddit.com/r/PCB/comments/1q3kh9f/stm32h743_flight_controller_review_request/) | Realistic H743VIT6, ICM-42688-P, BMP388, 9/5/3.3 V, microSD, USB-C and four-UART example; comments identify LQFP/BGA confusion, power-routing, regulator, IMU-LDO and shunt issues | Directly supports our LQFP choice, separated power/sensor placement, dedicated IMU LDO and external current-sense boundary | Community review is a warning list, not evidence that the board is flight-ready; verify every suggested fix against datasheets |
| 14 | [Udayate](https://github.com/Ozonised/Udayate), [video](https://www.youtube.com/watch?v=pUdvCbNR1gM&t=43s), [Kalman-AHRS](https://github.com/Ozonised/Kalman-AHRS), [LSM6DSL library](https://github.com/Ozonised/LSM6DSL-Platform-Independent-Library), and [Quaternion Visualiser](https://github.com/Ozonised/Quaternion-Visualiser) | Complete educational chain: KiCad hierarchy and STM32F411 hardware, platform-independent driver pattern, quaternion/EKF attitude code and serial visualization | Reuse the software architecture ideas: hardware abstraction, deterministic sensor readout, quaternion representation, logged serial output and offline visualization | Do not treat the F411 firmware, LSM6DSL driver or EKF as production autopilot code; port and validate with the selected ICM-42688-P and vehicle dynamics |
| 15 | [Pixhawk 2.1 schematics](https://github.com/MRazgunas/pixhawk2.1) | Practical Pixhawk2-era schematic reference and a useful example of subsystem separation | Study power, IMU, IO and connector partitioning | The repository has mixed licenses, including non-commercial restrictions on some boards; licensing and schematic revision must be checked before any reuse |
| 16 | [Beginner FC build discussion](https://www.reddit.com/r/diydrones/comments/1ts9v3u/building_a_flight_controller/) | Community advice recommends learning on known hardware and identifies control loops, sensor fusion, motor mixing and sensor processing as minimum knowledge | Use it as a risk/schedule reminder while still meeting the user’s custom-PCB requirement | It does not replace the project requirement to build the custom board; it only supports parallel bench validation |

The first two video pages were not consistently machine-readable during the web review. Their linked repositories were therefore treated as the evidence source. The third video has enough indexed description to identify its F405/I2C/UART architecture. This limitation is recorded rather than inventing frame-by-frame claims about video content.

### 23.3 Best-parts reuse map

The strongest combined design is not a literal clone of one reference:

| Design area | Best reference lesson | Rev A implementation |
|---|---|---|
| Main MCU | Shirley and the H743 review example | Bare STM32H743VIT6 in LQFP-100 with SWD, USB, boot/reset and a documented pin/timer/DMA map |
| Primary IMU | Betaflight guidelines, OpenFC, H743 review | ICM-42688-P on local SPI with a dedicated low-noise rail, local interrupt and controlled ground return |
| Barometer | Shirley/OpenFC comparison | BMP390 onboard under a protected vent, away from prop wash and switching inductors |
| Compass/GNSS | Pixhawk/PX4 rationale and community warnings | External module on UART+I2C or DroneCAN, physically separated from battery/motor fields |
| Modular ports | Pixhawk standards, Shirley GH connectors and PX4 companion guidance | Keyed/latching low-current ports with a project-defined pinout; exact Pixhawk compliance only after DS-009 verification |
| ESC boundary | OpenFC and OpenESC | FC carries signal/ground only; ESC board owns battery current, gate drive, shunts, thermal copper and motors |
| ESC protocol | Betaflight DShot/AM32/OpenESC | DShot first if the teammate’s ESC supports it; bidirectional DShot only after bench validation; PWM fallback |
| Power | Betaflight/H743 review warnings | External regulated FC 5 V, dedicated sensor rail, separate CM5 buck and external current shunt/voltage sense |
| Firmware | PX4/ArduPilot official docs plus Udayate learning code | ArduPilot-first or PX4-first integration; Udayate only for learning/bench estimator patterns, not a drop-in flight stack |
| CM5 | Official Raspberry Pi CM5/CM5IO docs | Separate CM5 carrier with camera/lidar interfaces and independent 5 V power; no CM5 soldered to FC |
| Development process | OpenFC production files and Phil’s Lab workflow | KiCad hierarchy, ERC/DRC, explicit pinout, manufacturing exports, current-limited bring-up and evidence logs |

---

## 24. Raspberry Pi Compute Module 5 integration

### 24.1 CM5 versus standard Pi 5 and CM4

The chosen name should be **Raspberry Pi Compute Module 5 (CM5)**. CM5 is the compute module form of the Raspberry Pi 5 generation, based on BCM2712, with optional RAM/eMMC variants and two 100-pin high-density connectors. It has no normal onboard USB, HDMI, Ethernet or camera sockets. A carrier board supplies those interfaces and the power/control circuitry. [Raspberry Pi’s Compute Module documentation](https://www.raspberrypi.com/documentation/computers/compute-module.html) describes CM5IO as a development carrier and reference design for a smaller custom carrier.

CM4 is a Pi 4-generation module. It can be a software fallback if already available, but it is not the preferred new design for this project because CM5 provides more Pi 5-class compute and expanded high-speed I/O. CM5 and CM4 share a similar module form factor, but the carrier interface and exposed capabilities are not identical; a CM4 carrier is not assumed to provide full CM5 functionality.

### 24.2 Recommended CM5 build

| Item | Recommendation | Reason |
|---|---|---|
| Module | CM5, 4 GB RAM for YOLO-nano/small tracking; 8 GB if running several models, ROS 2 and mapping together | Avoids paying for unused memory while leaving a path for larger perception software |
| Storage | eMMC variant for a fixed embedded demonstrator; Lite + retained microSD for fastest procurement | eMMC is more appliance-like; Lite is easier to swap and experiment with |
| Carrier | CM5IO for desk/bench integration; separate custom carrier for the airborne package | CM5IO is large development hardware; the custom carrier can expose only CSI, USB/UART, power, storage and cooling needed by the vehicle |
| Camera connection | CSI-2 FFC from camera to CM5 carrier | Lowest complexity for Pi camera modules and avoids FC bandwidth |
| Lidar connection | USB/UART/Ethernet to carrier depending module | CM5 can parse raw scans and build obstacle sectors/maps |
| FC connection | Dedicated 3.3 V UART with TX/RX/GND and optional CTS/RTS; MAVLink when using PX4/ArduPilot | Predictable, simple and independent from wireless/network availability |
| Power | Separate 5.1 V-class, 5 A-capable buck, with bulk capacitance, fuse/current limit and thermal validation | The CM5 datasheet specifies a single +5 V supply; camera/USB/perception loads create transient demand |
| Cooling | Carrier-level passive/active cooling as required by measured workload | YOLO and image processing are sustained loads, not just idle Linux operation |

Do not attach the CM5 module directly to the FC through an improvised daughterboard, and do not mount a CM5IO on the flight-control PCB. If a custom carrier is required, use the official [CM5 design files](https://www.raspberrypi.com/documentation/computers/compute-module.html) as a reference and treat it as its own PCB workstream.

### 24.3 CM5-to-FC data ownership

```text
Camera CSI-2 ──> CM5 capture ──> YOLO/tracker ──> object/target data
Lidar USB/UART/Ethernet ──> CM5 parser ──> obstacle sectors/map
FC IMU/GNSS/health ── MAVLink or versioned link ──> CM5 context
CM5 high-level result ──> FC validation ──> position/velocity/avoidance action
FC ──> CM5: attitude, position, battery, arming and health telemetry
```

The CM5 may perform:

- object detection and classification;
- object tracking and relative bearing estimation;
- camera recording and image compression;
- lidar scan filtering, sector reduction, mapping and logging;
- visual odometry or optical-flow processing if the camera and calibration support it;
- mission logic, path planning and high-level setpoint generation;
- a telemetry/data gateway to the ground station.

The CM5 must not perform the only copy of the inner rate loop, the only arming decision, direct motor PWM/DShot generation, or the only RC-loss failsafe. A CM5 message must carry a timestamp/sequence, frame definition, validity/confidence and timeout policy. The FC rejects stale, malformed, out-of-range or frame-inconsistent commands.

PX4 documents companion-computer collision prevention using offboard sensor data and `OBSTACLE_DISTANCE`; ArduPilot documents MAVLink companion computers and rangefinder/proximity paths. Those interfaces are the correct integration direction, but a single camera or single-point lidar does not guarantee all-direction collision avoidance. See [PX4 collision prevention](https://docs.px4.io/main/en/computer_vision/collision_prevention), [PX4 companion connection](https://docs.px4.io/main/en/companion_computer/pixhawk_companion), [ArduPilot companion computers](https://ardupilot.org/dev/docs/companion-computers.html), and [ArduPilot object avoidance](https://ardupilot.org/copter/docs/common-object-avoidance-landing-page.html).

---

## 25. Final Pixhawk-style modular architecture

### 25.1 The decision

Rev A adopts a **hybrid, externally modular and internally deterministic** FC:

```text
                         ┌──────────────────────────────┐
                         │ External GNSS + compass      │
                         │ UART/I2C or DroneCAN          │
                         └──────────────┬───────────────┘
                                        │
┌──────────────┐  RC_IN      ┌──────────▼──────────┐  ESC_SIG       ┌──────────────┐
│ TX/RX module ├────────────►│ Custom FC Rev A     ├───────────────►│ ESC board    │──► motors
└──────────────┘             │ H743 + IMU + baro  │ signal/ground   │ power stage  │
                             │ control + failsafe │                 └──────┬───────┘
┌──────────────┐ TELEM1      └─────┬──────┬────────┘                        │
│ Telemetry    │◄──────────────────┘      │ POWER1 sense/5V                │
└──────────────┘                         │                                 │
                                  ┌──────▼──────┐                           │
                                  │ Power/PDB   │◄── LiPo high-current ─────┘
                                  └──────┬──────┘
                                         ├── filtered 5 V FC regulator
                                         └── separate 5 V CM5 regulator

┌───────────────────┐ COMPANION UART  ┌──▼─────────────────────┐
│ CM5 carrier       │◄───────────────►│ CM5                    │
│ CSI/USB/UART/etc. │                 │ YOLO/tracking/lidar   │
└───────┬───────────┘                 └──────────┬────────────┘
        │ CSI-2 camera                            │ USB/UART/Ethernet lidar
        ▼                                         ▼
   perception camera                         scanning/3-D sensor
```

The primary ICM-42688-P and BMP390 stay on the FC PCB. The external compass/GNSS, ESC, receiver, telemetry, CM5, scanning lidar and camera remain replaceable. A future remote IMU can be added only as a timestamped smart sensor node over CAN/DroneCAN; raw high-rate IMU signals must not be placed on an arbitrary long cable.

### 25.2 Bus selection

| Interface | Use | Why |
|---|---|---|
| SPI | Onboard ICM-42688-P, optional flash/SD and other local devices | Fast, deterministic, short PCB traces; do not expose the primary IMU bus as a general harness |
| I2C | Onboard BMP390 and short GPS/compass/low-speed accessory link | Simple multi-drop bus, but cable/connector capacitance and pull-ups must be calculated |
| UART | Receiver, GNSS, telemetry, simple lidar and FC↔CM5 MAVLink | Point-to-point and easy to debug; assign one physical UART per critical function |
| CAN/DroneCAN | Remote smart sensors, power node, GNSS/compass, lidar or CAN ESC | Differential and robust for external modules; use line topology and two end terminations |
| PWM/DShot | FC to external ESC board | Signal-only actuator interface; DShot preferred when both sides support it |
| USB/CSI-2/Ethernet | CM5 camera and high-volume lidar/perception data | Keeps image/point-cloud bandwidth off the FC |

### 25.3 Connector family and proposed pin contract

The preferred FC low-current connector family is **JST GH 1.25 mm, keyed and latching**, or an equivalent locking family. This is a mechanical and harness recommendation, not a claim of Pixhawk compatibility. Exact Pixhawk compliance requires the selected DS-009/related standard revision and its full pinout/mechanical rules. Use the [Pixhawk standards overview](https://pixhawk.org/standards/) and [Pixhawk Standards repository](https://github.com/pixhawk/Pixhawk-Standards) as the governing reference if that route is selected.

| Port label | Logical signals | Connector guidance | Notes |
|---|---|---|---|
| `POWER1` | `5V_FC`, `GND`, `VBAT_SENSE`, `CURR_SENSE`, `PWR_STATUS`, `SPARE` | 6-pin keyed low-current connector | Regulated 5 V and measurement only; no battery current through FC |
| `ESC_SIG` | `M1`, `GND`, `M2`, `GND`, `M3`, `GND`, `M4`, `GND` | 8-pin keyed connector | Signal-only harness; no `VBAT` pin; use separate explicitly specified auxiliary power if required |
| `RC_IN` | `5V_AUX`, `GND`, `FC_RX`, `FC_TX` | 4-pin keyed connector | CRSF/ELRS/S.Bus choice and voltage must come from receiver team |
| `GPS1` | `5V_AUX`, `GND`, `FC_TX`, `FC_RX`, `SCL`, `SDA` | 6-pin, or larger if PPS/status is required | External GNSS+compass; exact Pixhawk GPS compatibility is not assumed |
| `CAN1`, `CAN2` | `5V_AUX`, `CANH`, `CANL`, `GND` | 4-pin keyed connector | Switchable 120 Ω termination, controlled stubs and labelled bus end |
| `TELEM1` | `5V_AUX`, `GND`, `TX`, `RX`, `CTS`, `RTS` | 6-pin keyed connector | Telemetry radio supply current is budgeted separately |
| `COMPANION` | `3V3_REF`, `GND`, `FC_TX`, `FC_RX`, `CTS`, `RTS` | 6-pin data connector | CM5 carrier has separate 5 V supply; no back-power through this port |
| `LIDAR_FC` | `5V_AUX`, `GND`, `TX`, `RX` | 4-pin keyed connector | Downward scalar rangefinder only after level/driver verification |
| `AUX_UART` | Explicitly rated supply, `GND`, `TX`, `RX` | 4-pin keyed connector | Future function must be documented before population |
| `SWD/DEBUG` | `SWDIO`, `SWCLK`, `NRST`, `3V3_REF`, `GND`, optional `SWO` | Test pads/Tag-Connect/1.27 mm header | Must remain accessible after all modules are attached |

Do not use the OpenESC 8-pin battery-inclusive harness pinout on this FC. OpenESC’s own documented 8-pin JST-SH connector carries `+BATT`, `GND`, current sense and four motor lines for its 4-in-1 ESC. That can be correct on the ESC board and still be unsafe on a logic-only FC. The ESC team must provide a separate mating harness drawing.

---

## 26. ESC, motors, battery and power research

### 26.1 FC-to-ESC protocol decision

Use four signal-level DShot channels as the first digital interface if the selected ESC supports them. DShot provides a defined digital command frame and can use the same line for bidirectional telemetry on supported firmware. [Betaflight’s DShot documentation](https://github.com/betaflight/betaflight.com/blob/master/docs/development/API/Dshot.mdx) describes the bidirectional line and rate trade-offs.

| Option | Benefits | Cost/risk | Rev A position |
|---|---|---|---|
| PWM | Easy oscilloscope bring-up and broad ESC compatibility | Less command integrity/telemetry; calibration concerns | Bring-up fallback |
| DShot300/600 | Digital command, no throttle calibration, supported by common firmware | Requires exact timer/DMA/output mapping; bidirectional mode changes timing | Preferred initial actuator protocol if teammate’s ESC supports it |
| Bidirectional DShot | eRPM/EDT feedback for filtering and diagnostics | Both firmware sides, line direction/timing and noise must be validated | Stretch after one-way DShot works |
| CAN/DroneCAN ESC | Robust multi-drop data and richer node status | More firmware, transceiver/node requirements and integration effort | Future or deliberate alternate architecture, not an unplanned addition |
| Separate telemetry line | May expose ESC data without bidirectional DShot | More pins/protocols and firmware work | Only if the exact ESC requires it |

The FC output reset state must be low/disabled or otherwise safe, and must remain safe through MCU reset, brownout, USB power, RC loss, CM5 loss and disarm. The FC only sends commands; it does not switch motor phases.

### 26.2 ESC workstream hand-off requirements

The ESC/motor team must provide:

1. battery cell-count range and fully charged input voltage;
2. per-channel continuous and burst current, test temperature and cooling conditions;
3. exact motor/propeller test data or manufacturer thrust/current tables;
4. DShot/PWM/CAN protocol, logic level, rate and reset behavior;
5. exact connector MPN, pin order, mating cable and ground return;
6. whether bidirectional DShot/EDT/separate telemetry is supported;
7. current/voltage shunt location and output scaling for FC ADCs;
8. BEC/5 V output rating and whether it may power FC, receiver, lidar or CM5;
9. firmware, bootloader and programming method; [AM32](https://github.com/am32-firmware/AM32) is an open ESC-firmware reference, not an automatic compatibility guarantee;
10. a propeller-off bench test procedure and current limit.

The [OpenESC-20x20 project](https://github.com/OpenDrone-hw/OpenESC-20x20) is a valuable reference because it documents a 4-in-1 AM32 ESC, 2–6S operation, 40 A/channel class, current sensing and a separate high-current board. Its exact MOSFET/gate-driver/shunt/regulator design should be treated as that board’s design, not a generic recipe for the teammate’s ESC.

### 26.3 Motor and propeller selection

The project cannot choose an exact motor from KV alone. The correct sequence is:

```text
Measure dry vehicle + payload + carrier + battery
        ↓
Choose propeller diameter allowed by frame and target noise/efficiency
        ↓
Select 4S/6S and motor KV class
        ↓
Use the manufacturer thrust/current table for that prop and voltage
        ↓
Check total thrust, peak current, ESC temperature and flight time
        ↓
Freeze motor + prop + ESC + battery as one matched set
```

Use `MTOW` for all-up mass including the CM5 carrier, cooling, CSI camera, lidar, wiring, battery mount and any FPV VTX. For a four-motor vehicle:

```text
T_hover_each = MTOW × g / 4
T_total_max target >= 2 × vehicle weight
I_ESC_continuous >= measured motor current with thermal margin
I_battery_peak >= sum of four peak motor currents with wiring/regulator margin
```

The 2× total-thrust value is an engineering target for control margin, not a certification requirement. Choose the actual margin with the instructor/team after the airframe is known.

Candidate classes:

| Platform | Candidate class | Starting interpretation |
|---|---|---|
| Light 5-inch FPV | T-Motor F60 Pro V 2207.5 or EMAX ECO II 2207 class | 1750–1950 KV is a common 6S direction; 2400–2550 KV is a common 4S direction; verify exact prop data |
| Payload/sensor 7–10 inch quad | EMAX ECO II 2810/2814 or comparable lower-KV motor | More plausible for CM5 + camera + lidar; exact KV/prop depends on MTOW and desired endurance |
| Larger UAS/UAM-style demonstrator | Larger low-KV propulsion system | Cannot be responsibly selected until frame, MTOW, prop diameter and battery voltage are supplied |

Reference pages: [T-Motor F60 Pro V](https://tmotorhobby.com/goods.php?id=1183), [EMAX ECO II 2207](https://emaxmodel.com/products/emax-eco-ii-series-2207-3-6s-1700kv-1900kv-2400kv-2750kv-brushless-motor), and [EMAX ECO II 2814](https://shop.emaxmodel.com/products/emax-ecoii-2814-730kv-830kv-brushless-motor-for-rc-drone). These are sourcing references, not a final order list.

### 26.4 LiPo and power tree

LiPo is a suitable propulsion battery, but a physically larger pack can make the aircraft heavier than the energy it adds. A 6S pack is 22.2 V nominal and 25.2 V fully charged. Rev A should not route this high-energy path through the flight-controller PCB.

```text
4S/6S LiPo
  ├── fuse/anti-spark/current protection as appropriate
  ├── short high-current path ──> PDB/4-in-1 ESC ──> motors
  ├── external filtered 5 V FC regulator ──> FC POWER1
  └── separate buck, 5.1 V-class / 5 A-capable ──> CM5 carrier

FC POWER1 ──> protection/load switch ──> 5V_SYS
5V_SYS ──> 3V3_DIG ──> H743 and digital peripherals
5V_SYS ──> low-noise sensor LDO/filter ──> ICM-42688-P
External PDB/shunt ──> scaled VBAT/CURR outputs ──> FC ADCs
```

For planning, a 25 W CM5 output at 90% efficiency is approximately 27.8 W from the battery: about 1.9 A at 4S nominal or 1.25 A at 6S nominal. The actual current changes with workload and conversion efficiency. The CM5 carrier regulator must be checked for input transients, thermal dissipation, cable drop, USB/camera load and brownout behavior.

Tattu’s published battery tables illustrate the mass trade-off: small high-C 6S 1200/1400 mAh packs are around 200–222 g in the cited FPV range, while a 6S 5000 mAh 60C pack is listed around 755 g. See the [Tattu FPV battery brochure](https://www.genstattu.com/content/instock/rc_product_brochure.pdf) and [current R-Line listings](https://genstattu.com/tattu-r-line-version-5-0-batteries/?page=2). Do not order a “big” battery until the selected motor/prop/ESC set can lift its mass with the required margin.

---

## 27. Lidar module shortlist and integration choice

### 27.1 Important distinction

A downward or forward single-point time-of-flight sensor returns one range along one beam. It is useful for height above ground, landing, terrain following or a single-direction stop cue. It is not equivalent to a 360° or 3-D obstacle map. For collision prevention, the system needs a scan, multiple directional sensors, a depth camera, or a CM5 perception algorithm that is validated in the flight stack.

### 27.2 Candidate modules

| Module | Published capability | Interface | Approx. mass/form factor | Best use here | Main limitation |
|---|---|---|---|---|---|
| [Benewake TF-Luna](https://en.benewake.com/TFLuna/index_proid_328.html?proid=329) | 0.2–8 m, up to 250 Hz, ≤0.35 W | UART/I2C/I/O | Small, under 5 g class | Downward altitude/landing on `LIDAR_FC` | Single beam, surface/lighting limits, verify signal level |
| [Benewake TFmini-S](https://en.benewake.com/TFminiS/index.html?proid=325) | 0.1–12 m, configurable up to 1 kHz | UART/I2C/I/O | 42×15×16 mm, about 5 g | Downward or one-direction range | Not a surrounding obstacle sensor |
| [Benewake TF02-i](https://en.benewake.com/TF02i/index.html?proid=861) | 0.1–40 m, up to 100 Hz conservative design value | CAN/RS-485 | 69×40.5×31.25 mm, about 60 g | Robust external forward/downward range node | Heavier and higher-power than TF-Luna/TFmini-S |
| [LightWare SF20/C](https://lightwarelidar.com/shop/sf20-c-100-m/) | 0.2–100 m, up to thousands of readings/s depending mode | USB/UART/I2C | About 7.5 g | High-quality single-beam range/altitude | Cost; one beam still is not a map |
| [LightWare SF45/B](https://lightwarelidar.com/shop/sf45-b-50-m/) | 320° scan, 0.2–50 m, high-rate scan modes | USB/UART/I2C | About 59 g | A single scanning lidar for obstacle sectors | Expensive; mounting/scan geometry and sunlight tests required |
| [RPLIDAR A1](https://www.slamtec.com/en/lidar/a1spec) | 360° planar, about 0.15–12 m, about 5.5 Hz | UART, 3.3 V logic | About 170 g | Indoor mapping/large prototype demonstration | Heavy, power-hungry for a small CM5 quad; planar only |
| [RPLIDAR S2](https://www.slamtec.com/en/s2/spec) | 360° planar, longer-range variants, about 10 Hz | High-speed UART/Ethernet | Larger/heavier class | Larger platform mapping | Cost, mass, power and planar coverage |
| [Livox Mid-360](https://www.livoxtech.com/de/mid-360/specs) | 3-D 360° scan, 40–70 m depending reflectivity, 200 kpts/s | Ethernet | About 265 g, 6.5 W | 3-D mapping/SLAM research | Too heavy/power-hungry for a small first airborne prototype |
| [ARK DIST SR/MR via PX4](https://docs.px4.io/main/en/sensor/rangefinders) | 8 cm to roughly 30/50 m | DroneCAN/UART | Compact smart-node class | Robust FC-connected range node | Availability/cost and exact integration need checking |

### 27.3 Decision for the team

Choose one explicit purpose before buying:

- **Altitude/landing:** TF-Luna or TFmini-S pointed downward, direct to `LIDAR_FC` UART. This is the simplest FC integration and can support height/landing features if the selected firmware driver is available.
- **Collision/obstacle perception:** SF45/B, RPLIDAR or a CM5-compatible depth/scan device connected to CM5. The CM5 converts raw measurements into obstacle sectors, distance messages or high-level avoidance data.
- **Longer industrial range:** TF02-i or an equivalent CAN/RS-485 module when its mass and mounting are acceptable.

PX4’s [distance-sensor documentation](https://docs.px4.io/main/en/sensor/rangefinders) and ArduPilot’s [rangefinder setup](https://en.ardupilot.org/copter/docs/common-rangefinder-setup.html) confirm UART/I2C/CAN connection patterns. ArduPilot distinguishes a single rangefinder from a proximity sensor in its [proximity documentation](https://en.ardupilot.org/copter/docs/common-proximity-landingpage.html); that distinction should be preserved in the project report and presentation.

---

## 28. Camera and FPV module shortlist

### 28.1 Camera roles

There are two different camera requirements:

1. **Perception camera:** feeds CM5 for YOLO, tracking, mapping, visual odometry or recording.
2. **Pilot FPV camera:** provides very low-latency video through an analog or digital VTX/goggle system.

One device may not satisfy both roles without an explicitly supported video-ingest path. Do not connect an analog FPV camera to an FC UART and expect the CM5 to receive frames.

### 28.2 Candidate modules

| Camera | Key capability | Interface/role | Recommendation |
|---|---|---|---|
| [Raspberry Pi Camera Module 3 Wide](https://www.raspberrypi.com/products/camera-module-3/) | 12 MP Sony IMX708, autofocus/HDR, 120° wide variant, 1080p50/720p120 modes | CSI-2 to CM5 | Default first YOLO/detection/recording camera; calibrate wide-angle distortion |
| [Raspberry Pi Global Shutter Camera](https://www.raspberrypi.com/products/raspberry-pi-global-shutter-camera/) | Sony IMX296, 1456×1088 up to 60 Hz, global shutter | CSI-2 to CM5 | Prefer for fast motion, optical flow or visual odometry; lower resolution |
| [Raspberry Pi HQ Camera](https://www.raspberrypi.com/products/raspberry-pi-high-quality-camera/) | 12.3 MP IMX477, C/CS or M12 lens options | CSI-2 to CM5 | Use when lens/optical selection matters; heavier and more mechanical work |
| [Raspberry Pi AI Camera](https://www.raspberrypi.com/products/ai-camera/) | IMX500 with on-module neural accelerator | CSI-2 to CM5 | Optional lower-load inference path without an AI HAT; model packaging/software adds scope |
| [RunCam Phoenix 2](https://shop.runcam.com/runcam-phoenix-2/) | Analog CVBS, 1000 TVL, low-latency FPV, 5–36 V, about 9 g | Separate analog VTX | Pilot FPV camera only; good if the team has an analog VTX/goggles path |
| [HDZero Nano90 V2](https://docs.hd-zero.com/camera-nano90-v2) | Digital FPV camera, 720×540/90 or 960×720/60, low-latency HDZero system | HDZero VTX/goggles ecosystem | Pilot FPV option; proprietary system and rolling shutter |
| [Caddx digital FPV comparison](https://www.caddxfpv.com/pages/product-comparison) | Digital FPV camera/VTX options, higher-resolution video | Proprietary VTX/goggles ecosystem | Pilot FPV option; not automatically a CM5 CSI input |

### 28.3 Decision for the project

Use **Camera Module 3 Wide** as the default CM5 perception camera if the priority is the fastest path to YOLO/tracking/recording. Use the **Global Shutter Camera** if visual odometry or fast-motion measurement matters more than image resolution. Use a dedicated analog/digital FPV camera only if the pilot needs a low-latency video link.

The camera team must provide the CM5 team with:

- camera model/lens/FOV and CSI cable length;
- resolution, frame rate, exposure and timestamp strategy;
- power/current requirement;
- lens distortion calibration and camera-to-body transform;
- whether output is detection, tracking, visual odometry, recording or pilot video;
- test scenes for blur, sunlight, vibration and propeller/arm occlusion.

The [Raspberry Pi camera documentation](https://www.raspberrypi.com/documentation/accessories/camera.html) should be used for FFC orientation, software configuration and supported modes.

---

## 29. Firmware, estimator and data-path recommendation

### 29.1 Recommended stack choice

Because the system needs external GNSS/compass, lidar, CM5/MAVLink, telemetry and possible avoidance, the preferred order is:

1. **ArduPilot-first** if the main demonstration is a broad vehicle autopilot with external rangefinder/proximity and companion-computer integration.
2. **PX4-first** if Pixhawk conventions, DroneCAN, ROS 2 and PX4 companion workflows are the assessment focus.
3. **Betaflight fallback** for the fastest manual/stabilized H743 hardware demonstration and DShot validation, not as the complete autonomy stack.

Do not attempt to write a complete new autopilot in less than one month. Use a minimal bring-up firmware or a mature stack’s board-port path. Udayate’s driver/EKF/visualizer repositories are excellent educational references, but their F411/LSM6DSL code is not a drop-in implementation for this H743/ICM-42688-P vehicle.

### 29.2 FC and CM5 data ownership

| Function | FC | CM5 | Required interface behavior |
|---|---|---|---|
| IMU sampling and rate loop | Owner | No | Local SPI, deterministic interrupt/timestamp |
| Attitude/rate control | Owner | No | CM5 cannot replace or gate the inner loop |
| Motor mixing and ESC commands | Owner | No | Safe output state on reset/disarm/failsafe |
| RC input and RC-loss failsafe | Owner | No | Dedicated receiver port, timeout and kill policy |
| GNSS/compass fusion | Main autopilot owner | May consume telemetry/context | External module transform/orientation documented |
| Downward scalar lidar | FC if direct | May log/forward | Sensor driver/voltage/update rate verified |
| Scanning/3-D lidar | Receives reduced result | Owner of parsing/filtering/map | Timestamp/frame/timeout and obstacle message contract |
| YOLO/tracking | Receives valid high-level result | Owner | Confidence and age are carried through |
| Mission/path planning | Executes validated setpoints | Computes proposal | FC bounds, timeout and mode gate every command |
| Logging | Flight-critical state/log trigger | High-volume image/point data | Logging failure never stops control |

### 29.3 Collision-avoidance boundary

For a CM5-based system, the safe data flow is:

```text
camera/lidar measurement
        ↓
CM5 calibration + timestamp + frame transform
        ↓
detector/tracker/scan filtering
        ↓
obstacle sectors / range message / high-level setpoint
        ↓
FC age/confidence/bounds/frame validation
        ↓
autopilot velocity/position constraint or rejection
```

The CM5 must not directly set four motor outputs. If the CM5 stops, the FC should either continue manual/stabilized flight or enter the explicitly selected autonomy-loss behavior. Collision prevention should be tested in a low-speed, controlled environment before any unrestricted flight.

---

## 30. Updated interface and procurement checklist

### 30.1 FC-side items to freeze

- STM32H743VIT6 package and exact boot/debug implementation;
- ICM-42688-P footprint, SPI pins, interrupt, chip-select and dedicated low-noise rail;
- BMP390 footprint, pressure vent and local bus;
- external GNSS/compass electrical contract;
- `POWER1` input voltage/current-sense scaling;
- `ESC_SIG` signal-only connector and four timer/DMA mappings;
- receiver protocol and `RC_IN` pinout;
- `TELEM1`, `COMPANION`, `LIDAR_FC`, `CAN1/CAN2` functions;
- connector family, mating housings, keying, pin-1 marking and cable drawings;
- external module supply budgets and hot-plug policy;
- SWD/USB/BOOT0/test points;
- four- or six-layer stack-up, sensor placement and power/ground planes.

### 30.2 External-module items to source or design

| Subsystem | First candidate direction | Procurement/design note |
|---|---|---|
| CM5 | CM5 4 GB or 8 GB plus CM5IO for bench; custom carrier later | Do not order a carrier before confirming CM5 variant, eMMC/Lite and CSI/USB needs |
| Perception camera | Camera Module 3 Wide; Global Shutter alternative | Camera and cable are CM5-side, not FC-side |
| Pilot FPV | RunCam Phoenix 2 analog or chosen HDZero/Caddx system | Separate VTX/goggles and power budget |
| Downward lidar | TF-Luna or TFmini-S | Direct FC UART after level/driver verification |
| Scanning lidar | SF45/B, RPLIDAR or larger-platform equivalent | CM5-side; validate mass, vibration and sunlight |
| Propulsion | 2207 class only for light 5-inch; 2810/2814 class for payload quad | Final selection requires MTOW/prop/voltage/test table |
| ESC | Teammate’s 4-in-1 board or OpenESC-style reference | Freeze signal protocol and power-source arrangement before FC routing |
| Battery | 4S/6S LiPo matched to propulsion | Capacity and C-rating are secondary to measured system current/mass |
| FC regulator | External known-good regulated 5 V power module for Rev A | Do not route raw LiPo through FC for the first board |
| CM5 regulator | Separate buck, 5.1 V-class, 5 A-capable, input-rated above full LiPo/transients | Measure thermal and brownout behavior under YOLO/camera/lidar workload |

### 30.3 Connector component examples

These are families/examples for procurement research, not final purchase authorization:

- JST GH board headers in the `SMxxB-GHS-TB` family with matching `GHR` housings/contacts, after checking pin count, current rating and exact footprint;
- JST-SH only where the mating external board explicitly requires it, such as a reference ESC harness;
- XT30/XT60, Micro-Fit or an equivalent appropriate high-current connector for the battery/propulsion harness, never a small FC signal connector for motor current;
- Tag-Connect or accessible SWD test pads for programming;
- USB-C receptacle with correct CC resistors and USB ESD protection.

The exact MPN must be checked against the actual supplier, footprint, mating housing, current, voltage, cable gauge, keying and stock before the BOM is released.

---

## 31. One-month execution plan with parallel team ownership

### Days 1–2: interface freeze

- measure or estimate airframe dry mass and payload;
- obtain the ESC team’s schematic, motor/prop table, battery cell count, connector and signal protocol;
- choose ArduPilot/PX4/Betaflight milestone;
- choose CM5 variant/carrier and camera role;
- choose lidar role: direct FC altitude or CM5 obstacle perception;
- issue one shared pinout and power-budget document.

### Days 3–6: FC schematic and firmware scaffold in parallel

- capture H743 power, reset, clock, SWD, USB and boot circuits;
- capture ICM-42688-P SPI/dedicated rail and BMP390;
- add external ports and protection;
- allocate timers/DMA/UART/CAN/ADC resources;
- start minimal sensor/USB/PWM firmware on a known H7 development platform if available;
- make CM5 carrier and perception teams prove camera capture and lidar parsing on the bench.

### Days 7–10: review and PCB layout

- complete ERC and datasheet review;
- place IMU/baro/MCU according to noise and mechanical reference rules;
- separate switching/power and sensor regions;
- route high-speed/clock/SPI/USB/CAN/UART with ground returns;
- place connectors with strain relief and pin-1 labels;
- run DRC, 3-D clearance and manufacturing checks.

### Days 11–14: fabrication and bring-up preparation

- export Gerbers, drill, BOM, pick-and-place and assembly drawing;
- order populated critical components and spares;
- prepare current-limited bench harness and loopback cables;
- prepare CM5 carrier/power bench harness;
- write the test matrix before the boards arrive.

### Days 15–21: FC bring-up

- inspect for shorts and orientation errors;
- power with current limiting and no ESC/motor connection;
- verify rails, reset, clock, SWD, USB and boot;
- read ICM-42688-P and BMP390 registers;
- test UART loopback, CAN two-node link, ADC sense and safe actuator output;
- log raw sensor data and check vibration/noise on a rigid bench fixture.

### Days 22–27: subsystem integration

- connect receiver and verify channel/failsafe/kill behavior;
- connect ESC board with props removed and current limits;
- test one-way DShot or PWM first; then bidirectional telemetry only if stable;
- connect GNSS/compass and calibrate orientation/offset;
- connect CM5 UART/MAVLink and validate timeout/rejection;
- connect camera and lidar, benchmark inference/latency and publish obstacle data only after timestamp/frame tests.

### Days 28–30: demonstration gate

- run the full propeller-off system test;
- capture power, temperature, sensor, RC, ESC, CM5 and failsafe evidence;
- perform a restrained rig/tether test only with instructor/team approval;
- document known limitations; do not describe the prototype as certified or collision-safe solely because software messages are flowing.

This schedule preserves the user’s required scope while making the first board a usable core. The external connector capability can be physically present before every external sensor has mature firmware.

---

## 32. Updated decision register

### Decisions now recommended/frozen

- custom bare STM32H743VIT6 FC, not a ready-made MCU/FC board;
- ICM-42688-P primary IMU on local SPI and dedicated low-noise rail;
- BMP390 onboard under a protected vent;
- external GNSS/compass;
- hybrid Pixhawk-style modular system;
- logic-only FC-to-ESC signal harness with ground returns;
- separate FC 5 V and CM5 5 V power paths;
- CM5 on a separate CM5IO/custom carrier;
- camera on CM5 via CSI-2/USB, not on the FC;
- scanning/3-D lidar on CM5; downward scalar lidar may be direct to FC;
- DShot-first actuator interface where the ESC supports it, PWM fallback;
- ArduPilot-first or PX4-first application path, selected before firmware pin mapping;
- controlled bench/rig first, no assumption of safe free flight.

### Decisions still requiring team data

1. exact MTOW, propeller diameter, motor KV, battery cell count and flight-time target;
2. exact ESC board connector, protocol, current/voltage sense and BEC arrangement;
3. receiver protocol and electrical levels;
4. CM5 RAM/storage/carrier variant;
5. camera role and exact module;
6. lidar role and exact module/mount orientation;
7. exact connector pinout: formal Pixhawk standard or clearly labelled project-specific contract;
8. final autopilot firmware and custom-board target/porting plan;
9. external-regulator ratings and thermal test results.

---

## 33. Sources added for this addendum

### Compute and companion integration

- [Raspberry Pi Compute Module hardware](https://www.raspberrypi.com/documentation/computers/compute-module.html)
- [Raspberry Pi CM5 datasheet](https://datasheets.raspberrypi.com/cm5/cm5-datasheet.pdf)
- [Raspberry Pi CM5IO](https://www.raspberrypi.com/products/compute-module-5-io-board/)
- [PX4 companion computers](https://docs.px4.io/main/en/companion_computer/pixhawk_companion)
- [PX4 companion Raspberry Pi connection](https://docs.px4.io/main/en/companion_computer/pixhawk_rpi)
- [PX4 collision prevention](https://docs.px4.io/main/en/computer_vision/collision_prevention)
- [ArduPilot companion computers](https://ardupilot.org/dev/docs/companion-computers.html)
- [ArduPilot object avoidance](https://ardupilot.org/copter/docs/common-object-avoidance-landing-page.html)

### Lidar and camera

- [Benewake TF-Luna](https://en.benewake.com/TFLuna/index_proid_328.html?proid=329)
- [Benewake TFmini-S](https://en.benewake.com/TFminiS/index.html?proid=325)
- [Benewake TF02-i](https://en.benewake.com/TF02i/index.html?proid=861)
- [LightWare SF20/C](https://lightwarelidar.com/shop/sf20-c-100-m/)
- [LightWare SF45/B](https://lightwarelidar.com/shop/sf45-b-50-m/)
- [PX4 supported rangefinders](https://docs.px4.io/main/en/sensor/rangefinders)
- [ArduPilot rangefinder setup](https://en.ardupilot.org/copter/docs/common-rangefinder-setup.html)
- [ArduPilot proximity sensors](https://en.ardupilot.org/copter/docs/common-proximity-landingpage.html)
- [Raspberry Pi Camera Module 3](https://www.raspberrypi.com/products/camera-module-3/)
- [Raspberry Pi Global Shutter Camera](https://www.raspberrypi.com/products/raspberry-pi-global-shutter-camera/)
- [Raspberry Pi HQ Camera](https://www.raspberrypi.com/products/raspberry-pi-high-quality-camera/)
- [Raspberry Pi AI Camera](https://www.raspberrypi.com/products/ai-camera/)
- [RunCam Phoenix 2](https://shop.runcam.com/runcam-phoenix-2/)

### ESC, motor and battery

- [Betaflight DShot API](https://github.com/betaflight/betaflight.com/blob/master/docs/development/API/Dshot.mdx)
- [AM32 firmware](https://github.com/am32-firmware/AM32)
- [OpenESC-20x20](https://github.com/OpenDrone-hw/OpenESC-20x20)
- [T-Motor F60 Pro V](https://tmotorhobby.com/goods.php?id=1183)
- [EMAX ECO II 2207](https://emaxmodel.com/products/emax-eco-ii-series-2207-3-6s-1700kv-1900kv-2400kv-2750kv-brushless-motor)
- [EMAX ECO II 2814](https://shop.emaxmodel.com/products/emax-ecoii-2814-730kv-830kv-brushless-motor-for-rc-drone)
- [Tattu FPV battery brochure](https://www.genstattu.com/content/instock/rc_product_brochure.pdf)
- [Tattu R-Line listings](https://genstattu.com/tattu-r-line-version-5-0-batteries/?page=2)

### Standards and open references

- [Pixhawk Reference Standards](https://pixhawk.org/standards/)
- [Pixhawk Standards repository](https://github.com/pixhawk/Pixhawk-Standards)
- [OpenFC-Lite-Mini](https://github.com/OpenDrone-hw/OpenFC-Lite-Mini)
- [HomeGliders FCV2](https://github.com/HomeGliders/FCV2)
- [Shirley-FC-Dev-Board](https://github.com/Bare-Metal-Foundry/Shirley-FC-Dev-Board)
- [Udayate](https://github.com/Ozonised/Udayate)
- [Udayate Kalman-AHRS](https://github.com/Ozonised/Kalman-AHRS)
- [Udayate LSM6DSL library](https://github.com/Ozonised/LSM6DSL-Platform-Independent-Library)
- [Udayate Quaternion Visualiser](https://github.com/Ozonised/Quaternion-Visualiser)
- [Pixhawk2.1 schematics](https://github.com/MRazgunas/pixhawk2.1)

---

## Final integrated recommendation

The project should proceed with a **custom bare STM32H743VIT6 hybrid Pixhawk-style FC**. Put the ICM-42688-P and BMP390 on the FC, expose keyed external ports for the ESC signal harness, receiver, GNSS/compass, telemetry, CAN, direct downward lidar and CM5 data, and keep battery/motor current on the separate ESC/PDB workstream. Use a separate CM5 carrier and a separate 5 V regulator for YOLO, tracking, camera, scanning lidar and high-level collision/mission logic. Use a dedicated low-latency FPV camera/VTX only if pilot video is also required.

The two most important integration rules are:

1. **CM5 does perception and high-level logic; the FC remains the real-time flight and failsafe authority.**
2. **The FC-to-ESC connector carries signals and grounds, not raw battery current.**

Do not freeze the exact motor, ESC, battery, lidar, camera or connector pinout until the responsible teams return their mass, voltage, protocol, current, mounting and cable information. Once those contracts are supplied, the schematic, KiCad hierarchy, PCB placement/routing review, BOM and bring-up test plan can be generated around them and independently verified at the bench.
