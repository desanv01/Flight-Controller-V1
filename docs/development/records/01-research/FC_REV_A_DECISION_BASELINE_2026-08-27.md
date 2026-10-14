> Historical technical record. Names and private workstation/session references were neutralized for publication. Dates and assertions describe the recorded stage, not current physical qualification. See the current validation-status page for later checks.

# Flight Controller Rev A — Decision Baseline and Interface Contract

Date: 2026-08-27

Revision note: this revision adds the Pixhawk-style modular connectivity decision and the external-port contract. The current addendum also fixes the companion-computer definition to Raspberry Pi Compute Module 5 (CM5), and adds the ESC, motor, LiPo/power, lidar and camera integration boundary.

## Authority and scope

The current user message is the controlling instruction set. The earlier research report is background/reference material; its section numbering, recommendations, and preliminary BOM are not fabrication instructions. This is a student prototype plan, not an aircraft-certification or ready-to-fly approval.

## Decisions now treated as fixed

- The flight controller must be a custom PCB containing a bare MCU chip and the surrounding components. No ready-made MCU/FC development board is the final flight controller.
- The first design should clone/adapt a proven open DIY/reference design wherever practical, because the implementation window is less than one month.
- The FC, ESC/motor board, transmitter/receiver, camera attachment, and lidar attachment are separate team workstreams and must be joined through an explicit interface contract.
- Raspberry Pi Compute Module 5 (CM5) is the optional companion computer. A standard Raspberry Pi 5 SBC is not the selected airborne form factor. CM5 must be mounted on a separate CM5IO/custom carrier board; it must not be soldered directly onto the FC PCB and must not be required for the FC's basic stabilization or RC-loss response.
- The FC shall use a Pixhawk-style, system-level modular architecture: ESCs, receiver, telemetry, CM5 carrier, GNSS/compass, CAN peripherals, and applicable lidar/auxiliary sensors connect through keyed external ports rather than being permanently soldered to the FC assembly.
- Rev A shall use a hybrid sensor boundary: the primary high-rate IMU and barometer stay on the FC PCB; the compass/GNSS and other replaceable or noise-sensitive peripherals are external. A remote IMU/barometer is a future sensor-node option, not a raw long-cable Rev A connection.
- The FC is a logic-and-sensing board, not the propulsion power-distribution board: the FC receives regulated 5 V and measurement signals, while battery current, motor phases, ESC switching heat and high-current copper remain on the separate ESC/power assembly.
- The preferred low-current external connector family is a keyed/latching JST-GH 1.25 mm family or an electrically equivalent locking family. This is a project-level recommendation; the board is called Pixhawk-inspired until the exact Pixhawk standard revision and pinout are deliberately followed and verified.
- The perception split is fixed for Rev A: camera data and scanning/3-D lidar data are processed on CM5; only validated, time-bounded results or high-level setpoints cross to the FC. A downward scalar rangefinder may connect directly to the FC when its voltage/protocol/driver are verified.
- The first flight milestone is a controlled bench/rig demonstration. Propeller-off tests, current limiting, inspection, and instructor/team approval are required before any powered flight test.

## Working hardware baseline — provisional until parts are frozen

Use the H7/Shirley architecture as the closest starting point, with OpenFC and Betaflight layout rules as cross-checks:

- STM32H743VIT6, bare LQFP MCU, with USB, SWD, boot/reset, debug test points, and enough UART/SPI/I2C/CAN resources.
- ICM-42688-P as the primary high-rate IMU on SPI, with its own low-noise sensor supply and a dedicated chip-select/interrupt connection.
- BMP390 on I2C; external magnetometer/GNSS preferred so the magnetic sensor is physically separated from switching power and motor wiring.
- Four motor outputs required for the quad; reserve a clean eight-output-capable timer map only if it does not compromise the first board.
- Regulated 5 V input from the power/ESC side for Rev A, USB-C as a protected bench/debug input, and separate digital/sensor regulation. Do not route motor current through the FC.
- External flash or microSD logging only if it can be implemented without delaying the minimum FC bring-up.

These parts remain recommendations, not purchase authorization. Exact MPN, package, footprint, availability, voltage, current, and firmware support must be checked before the schematic is released.

## Modularity decision

### What “Pixhawk-style modular” means for this project

The project should copy the *system principle* of Pixhawk: a small real-time flight-control core with standardized, labeled, replaceable external interfaces. It does not mean that every sensor IC must be physically outside the FC, and it does not automatically make the custom board electrically compatible with a Pixhawk. The official Pixhawk standards cover pinouts, architecture, PCB guidance, and connector specifications; exact compatibility requires following the selected standard revision rather than merely using the same connector family.

The practical Rev A boundary is:

```text
ON THE FC PCB                         EXTERNAL / REPLACEABLE MODULES
----------------                      -----------------------------
STM32H743 + power                    ESC / motor board
Primary ICM-42688-P IMU              RC receiver
BMP390 barometer                     GNSS + external compass
USB-C / SWD / boot                   Telemetry radio
CAN transceiver(s)                   Raspberry Pi CM5 + carrier
ADC protection                       Downward or simple lidar
                                     Scanning lidar and camera via CM5
```

This is “externally modular, internally deterministic.” It satisfies the team’s modular connection requirement while keeping the sensor data used by the fastest stabilization loop on short, controlled PCB traces.

### Architecture options considered

| Option | FC-board contents | Advantages | Main risks/costs | Rev A decision |
|---|---|---|---|---|
| Fully modular raw-sensor FC | MCU and power only; IMU, barometer, compass, GNSS and other sensors are all external | Maximum replaceability, easy physical separation, very visible modularity | Remote SPI/I2C wiring, cable capacitance/EMI, connector failure, extra latency and timestamp uncertainty, sensor-frame/alignment work, more firmware, no local sensor for reliable boot/bring-up | **Reject for Rev A** |
| Hybrid Pixhawk-style FC | MCU, primary IMU and barometer on board; ESC, receiver, GNSS/compass, CM5, telemetry, CAN and suitable lidar external | Good control-loop integrity, external compass placement, serviceable team interfaces, realistic firmware and PCB scope | More connectors and protection than a compact FPV FC; still requires precise port and firmware definition | **Adopt for Rev A** |
| Mostly onboard FC | MCU and most sensors on board; only ESC, receiver and CM5 external | Lowest connector count and simplest harness | Compass is closer to switching/motor fields; less serviceable; conflicts with the separate sensor workstreams | **Not the selected architecture** |

### Why the primary IMU stays onboard

The rate loop depends on frequent, time-consistent gyro/accelerometer samples. A local SPI IMU gives short traces, a controlled return path, a known mechanical relationship to the FC, and a predictable interrupt/timestamp path. A remote IMU is possible, but it should be a complete smart sensor node with its own MCU, timestamping, calibration and CAN/DroneCAN interface. It should not be a bare IMU hanging from a long unbuffered SPI or I2C cable.

The onboard IMU is therefore a reliability and schedule decision, not a rejection of modular design. A future Rev B may add a second onboard IMU or a remote CAN IMU node if the firmware and validation plan justify it.

### Why the barometer stays onboard for Rev A

The BMP390 is low-rate compared with the IMU, but an onboard device avoids a second remote sensor protocol and connector. It must be placed under a protected vent, away from direct prop wash and pressure disturbances. If the airframe requires a physically remote pressure location, use a dedicated external sensor node with a documented pressure inlet and CAN/UART interface; do not simply extend a raw I2C cable without checking bus capacitance and rise time.

### Why the compass/GNSS is external

The compass benefits from being physically separated from battery conductors, motor phases, ESC switching currents, inductors and ferromagnetic hardware. GNSS also needs antenna placement and sky visibility that the FC PCB cannot guarantee. The preferred module is an external GPS/compass unit connected by UART plus I2C, or by DroneCAN where a compatible node is available. Its mounting orientation and position relative to the FC must be documented for firmware calibration and frame transforms.

## Modular bus and connector strategy

### Bus selection

| Bus/interface | Rev A use | Cable rule | Design decision |
|---|---|---|---|
| SPI | Primary onboard IMU, memory, SD, and other local devices | Keep on the PCB or on a very short, mechanically retained daughterboard; route over a continuous return path | Do not expose the high-rate IMU SPI bus as a general long harness |
| I2C | Onboard BMP390 and short external compass/low-speed accessory port | Treat as a short, low-speed bus; calculate total pull-up/cable/connector capacitance; make pull-ups selectable | Suitable for GPS/compass only when the cable and loading are verified |
| UART | RC receiver, GNSS, telemetry radio, simple lidar, and FC↔CM5 MAVLink/data link | Point-to-point; signal level must be compatible; include a ground return | Use dedicated labeled UART ports rather than one ambiguous expansion header |
| CAN / DroneCAN | Remote sensor nodes, external GNSS/compass, lidar nodes, and CAN-capable ESC/power modules | Differential pair, line topology, short stubs, 120 Ω termination only at the two bus ends | Preferred robust path for future smart external sensors |
| PWM/DShot | FC to the external ESC board | One defined signal and ground return per output; no motor current on this harness | Four outputs required; bidirectional DShot telemetry only if the selected firmware/ESC path supports it |
| USB/CSI-2/Ethernet | Camera and high-volume data on CM5 | Camera stays on CM5; do not route camera frames through the FC | FC gets only trigger/status or processed measurements when required |

NXP’s I2C specification treats wire, connector and pin capacitance as part of the bus capacitance and gives a 400 pF limit for the common Standard/Fast modes. TI’s long-cable guidance describes buffers/extenders for cases that exceed the normal bus loading. This is why an external compass on a short harness is reasonable, while a remote raw IMU on an arbitrary cable is not a good Rev A assumption. CAN is better suited to remote nodes: the CAN in Automation guidance calls for a line topology and 120 Ω termination at the two bus ends.

### Proposed logical port map

The names below are the design contract. The final connector family, pin order and MPN remain to be frozen after the ESC, receiver, GNSS/compass, lidar and power-board teams provide their exact requirements.

| Port label | Signals | Intended module | Important boundary |
|---|---|---|---|
| `POWER1` | Regulated 5 V, GND, scaled battery-voltage sense, protected current-sense input; optional power-status signal | ESC/power board or external power module | Logic/measurement only; motor and battery current paths do not pass through the FC PCB |
| `ESC_OUT` | `M1..M4` signal, signal grounds; optional telemetry returns or CANH/CANL on a separate CAN port | External ESC board | Use the exact PWM/DShot/CAN choice agreed with the ESC workstream; define reset/disable state |
| `RC_IN` | Module supply, GND, receiver UART RX; optional TX/telemetry | External transmitter/receiver assembly | Protocol and voltage must be frozen; FC owns RC timeout and arming/failsafe response |
| `GPS1` | Module supply, GND, GNSS UART TX/RX, PPS; optional I2C SDA/SCL for compass | External GNSS + compass module | A Pixhawk-compatible GPS port requires the exact selected Pixhawk pinout, not just a JST-GH connector |
| `GPS2/AUX_I2C` | Supply, GND, SDA/SCL, optional interrupt | Second GNSS/compass or short low-speed accessory | Pull-ups must be selectable; no assumption of unlimited cable length or hot-plugging |
| `CAN1`, `CAN2` | Supply, GND, CANH, CANL; optional shield/drain strategy | DroneCAN GPS/compass, lidar, power node or CAN ESC | Add switchable 120 Ω termination; use a bus backbone, not an uncontrolled star |
| `TELEM1` | UART TX/RX/GND; optional CTS/RTS | Ground telemetry radio or serial peripheral | 3.3 V logic; protect external signals; no high-current supply requirement |
| `COMPANION` | UART TX/RX/GND and optional CTS/RTS; optional Ethernet/USB only if separately designed | Raspberry Pi CM5 on a separate carrier | Data connector is not the CM5 power source; the carrier gets a separate filtered 5 V supply sized for the CM5 workload |
| `LIDAR_FC` | UART, I2C or CAN as selected, supply and GND | Downward scalar rangefinder or low-latency lidar | Direct FC connection is preferred for altitude/landing data when the flight stack supports the sensor |
| `AUX_UART` | UART TX/RX/GND, optional interrupt/status | Future rangefinder or sensor | One logical function per labeled port; do not silently share with receiver/GNSS |
| `AUX_SPI` | Short local SPI plus chip-select/interrupt/GND | Engineering daughterboard or future local sensor | Not a general long flight harness; use a local smart node for remote high-rate sensors |
| `SWD/DEBUG` | SWDIO, SWCLK, NRST, 3V3 reference, GND; BOOT0 test access | ST-LINK/debugger | Keep accessible even when all external modules are connected |
| `USB-C` | USB D+/D−, VBUS sensing/protected input, GND | Bench flashing/configuration/logging | USB power mux/protection must not create an uncontrolled back-power path |

### Connector rules

1. Use keyed, locking, vibration-tolerant connectors with a documented mating cable. Do not use loose Dupont jumpers for the flight harness.
2. Put at least one ground return beside fast or noise-sensitive signal groups. Keep CANH/CANL as a differential pair and keep their untwisted connector section short.
3. Print the port name, pin 1/index and signal names on the silkscreen or in an accompanying wiring drawing. “UART1” alone is not enough; label the function as `RC_IN`, `GPS1`, `COMPANION`, etc.
4. Separate power pins from signal groups and specify each port’s allowed voltage/current. A port’s accessory supply is not automatically a safe source for another team’s board.
5. Add ESD/overvoltage protection where the risk justifies it, especially on long external UART, CAN, USB and exposed power inputs. Keep protection placement close to the connector and verify its capacitance against the signal rate.
6. Make external-module power switching/current limiting a deliberate decision. Rev A does not assume safe hot-plugging; power down before changing a module unless that port is specifically designed and tested for hot-swap.
7. Use a continuous ground plane and controlled return paths on the FC. Use twisted/shielded wiring and physical separation from motor phases and battery leads where the harness is exposed to switching noise.
8. Put selectable I2C pull-ups and CAN termination on the appropriate side of the interface. Avoid duplicate strong pull-ups or duplicate CAN termination from multiple modules.
9. Give every external sensor a documented voltage level, protocol, address/node ID, orientation, position relative to the FC, cable length and maximum update rate.
10. Provide test points and a bench loopback/test cable for each critical external interface. The modular design must be testable without attaching the complete vehicle.

## Sensor and subsystem placement decisions

| Subsystem | Rev A placement | Connection approach | Reason |
|---|---|---|---|
| Primary IMU | On FC PCB, near the defined mechanical reference | Short dedicated SPI and interrupt traces, dedicated low-noise supply | Lowest latency and most deterministic rate-loop measurement |
| Barometer | On FC PCB under protected vent | Local SPI/I2C | Avoids remote-bus complexity; manage airflow and pressure port carefully |
| External compass | Separate GPS/compass module | I2C/UART or DroneCAN | Move magnetic sensing away from motor/ESC/battery fields |
| GNSS | External mast/module | UART + PPS/I2C or DroneCAN | Antenna visibility, physical separation and serviceability |
| Downward rangefinder | Direct FC if it supplies a scalar altitude measurement | UART/I2C/CAN | Lower delay for altitude/landing assistance; use CM5 only if the sensor interface requires it |
| Scanning/3-D lidar | External CM5-connected or CAN sensor | USB/UART/Ethernet to CM5, or smart CAN node | CM5 can filter scans, make sectors/maps and forward only useful data |
| Camera | On the CM5 side | CSI-2 or USB to CM5 | FC does not have the bandwidth or role for raw image frames |
| ESC/motor power stage | External ESC board | FC logic outputs and optional telemetry/CAN | Keeps high current, switching heat and motor noise out of the FC |

## Firmware impact of modularity

Modular connectors do not by themselves provide plug-and-play firmware. The selected flight stack must know which physical UART, SPI/I2C bus, CAN node, timer, ADC and interrupt correspond to each logical function. PX4 and ArduPilot both require board-specific configuration/port definitions for a new custom target. A strict Pixhawk connector pinout can reduce wiring ambiguity and improve ecosystem compatibility, but it does not eliminate custom board support work.

For the current firmware decision:

- Betaflight is the shortest route to manual/stabilized quad flight, but its strongest value is the local IMU + motor-output path; external GPS/compass/lidar/CM5 autonomy is not its most natural Rev A scope.
- ArduPilot is the strongest fit if the external GPS/compass, rangefinder/lidar and MAVLink companion path must participate in the vehicle behavior.
- PX4 is the strongest fit if exact Pixhawk/DroneCAN/companion-computer conventions and a PX4 ecosystem demonstration are central, but custom-board porting must be budgeted explicitly.

The FC must still fly and enter its RC-loss failsafe without CM5. Any CM5 setpoint, obstacle or vision message must have a timeout, validity check and defined rejection/failsafe behavior.

## System architecture

```text
 TX/RX receiver ──`RC_IN` UART──> custom FC ──`ESC_OUT` M1..M4 + GND──> ESC board ──> motors
                                      │
                                      ├── onboard primary IMU + barometer
                                      ├──`GPS1` UART/I2C or `CAN1`──> external GNSS/compass
                                      ├──`LIDAR_FC` or `CAN2`──> low-latency/downward lidar (if selected)
                                      ├──`COMPANION` UART──> Raspberry Pi CM5 + carrier (optional)
                                      │                         ├── camera via CSI-2 or USB
                                      │                         └── scanning lidar via USB/UART/Ethernet
                                      └──`TELEM1` / logging / debug

Power board/ESC board ──`POWER1` regulated 5 V + sense──> FC
Power board/ESC board ──separate filtered 5 V, 5 A-capable──> CM5 carrier board
```

The FC owns the deterministic inner loop: IMU sampling, attitude/rate estimation, PID/control allocation, motor output, RC input, arming, and failsafe. CM5 owns optional high-level work: camera capture/encoding, computer vision, mapping, heavy lidar processing, mission logic, data logging, and telemetry routing. Raw camera frames or a raw point cloud should not pass through the FC.

## Provisional interface contract

| Workstream | FC-side contract | Must be supplied before pinout freeze |
|---|---|---|
| ESC/motors | `ESC_OUT`: four signal outputs plus adjacent grounds; PWM/DShot/CAN and optional telemetry/current/voltage return | signal protocol, logic level, update rate, connector pinout, power-source arrangement, failsafe behavior |
| TX/RX | `RC_IN`: dedicated receiver UART, supply and GND; receiver is external; FC handles RC timeout and kill/arm policy | CRSF/ELRS/S.Bus/etc., baud rate, voltage, channel map, failsafe values, kill-switch channel |
| Raspberry Pi CM5 + carrier | `COMPANION`: dedicated 3.3 V UART TX/RX/GND, optional flow control; MAVLink if using PX4/ArduPilot, otherwise a versioned binary packet protocol | chosen firmware, baud rate, message ownership, setpoint timeout, time-sync method, carrier UART mapping; CM5 power must be separate |
| Camera | Camera connects to CM5 through CSI-2 or USB; FC receives only trigger/timestamp/status if needed | camera model, cable, power, frame rate/resolution, recording vs detection vs visual odometry |
| Lidar | `LIDAR_FC` or `CANx` for a downward scalar rangefinder; scanning/3-D lidar connects to CM5 or a smart CAN node and returns filtered distance/obstacle data | model, UART/I2C/CAN/USB interface, voltage, baud/data rate, orientation, field of view, altitude vs avoidance purpose |
| GNSS/magnetometer | `GPS1`, `GPS2/AUX_I2C`, or `CANx`; external module with GNSS on UART/PPS and compass on I2C/CAN as selected | module, protocol, supply, connector, cable length, physical location, orientation, calibration plan |
| Other external sensors | Labeled `CAN`, `AUX_UART`, or short `AUX_I2C`/daughterboard port; remote high-rate sensors require a local smart node | sensor type, update rate, bus loading, node ID/address, frame convention, cable length and timeout |

## CM5 operating rule

CM5 is optional for manual/stabilized flight. It may send high-level position/velocity/attitude requests or obstacle information, but the FC must reject stale/lost CM5 commands and remain able to disarm or enter a defined failsafe. The carrier gets its own filtered 5 V supply; CM5 is not powered through the FC telemetry header. Camera FFCs, USB peripherals, cooling and storage belong to the carrier subsystem, not to the FC connector contract.

## Source roles

- Shirley-FC-Dev-Board: closest H7 schematic/power/pinout/documentation baseline; its published design uses H743ZIT6, ICM-40609-D, MMC5983MA, BMP390 and GH1.25-style ports, so it is an architecture reference rather than an exact Rev A parts list.
- OpenFC-Lite-Mini: compact custom-chip Betaflight layout, dedicated IMU rail, ESC signal boundary, and manufacturing discipline.
- Betaflight manufacturer guidelines: high-rate SPI IMU, H7 timer/DMA/output, I2C barometer/magnetometer, and routing checks.
- Pixhawk hardware and Pixhawk2.1: system interfaces, connector conventions, and license-aware reference architecture.
- FCV2: KiCad project/hierarchy and connector-organization reference; inspect the archive and verify its exact electrical design before reuse, and do not treat it as the Rev A H743 sensor baseline.
- Udayate/Kalman-AHRS/Quaternion-Visualiser: educational firmware, estimator, driver-abstraction, and bench-visualization references; not a drop-in flight stack.
- Reddit and video sources: design-review warnings, failure modes, and project-scope evidence; not authoritative electrical specifications.

## Bring-up gates

1. ERC-clean schematic, verified pin map, power-tree calculations, footprints, and interface sign-off from all five workstreams.
2. PCB DRC/3-D/gerber inspection, test points, assembly drawing, and continuity checks.
3. Power-only bring-up: current-limited 5 V, rail measurements, reset/boot/SWD/USB, clock, and thermal check.
4. Sensor bring-up: SPI IMU, I2C barometer, calibration, timestamps, and logged raw data.
5. Modular-port bring-up: connector pinout/continuity, supply current, UART loopback, CAN two-node test with correct termination, I2C rise-time/loading check, and ESD/protection inspection.
6. RC/ESC bench test with props removed, output-mapping verification, and failsafe/kill test.
7. CM5/camera/lidar integration only after FC manual/stabilized bench behavior is known-good.

## Open decisions before schematic freeze

1. Choose whether Rev A will follow the exact Pixhawk Connector Standard pinouts or use a clearly labeled Pixhawk-inspired pinout. The same connector body alone is not compatibility.
2. Confirm the exact connector family, locking method, cable assembly and mounting/strain-relief approach.
3. Confirm ESC signalling: four PWM/DShot lines, bidirectional DShot telemetry, CAN ESC, or a defined combination.
4. Confirm receiver protocol and whether the receiver port supplies 5 V or only signal/reference power.
5. Confirm whether the lidar workstream needs a direct FC altitude input, a CM5 obstacle-processing path, or both.
6. Confirm the GNSS/compass module and decide UART+I2C versus DroneCAN.
7. Confirm that the primary IMU and barometer remain populated on the FC for Rev A; any external sensor-node experiment becomes a separate stretch target.
8. Select Betaflight, ArduPilot or PX4 early enough that the port map and driver support are checked before routing.

## Research references added for the modularity decision

- [Pixhawk Reference Standards](https://pixhawk.org/standards/) — standards scope, connector specifications and architecture guidance.
- [PX4 GNSS/GPS and compass setup](https://docs.px4.io/main/en/gps_compass/) — external GPS/compass connector patterns, UART/I2C/CAN choices and placement guidance.
- [PX4 magnetometer guidance](https://docs.px4.io/main/en/gps_compass/magnetometer) — external compass rationale and calibration considerations.
- [PX4 ARK CANnode](https://docs.px4.io/main/en/dronecan/ark_cannode) — example of a local sensor MCU/CAN-node approach for modular sensors.
- [PX4 companion-computer serial connection](https://docs.px4.io/main/en/companion_computer/pixhawk_companion) — serial electrical/interface considerations for Pixhawk-to-companion links.
- [ArduPilot companion computers](https://ardupilot.org/dev/docs/companion-computers.html) and [rangefinder setup](https://ardupilot.org/plane/docs/common-rangefinder-setup.html) — companion processing and direct external rangefinder roles.
- [NXP UM10204 I2C specification](https://community.nxp.com/pwmxy87654/attachments/pwmxy87654/nxp-designs/931/1/UM10204.pdf) and [TI long-cable I2C guidance](https://www.ti.com/kr/lit/pdf/sdaa306) — bus capacitance, rise time and extender boundaries.
- [CAN in Automation high-speed CAN guidance](https://www.can-cia.org/can-knowledge/can-hs-transmission) — line topology, bus length and 120 Ω termination guidance.

---

## Addendum — CM5, sensors, propulsion and modular-system decisions

This addendum is the current engineering interpretation of the user’s request. The linked reports and community projects remain reference material; they do not override these decisions or authorize copying a design without checking its license, electrical assumptions and measured evidence.

### Companion computer: use CM5 as a separate subsystem

“Raspberry Pi 5 computer module” should be written precisely as **Raspberry Pi Compute Module 5 (CM5)**. CM5 contains the Raspberry Pi 5-class BCM2712 computer, memory and optional eMMC, but it does not provide the normal Pi USB, HDMI, Ethernet or camera connectors. It uses two 100-pin high-density connectors and needs a carrier board. The official [Compute Module documentation](https://www.raspberrypi.com/documentation/computers/compute-module.html) describes CM5IO as both a development carrier and a reference for a smaller custom carrier.

The Rev A implementation is:

```text
Main LiPo
   ├── high-current PDB/ESC wiring ──> ESC board ──> motors
   ├── external filtered 5 V FC module ──> FC POWER1
   └── separate 5 V, 5 A-capable buck ──> CM5 carrier ──> CM5
                                            ├── CSI-2 camera
                                            ├── USB/UART/Ethernet lidar as selected
                                            └── cooling and storage

FC COMPANION UART <── MAVLink or versioned packet link ──> CM5 carrier UART
```

Do not solder the CM5 directly onto the FC. Do not use the FC telemetry header as the CM5 power source. Use CM5IO for a bench proof-of-concept if it is available, then make a separate custom CM5 carrier only if the final airborne packaging requires it. The CM5IO is a large development board, not the airborne carrier itself.

For the first perception experiment, a **4 GB CM5** is sufficient for a lightweight YOLO model, camera capture and a small tracking pipeline; select 8 GB if the team will run several models, ROS 2, large image buffers or simultaneous mapping. Prefer an eMMC variant for a fixed embedded installation, or a Lite variant with a properly retained microSD for the fastest prototype procurement. This is a procurement choice, not an FC schematic decision.

The CM5 carrier power target is a regulated 5 V rail with enough transient margin for the chosen workload. The CM5 datasheet gives a single +5 V input and typical operating consumption around 900 mA, while Raspberry Pi’s CM5IO guidance supports a 5 V / 5 A input for full peripheral use. Therefore the power tree should be designed around a **separate 5.1 V-class, 5 A-capable regulator**, verified against the exact carrier, cable drop, camera, USB load and thermal conditions. The regulator input must tolerate the fully charged LiPo and switching transients; a 6S pack reaches 25.2 V before transients.

The FC-to-CM5 link should be a dedicated 3.3 V UART with TX/RX, common ground and optional CTS/RTS. Start at a conservative tested baud rate, then increase to 921600 only after signal integrity and packet-loss testing. MAVLink is the preferred protocol when using PX4 or ArduPilot. The carrier’s UART must be mapped explicitly, the Linux serial console must be disabled or moved, and no 5 V signal may enter CM5 GPIO. A physical UART link is simpler and more predictable than making the FC depend on Ethernet or Wi-Fi.

### What CM5 does in this vehicle

The CM5 is appropriate for work that is computationally heavy, Linux-dependent or not required for immediate stabilization:

| CM5 function | Inputs | Output to FC | FC safety rule |
|---|---|---|---|
| YOLO object detection | CSI-2/USB camera frames | Object class, confidence, image position and timestamp | Informational until validated; never directly drives motor PWM |
| Object tracking | Camera detections plus motion model | Target bearing/relative motion or target ID | Reject stale detections and out-of-range commands |
| Lidar processing | USB/UART/Ethernet/serial scan or point data | Obstacle sectors, nearest obstacle or `OBSTACLE_DISTANCE`-type data | Require timestamp, frame orientation and timeout |
| Sensor fusion/perception | Camera, lidar, FC attitude/GNSS over MAVLink | Relative pose, obstacle map or landing cue | FC validates message age, frame and bounds |
| Mission/path logic | GPS, map, operator commands and perception | High-level position/velocity/setpoint requests | FC remains the authority for arming, attitude/rate control and failsafe |
| Recording/telemetry gateway | Camera, FC logs and network | Stored evidence or ground link | Logging failure must not stop the inner loop |

The FC continues to own IMU sampling, state estimation needed for stabilization, attitude/rate control, mixer/control allocation, motor outputs, RC loss, arming and emergency disarm. The CM5 may be powered off and the vehicle must still enter a safe non-autonomous/manual state.

PX4 documents companion-computer collision prevention through offboard sensor data and `OBSTACLE_DISTANCE`; ArduPilot documents companion computers using MAVLink and supports rangefinders/proximity sensors for avoidance. These interfaces make the CM5 useful, but they do not make a single camera or single-point lidar a complete collision-avoidance system. See [PX4 collision prevention](https://docs.px4.io/main/en/computer_vision/collision_prevention), [ArduPilot companion computers](https://ardupilot.org/dev/docs/companion-computers.html), and [ArduPilot rangefinder/proximity documentation](https://ardupilot.org/copter/docs/common-rangefinder-setup.html).

### Rev A connector recommendation

Use a keyed/latching **JST-GH 1.25 mm family** for low-current FC external ports, or an equivalent locking connector with the same documented mechanical and electrical properties. The connector family is recommended because it is compact and commonly used in Pixhawk-style avionics harnesses; it does not by itself make this board Pixhawk-compatible. If the team claims exact compliance, follow the selected [Pixhawk connector standard](https://pixhawk.org/standards/) pin-for-pin and record the standard revision.

The following is the proposed project pin contract. It is a logical proposal until every team provides its mating-board schematic:

| Port | Proposed logical pins | Use and restriction |
|---|---|---|
| `POWER1` | `5V_FC`, `GND`, `VBAT_SENSE`, `CURR_SENSE`, `PWR_STATUS`, `SPARE` | Regulated 5 V and measurement only; no motor current and no raw battery on FC traces |
| `ESC_SIG` | `M1`, `GND`, `M2`, `GND`, `M3`, `GND`, `M4`, `GND` | Signal-only DShot/PWM harness; never copy an ESC battery pinout onto this FC connector |
| `RC_IN` | `5V_AUX`, `GND`, `FC_RX`, `FC_TX` | External CRSF/ELRS/S.Bus receiver after protocol and voltage are frozen |
| `GPS1` | `5V_AUX`, `GND`, `FC_TX`, `FC_RX`, `SCL`, `SDA` | GNSS plus compass; add PPS on a larger connector only if firmware uses it |
| `CAN1/CAN2` | `5V_AUX`, `CANH`, `CANL`, `GND` | DroneCAN sensors/power nodes; switchable 120 ohm termination on the correct bus end |
| `TELEM1` | `5V_AUX`, `GND`, `TX`, `RX`, `CTS`, `RTS` | Telemetry radio; 5 V accessory current must be budgeted separately |
| `COMPANION` | `3V3_REF`, `GND`, `FC_TX`, `FC_RX`, `CTS`, `RTS` | Data-only CM5 link; CM5 carrier has its own 5 V regulator |
| `LIDAR_FC` | `5V_AUX`, `GND`, `TX`, `RX` | Downward scalar rangefinder; verify whether the sensor I/O is 3.3 V or 5 V before mating |
| `AUX_UART` | `3V3/5V as explicitly specified`, `GND`, `TX`, `RX` | Future sensor; one labeled function, not an unowned spare header |
| `SWD/DEBUG` | `SWDIO`, `SWCLK`, `NRST`, `3V3_REF`, `GND`, optional `SWO` | Accessible test pads or Tag-Connect; BOOT0 remains available |

`ESC_SIG` is intentionally different from the high-current ESC battery connector. A reference such as [OpenESC-20x20](https://github.com/OpenDrone-hw/OpenESC-20x20) uses an 8-pin JST-SH harness that includes battery positive, current and four motor lines for its own 4-in-1 board. That is an ESC-board power interface, not a safe reason to route battery positive through this FC. The ESC team must provide its own final harness drawing.

### ESC and motor integration contract

The first choice should be **four signal-level DShot outputs plus ground returns** if the ESC firmware supports DShot. Bidirectional DShot is useful for eRPM/telemetry and filtering, but only enable it after confirming that the exact flight stack, timer/DMA mapping, ESC firmware and signal wiring support it. Ordinary PWM is an acceptable bring-up fallback. CAN/DroneCAN ESC control is a separate architecture and should not be mixed into Rev A casually.

The ESC workstream must return these items before FC pinout freeze:

- battery cell-count range and absolute input voltage;
- continuous and burst current per channel, with thermal test evidence;
- motor-signal protocol, logic level, update rate and reset state;
- exact connector part number, pin order, mating cable and ground arrangement;
- whether bidirectional DShot, EDT, separate telemetry or CAN is used;
- location and rating of current/voltage shunts and the FC ADC scaling;
- BEC/5 V output capability, if any, and whether it is allowed to power the FC or CM5;
- ESC firmware and boot/programming method, such as AM32 where applicable.

The FC output must remain disabled until arming and must go to a defined safe state during reset, brownout, RC timeout and CM5 link loss. The CM5 must never connect directly to an ESC gate, motor phase or raw battery line.

Motor selection cannot be frozen from KV alone. Use measured manufacturer thrust/current tables for the chosen propeller, cell count and all-up mass. The initial classes are:

| Vehicle class | Motor/prop direction | Battery/ESC starting direction | Status |
|---|---|---|---|
| 5-inch light FPV demonstrator | 2207/2207.5 class, roughly 1750–1950 KV for 6S or 2400–2550 KV for 4S | 4-in-1 ESC roughly 35–45 A after test-table check | Only if the CM5/lidar payload is very light |
| 7–10 inch sensor/payload quad | 2810/2814 or similar lower-KV class with larger prop | 4S/6S and roughly 40–60 A ESC class, confirmed from data | More plausible for CM5 plus camera/lidar |
| Larger UAS/UAM-like demonstrator | Larger low-KV motors and propellers | Possibly separate high-current ESC/PDB and higher-voltage battery | Cannot be selected without MTOW, prop diameter and flight-time target |

Use the manufacturer pages for [T-Motor F60 Pro V 2207.5](https://tmotorhobby.com/goods.php?id=1183) and [EMAX ECO II 2207](https://emaxmodel.com/products/emax-eco-ii-series-2207-3-6s-1700kv-1900kv-2400kv-2750kv-brushless-motor) as examples of the 5-inch class, and the [EMAX ECO II 2814 family](https://shop.emaxmodel.com/products/emax-ecoii-2814-730kv-830kv-brushless-motor-for-rc-drone) as an example of a larger-prop class. These pages are candidate references, not a final motor order.

Use these sizing checks:

```text
T_hover_each = MTOW × g / 4
T_total_max target >= 2 × vehicle weight   (engineering margin target, not certification)
I_ESC_continuous >= measured motor current with thermal margin
I_battery_peak >= sum of four motor peak currents with wiring/regulator margin
flight time ≈ usable battery energy / measured average propulsion power
```

The final motor, propeller, ESC and battery must be selected as a matched set from thrust/current data. The CM5 carrier, cooling, camera, lidar, wiring and mounting hardware must be included in MTOW before the set is frozen.

### LiPo and power decision

LiPo is a reasonable propulsion choice for the prototype, but the larger battery is not automatically better: its mass increases the thrust and current requirement. A 6S battery is 22.2 V nominal and 25.2 V fully charged. The FC and CM5 must therefore be fed through separately rated regulators, not through an improvised resistor, linear regulator or unknown ESC BEC.

Rev A power tree:

```text
4S/6S LiPo and main fuse/anti-spark as required
   ├── short, high-current path ──> PDB/4-in-1 ESC ──> motors
   ├── filtered external 5 V, approximately 1–2 A FC budget ──> FC POWER1
   └── separate buck, 5.1 V-class / 5 A-capable ──> CM5 carrier

FC POWER1 ──> protection/load switch ──> 5V_SYS ──> 3V3_DIG and low-noise IMU rail
FC ADCs <── scaled VBAT and external current-sense output
```

At 25 W of CM5-carrier output, a 90% efficient converter dissipates approximately 2.8 W and draws approximately 1.9 A from a 4S nominal pack or 1.25 A from a 6S nominal pack. These are planning calculations; measure the actual workload and converter temperature. Keep the CM5 buck physically and electrically away from the IMU and barometer, provide bulk capacitance and a fuse/current limit, and test brownout behavior.

Candidate battery scale examples show why MTOW matters: Tattu lists 6S 1200/1400 mAh high-C packs in the roughly 200–222 g class for small FPV vehicles, while its 6S 5000 mAh 60C pack is listed at about 755 g. The [Tattu FPV battery brochure](https://www.genstattu.com/content/instock/rc_product_brochure.pdf) and [current R-Line listings](https://genstattu.com/tattu-r-line-version-5-0-batteries/?page=2) are useful sourcing references, not permission to order before thrust and flight-time calculations.

### Lidar selection and placement

One rangefinder gives one line-of-sight distance. It can support altitude hold or landing, but it does not by itself see obstacles around the vehicle. A collision-avoidance demonstration needs a scanning lidar, multiple directional rangefinders, a depth camera, or a validated camera/lidar perception pipeline.

| Candidate | Approximate capability | Interface | Best role in this project | Decision note |
|---|---|---|---|---|
| Benewake TF-Luna | 0.2–8 m, under 5 g, up to 250 Hz | UART/I2C/I/O | Downward altitude/landing sensor | Strong lightweight Rev A candidate; verify logic level and surface reflectivity limits |
| Benewake TFmini-S | 0.1–12 m, about 5 g, up to 1 kHz configurable | UART/I2C/I/O | Downward or single forward distance | Good low-mass choice; one beam is not full avoidance |
| Benewake TF02-i | 0.1–40 m, about 60 g | CAN/RS-485 | Robust forward/downward industrial range | More weight and power; useful if the team wants a smart bus |
| LightWare SF20/C | 0.2–100 m, 7.5 g | USB/UART/I2C | Higher-quality single-beam range | Attractive performance; cost and availability need checking |
| LightWare SF45/B | 320° scan, up to 50 m, about 59 g | USB/UART/I2C | Forward/near-360 obstacle sectors | Best single-lidar collision reference if budget permits |
| RPLIDAR A1 | 360° planar, about 12 m, about 170 g | UART | Indoor mapping/obstacle demonstration | Usually too heavy and high for a small CM5 quad |
| RPLIDAR S2 | 360° planar, longer range, about 10 Hz | High-speed UART/Ethernet | Larger platform mapping | More capable but expensive/heavy; still only a plane |
| Livox Mid-360 | 3-D, 40–70 m depending reflectivity, about 265 g, 6.5 W | Ethernet | 3-D mapping/SLAM research | Excellent capability but not appropriate for a small first airborne prototype |
| ARK DIST SR/MR | 8 cm to roughly 30/50 m | DroneCAN/UART | Robust FC-connected altitude/range node | Attractive if a DroneCAN-compatible module is available |

For the under-one-month milestone, choose one of two explicit paths:

1. **Altitude/landing path:** TF-Luna or TFmini-S pointed down, connected to `LIDAR_FC` UART, and configured as an FC rangefinder.
2. **Perception/avoidance path:** scanning lidar or a camera/depth pipeline connected to CM5; CM5 publishes obstacle sectors or high-level avoidance data over MAVLink/DroneCAN. Do not label a forward TF-Luna as “collision avoidance” without stating its one-beam limitation.

Relevant driver and interface references are [PX4 distance sensors](https://docs.px4.io/main/en/sensor/rangefinders), [ArduPilot rangefinders](https://en.ardupilot.org/copter/docs/common-rangefinder-setup.html), and [ArduPilot proximity sensors](https://en.ardupilot.org/copter/docs/common-proximity-landingpage.html).

### Camera selection and placement

The camera team must distinguish the pilot’s FPV camera from the CM5 perception camera:

| Camera | Strength | Interface/role | Recommendation |
|---|---|---|---|
| Raspberry Pi Camera Module 3 Wide | 12 MP IMX708, autofocus/HDR, 120° wide option | CSI-2 to CM5 | Default first YOLO/detection/recording camera; calibrate wide-angle distortion |
| Raspberry Pi Global Shutter Camera | IMX296, 1456×1088 at up to 60 Hz, global shutter | CSI-2 to CM5 | Prefer for fast motion, optical flow or visual odometry; lower resolution |
| Raspberry Pi HQ Camera | 12.3 MP IMX477, interchangeable C/CS/M12 optics | CSI-2 to CM5 | Choose when lens/optics matter; heavier and less plug-and-play |
| Raspberry Pi AI Camera | IMX500 with on-module neural accelerator | CSI-2 to CM5 | Optional if the team wants lower CM5 CPU load without an AI HAT; model deployment adds software work |
| RunCam Phoenix 2 | Analog CVBS, 1000 TVL, low-latency FPV, 5–36 V | Dedicated analog VTX | Pilot FPV only; not a CSI/YOLO input without a capture path |
| HDZero/Caddx digital FPV camera | Low-latency digital FPV ecosystem | Proprietary VTX/goggles link | Pilot FPV only unless a separate supported ingest path is engineered |

Use a CM5 CSI camera for YOLO, tracking, mapping and recording. Use a dedicated analog/digital FPV camera and VTX if the pilot needs low-latency live video. Do not assume that one FPV camera can simultaneously provide safe pilot video and a clean CM5 inference stream. The official references are [Camera Module 3](https://www.raspberrypi.com/products/camera-module-3/), [Global Shutter Camera](https://www.raspberrypi.com/products/raspberry-pi-global-shutter-camera/), [HQ Camera](https://www.raspberrypi.com/products/raspberry-pi-high-quality-camera/), and [RunCam Phoenix 2](https://shop.runcam.com/runcam-phoenix-2/).

### Firmware recommendation for this system

The application now includes GNSS/compass, range sensing, companion-computer messages, possible obstacle sectors and modular telemetry. Therefore:

- **ArduPilot-first** is the recommended application path when the priority is integrating external GPS/compass, rangefinder/proximity sensors and MAVLink companion behavior in a relatively broad vehicle stack.
- **PX4-first** is the alternative when the assessment specifically values Pixhawk conventions, DroneCAN, ROS 2 or PX4 companion-computer workflows.
- **Betaflight** remains the fastest fallback for a manual/stabilized quad and for validating the custom H743 sensor/output hardware, but it is not the best single firmware choice for the complete perception/autonomy scope.
- Do not write a new complete autopilot in the remaining month. Use Udayate’s educational estimator/driver code and open firmware targets as learning references, then port/adapt a mature stack or use a minimal bench firmware while the hardware is verified.

The first firmware decision should be made before assigning UARTs, timers, DMA channels, CAN instances and bootloader resources. A connector is only a mechanical contract; firmware must map it to a real peripheral and fail safely when the connected module disappears.

### What can be produced in the implementation phase

Given the exact MCU, sensors, regulator MPNs, ESC schematic/pinout, receiver, lidar, camera carrier and chosen firmware, I can prepare and review:

- KiCad hierarchical schematic and net-labelled power/interface sheets;
- STM32 pin, alternate-function, timer/DMA, interrupt and boot/debug map;
- footprints, placement constraints, return-path and routing instructions;
- PCB layout edits or a review of an existing `.kicad_pcb`;
- ERC/DRC issue triage, connector pinout/harness drawings and test points;
- manufacturer BOM, MPN substitutions with constraint checks, and fabrication exports;
- bring-up firmware scaffolding, sensor-driver integration plans, bench scripts and test checklists.

The team must still verify every datasheet, footprint, physical clearance, solder joint, power measurement, thermal result and flight-safety decision. A generated schematic is not certification or a substitute for an oscilloscope/current-limited bring-up. The most efficient workflow is to freeze the external contracts first, then build the FC schematic around those contracts.

### Remaining decisions required before schematic freeze

1. Vehicle dry mass, payload mass, target MTOW, propeller diameter and desired flight time.
2. 4S versus 6S propulsion choice and the exact motor/prop/ESC test-table set.
3. ESC signal protocol and the teammate’s final connector/harness drawing.
4. Receiver protocol, voltage and failsafe/kill-channel behavior.
5. CM5 variant, storage, carrier approach and camera model.
6. Whether the lidar is a downward FC rangefinder or a CM5 obstacle sensor, and its exact mounting direction.
7. ArduPilot versus PX4 as the main integration stack; Betaflight only as a limited fallback.
8. Pixhawk exact DS-009 pinout compliance versus a clearly labeled project-specific Pixhawk-inspired pinout.

The current baseline remains: **custom bare STM32H743VIT6 FC, onboard ICM-42688-P and BMP390, external GNSS/compass, signal-only modular ESC interface, separate CM5 carrier and power, CM5-side camera/scanning lidar, and controlled bench-first verification.**
