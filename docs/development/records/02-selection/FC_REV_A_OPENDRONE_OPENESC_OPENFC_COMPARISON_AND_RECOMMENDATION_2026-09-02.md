> Historical technical record. Names and private workstation/session references were neutralized for publication. Dates and assertions describe the recorded stage, not current physical qualification. See the current validation-status page for later checks.

# FC Drone FC Rev A — OpenDrone/OpenESC/OpenFC Analysis and Recommended Hybrid Approach

I re-read the three project-control files and the earlier Stage 01 record:

- Stage map and workflow (private source record)
- Master research and decision record (private source record)
- Chat handoff summary (private source record)
- Stage 01 circuit-selection record (private source record)

I also inspected the current OpenDrone organization, OpenFC-Lite repository/design files, OpenESC repository/design files, product pages, and official MCU/sensor/regulator documentation.

## Bottom-line recommendation

**[RECOMMENDATION] Do not use the OpenFC-Lite circuit unchanged as the FC FC.**

Use a **selective hybrid design**:

- `[DECISION]` STM32H743VIT6
- `[DECISION]` ICM-42688-P over local SPI
- `[DECISION]` BMP390 onboard with protected vent
- `[RECOMMENDATION]` Shirley-style H743 power/core architecture
- `[RECOMMENDATION]` OpenFC-style quiet sensor rail and six-layer layout discipline
- `[RECOMMENDATION]` Pixhawk-style modular port organization
- `[DECISION]` OpenESC remains an external ESC
- `[RECOMMENDATION]` OpenESC-compatible DShot interface, but raw battery must remain isolated from the FC
- `[DECISION]` CM5 separately powered and not required for stabilization or failsafe

The OpenDrone FC and ESC are electrically related, but adopting both unchanged would create a **Betaflight/RP2354 system**, not the planned **H743/ArduPilot-capable FC flight controller**.

---

# 1. What the current OpenDrone designs actually contain

## OpenESC-20x20

`[VERIFIED]` The current repository describes a four-in-one sensorless BLDC ESC with:

| Item | Current OpenESC-20x20 design |
|---|---|
| Motor channels | 4 independent channels |
| Motor MCU | 4 × AT32F421G8U7 |
| Gate driver | 4 × NSG2065Q |
| MOSFETs | 6 × DOY180N03T per channel |
| Firmware | AM32 |
| Protocol | DShot, bidirectional DShot, extended DShot |
| Input | 2–6S LiPo, 6.0–25.2 V |
| BEC | None |
| Current sense | One board-level current-sense chain |
| Published current rating | 40 A/channel |
| Connector | JST-SH 8-pin |
| PCB | 6-layer, 1.6 mm, 2 oz copper |
| Mounting | 20 × 20 mm |
| Board size | Approximately 31.2 × 33.0 mm |

Sources: [OpenESC repository](http[LOCAL_SOURCE] [OpenESC README](http[LOCAL_SOURCE] [OpenESC technical notes](http[LOCAL_SOURCE]

Its connector is not signal/ground-only:

| Pin | Function | Treatment for FC FC |
|---:|---|---|
| 1 | Raw `+BATT` | `[RECOMMENDATION]` Leave isolated/NC on FC initially |
| 2 | `GND` | FC signal reference |
| 3 | `/CURR` | `[CANDIDATE]` Optional conditioned ADC input |
| 4 | Unconnected | Leave NC |
| 5 | `/M1` | H743 DShot/PWM output |
| 6 | `/M2` | H743 DShot/PWM output |
| 7 | `/M3` | H743 DShot/PWM output |
| 8 | `/M4` | H743 DShot/PWM output |

The ESC’s pin 1 is raw battery voltage, not a regulated 5 V output. Therefore, the FC must not treat the OpenESC connector as if it provides BEC power.

`[OPEN]` The 40 A/channel figure is a repository-published rating, not a substitute for the ESC team’s final thermal validation using the selected motor, propeller, battery, cooling, and flight duty cycle.

## OpenFC-Lite 30×30

`[VERIFIED]` The current OpenFC-Lite 30×30 design contains:

| Item | Current OpenFC-Lite 30×30 design |
|---|---|
| MCU | RP2354B, QFN-80 |
| Firmware | Betaflight |
| IMU | Bosch BMI270 |
| Barometer | None |
| Logging | microSD |
| OSD | Analog/digital OSD |
| UARTs | 4 total; 2 hardware plus 2 PIO-generated |
| Motor outputs | 4 × bidirectional DShot |
| Input | 3–8S LiPo, 9.0–33.6 V |
| BEC | Switchable 10 V plus always-on 5 V, 3.5 A |
| USB | USB-C |
| Mounting | 30.5 × 30.5 mm |
| Board size | Approximately 37.9 × 37.9 mm |
| PCB | 6-layer, 1.6 mm |

Sources: [OpenFC-Lite repository](http[LOCAL_SOURCE] [OpenFC-Lite README](http[LOCAL_SOURCE] [OpenFC-Lite technical notes](http[LOCAL_SOURCE] [30×30 product page](http[LOCAL_SOURCE]

The RP2350 datasheet confirms that RP2354B is a QFN-80 device with 48 GPIO, 520 kB SRAM, 2 MB stacked flash, dual Cortex-M33 processors, and an internal switched-mode core supply. [Raspberry Pi RP2350 datasheet](http[LOCAL_SOURCE]

Its power architecture is approximately:

```text
Raw battery
   ├──> 10 V buck ──> switchable VTX rail
   └──> 5 V buck ──> 5 V rail
                    ├──> 3.3 V logic LDO
                    └──> 1.8 V IMU analog LDO

3.3 V ──> RP2354 internal core regulator
```

This is a useful topology reference, but it cannot be transferred directly to the STM32H743 because the MCU power, clock, boot, USB, package, and pin requirements are different.

## OpenFC-Lite Mini 20×20

The earlier OpenFC-Lite-Mini design is the smaller RP2354A version:

- 20 × 20 mm mounting
- RP2354A
- 3–6S input
- 3 UARTs
- 3 A 5 V supply
- BMI270
- no barometer
- Betaflight firmware

Source: [OpenFC-Lite-Mini repository](http[LOCAL_SOURCE]

The Mini is mechanically closer to the OpenESC-20x20, but it is even less suitable as the FC FC because of the RP2354A, limited port capacity, Betaflight architecture, and absence of BMP390.

## OpenDrone project status

`[VERIFIED]` The OpenDrone organization lists OpenESC and OpenFC-Lite as open-hardware projects under CERN-OHL-S-2.0. The current roadmap still classifies the products under alpha/early-stage development, while the 30×30 OpenFC product is marked as coming soon. Sources: [OpenDrone organization](http[LOCAL_SOURCE] [OpenDrone roadmap](http[LOCAL_SOURCE]

Therefore:

`[OPEN]` Do not freeze the FC design against an unpinned GitHub `main` branch. Use a specific OpenDrone commit and board revision when the ESC team confirms its final design.

The YouTube channel was checked, but automated access to the channel/video content was throttled. I therefore did not use videos as electrical evidence.

---

# 2. Earlier reference designs and their proper roles

The earlier reference set was not intended to be copied wholesale. Its purpose was to borrow specific circuit principles.

| Reference | Useful contribution | What must not be copied blindly |
|---|---|---|
| [OpenFC-Lite-Mini](http[LOCAL_SOURCE] | Quiet IMU rail, compact six-layer layout, microSD, external ESC concept | RP2354A, BMI270, PIO UARTs, no barometer, raw-battery assumptions |
| [OpenFC-Lite](http[LOCAL_SOURCE] | Larger OpenDrone FC architecture, modular connectors, sensor separation | RP2354B pinout, Betaflight target, analog OSD chain, no reverse-polarity protection |
| [Shirley-FC-Dev-Board](http[LOCAL_SOURCE] | Closest H743 architecture, separated power domains, SDMMC, USB ESD, CAN, SWD, modular ports | H743ZIT6 pinout, sensor selection, exact firmware mapping |
| [Shirley hardware overview](http[LOCAL_SOURCE] | H743 system organization and bring-up structure | Exact component values without rechecking datasheets |
| [Shirley design decisions](http[LOCAL_SOURCE] | Power and interface rationale | Direct schematic reuse without package/pin verification |
| [Pixhawk hardware](http[LOCAL_SOURCE] | Modular interface philosophy, power monitoring, serviceability | Pixhawk-compatible claims, connector pinouts, firmware identity |
| [Pixhawk standards](http[LOCAL_SOURCE] | Functional port naming and documentation discipline | Assuming our board is electrically Pixhawk-compatible |
| [HomeGliders FCV2](http[LOCAL_SOURCE] | Hierarchical schematic organization and workflow | Exact circuit values and validation claims |
| [HomeGliders video](http[LOCAL_SOURCE] | Educational build process | Electrical authority |
| [STM32F405 educational build](http[LOCAL_SOURCE] | MCU/sensor bring-up sequencing | Production autopilot architecture |
| [Betaflight manufacturer guidelines](http[LOCAL_SOURCE] | SPI IMU, interrupt, timer/DMA, ADC and layout review prompts | Betaflight-specific firmware assumptions |
| [H743 community review](http[LOCAL_SOURCE] | Review checklist for H743/IMU/barometer boards | Community claims without primary verification |
| [Custom FC discussion](http[LOCAL_SOURCE] | Current-sense and regulator review prompts | Part ratings and layout claims |
| [Custom FC discussion](http[LOCAL_SOURCE] | Scope and risk awareness | Validated circuit basis |
| [Custom FC discussion](http[LOCAL_SOURCE] | Failure-mode questions | Safety evidence |
| [Custom FC discussion](http[LOCAL_SOURCE] | Bench-first development sequence | Complete design reference |
| [Udayate](http[LOCAL_SOURCE] and [Kalman-AHRS](http[LOCAL_SOURCE] | Driver and estimator learning | Drop-in autopilot firmware |
| [LSM6DSL library](http[LOCAL_SOURCE] | Sensor abstraction ideas | Selected IMU implementation |
| [Pixhawk 2.1 repository](http[LOCAL_SOURCE] | Documentation and redundancy concepts | Old pinout, licensing, and hardware assumptions |

The earlier recommended hybrid was:

```text
Shirley H743 power/core architecture
        +
OpenFC-style quiet sensor rail and six-layer discipline
        +
Pixhawk-style modular port organization
        +
Betaflight-style SPI/timer/DMA review
        +
Exact STM32H743VIT6/ICM-42688-P/BMP390 implementation
```

The new OpenESC information adds one more component:

```text
External OpenESC DShot interface
        +
raw battery electrically isolated from the FC
```

---

# 3. The main options

| Option | Description | Baseline compatibility | Effort/risk | Verdict |
|---|---|---:|---:|---|
| 1. OpenFC-Lite unchanged + OpenESC | RP2354B, BMI270, Betaflight, no BMP390 | Low | Low initial effort, high project divergence | `[DNP]` for FC |
| 2. Fork OpenFC-Lite and replace major blocks | Replace RP2354B with H743, BMI270 with ICM, add BMP390/CAN/SWD | Medium | Very high; effectively a new board | `[CANDIDATE]` but not preferred |
| 3. H743 selective hybrid | H743 custom FC using Shirley/OpenFC/Pixhawk principles | High | Moderate and controllable | `[RECOMMENDATION]` |
| 4. Pure H743 design from scratch | No meaningful OpenFC reuse | High | Highest development effort | `[CANDIDATE]` |
| 5. OpenFC-Lite topology as a reference only | Borrow power/sensor/layout ideas without copying MCU architecture | High | Moderate | `[RECOMMENDATION]` |

## Why Option 1 is not appropriate

Using OpenFC-Lite unchanged would require changing several settled project decisions:

- RP2354B instead of STM32H743VIT6
- BMI270 instead of ICM-42688-P
- no onboard BMP390
- Betaflight instead of ArduPilot-leading architecture
- PIO UART implementation instead of H743 hardware UART allocation
- no native H743 SWD/BOOT0 implementation
- no direct compatibility with the planned CM5, GNSS, CAN and scalar-lidar architecture

The OpenFC-Lite product is a good compact Betaflight FPV FC, but it is not the same functional class as the planned FC mission controller.

## Why Option 2 is more work than it first appears

Replacing only the MCU and IMU is not enough. The following would require redesign:

1. RP2354B QFN-80 sheet and power system
2. H743 LQFP100 pinout and all power pins
3. H743 VCAP capacitors and internal regulator support
4. H743 clock and reset circuits
5. USB FS and boot/recovery paths
6. SWDIO, SWCLK, NRST and BOOT0 access
7. UART allocation
8. Timer, alternate-function and DMA allocation
9. ICM-42688-P sensor circuit
10. BMP390 circuit and vent
11. CAN transceiver circuits
12. ArduPilot board definition
13. CM5 and external modular ports
14. power input protection and power-tree assumptions

That is not a small modification. It is a new H743 FC using OpenFC ideas.

---

# 4. Recommended FC FC circuit

## Recommended power tree

`[RECOMMENDATION]`

```text
LiPo battery
   ├──> PDB / high-current propulsion path
   │       └──> OpenESC ───> motors
   │
   ├──> external regulated 5V_FC
   │       └──> input protection / source-OR
   │               └──> 5V_FC_PROT
   │                       ├──> 3V3_MAIN buck
   │                       │       └──> STM32H743 digital VDD
   │                       │
   │                       ├──> low-noise 3V3_SENS LDO
   │                       │       ├──> ICM-42688-P
   │                       │       └──> BMP390
   │                       │
   │                       ├──> filtered 3V3_ANA
   │                       │       └──> VDDA / VREF+
   │                       │
   │                       └──> limited 5V_AUX
   │                               └──> external receiver/GNSS/telemetry/lidar
   │
   └──> external PDB monitor
           ├──> conditioned VBAT_SENSE
           └──> conditioned CURR_SENSE

Separate external CM5 supply
   └──> CM5 carrier 5.1 V-class rail
```

`[ASSUMPTION]` The FC receives a regulated external 5 V input.

`[OPEN]` If the power team cannot provide a suitable 5 V rail, a raw-battery FC front end must be designed separately with reverse-polarity protection, TVS, fuse/inrush control, input filtering, transient measurements, and thermal analysis.

## H743 core

The STM32H743VI family provides a 480 MHz Cortex-M7, up to 2 MB flash and up to 1 MB RAM. [ST STM32H743VI product page](http[LOCAL_SOURCE] [ST H743 datasheet](http[LOCAL_SOURCE]

`[VERIFIED]` The minimum H743 support circuit must include:

- All LQFP100 `VDD` and `VSS` pins connected correctly
- `3V3_MAIN` for digital supply
- `VCAP1` and `VCAP2`, each with the datasheet-required low-ESR capacitor
- Filtered `VDDA`
- Correct `VSSA` connection
- `VREF+` decoupling according to the selected ADC/reference topology
- USB FS pins and VBUS sensing
- NRST access
- BOOT0 default state and recovery access
- SWDIO, SWCLK, reference ground and NRST
- HSE oscillator option
- Optional LSE/RTC footprint

For the LQFP100 package, the earlier Stage 01 record identified:

- `VDD`: pins 11, 27, 50 and 75
- `VSS`: pins 10, 26, 49 and 74
- `VCAP`: pins 48 and 73
- `VDDA`: pin 21
- `VSSA`: pin 19
- `VREF+`: pin 20
- USB VBUS: PA9, pin 68
- USB DM: PA11, pin 70
- USB DP: PA12, pin 71
- SWDIO: PA13, pin 72
- SWCLK: PA14, pin 76
- BOOT0: pin 94

These must still be checked against the exact selected STM32H743VIT6 library symbol before schematic freeze.

## IMU

`[DECISION]` Retain the ICM-42688-P over SPI.

TDK specifies:

- Separate `VDD` and `VDDIO`
- Both supplies valid from approximately 1.71–3.6 V
- SPI up to 24 MHz
- 2.5 × 3.0 mm LGA package
- Dedicated interrupt capability
- High-performance gyro/accelerometer noise characteristics

Sources: [TDK ICM-42688-P product page](http[LOCAL_SOURCE] [official ICM-42688-P datasheet](http[LOCAL_SOURCE]

`[RECOMMENDATION]`

- Dedicated local SPI bus
- Dedicated chip-select
- Dedicated `INT1`
- `3V3_SENS` for both IMU supply domains initially
- Local decoupling exactly according to the TDK datasheet
- Keep the sensor away from switching nodes, high-current copper, connectors and mounting stress
- Leave `INT2`, FSYNC and external-clock treatment explicitly open

The OpenFC 1.8 V IMU rail is a useful low-noise topology idea, but the ICM-42688-P does not force a 1.8 V rail. Using a common low-noise 3.3 V sensor rail also simplifies BMP390 integration.

## Barometer

`[DECISION]` Add BMP390 onboard.

Bosch specifies:

- `VDD`: approximately 1.65–3.6 V
- `VDDIO`: approximately 1.2–3.6 V
- I²C and SPI
- Up to 200 Hz maximum sampling rate
- Small 10-pin LGA package
- Protected venting requirements

Source: [Bosch BMP390 product page](http[LOCAL_SOURCE]

`[RECOMMENDATION]`

- Use a short local I²C connection
- Keep the primary IMU on dedicated SPI
- Use deterministic `CSB` and `SDO` straps
- Provide documented I²C pull-up ownership
- Include local 100 nF supply capacitors
- Use a protected vent and mechanical keep-out

`[OPEN]` Exact vent opening, enclosure treatment, coating restrictions and prop-wash mitigation.

## Main regulator

`[CANDIDATE] TPS62162-class buck`

- 3–17 V input
- Up to 1 A
- Compact synchronous buck
- Suitable for a protected 5 V input

Source: [TI TPS62162](http[LOCAL_SOURCE]

`[CANDIDATE] LMR33630-class buck`

- Approximately 3.8–36 V input
- Up to 3 A
- More suitable for a conditional raw-battery or higher-load branch
- Greater switching-node, thermal and EMI burden

Source: [TI LMR33630](http[LOCAL_SOURCE]

`[RECOMMENDATION]` Use a TPS62162-class device for `5V_FC_PROT → 3V3_MAIN` if the measured FC load is comfortably below the 1 A design envelope. Retain an LMR33630-class alternative if the power architecture changes to raw-battery entry.

## Quiet sensor regulator

`[RECOMMENDATION] LP5912-class low-noise LDO`

TI specifies the LP5912 family for:

- 1.6–6.5 V input
- Up to 500 mA
- Low output noise
- High PSRR
- 1 µF ceramic input/output capacitors
- Enable, power-good and output-discharge features

Source: [TI LP5912 datasheet](http[LOCAL_SOURCE]

`[CANDIDATE] LP5907`

- Up to 250 mA
- Low-noise design
- High PSRR
- Smaller current margin

Source: [TI LP5907](http[LOCAL_SOURCE]

The final LDO depends on measured sensor/peripheral loading, thermal dissipation and supply availability.

## CAN

`[RECOMMENDATION]` Add at least one external 3.3 V CAN transceiver footprint.

`[CANDIDATE] TCAN332`

- 3.3 V supply
- ISO 11898-2 compatible
- Up to 1 Mbps for the standard device
- ±12 V common-mode range
- ±14 V bus-fault protection
- SOT-23 or SOIC package options
- Integrated protection features

Source: [TI TCAN332 datasheet](http[LOCAL_SOURCE]

`[CANDIDATE] SN65HVD230`

- 3.3 V CAN transceiver
- Up to 1 Mbps
- Alternate procurement/footprint option

`[OPEN]`

- One or two CAN buses
- Bus bitrate
- Termination location
- Connector pinout
- CAN TVS/common-mode choke
- DroneCAN node/message contract

## USB and debug

`[RECOMMENDATION]`

- USB-C
- USB full-speed device interface
- USB VBUS sensing
- USB ESD protection
- SWD pads or low-profile debug footprint
- NRST pad
- BOOT0 recovery pad/jumper
- Optional SWO pad

The OpenFC USB-C implementation is useful as a mechanical/connector reference, but the H743 USB and recovery circuit must be redesigned for the STM32 package.

`[CANDIDATE] USBLC6-2`

ST specifies two USB data-line protection channels, VBUS protection, low capacitance and IEC 61000-4-2 level 4 device protection. [ST USBLC6-2](http[LOCAL_SOURCE]

`[CANDIDATE] TPD4EUSB30`

TI specifies a low-capacitance multi-channel USB protection array. [TI TPD4EUSB30 datasheet](http[LOCAL_SOURCE]

`[DNP]` USB-only recovery. The custom H743 FC should not depend solely on USB recovery.

## Storage

`[RECOMMENDATION]` Provide removable microSD if ArduPilot flight logging is a real requirement.

Advantages:

- Removable logs
- Easier debugging
- Useful during estimator and failsafe development
- High capacity

Disadvantages:

- More pins
- Connector and ESD concerns
- Additional EMI and mechanical work
- Firmware storage mapping required

`[CANDIDATE] W25Q128JV SPI/QSPI NOR`

- 128 Mbit / 16 MB
- Approximately 2.7–3.6 V supply
- Compact
- Simpler mechanically than microSD

Source: [Winbond W25Q128JV documentation](http[LOCAL_SOURCE]

`[OPEN]` Final storage choice must be coordinated with ArduPilot’s board definition and parameter-storage policy.

## OSD and VTX

`[CANDIDATE]` OpenFC’s analog OSD chain can be reused only if an analog camera/VTX requirement is confirmed.

`[DNP/OPEN]` If the FC camera system is CM5/digital rather than analog FPV, remove the analog OSD chain and the switchable 10 V VTX rail. This reduces circuitry, switching noise and firmware scope.

The OpenFC OSD circuit is not automatically useful for a CM5 camera link.

## GNSS, receiver, telemetry and lidar

OpenFC-Lite does not contain a GNSS receiver or compass. It provides external serial/I²C-style expansion, but GPS/GNSS is not implemented onboard.

`[DECISION]` FC GNSS/compass remains external.

`[OPEN]`

- GNSS module
- Compass module
- UART/I²C/PPS requirements
- Connector
- Pinout
- Firmware mapping
- Magnetic placement

The FC must provide a modular `GPS1` interface, but the external GNSS module is not part of the OpenFC circuit.

## CM5

`[DECISION]` CM5 remains separately powered.

The FC should expose only the required data interface:

```text
CM5 carrier
   ├── separate regulated power
   └── data link to FC
```

`[OPEN]`

- UART, CAN, SPI or another link
- Flow control
- Connector
- Cable length
- Ground/reference arrangement
- CM5 carrier details

The CM5 must not be needed for:

- Basic stabilization
- Arming/disarming
- Radio failsafe
- Direct motor waveform generation
- Safe motor shutdown

---

# 5. Exact OpenESC accommodation

## Preferred first-prototype arrangement

`[RECOMMENDATION]` Use an interposer or adapter during the first electrical integration.

The interposer should:

- Map four H743 outputs to OpenESC `/M1`–`/M4`
- Provide a reliable signal ground
- Leave OpenESC pin 1 raw `+BATT` isolated
- Leave pin 4 unused
- Optionally route `/CURR` to a protected test point/ADC input
- Allow oscilloscope probing of every DShot line

This preserves the current project’s signal/ground-only boundary while avoiding immediate connector-contract risk.

## Possible final arrangement

`[RECOMMENDATION]` A direct OpenESC-compatible connector may be used later:

```text
FC connector pin 1: OpenESC +BATT  -> electrically NC on FC
FC connector pin 2: GND            -> FC ground
FC connector pin 3: /CURR          -> optional conditioned ADC
FC connector pin 4: telemetry      -> NC for this OpenESC revision
FC connector pins 5–8              -> M1–M4 bidirectional DShot/PWM
```

However, this is only acceptable after:

- Connector mate and orientation verification
- Cable/ground-return testing
- Pin-1 isolation verification
- DShot waveform testing
- Bidirectional telemetry testing
- ESC reset/disconnect testing

## Do not use direct raw-battery integration yet

`[CANDIDATE / NOT RECOMMENDED FOR REV A]`

Connecting OpenESC pin 1 directly into the FC could provide FC raw-battery sensing or power, but it would:

- Change the project’s signal-only boundary
- Bring ESC/PDB transients into the FC
- Require reverse-polarity and overvoltage protection
- Require new input filtering and thermal analysis
- Couple FC behavior to ESC-side power integrity
- Potentially include additional loads in the ESC current-sense path

Do not use this approach unless the architecture is explicitly changed and the power team supplies measured battery/transient data.

---

# 6. DShot and firmware implications

`[VERIFIED]` OpenESC uses AM32 and bidirectional/extended DShot. AM32 also supports DShot and PWM-related operation. [AM32 firmware](http[LOCAL_SOURCE]

ArduPilot’s documentation states:

- DShot300 and DShot600 are preferred for bidirectional DShot
- DShot150 is more robust for long/noisy signal cables
- DShot600 is widely tested for smaller vehicles
- DShot output allocation depends on the board’s timer/DMA arrangement
- A new board requires an explicit firmware hardware definition
- Bdshot-capable outputs should be tested with an AM32 or BLHelI32 ESC

Sources: [ArduPilot DShot documentation](http[LOCAL_SOURCE] [ArduPilot new-board porting](http[LOCAL_SOURCE]

Therefore:

`[DECISION]` DShot remains the preferred protocol.

`[DECISION]` PWM remains the propeller-off bring-up fallback.

`[OPEN]` Exact H743 output pins, timer groups, alternate functions, DMA/DMAMUX assignments and ArduPilot `hwdef.dat` mapping.

This is another reason the OpenFC PIO-UART/GPIO mapping cannot simply be copied.

---

# 7. What can be frozen now

| Item | Status |
|---|---|
| STM32H743VIT6 | `[DECISION]` |
| ICM-42688-P over SPI | `[DECISION]` |
| BMP390 onboard | `[DECISION]` |
| External GNSS/compass | `[DECISION]` |
| External receiver | `[DECISION]` |
| External ESC | `[DECISION]` |
| CM5 separate power | `[DECISION]` |
| CM5 not required for failsafe/stabilization | `[DECISION]` |
| DShot preferred | `[DECISION]` |
| PWM bring-up fallback | `[DECISION]` |
| OpenFC quiet sensor-rail concept | `[RECOMMENDATION]` |
| Shirley H743 power/core concept | `[RECOMMENDATION]` |
| Pixhawk-style modular port naming | `[RECOMMENDATION]` |
| OpenESC 8-pin interface as a candidate | `[CANDIDATE]` |
| OpenESC exact commit/revision | `[OPEN]` |
| ESC final voltage/current/thermal envelope | `[OPEN]` |
| FC input power source | `[ASSUMPTION]` external regulated 5 V |
| Exact FC connector and pinout | `[OPEN]` |
| Exact H743 timer/DMA map | `[OPEN]` |
| CAN transceiver and bus contract | `[CANDIDATE]/[OPEN]` |
| microSD versus SPI NOR | `[OPEN]` |
| Analog OSD/VTX rail | `[OPEN]` |
| CM5 data interface | `[OPEN]` |
| GNSS/compass module and connector | `[OPEN]` |
| Final regulator MPNs | `[CANDIDATE]/[OPEN]` |
| PCB routing and purchase BOM | `[OPEN]` and later stage |

---

# 8. Cross-team game plan

## Step 1 — ESC team supplies an interface-control table

The ESC team should provide:

- Immutable repository commit/tag
- Board revision
- Final battery range
- Motor/propeller operating envelope
- Confirmed connector part and mating housing
- Connector orientation and pin numbering
- Signal voltage levels and thresholds
- DShot rates supported
- Bidirectional DShot behavior
- PWM fallback behavior
- `/CURR` output scale and valid operating range
- ESC reset and disconnect behavior
- AM32 firmware commit/binary
- AM32 configuration procedure
- Thermal test conditions
- Current-sense validation results

## Step 2 — FC team freezes only the interface boundary

The FC team reserves:

- Four H743 timer/DMA-capable motor outputs
- Signal-ground return arrangement
- Optional `/CURR` ADC input
- Test points
- Optional series-resistor footprints
- Pin-1 raw-battery isolation

The FC should not be redesigned around the ESC’s internal MOSFET or gate-driver circuit.

## Step 3 — Firmware and schematic are developed together

Before routing:

- Select ArduPilot board identity
- Map H743 timers and DMA
- Map UARTs for receiver, GNSS, telemetry, lidar and CM5
- Map FDCAN
- Map SPI/I²C
- Define storage
- Define bootloader and SWD recovery
- Define DShot output groups

## Step 4 — First bench integration uses an adapter

Perform propeller-off tests:

1. Confirm no raw battery reaches the FC
2. Check signal-ground continuity
3. Check H743 reset/boot motor-output states
4. Test PWM fallback
5. Test DShot300
6. Test DShot600
7. Test bidirectional DShot
8. Test ESC telemetry
9. Test FC reset while ESC is powered
10. Test ESC reset while FC remains powered
11. Test each motor channel independently
12. Validate `/CURR` against a calibrated external current measurement

## Step 5 — Freeze connector and schematic

Only after the above tests should the team freeze:

- Connector
- Pinout
- Cable
- Output protection
- ADC conditioning
- Firmware output map
- Power-entry behavior

PCB routing and final purchasing documents should follow that freeze.

## Final recommendation

For the FC project, choose:

```text
Custom STM32H743VIT6 FC
+ ICM-42688-P
+ BMP390
+ Shirley-style H743 power/core implementation
+ OpenFC-style quiet sensor-rail/layout discipline
+ Pixhawk-style modular interfaces
+ external OpenESC using DShot
+ OpenESC adapter or isolated 8-pin interface
+ external FC and CM5 power
```

Do not use the OpenFC-Lite RP2354B circuit unchanged. Use it as a well-documented reference for layout discipline, sensor-power separation, modularity and ESC-interface ideas.
