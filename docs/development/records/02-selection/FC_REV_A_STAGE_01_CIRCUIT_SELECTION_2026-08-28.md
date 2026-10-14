> Historical technical record. Names and private workstation/session references were neutralized for publication. Dates and assertions describe the recorded stage, not current physical qualification. See the current validation-status page for later checks.

# FC Drone FC Rev A — Stage 01 Circuit Selection

**Artifact:** `FC_REV_A_STAGE_01_CIRCUIT_SELECTION_2026-08-28.md`  
**Date:** 2026-08-28  
**Scope:** circuit blocks, power-tree branches, STM32H743VIT6 core support, candidate topology/part comparison, and bounded selection recommendations.  
**Explicitly out of scope:** PCB routing, final connector pinout, final purchase BOM, and selection of ESC, motor, battery, receiver, camera, lidar, CM5 variant, or external connector mate.

## 0. Status legend and stage inputs

- **[DECISION]** fixed by the project baseline or selected for schematic planning at this stage.
- **[RECOMMENDATION]** preferred technical direction, pending the open dependencies listed below.
- **[CANDIDATE]** viable option that still needs system, footprint, availability, thermal, firmware, or manufacturing checks.
- **[ASSUMPTION]** bounded working assumption used to keep Stage 01 moving.
- **[OPEN]** not verified or not supplied; must be resolved before the affected item is frozen.
- **[VERIFIED]** checked against an official datasheet, official firmware documentation, or the linked source itself.

### 0.1 Fixed project baseline

- **[DECISION]** Bare `STM32H743VIT6` in the LQFP100 package on the custom FC PCB.
- **[DECISION]** Onboard `ICM-42688-P` over SPI on a quiet sensor rail.
- **[DECISION]** Onboard `BMP390` with a protected pressure vent.
- **[DECISION]** Hybrid Pixhawk-inspired architecture: high-rate stabilization sensors local to the FC; GNSS/compass, receiver, telemetry, scalar lidar, and CM5 externally modular.
- **[DECISION]** External ESC board; the FC-to-ESC interface is signal and ground only. Raw battery, motor phases, and high-current copper remain on the ESC/PDB side.
- **[DECISION]** CM5 is separately powered and is not required for stabilization, arming/disarming, direct motor waveforms, or failsafe behavior.
- **[DECISION]** DShot is preferred when the selected ESC supports it; PWM is the bring-up fallback; CAN/DroneCAN is a separate architecture option.
- **[DECISION]** ArduPilot is the leading integrated firmware direction; PX4 is the strong alternative; Betaflight is a bring-up/reference source rather than the selected integrated autopilot.

### 0.2 Stage 01 inputs that remain missing

These are not silently filled in. The user explicitly authorized proceeding with bounded assumptions, so the effects are recorded instead of blocking the comparison.

| Missing input | Current bounded treatment | What it can still change |
|---|---|---|
| ESC/PDB electrical interface, regulated output, signal threshold, telemetry/current-sense availability, transients | **[ASSUMPTION]** FC receives an external regulated `5V_FC`; ESC signal boundary remains signal/GND only | 5 V entry protection, regulator choice, signal conditioning, ADC source, telemetry wiring |
| Battery cell count and full/minimum voltage | **[ASSUMPTION]** 4S and 6S remain active; 6S is 22.2 V nominal and 25.2 V full | Raw-battery buck option, TVS/transient rating, battery-divider values, thermal calculations |
| Receiver protocol, logic level, inversion, and supply current | **[OPEN]** generic 3.3 V UART-capable port only | Inverter/level shifter, UART assignment, pull-ups, connector power budget |
| Exact firmware target/build and required logging/port map | **[ASSUMPTION]** ArduPilot lead, PX4-compatible hardware direction preserved | timer/DMA allocation, UART/CAN mapping, SD/SPI-flash use, HSE choice, bootloader/hwdef |
| PCB supplier, layer stack, assembly limits, minimum package/trace/clearance rules | **[ASSUMPTION]** 4-layer default; 6-layer remains possible | LDO/buck package, connector family, microSD/flash package, impedance and thermal implementation |
| External sensor/payload loads and cable lengths | **[OPEN]** low-current modular ports with current-limited `5V_AUX` | per-port protection, current limiting, CAN termination, ESD and inrush design |

## 1. Reconstructed supplied design/reference comparison — full links

The following reproduces the comparison from the project master record and handoff. These sources are references for architecture, bring-up, layout organization, or review lessons. They are not automatic Rev A schematics, pin maps, firmware targets, or purchase lists.

### 1.1 The 16 supplied reference items

| # | Full link(s) supplied earlier | Circuit/design contribution | Reuse for Rev A | Incompatibility or authority limit | Stage label |
|---:|---|---|---|---|---|
| 1 | `http[LOCAL_SOURCE]`<br>`http[LOCAL_SOURCE]`<br>`http[LOCAL_SOURCE]` | OpenFC-Lite-Mini shows a compact open FC with separate buck/LDO domains, dedicated IMU rail, microSD, multiple UARTs, USB-C, current sense, and an external 4-in-1 ESC concept. The repository notes also show that its ESC connector carries more than signal/GND. | Separate sensor supply, serviceable port thinking, staged manufacturing review, six-layer reference discipline, and the signal-level portion of the ESC boundary. | RP2354A, BMI270, no barometer, PIO/Betaflight-oriented implementation, no SWD, no reverse-polarity protection, and raw battery on its ESC connector do not transfer to this baseline. | `[VERIFIED]` source reviewed; reuse remains `[CANDIDATE]` |
| 2 | `http[LOCAL_SOURCE]`<br>`http[LOCAL_SOURCE]` | A small DIY FC repository containing KiCad project material. Its primary value is schematic/page organization and workflow inspection. | Net naming, hierarchical schematic organization, footprint/documentation workflow after exact files are inspected. | Exact circuit values, revision status, validation, MCU/sensor compatibility, and video details are not sufficiently verified from the accessible material. | `[VERIFIED]` repository link; circuit reuse `[OPEN]` |
| 3 | `http[LOCAL_SOURCE]` | Educational STM32F405 FC build with a basic sensor/control-loop signal flow. | Bring-up order: prove MCU, sensor communication, timing, and a minimal loop before adding every payload feature. | Educational implementation is not enough evidence for estimator timing, filtering, frame conventions, failsafe, power integrity, or aircraft safety. | `[VERIFIED]` link; process reuse `[CANDIDATE]` |
| 4 | `http[LOCAL_SOURCE]`<br>`http[LOCAL_SOURCE]` | Mature Pixhawk open hardware and current standards: modular port categories, power monitoring, serviceability, debug conventions, and documented interfaces. | Port/function partitioning, documentation discipline, redundant/robust interface thinking, and power-monitor concepts. | Pixhawk-inspired does not mean Pixhawk-compatible. Exact connector standard, pin mapping, mechanical interface, electrical levels, licensing, and firmware board identity must be separately met and verified. | `[VERIFIED]` reference; Rev A compatibility claim `[OPEN]` |
| 5 | `http[LOCAL_SOURCE]` | Community H743 custom-FC discussion with lessons about current measurement, external shunt, regulators, and compass placement. | Review prompts for current-sense placement, magnetics, regulator heat, and bench testing. | Reddit is anecdotal; no part rating, footprint, layout, or electrical claim is accepted without a primary datasheet or measurement. | `[VERIFIED]` link; technical reuse `[CANDIDATE]` |
| 6 | `http[LOCAL_SOURCE]` | Community account of the complexity of building an FC from scratch. | Scope and risk awareness; staged test planning. | Not a validated electrical reference. | `[VERIFIED]` link; process reuse `[CANDIDATE]` |
| 7 | `http[LOCAL_SOURCE]` | Community architecture and failure-mode discussion, including more advanced/AI-oriented ideas. | Awareness of failure modes and system-boundary questions. | Low authority; not a circuit basis and not evidence for CM5/FC safety behavior. | `[VERIFIED]` link; design reuse `[CANDIDATE]` |
| 8 | `http[LOCAL_SOURCE]` | Community recommendation to prove STM32 + gyro + basic loop before adding logging, baro, or lidar. | Bring-up sequencing and scope control. | Does not replace the required modular ports, power protection, or firmware validation. | `[VERIFIED]` link; process reuse `[CANDIDATE]` |
| 9 | `http[LOCAL_SOURCE]`<br>`http[LOCAL_SOURCE]`<br>`http[LOCAL_SOURCE]` | Closest architecture reference: H743ZIT6, onboard IMU/magnetometer/barometer, SDMMC, 5 V MUX, separate digital/analog 3.3 V domains, USB ESD, four ESC outputs, GPS/RC/telemetry/USB/FDCAN, and Tag-Connect SWD. | Hierarchical power domains, external 5 V power-module concept, separate analog/sensor treatment, port partition, SD/debug provision, and H7 implementation review. | Different H743 package, sensor set, pin map, and firmware assumptions. Repository design claims remain reference-only; ST/Bosch/TDK/TI datasheets control Rev A. | `[VERIFIED]` source and documents; architecture reuse `[RECOMMENDATION]` |
| 10 | `http[LOCAL_SOURCE]` | Intended as a PCB review reference. | Only after the original URL/post is resolved. | The path supplied earlier appears malformed/uncertain. No technical conclusion is assigned to it until rechecked. | `[OPEN]` |
| 11 | `http[LOCAL_SOURCE]` | Practical FC guidance: SPI IMU with CS/interrupt, dedicated IMU regulator, H7 timer/DMA/DMAMUX awareness, I2C baro/mag, ADC, SD/blackbox, and layout review points. | IMU interrupt/bus discipline, power-noise target as a design recommendation, timer/DMA collision review, and bring-up checklist. | Betaflight-specific guidance must be adapted to ArduPilot/PX4 and the Rev A modular architecture; it is not a substitute for sensor or MCU datasheets. | `[VERIFIED]` guideline; adapted reuse `[RECOMMENDATION]` |
| 12 | `http[LOCAL_SOURCE]` | Duplicate of item 1. | Same reuse map as item 1. | Not independent evidence. | `[VERIFIED]` duplicate; no new weight |
| 13 | `http[LOCAL_SOURCE]` | Community H743VIT6/ICM-42688-P/BMP388 FC review with 9/5/3.3 V domains, USB-C, microSD, UARTs, and four-layer style. | Closest part-family comparison for checking common schematic omissions and review questions. | Community post; all pin, regulator, footprint, shunt, and layout claims must be rechecked against official documents. | `[VERIFIED]` link; technical reuse `[CANDIDATE]` |
| 14 | `http[LOCAL_SOURCE]`<br>`http[LOCAL_SOURCE]`<br>`http[LOCAL_SOURCE]`<br>`http[LOCAL_SOURCE]`<br>`http[LOCAL_SOURCE]` | Educational STM32 drivers, AHRS/EKF concepts, sensor abstraction, quaternion visualization, and test scaffolding. | Driver/test structure and estimator-learning material. | Not a drop-in autopilot, not the selected sensor, and not a replacement for ArduPilot/PX4 flight validation. | `[VERIFIED]` links; learning reuse `[CANDIDATE]` |
| 15 | `http[LOCAL_SOURCE]` | Pixhawk 2.1 schematic/architecture reference with port, power, and redundancy ideas. | Documentation style, port/power concepts, and interface review prompts. | Older assumptions and mixed licensing; each file must be reviewed before any reuse. | `[VERIFIED]` link; reuse `[CANDIDATE]` |
| 16 | `http[LOCAL_SOURCE]` | Beginner custom-FC discussion emphasizing known-good hardware and hardware-first testing. | Bench-first process and risk control. | Not a validated circuit or firmware reference. | `[VERIFIED]` link; process reuse `[CANDIDATE]` |

### 1.2 Cross-design circuit comparison

| Topic | OpenFC-Lite-Mini | Shirley-FC-Dev-Board | Pixhawk / Betaflight guidance | Rev A conclusion |
|---|---|---|---|---|
| FC power entry | Battery-oriented compact FC; separate bucks/LDOs, USB/battery OR concept, but no reverse-polarity protection in the repository notes | External 5 V power-module concept, 5 V MUX, 3V3 digital buck, separate 3V3 analog LDO | Power monitoring and documented power states are emphasized | Use Shirley-style domain separation with a protected external `5V_FC`; do not copy OpenFC raw-battery connector or its missing reverse-polarity protection |
| IMU rail and bus | Dedicated IMU analog rail; SPI sensor; high-rate FC layout | Separate analog/digital rails and local high-rate sensors | Dedicated IMU LDO, SPI, CS and interrupt are recommended | Fixed `ICM-42688-P` over SPI on `3V3_SENS`, CS plus INT1, local decoupling, short quiet routing |
| Barometer | OpenFC has no barometer in the current README | BMP390 local bus with protected onboard placement | I2C barometer/magnetometer is a common practical topology | Keep BMP390 onboard with protected vent; prefer short local I2C so the IMU SPI bus remains dedicated |
| Motor boundary | Signal-level DShot concept, but the OpenFC ESC connector also carries battery/current/telemetry signals | Four local timer outputs and modular ESC wiring | H7 timer/DMA and DShot support are emphasized | Reuse only the signal/GND concept; Rev A `ESC_SIG` must not carry VBAT, BEC, or motor current |
| Logging | microSD on SPI | SDMMC1 4-bit microSD | SD/blackbox is useful but consumes pins and adds EMI/mechanical work | Provision removable microSD if ArduPilot logging is required; keep SPI NOR as an alternate/DNP option until firmware storage is frozen |
| USB/debug | USB-C, USB-only flashing, no SWD in the repository notes | USB FS, ESD, Tag-Connect SWD/SWO | SWD and accessible debug/test points are preferred for custom H7 work | Hybrid: USB-C FS plus SWD/NRST/BOOT0/test pads; do not rely on USB-only recovery |
| Modularity | Compact serviceable connectors | GH1.25 ports for RC/GPS/telemetry/CAN | Pixhawk categories and documentation discipline | Use Pixhawk-like functional port names, but leave exact connector mate/pinout open |
| Firmware relevance | RP2354A/PIO/Betaflight-oriented | H743 reference with its own mapping | ArduPilot/PX4 need explicit board definitions and timing maps | H743 electrical design is independent of the reference firmware targets; final `hwdef`/board mapping remains open |

## 2. Official sources controlling electrical and firmware claims

The following direct links were checked or retained as the primary control sources. Community designs above are not allowed to override them.

### 2.1 MCU and sensor datasheets

- **[VERIFIED]** ST `STM32H743VI` datasheet, DS12110 Rev 11: `http[LOCAL_SOURCE]`
- **[VERIFIED]** ST product page for `STM32H743VIT6`: `http[LOCAL_SOURCE]`
- **[VERIFIED]** TDK/InvenSense `ICM-42688-P` product page: `http[LOCAL_SOURCE]`
- **[VERIFIED]** TDK/InvenSense `ICM-42688-P` official datasheet used for supply/interface/circuit checks: `http[LOCAL_SOURCE]`
- **[VERIFIED]** Bosch `BMP390` product page: `http[LOCAL_SOURCE]`
- **[VERIFIED]** Bosch `BMP390` datasheet: `http[LOCAL_SOURCE]`

### 2.2 Regulators, power mux, CAN, USB ESD, and storage

- **[VERIFIED]** TI `LMR33630` datasheet: `http[LOCAL_SOURCE]`
- **[VERIFIED]** TI `TPS62162` datasheet: `http[LOCAL_SOURCE]`
- **[VERIFIED]** TI `LM5163` datasheet: `http[LOCAL_SOURCE]`
- **[VERIFIED]** TI `LP5907` product page: `http[LOCAL_SOURCE]`
- **[VERIFIED]** TI `LP5907` datasheet: `http[LOCAL_SOURCE]`
- **[VERIFIED]** TI `LP5912` product page: `http[LOCAL_SOURCE]`
- **[VERIFIED]** TI `LP5912` datasheet: `http[LOCAL_SOURCE]`
- **[VERIFIED]** TI `TPS2116` product/datasheet entry: `http[LOCAL_SOURCE]` and `http[LOCAL_SOURCE]`
- **[VERIFIED]** TI `TPS2113A` datasheet: `http[LOCAL_SOURCE]`
- **[VERIFIED]** TI `TCAN332` product page: `http[LOCAL_SOURCE]`
- **[VERIFIED]** TI `TCAN33x` datasheet: `http[LOCAL_SOURCE]`
- **[VERIFIED]** TI `SN65HVD230` datasheet: `http[LOCAL_SOURCE]`
- **[VERIFIED]** ST `USBLC6-2` product page: `http[LOCAL_SOURCE]`
- **[VERIFIED]** ST `USBLC6-2` datasheet page: `http[LOCAL_SOURCE]`
- **[VERIFIED]** TI `TPD4EUSB30` product page: `http[LOCAL_SOURCE]`
- **[VERIFIED]** TI `TPD4EUSB30` datasheet: `http[LOCAL_SOURCE]`
- **[VERIFIED]** Winbond `W25Q128JV` documentation page: `http[LOCAL_SOURCE]`
- **[VERIFIED]** Winbond `W25Q128JV` datasheet mirror at the manufacturer domain: `http[LOCAL_SOURCE]`

### 2.3 USB-C and firmware documentation

- **[VERIFIED]** USB-IF USB Type-C specification page: `http[LOCAL_SOURCE]`
- **[VERIFIED]** USB-IF document library: `http[LOCAL_SOURCE]`
- **[VERIFIED]** TI USB Type-C guide (sink-only CC and power-path discussion): `http[LOCAL_SOURCE]`
- **[VERIFIED]** ArduPilot custom-board porting: `http[LOCAL_SOURCE]`
- **[VERIFIED]** ArduPilot flight-controller I/O/UART guidance: `http[LOCAL_SOURCE]`
- **[VERIFIED]** ArduPilot DShot guidance: `http[LOCAL_SOURCE]`
- **[VERIFIED]** ArduPilot companion-computer documentation: `http[LOCAL_SOURCE]`
- **[VERIFIED]** ArduPilot rangefinder setup: `http[LOCAL_SOURCE]`
- **[VERIFIED]** PX4 companion-computer documentation: `http[LOCAL_SOURCE]`
- **[VERIFIED]** PX4 collision prevention: `http[LOCAL_SOURCE]`
- **[VERIFIED]** PX4 rangefinder documentation: `http[LOCAL_SOURCE]`
- **[VERIFIED]** Betaflight manufacturer design guidelines: `http[LOCAL_SOURCE]`
- **[VERIFIED]** Betaflight DShot documentation: `http[LOCAL_SOURCE]`

## 3. Required circuit blocks and power-tree branches

### 3.1 Recommended Stage 01 power tree

```text
LiPo battery
  +--> ESC/PDB high-current path --> external ESCs --> motors
  |
  +--> external regulated 5V_FC [ASSUMPTION; source/rating OPEN]
          |
          +--> input protection / reverse-current or source-OR stage [OPEN]
          |       |
          |       +--> 5V_FC_PROT --> limited 5V_AUX ports [OPEN load budget]
          |       |
          |       +--> 3V3_MAIN buck --> H743 VDD, digital peripherals, logic
          |       |
          |       +--> 3V3_ANA filter / optional LDO --> H743 VDDA/VREF+
          |       |
          |       +--> 3V3_SENS low-noise LDO --> ICM-42688-P + BMP390
          |
          +--> USB-C VBUS --> USB attach/detection and USB-domain policy [OPEN]

  external PDB/shunt/current monitor
          +--> conditioned VBAT_SENSE / CURR_SENSE --> H743 ADC inputs

  separate CM5 carrier power branch
          +--> 5.1 V-class, 5 A-capable starting target [ASSUMPTION; measured load OPEN]
```

**[RECOMMENDATION]** Treat `5V_FC` as a defined external regulated input for Rev A. This keeps raw battery and motor current off the custom FC, matches the settled signal-only ESC boundary, and avoids freezing a voltage-dependent high-voltage buck before ESC/PDB data arrives.

**[OPEN]** If the ESC/PDB team cannot provide a suitable regulated FC input, add a conditional raw-battery front-end study. It must include the actual 4S/6S range, switching transients, reverse-polarity strategy, TVS/fuse/inrush behavior, thermal dissipation, and connector/cable drop. It is not accepted as the current default.

### 3.2 Power-domain policy

| Net/branch | Function | Stage 01 treatment |
|---|---|---|
| `5V_FC_PROT` | Protected regulated FC input | **[RECOMMENDATION]** Make it the source for the 3.3 V buck, sensor LDO, and limited auxiliary branch. Exact protection/OR circuit is **[OPEN]** until source and USB-power policy are known. |
| `3V3_MAIN` | H743 digital and general logic | **[RECOMMENDATION]** Synchronous buck from `5V_FC_PROT`; exact MPN/package is **[CANDIDATE]**. |
| `3V3_ANA` | H743 `VDDA`/`VREF+` and ADC reference domain | **[RECOMMENDATION]** Filtered branch from `3V3_MAIN` with ferrite/RC plus local capacitors; a dedicated LDO is **[CANDIDATE]** if ADC noise measurements require it. |
| `3V3_SENS` | ICM/BMP low-noise supply | **[RECOMMENDATION]** Dedicated 3.3 V low-noise LDO fed from protected 5 V. Do not feed a fixed 3.3 V LDO from a nominal 3.3 V buck without dropout headroom. |
| `5V_AUX` | External receiver/GNSS/telemetry/CAN/lidar service power | **[OPEN]** Current-limit or load-switch per budget; do not promise a connector current before load data. |
| `USB_VBUS` | USB-C attach/USB power input | **[OPEN]** Decide whether USB powers the FC, only detects attach, or is isolated from the aircraft rail. Avoid back-feed. |
| `CM5_5V1` | CM5 carrier power | **[DECISION]** Separate carrier/regulator branch; never derive the CM5 main load from `3V3_SENS` or a small FC rail. |

## 4. STM32H743VIT6 minimum core-support verification

The exact package is important. The current ST datasheet’s LQFP100 Figure 5 shows the following package-specific mapping and does not expose all supply names present on larger packages.

### 4.1 Core-support matrix

| Circuit block | Officially verified requirement | Stage 01 circuit selection | Status / remaining check |
|---|---|---|---|
| Main digital supply | `VDD` operating range is 1.62–3.6 V in the device family; all main supply and ground pins must be connected within permitted range. | Use `3V3_MAIN` for all exposed `VDD` pins. For LQFP100, connect `VDD` pins 11, 27, 50, and 75; connect `VSS` pins 10, 26, 49, and 74. | `[VERIFIED]` pinout/datasheet; capacitor placement and exact schematic symbol still require ERC review. |
| `VDDLDO` | The datasheet lists `VDDLDO` as the internal-regulator supply and notes that when the pin is unavailable on a package it is internally tied to `VDD`. | Do not invent an external `VDDLDO` pin on LQFP100. Follow the current LQFP100 figure and package note. | `[VERIFIED]` package rule; final library symbol must be checked against the exact device/orderable. |
| `VCAP` | Internal core regulator requires external low-ESR capacitors; datasheet gives 2.2 µF nominal, ±20% tolerated, ESR <100 mΩ. Two capacitors are shown in the power scheme. | One 2.2 µF low-ESR ceramic from each LQFP100 `VCAP` pin to ground; the current Figure 5 maps them to pins 48 and 73. No load or signal trace on these nodes. | `[VERIFIED]` electrical requirement; exact capacitor dielectric/package is `[RECOMMENDATION]` pending assembly limits. |
| Analog supply and ground | `VDDA` is required when ADC/analog functions are used; `VSSA` is the analog ground. LQFP100 exposes `VDDA` pin 21, `VSSA` pin 19, and `VREF+` pin 20. | `3V3_ANA` to `VDDA`; continuous ground plane with controlled analog return; `VSSA` to ground. | `[RECOMMENDATION]` topology; filter impedance and ADC noise budget remain `[OPEN]`. |
| ADC reference | ST shows either separated `VREF+` or `VREF+` connected to `VDDA`; the connected option uses 1 µF // 100 nF at the reference/analog node. | Prefer `VREF+` tied to `VDDA` with the datasheet decoupling network unless a later precision-reference requirement appears. | `[RECOMMENDATION]`; verify exact ADC configuration in the selected firmware and schematic review. |
| USB supply domain | The family supports `VDD33USB`/`VDD50USB` behavior, but the LQFP100 Figure 5 has no separate external USB supply pins and shows the package-specific power-pin set. | Use USB FS on the LQFP100 package-specific arrangement; do not place components on unbonded larger-package supply pins. | `[VERIFIED]` package-specific figure/notes; USB power/back-feed policy remains `[OPEN]`. |
| USB FS pins | LQFP100 maps `PA9` pin 68 to `OTG_FS_VBUS`, `PA11` pin 70 to `OTG_FS_DM`, and `PA12` pin 71 to `OTG_FS_DP`. | USB 2.0 full-speed device/configuration port using PA11/PA12 and VBUS sensing at PA9. No external high-speed ULPI PHY in Rev A. | `[VERIFIED]` pin functions; USB-C connector/ESD/series network `[CANDIDATE]` until final SI and footprint review. |
| High-speed USB | H743 OTG_HS1 high-speed operation needs an external ULPI PHY; internal FS PHY supports the lower-speed mode. | Defer HS PHY. Use internal USB FS unless a future system requirement explicitly needs HS. | `[RECOMMENDATION]` based on scope and pin budget; future HS is `[OPEN]`. |
| `NRST` | CMOS reset input has a permanent 30–50 kΩ equivalent pull-up; ST’s recommended protection figure includes a 0.1 µF capacitor and requires the external circuit to pull below the reset low threshold. | Accessible NRST test pad and optional pushbutton; place the datasheet reset capacitor footprint. Add supervisor only if brownout/reset testing justifies it. | `[VERIFIED]` internal pull-up and network guidance; exact supervisor/DNP choice `[CANDIDATE]`. |
| `BOOT0` | LQFP100 `BOOT0` is pin 94; the pin’s input range is separately specified and the absolute input limit is 9 V. | Default-low external pulldown, jumper/test pad for recovery, and documented boot procedure. | `[RECOMMENDATION]`; resistor value, jumper style, and firmware boot policy `[OPEN]`. |
| SWD | LQFP100 `PA13/JTMS-SWDIO` is pin 72; `PA14/JTCK-SWCLK` is pin 76. `PB3/JTDO/TRACESWO` is pin 89 if SWO is retained. | SWDIO, SWCLK, NRST, 3V3 reference, GND, and optional SWO test pads or a low-profile debug footprint. | `[VERIFIED]` pin functions; exact physical connector and pin order deliberately `[OPEN]`. |
| HSE | `PH0-OSC_IN` is pin 12 and `PH1-OSC_OUT` is pin 13. HSE can be crystal/resonator or external clock depending on firmware and clock tree. | Keep an HSE footprint option for the selected firmware clock requirement; do not freeze frequency yet. | `[RECOMMENDATION]`; exact oscillator, load capacitors, and frequency `[OPEN]`. |
| LSE/RTC | `PC14-OSC32_IN` pin 8 and `PC15-OSC32_OUT` pin 9 are available for a 32.768 kHz LSE option; RTC can also use other clock sources. | LSE is optional/DNP unless timekeeping or firmware needs it; preserve pads if space permits. | `[CANDIDATE]`; final RTC/time-sync requirement `[OPEN]`. |
| Timer/DMA outputs | H7 provides flexible alternate functions and DMAMUX/timer resources; output selection must not conflict with other timing-sensitive peripherals. | Reserve four timer channels for `M1..M4` DShot/PWM and keep output test pads. Exact AF/timer/DMA map is deferred to the firmware-aware pin map. | `[RECOMMENDATION]`; exact assignment `[OPEN]`. |
| FDCAN | H743 provides FDCAN controller resources; the external CAN physical layer still needs a transceiver, protection, termination, and defined bus contract. | Reserve at least one FDCAN-capable path; second CAN is a system option. | `[VERIFIED]` MCU capability; exact pins, transceiver, bitrate, and bus topology `[OPEN]`. |
| SDMMC/SPI/QSPI | H743 alternate-function tables include SDMMC1 and multiple SPI/QUADSPI resources; pin conflicts are package/mapping dependent. | Keep removable microSD and SPI NOR as mutually competing logging options until firmware and port map are frozen. | `[VERIFIED]` MCU capability; final peripheral choice `[OPEN]`. |
| Unused pins | Every unused or reserved pin needs an explicit safe state in the schematic/firmware review. | Add a no-connect/safe-state table and avoid leaving reserved sensor pins undefined. | `[RECOMMENDATION]`; final table `[OPEN]` until complete pin map. |

### 4.2 Minimum H743 schematic net groups

These are schematic planning groups, not a final connector pinout or PCB route:

`3V3_MAIN`, `3V3_ANA`, `3V3_SENS`, `GND`, `VSSA`, `VDDA`, `VREF+`, `VCAP1`, `VCAP2`, `VBAT`, `NRST`, `BOOT0`, `SWDIO`, `SWCLK`, optional `SWO`, optional `HSE_IN/HSE_OUT`, optional `LSE_IN/LSE_OUT`, `USB_VBUS`, `USB_DM`, `USB_DP`, four timer outputs, ADC monitor inputs, UARTs, FDCAN, storage, buzzer, LEDs, and test points.

## 5. Candidate topology and component matrix

### 5.1 Main power and 3.3 V conversion

| Option | Official electrical data | Advantages | Limitations/dependencies | Stage recommendation |
|---|---|---|---|---|
| `TPS62162`-class buck | TI datasheet: 3–17 V input, up to 1 A, adjustable output range includes 3.3 V, compact synchronous converter. `http[LOCAL_SOURCE]` | Fits a protected 5 V input, compact, likely adequate for bare H743 plus sensors and logic. | Not a raw 6S-input part; 1 A requires a real total-load and transient budget; exact package/MPN/inductor/layout open. | **[RECOMMENDATION]** for `5V_FC_PROT -> 3V3_MAIN` if the measured FC load is below the verified 1 A design envelope. |
| `LMR33630`-class buck | TI datasheet: 3.8–36 V input, 1–24 V adjustable output, 3 A, 400 kHz/1.4 MHz/2.1 MHz options, PGOOD/EN, thermal/current/short protection. `http[LOCAL_SOURCE]` | More input and current headroom; can serve a raw 4S/6S conditional front end or a higher-load 5 V/3.3 V branch. | Larger switching/thermal/layout burden; 36 V maximum can have little transient margin above a 6S pack without a specified TVS/front end; switching node must be kept away from sensors. | **[CANDIDATE]** retained as the robust/high-voltage alternative, not automatically selected. |
| `LM5163`-class buck | TI datasheet: 100 V input and 0.5 A synchronous buck family. `http[LOCAL_SOURCE]` | High input-transient headroom for a conditional raw-battery branch. | 0.5 A output limit; may not cover all FC/auxiliary loads; more design work and no need under the current external-5-V assumption. | **[CANDIDATE]** only if raw-battery entry is forced by PDB data. |
| Separate 5 V and 3.3 V bucks | Two conversion stages with an explicit `5V_FC` branch and `3V3_MAIN` branch. | Clear power budgeting and can support external 5 V peripherals. | More area/parts; should not be added without load data. | **[OPEN]** until PDB/auxiliary-load data. |

**Selection:** `[RECOMMENDATION]` use a protected external `5V_FC` as the Stage 01 input contract, then a `TPS62162`-class 3.3 V main buck if the load budget permits. Preserve an `LMR33630`-class alternative for raw-battery or higher-load cases. Exact MPN, package, inductor, switching frequency, compensation/layout, and thermal result remain `[OPEN]`.

### 5.2 Quiet sensor rail

| Option | Official electrical data / design behavior | Advantages | Limitations | Stage recommendation |
|---|---|---|---|---|
| `LP5912` 3.3 V low-noise LDO | TI specifies 1.6–6.5 V input, up to 500 mA, 12 µV RMS typical output noise, 75 dB typical PSRR at 1 kHz, 1 µF ceramic input/output, enable/power-good/output discharge. `http[LOCAL_SOURCE]` | Meets the 500 mA class of margin suggested by Betaflight’s ICM-42688-P guidance; good 5 V-to-3.3 V sensor branch. | 3.3 V fixed-output variant and exact orderable/package must be checked; dissipates `(5 V - 3.3 V) × sensor current`. | **[RECOMMENDATION]** feed from `5V_FC_PROT`, not from nominal `3V3_MAIN`. |
| `LP5907` 3.3 V low-noise LDO | TI specifies 2.2–5.5 V input, up to 250 mA, low noise and high PSRR class; `http[LOCAL_SOURCE]` and `http[LOCAL_SOURCE]` | Electrically ample for the very low sensor load and compact. | 250 mA is below the Betaflight guideline’s suggested 500 mA LDO class for ICM-42xxx designs; exact output/input capacitance and orderable remain to be checked. | **[CANDIDATE]** if current/noise/availability and the team accepts the lower margin. |
| Ferrite/RC only | Passive isolation from `3V3_MAIN`. | Small and inexpensive. | Does not regulate or guarantee the rail under load; cannot substitute for a dedicated low-noise LDO for the primary IMU. | **[CANDIDATE/DNP]** footprint option for measurement, not the default. |
| LDO after nominal 3.3 V buck | 3.3 V output LDO requires input headroom above 3.3 V according to its dropout. | Can isolate buck ripple if the buck is deliberately set above 3.3 V. | Incorrect if `3V3_MAIN` is exactly 3.3 V; output may fall out of regulation. | **[OPEN]** only if a 3.5–4 V intermediate rail is deliberately designed and thermal-checked. |

**Selection:** `[RECOMMENDATION]` dedicate `3V3_SENS` to the ICM-42688-P and BMP390. Use a low-noise 3.3 V LDO from protected 5 V, with `LP5912`-class margin as the leading candidate. Keep the sensor ground continuous with the main ground plane; do not create a high-impedance “analog ground island” that breaks return paths.

### 5.3 ICM-42688-P IMU circuit

| Topology | Verified facts and dependencies | Stage status |
|---|---|---|
| SPI on dedicated local bus | TDK specifies separate `VDD` and `VDDIO`, each 1.71–3.6 V; SPI host rate up to 24 MHz; the official application circuit shows 0.1 µF + 2.2 µF at `VDD` and 10 nF at `VDDIO`. The package is 2.5 × 3.0 × 0.91 mm LGA-14. Official links: `http[LOCAL_SOURCE]` and `http[LOCAL_SOURCE]`. | **[DECISION]** fixed baseline. Use `3V3_SENS` for both supplies unless a later firmware/rail analysis requires another valid voltage. Provide dedicated CS and INT1; keep INT2/FSYNC/CLKIN optional. |
| I2C for IMU | Supported by the part, but slower and less aligned with the high-rate primary-stabilization role. | **[CANDIDATE/DNP]** not recommended for Rev A primary IMU. |
| External clock on `INT2/FSYNC/CLKIN` | Part supports an external clock input, but its use depends on firmware timing requirements and clock architecture. | **[OPEN]** leave per the official connection guidance; do not silently add an oscillator or tie the pin incorrectly. |
| Sensor power switching | The sensor’s host interface must not be driven into an unpowered I/O domain; independent rail switching needs isolation/firmware sequencing. | **[RECOMMENDATION]** keep `3V3_SENS` always present while H743 I/O is active, unless a reviewed power-isolation circuit is added. |
| Noise/layout | Betaflight guidance recommends a dedicated IMU LDO and gives a <50 µV p-p rail-noise design target plus at least 500 mA LDO class; this is a design recommendation, not an ICM datasheet limit. | **[RECOMMENDATION]** use as a measurement target and keep the IMU away from switching nodes, connectors, mounting stress, and high-current paths. |

### 5.4 BMP390 barometer circuit

| Topology | Verified facts and dependencies | Stage status |
|---|---|---|
| Local I2C | Bosch specifies `VDD` 1.65–3.6 V, `VDDIO` 1.2–3.6 V, I2C/SPI interfaces, 100 nF recommended at each supply in the I2C diagram, and 4.7 kΩ I2C pull-ups in the same diagram. `CSB` high at power-on selects I2C; `SDO` selects address 0x76/0x77. Official datasheet: `http[LOCAL_SOURCE]`. | **[RECOMMENDATION]** short local I2C bus on `3V3_SENS`, with documented pull-up ownership and a deterministic CSB/SDO strap. This preserves the primary SPI bus for the IMU. |
| Local SPI | Bosch supports 3-/4-wire SPI up to 10 MHz; `CSB` low selects SPI. | **[CANDIDATE]** retain only if the chosen firmware/driver or bus-integrity plan needs SPI. It consumes another CS and does not automatically improve a short onboard barometer link. |
| Protected vent | Bosch requires appropriate venting for ambient pressure and gives mounting cautions including clearance, liquid/light exposure, and no vapor-phase soldering. | **[DECISION]** protected vent and mechanical keep-out; exact opening, enclosure, coating, and prop-wash treatment `[OPEN]`. |
| Barometer interrupt | The device has an interrupt function, but the FC firmware may poll or use data-ready depending on driver. | **[CANDIDATE]** provide an optional INT net/test pad without consuming the final pinout until firmware mapping is known. |

### 5.5 CAN physical layer

| Candidate/topology | Verified facts | Stage status |
|---|---|---|
| `TCAN332` / `TCAN332DCN` | TI specifies a single 3.3 V supply, ISO 11898-2 compatibility, standard-device data rate up to 1 Mbps, ±12 V common-mode range, ±14 V bus-fault protection, SOT-23/SOIC options, and high ESD/protection features. Official links: `http[LOCAL_SOURCE]` and `http[LOCAL_SOURCE]`. | **[RECOMMENDATION]** for classic 1 Mbps DroneCAN/CAN-style use if the bus contract is supplied. Exact package/MPN and availability `[OPEN]`. |
| `TCAN332G` class | TI identifies the G variants for CAN FD timing/data-rate capability up to the 5 Mbps class. | **[CANDIDATE]** if the external system explicitly requires CAN FD; do not pay the pin/firmware/EMC complexity cost without that requirement. |
| `SN65HVD230` | TI specifies 3.3 V operation, ISO 11898-2 compatibility, up to 1 Mbps, SOIC-8, and older protection characteristics. Official datasheet: `http[LOCAL_SOURCE]`. | **[CANDIDATE]** alternate if procurement or footprint favors it; TCAN332 has the stronger current integrated protection story. |
| Termination | A CAN transceiver is not the bus termination. A nominal 120 Ω termination is normally enabled only at each physical bus end; split termination/common-mode filtering depends on cable/EMC data. | **[RECOMMENDATION]** selectable 120 Ω provision at the FC port; exact switch/jumper and whether the FC is always an endpoint `[OPEN]`. |
| Protection | CAN cable exposure may justify TVS/common-mode choke; the choice depends on cable length, environment, and transceiver protection. | **[CANDIDATE]** TVS and choke footprints; exact parts and placement `[OPEN]`. |

### 5.6 USB-C, USB FS, ESD, and power-path options

| Option | Technical comparison | Stage status |
|---|---|---|
| USB-C USB 2.0 FS, device/configuration only | Uses H743 PA11/PA12 FS data pins and PA9 VBUS sense; no HS ULPI PHY. Lowest pin/EMI/firmware complexity consistent with configuration/debug. | **[RECOMMENDATION]** |
| USB-C sink-only CC network | USB-IF controls the connector standard. TI’s guide describes the simple sink-only case using 5.1 kΩ `Rd` on CC1/CC2, but VBUS capacitance and power-path behavior can require isolation/load switching. | **[RECOMMENDATION]** use only after deciding whether USB may power the FC; exact CC/power path `[OPEN]`. |
| `USBLC6-2` class | ST lists two data-line protection, VBUS protection, 3.5 pF max line capacitance, SOT-666/SOT23-6L options, and IEC 61000-4-2 level 4 device compliance. Official links: `http[LOCAL_SOURCE]` and `http[LOCAL_SOURCE]`. | **[RECOMMENDATION]** for USB 2.0 FS if the package/land pattern is accepted. |
| `TPD4EUSB30DQAR` class | TI specifies four channels, 0.8 pF typical I/O capacitance in the DQA package, USB 3.0 suitability, ±8 kV IEC contact rating, and 5 A 8/20 µs surge rating. Official datasheet: `http[LOCAL_SOURCE]`. | **[CANDIDATE]** low-capacitance alternative; its data-line device does not by itself define the VBUS power protection path, and the USON package/assembly must be checked. |
| USB VBUS powers `5V_FC` directly | Simple but risks back-feed, uncontrolled inrush, and interaction with aircraft 5 V. | **[OPEN/DNP]** not accepted without a reviewed source-OR/load-switch design. |
| USB VBUS only for detection/USB domain | Avoids back-feed and aircraft-rail interaction; requires an explicit USB-domain implementation consistent with the LQFP100 supply arrangement. | **[RECOMMENDATION]** leading policy, pending firmware/service requirements. |
| Example receptacle `USB4105-GF-A` | Earlier project notes listed it only as an example candidate. | **[CANDIDATE]** exact footprint, mating plug, shell/grounding, retention, current rating, and supplier availability must be verified before use. |

### 5.7 SWD, boot, reset, and bring-up access

| Topology | Advantages | Limitations | Stage status |
|---|---|---|---|
| SWD test pads + optional Tag-Connect/low-profile footprint | Small, direct production/debug access, no permanent tall header | Requires a fixture/cable and exact pad spacing; no final mate yet | **[RECOMMENDATION]** |
| 2.54 mm SWD header | Easy bench access and probing | Larger, heavier, less protected in aircraft | **[CANDIDATE]** for bench prototype only |
| USB-only flashing | Reduces connector count | Weaker recovery path if boot/USB/power is wrong; OpenFC reference explicitly lacks SWD | **[DNP]** for Rev A custom H743 |
| Datasheet NRST network + accessible test point | Low part count and reliable manual/programmer reset | Brownout supervisor not guaranteed by simple RC | **[RECOMMENDATION]**; supervisor `[CANDIDATE]` if testing shows need |
| BOOT0 pulldown + jumper/test pad | Default normal boot with recovery access | Requires a documented recovery sequence | **[RECOMMENDATION]**; exact resistor/jumper `[OPEN]` |

### 5.8 ADC battery/current monitoring

| Option | Technical behavior | Stage status |
|---|---|---|
| External PDB/shunt monitor -> FC ADC | Keeps high-current copper and shunt on the PDB/ESC side; FC receives low-current analog monitor signals and performs calibration/failsafe handling. | **[RECOMMENDATION]** matches the fixed architecture. Exact monitor output range, gain, ground reference, and connector source `[OPEN]`. |
| Direct battery divider on FC | Simple voltage measurement, but exposes the FC to raw-battery transients and depends on full-charge range. | **[CANDIDATE/CONDITIONAL]** only if the source is protected and intentionally brought to the FC. Not the default. |
| Divider + RC at ADC | A resistor divider plus series resistor/capacitor can attenuate and filter the signal; the ADC pin must remain within `VREF+`/`VDDA`. | **[RECOMMENDATION]** provide value footprints and test points, but leave values `[OPEN]` until 4S/6S and monitor scale are known. |
| Buffered ADC input | Reduces divider loading and can drive faster ADC sampling; adds op-amp offset, power, stability, and fault-protection work. | **[CANDIDATE]** only if the source impedance/sample-time calculation requires it. |
| Digital power monitor over CAN/UART | Can move scaling/calibration to a smart PDB/module. | **[CANDIDATE]** if the external power monitor exposes a verified protocol; do not assume it replaces FC-owned power failsafe. |

OpenFC’s `100 kΩ/10 kΩ` battery-divider and `1 kΩ + 100 nF` current-filter values are reference examples only. They are not frozen Rev A values because the source scale, ADC reference, battery range, allowable fault current, and firmware calibration are not yet supplied.

### 5.9 ESC signal output circuit

| Option | Circuit treatment | Stage status |
|---|---|---|
| DShot | Four H743 timer-capable 3.3 V outputs, one per motor, with signal-ground return. Optional small series-resistor footprints near the MCU can control edge ringing. Exact timer/DMA/AF map depends on the final firmware allocation. | **[DECISION]** preferred protocol direction; electrical pin map `[OPEN]`. |
| PWM fallback | Same output boundary can be used for PWM bring-up if the selected ESC accepts it. | **[DECISION]** fallback; exact frequency/polarity/arming behavior `[OPEN]`. |
| CAN/DroneCAN ESC | Moves motor protocol to CAN transceiver/bus contract and is a different architecture, not a drop-in DShot option. | **[CANDIDATE]** only if the external ESC team selects it. |
| Level shifting | Avoid by default because the H743 is a 3.3 V MCU and the external ESC logic level is unknown. | **[RECOMMENDATION]** add only if the selected ESC input threshold requires it; signal logic `[OPEN]`. |
| Pull-down/default state | A defined safe output state is needed during reset/boot. | **[RECOMMENDATION]** include footprints/options after the selected ESC input behavior is known; do not assume a resistor value. |
| Connector power | No battery, BEC, or high-current motor power on `ESC_SIG`. | **[DECISION]** signal/GND only; connector pinout/mate `[OPEN]`. |

### 5.10 Storage and logging

| Option | Technical comparison | Firmware/implementation dependency | Stage status |
|---|---|---|---|
| microSD via SDMMC1 4-bit | Removable logs, high capacity, convenient for ArduPilot/PX4 development; H743 has SDMMC resources and the LQFP100 exposes a usable candidate pin group. | Consumes several pins, has connector/ESD/EMI/mechanical concerns, and needs final firmware mapping and card-power policy. | **[RECOMMENDATION]** if integrated autopilot logging is required for Rev A. |
| microSD via SPI | Fewer dedicated SDMMC signals and can share an SPI controller with careful CS discipline. | Lower/less deterministic throughput and bus-sharing/EMI decisions; firmware support still required. | **[CANDIDATE]** |
| `W25Q128JV` SPI/Quad-SPI NOR | Winbond specifies a 128 Mbit/16 Mbyte device, 2.7–3.6 V supply, standard/Dual/Quad SPI, and up to 133 MHz clock class. Official links: `http[LOCAL_SOURCE]` and `http[LOCAL_SOURCE]`. | Requires firmware storage integration, reserved flash region/parameter policy, and exact package/land-pattern verification. | **[CANDIDATE]** simpler compact option; can be DNP when microSD is populated. |
| No storage | Simplest motor/sensor proof-of-life and lowest pin/EMI risk. | Weakens estimator/flight-log debugging and integrated-autopilot development. | **[CANDIDATE/DNP]** for the first electrical bring-up build only. |

ArduPilot’s custom-board porting guidance requires the storage method and flash reservation to be represented in the board definition; it also allows a no-storage build. Therefore, storage cannot be frozen from a reference PCB alone.

### 5.11 Buzzer, LEDs, and indicators

| Option | Circuit | Stage status |
|---|---|---|
| Status/power LED | MCU GPIO -> current-limiting resistor -> LED to ground or supply, with a defined reset state. | **[RECOMMENDATION]** one power LED and at least one firmware status LED; exact colors/MPNs `[OPEN]`. |
| Active buzzer, low-side NMOS | `5V_AUX` or approved buzzer rail -> buzzer -> NMOS drain; source to GND; gate from GPIO with pulldown and optional series resistor. `2N7002K-7-W` was the earlier example candidate. | **[RECOMMENDATION]** robust for an unknown low-current buzzer; exact buzzer voltage/current and MOSFET MPN `[OPEN]`. |
| Direct MCU buzzer drive | Fewer parts. | Only valid for a verified low-current load within GPIO limits; not safe as the generic interface. | **[CANDIDATE/DNP]** |
| BJT low-side switch | Cheap and simple. | Base-current calculation and saturation loss; less flexible for unknown loads. | **[CANDIDATE]** alternate |

### 5.12 External modular ports and protection blocks

| Port group | Required circuit blocks | What remains open |
|---|---|---|
| `POWER1` | Protected `5V_FC` input, GND, conditioned `VBAT_SENSE`, conditioned `CURR_SENSE`, optional status signal, test points. | Source voltage/current, shunt/monitor output, fuse/TVS/OR strategy, exact connector/mate/pinout. |
| `ESC_SIG` | Four timer outputs, four signal-ground returns, optional series resistors/test pads. No VBAT. | ESC protocol/threshold, telemetry feedback, exact timer/DMA map, connector/mate/pinout. |
| `RC_IN` | UART-capable RX/TX, approved `5V_AUX` if required, GND, ESD/series protection appropriate to cable. | Receiver protocol, inversion, logic level, current, exact pinout. |
| `GPS1` | UART, optional I2C, optional PPS, `5V_AUX`, GND, connector-side ESD/series protection. | GNSS/compass model, PPS use, magnetic placement, I2C ownership, cable length. |
| `CAN1/CAN2` | H743 FDCAN -> 3.3 V transceiver -> CANH/CANL, GND, optional `5V_AUX`, selectable termination, cable protection. | Number of buses, bitrate, node IDs/messages, termination position, TVS/choke, connector/pinout. |
| `TELEM1` | UART TX/RX and optional CTS/RTS with ESD/series protection; `5V_AUX` only within budget. | Radio protocol, flow-control requirement, supply/current, connector/pinout. |
| `COMPANION` | UART/CAN data link, common ground/reference, no CM5 main-power path. | CM5 carrier interface, transport (UART/MAVLink/CAN), direction/flow control, command/failsafe contract. |
| `LIDAR_FC` | Low-volume validated scalar-lidar UART/CAN path and approved auxiliary power. | Exact lidar model/role/interface/rate/frame/invalid-data behavior. |
| `AUX_UART/AUX_SPI` | Optional data ports with ESD/series protection and test pads. | Required number, voltage, bus ownership, and final map. |

The earlier `JST-GH 1.25 mm` family and `SM04B-GHS-TB-LF-SN` example remain connector candidates only. Exact mating housing, keying, current, retention, cable, supplier, and pin order are intentionally `[OPEN]`.

## 6. Recommended hybrid circuit design

### 6.1 Yes — a hybrid circuit is the correct Rev A approach

The recommended design combines **compatible circuit principles**, not whole-board clones:

| Borrowed principle | Source | How it is adapted |
|---|---|---|
| Hierarchical power domains and external 5 V power-module thinking | Shirley-FC-Dev-Board | `5V_FC_PROT -> 3V3_MAIN`, separate `3V3_ANA`, separate `3V3_SENS`; exact parts are re-evaluated for H743VIT6 and supplied loads. |
| Dedicated quiet IMU rail and signal-level ESC concept | OpenFC-Lite-Mini | Use only the low-current signal/GND portion of its ESC idea; reject its raw-battery connector/power assumptions and use the fixed Rev A signal-only boundary. |
| SPI IMU with CS/interrupt and H7 timer/DMA review | Betaflight guidance | Apply to ICM-42688-P and ArduPilot/PX4 allocation; treat noise/500 mA guidance as a design target, not a TDK specification. |
| H743 core, package power, USB, VCAP, and alternate functions | ST datasheet | Use the exact LQFP100 Figure 5 and DS12110 Rev 11, including VCAP pins 48/73 and package-specific absent supply pins. |
| Onboard BMP390 and protected vent | Project baseline + Bosch datasheet + Shirley architecture | Use local I2C and Bosch straps/caps; do not copy Shirley’s H743ZI pin map. |
| Functional modular ports and serviceability | Pixhawk standards + Shirley | Use names such as `POWER1`, `GPS1`, `CAN1`, `TELEM1`, and `COMPANION`; do not claim standard-compatible pinout until the exact standard is intentionally implemented. |
| Firmware-aware storage/DShot/board port | ArduPilot/PX4 docs | Freeze the hardware/firmware contract together; retain PWM bring-up and a no-storage electrical build option. |

### 6.2 Hybrid topology to carry into the Stage 02 schematic plan

```text
Protected external 5V_FC
  +--> 5V_AUX current-limited branch ------------------> external low-current ports
  +--> TPS62162-class 3V3_MAIN buck -------------------> H743 VDD and digital logic
  +--> 3V3_ANA filter / optional analog LDO -----------> H743 VDDA/VREF+
  +--> LP5912-class 3.3V low-noise LDO ---------------> 3V3_SENS
                                                          +--> ICM-42688-P VDD/VDDIO
                                                          +--> BMP390 VDD/VDDIO

H743 LQFP100
  +--> dedicated SPI + CS + INT1 ----------------------> ICM-42688-P
  +--> short local I2C + CSB-high + SDO strap ---------> BMP390
  +--> four timer/DMA outputs + signal grounds --------> ESC_SIG only
  +--> FDCAN controller -------------------------------> TCAN332-class transceiver
  +--> USB FS PA11/PA12 + VBUS sense PA9 --------------> USB-C + ESD
  +--> SWDIO/SWCLK/NRST/BOOT0 -------------------------> debug/recovery pads
  +--> ADC inputs <------------------------------------- conditioned PDB monitor
  +--> SDMMC1 or SPI/QSPI storage ---------------------> logging option
  +--> GPIO + NMOS ------------------------------------> buzzer; LEDs via resistors

CM5 carrier
  +--> separate 5.1V-class rail and bulk capacitance
  +--> data-only FC link; never required for basic stabilization/failsafe
```

### 6.3 Why this combination is technically preferred

1. **Noise and timing:** the primary IMU is local, on SPI, with a dedicated low-noise rail and interrupt; it is not exposed to a long modular sensor cable.
2. **Power safety:** raw battery and motor current remain on the ESC/PDB side. The FC only receives a defined regulated input and low-current monitor signals.
3. **H743 package correctness:** the design follows the exact LQFP100 power/USB/debug map rather than copying a larger H743 package.
4. **Firmware flexibility:** four timer outputs can support DShot or PWM bring-up, while the MCU retains UART/CAN/ADC/storage options for ArduPilot or PX4.
5. **Serviceability:** external navigation, telemetry, receiver, lidar, CAN, and CM5 ports remain modular without making CM5 part of the stabilization safety loop.
6. **Controlled optionality:** microSD vs SPI flash, one vs two CAN buses, USB power policy, reset supervisor, and high-voltage raw-battery input remain explicit options instead of hidden assumptions.

## 7. Stage 01 circuit-selection record

### 7.1 Carry forward as schematic-level decisions

- **[DECISION]** Bare H743VIT6 LQFP100 with all exposed VDD/VSS, VDDA/VSSA/VREF+, VCAP, NRST, BOOT0, and debug support.
- **[DECISION]** Two H743 VCAP capacitors at the exact LQFP100 VCAP pins 48 and 73.
- **[DECISION]** Onboard ICM-42688-P over local SPI with dedicated CS and INT1.
- **[DECISION]** Onboard BMP390 with protected vent; local I2C is the leading bus choice.
- **[DECISION]** External ESC board and signal/GND-only `ESC_SIG` boundary.
- **[DECISION]** CM5 data-only FC link and separate CM5 power.
- **[RECOMMENDATION]** External regulated protected `5V_FC` input as the default source contract.
- **[RECOMMENDATION]** `3V3_MAIN` buck plus separate 3.3 V low-noise sensor LDO fed from protected 5 V.
- **[RECOMMENDATION]** Separate/filtered `3V3_ANA` for `VDDA/VREF+` rather than placing H743 analog reference directly on a noisy switching node.
- **[RECOMMENDATION]** USB-C USB 2.0 FS, low-capacitance ESD, SWD pads, BOOT0 access, NRST pad, and test points.
- **[RECOMMENDATION]** TCAN332-class transceiver for a classic 1 Mbps CAN path, with selectable 120 Ω termination provision.
- **[RECOMMENDATION]** Four timer outputs with DShot preferred and PWM bring-up fallback; exact AF/DMA map deferred.
- **[RECOMMENDATION]** Removable microSD provision if the ArduPilot logging requirement is confirmed; SPI NOR as a compact alternate/DNP option.
- **[RECOMMENDATION]** Low-side NMOS buzzer driver and resistor-limited status LEDs.

### 7.2 Candidate/DNP options to show in the schematic, not in a final BOM

- **[CANDIDATE]** `LMR33630`-class high-input/current buck for a conditional raw-battery or higher-load branch.
- **[CANDIDATE]** `LM5163`-class high-voltage/low-current buck only if transient data demands it.
- **[CANDIDATE]** `LP5907` as a smaller sensor LDO if the measured load and Betaflight-derived margin are accepted.
- **[CANDIDATE]** `USBLC6-2` versus `TPD4EUSB30DQAR` USB ESD footprint choice.
- **[CANDIDATE]** `SN65HVD230` as a CAN transceiver alternate.
- **[CANDIDATE]** SPI NOR `W25Q128JV` versus microSD logging.
- **[CANDIDATE]** Reset supervisor, CAN TVS, common-mode choke, UART ESD/series networks, ADC buffer, second CAN, and optional LSE.
- **[DNP]** USB-only recovery, raw VBAT on `ESC_SIG`, CM5-fed stabilization, and a long raw external IMU cable.

## 8. Open dependencies and freeze gates

The following must be resolved before the affected circuit is promoted from recommendation/candidate to final schematic or BOM:

1. **[OPEN] ESC/PDB:** regulated FC input voltage/current, connector source, ground arrangement, transient waveform, signal threshold, telemetry/current-monitor outputs.
2. **[OPEN] Battery:** full-charge/minimum voltage, 4S/6S final choice, expected cable inductance and switching transient.
3. **[OPEN] Firmware:** exact ArduPilot board target/hwdef or PX4 board target, clock frequency, logging method, UART numbering, FDCAN mapping, timer/DMA map, DShot telemetry/bidirectional requirement.
4. **[OPEN] Receiver:** protocol, UART direction, logic level, inversion, failsafe signaling, supply current.
5. **[OPEN] External port loads:** each receiver/GNSS/telemetry/lidar/CAN device’s voltage, current, cable length, hot-plug expectation, ESD exposure, and connector mate.
6. **[OPEN] CM5 link:** carrier interface, data transport, flow control, common-ground strategy, command limits, heartbeat and failure behavior. CM5 power remains separate.
7. **[OPEN] Storage:** microSD versus SPI NOR, expected log rate/capacity, removable-card mechanics, firmware support.
8. **[OPEN] USB power:** device-only/data-only versus USB-powered FC, CC implementation, VBUS capacitance, source-OR/load-switch behavior, connector and shell grounding.
9. **[OPEN] Manufacturing:** PCB stackup, impedance capability, LGA assembly, USON/SOT package limits, microSD/connector retention, stencil/reflow limits.
10. **[OPEN] Exact MPN/footprint:** all regulators, LDOs, transceiver, ESD array, flash, MOSFET, crystals, connectors, TVS parts, and capacitors still need current manufacturer package/land-pattern/availability checks.

## 9. Stage 02 review checklist

- [ ] Reconfirm current ST datasheet revision and exact `STM32H743VIT6` symbol/pin mapping.
- [ ] ERC-check every VDD/VSS, VCAP, VDDA/VSSA/VREF+, VBAT, NRST, BOOT0, USB, and debug connection.
- [ ] Verify two 2.2 µF VCAP capacitors, ESR/dielectric/package, and zero-load routing.
- [ ] Verify `3V3_SENS` LDO input headroom, output stability capacitors, measured load, PSRR/noise, and thermal loss from 5 V.
- [ ] Calculate `3V3_MAIN` load, peak current, buck inductor, switching frequency, thermal rise, and `5V_FC` input budget.
- [ ] Complete firmware-aware timer/DMA/AF allocation for four DShot/PWM outputs, SPI IMU, local I2C baro, UARTs, CAN, ADC, USB, and storage.
- [ ] Confirm ICM-42688-P orientation, land pattern, VDD/VDDIO capacitors, CS, INT1, and optional INT2/clock treatment.
- [ ] Confirm BMP390 I2C straps, 100 nF capacitors, 4.7 kΩ pull-ups, address, CSB-at-POR behavior, vent opening, and keep-out.
- [ ] Define CAN bitrate/node/message contract, physical termination position, TVS/choke decision, and port power budget.
- [ ] Define USB-C sink/device policy, CC resistors/controller need, VBUS/back-feed protection, ESD placement, shell return, and D+/D− series-option footprints.
- [ ] Decide SWD pad/fixture geometry and recovery procedure for NRST/BOOT0.
- [ ] Set ADC divider/filter values from actual battery/monitor range and H743 ADC sample-time/source-impedance limits.
- [ ] Decide microSD versus SPI NOR and complete firmware storage reservation/parameter strategy.
- [ ] Verify buzzer load and GPIO/MOSFET behavior in reset and boot states.
- [ ] Verify connector family, exact mate, cable, current, keying, retention, pinout, and supplier only after team interfaces arrive.
- [ ] Perform schematic review against the full official source list and record each unresolved item; do not release a final purchase BOM from this artifact.

## 10. Bottom-line selection

**[RECOMMENDATION]** Use the hybrid circuit described here: Shirley-style power-domain separation, OpenFC-style dedicated sensor-rail discipline and signal-level ESC boundary, Betaflight-style SPI/interrupt/timer review, and the exact ST H743VIT6 package implementation. The leading Stage 01 path is:

`protected external 5V_FC -> 3V3_MAIN buck + 3V3_SENS low-noise LDO + filtered 3V3_ANA`, with local SPI `ICM-42688-P`, local I2C `BMP390`, H743-owned DShot/PWM outputs, external CAN transceiver(s), USB FS + ESD + SWD/BOOT0/NRST, conditioned ADC monitoring, and optional microSD/SPI NOR logging.

This is a circuit-selection recommendation, not a final BOM or routed design. The external team inputs in Section 8 are the freeze gates.

## 11. OpenESC-20x20 ESC integration addendum

**Analysis date:** 2026-08-28  
**Source reviewed:** OpenDrone-hw/OpenESC-20x20 (historical source reference)

Four independent copies share the battery input, current monitor and FC connector.
```

The repository lists four `AT32F421G8U7` MCUs, four `NSG2065Q` drivers and 24 `DOY180N03T` MOSFETs. It is not a shared-MCU ESC. The local library also contains historical/alternate symbols, so the placed schematic/PCB parts—not every library symbol—are the relevant current design.

### 11.3 External electrical interface actually present on the ESC

**[VERIFIED]** The placed `J1` is `SM08B-SRSS-TB`, and the PCB net assignment is:

| ESC J1 pin | Net in repository | Function | FC consequence |
|---:|---|---|---|
| 1 | `+BATT` | Battery-positive output after the ESC input shunt | Raw pack voltage is physically available; do not connect it to the FC unless a new protected power contract is explicitly approved. |
| 2 | `GND` | Common signal/power return | The repository exposes one numbered connector ground; cable impedance and return routing must be tested. |
| 3 | `/CURR` | Board-level current-monitor analog output | Optional FC ADC input; scale and mid-throttle validity must be bench-verified first. |
| 4 | unconnected | No dedicated telemetry wire | Extended telemetry depends on bidirectional DShot on pins 5–8. |
| 5 | `/M1` | Motor-channel 1 DShot line | H743 timer/DMA-capable output; bidirectional return path required for telemetry. |
| 6 | `/M2` | Motor-channel 2 DShot line | Same requirement. |
| 7 | `/M3` | Motor-channel 3 DShot line | Same requirement. |
| 8 | `/M4` | Motor-channel 4 DShot line | Same requirement. |

This is the key conflict with the earlier conceptual FC `ESC_SIG` grouping of `M1/GND, M2/GND, M3/GND, M4/GND`. The exact eight-pin FC port contract was still open, but it cannot be copied one-to-one from that conceptual grouping into this ESC connector without an adapter or an explicit pinout change.

### 11.4 Power and current-monitor implications

- **[VERIFIED]** The repository states a 2S–6S input range of 6.0–25.2 V and no BEC. The ESC therefore does not supply the FC or CM5 logic rails.
- **[VERIFIED]** The ESC power tree is battery input -> 0.2 mOhm shunt/current amplifier -> `+BATT`, with a local buck to approximately `+10V` and an LDO to `+3V3` for the ESC electronics.
- **[VERIFIED]** Current sensing is board-level, not four-channel. The stated chain is one 0.2 mOhm shunt plus `INA186A3IDCKR` at 100 V/V, giving a stated 20 mV/A and 165 A full-scale value against a 3.3 V ADC.
- **[VERIFIED]** Rev3.2 adds `R91/R92 = 1 kOhm`, `C52/C54 = 100 nF` to ground and `C51 = 1 uF` across the amplifier inputs. The repository explicitly says the improved network is not yet hardware-verified at mid-throttle.
- **[RECOMMENDATION]** Keep the FC’s protected external `5V_FC` architecture and separate CM5 supply. Initially leave ESC J1 pin 1 unconnected on the FC. Provide an optional, protected/testable ADC path for pin 3 only if the rev3.2 current-sense acceptance test passes.
- **[OPEN]** If anyone proposes powering the FC from J1 pin 1, the team must first provide battery transient waveforms, connector/cable current limits, reverse/inrush/overvoltage strategy, thermal calculations and a revised system power contract. This would change the present signal/GND-only FC boundary.

### 11.5 DShot, PWM and firmware implications

- **[VERIFIED]** The repository identifies AM32 as the ESC firmware and bidirectional DShot/extended DShot as the intended protocol. The official AM32 project also lists DShot 300/600, bidirectional DShot and servo PWM support: AM32 (historical source reference)

Use a mating connector/cable with the OpenESC pin order, but on the FC:

```text
J1-1  +BATT  -> NC on FC
J1-2  GND    -> FC ground
J1-3  /CURR  -> NC initially; optional conditioned ADC/test-point path later
J1-4  NC     -> NC
J1-5..8     -> four H743 bidirectional-DShot/PWM-capable outputs
```

This keeps raw battery and high-current propulsion copper off the FC while avoiding an immediate ESC PCB modification. It does require the project to replace the conceptual alternating-ground `ESC_SIG` pinout with this exact connector contract, and it requires signal-integrity testing because the ESC exposes one numbered ground return.

#### Option B — adapter/interposer (**[RECOMMENDATION]** for first bench prototype if the current FC connector contract is retained)

Keep the FC’s current signal/GND port concept and use a small harness/interposer to map four signals to `/M1`–`/M4`, fan out the common ESC ground, leave `+BATT` isolated, and optionally route `/CURR` to a protected test/ADC node.

This isolates connector orientation and pinout changes and provides useful test points. The trade-offs are extra mass, a connector failure mode and an unverified common-ground/cable topology. It must not be treated as a permanent solution until DShot waveform and return-path tests pass.

#### Option C — direct full J1 power/current integration (**[CANDIDATE / NOT RECOMMENDED FOR REV A]**)

Connect `+BATT` to a deliberately redesigned FC raw-battery input/protection stage and `/CURR` to the ADC. This eliminates an adapter and exposes current telemetry, but it contradicts the present signal/GND-only boundary and brings ESC/PDB transients into the FC connector and power tree. It should only be reconsidered after an explicit architecture change and measured transient/power testing.

#### Option D — revised ESC-side interface (**[CANDIDATE / FUTURE]**)

Retain the OpenESC power stage but revise the harness/board interface to provide the project’s desired signal/ground grouping, optional current monitor and documented protection. This is the cleanest long-term contract if the cable/ground tests fail, but it is a new ESC revision and no longer the exact unchanged repository interface.

### 11.9 Cross-team game plan

1. **[DECISION GATE] Lock the source revision.** The ESC owner must nominate an immutable commit/tag and board revision; “the GitHub main branch” is not enough.
2. **[DECISION GATE] Choose Option A or B for the first prototype.** Preserve the FC raw-power boundary unless the user explicitly approves Option C.
3. **[OPEN INPUT] Publish an ESC-FC interface-control table** containing connector mate, orientation, cable length/gauge, pin order, ground arrangement, signal voltage/threshold, DShot rate, PWM fallback, telemetry behavior, `/CURR` scale/validity, and disconnect/failsafe behavior.
4. **[FC ACTION] Reserve but do not freeze** four H743 timer/DMA-capable output candidates, one optional ADC input for `/CURR`, test points and optional series/protection footprints. Keep the IMU, BMP390, power-domain and CM5 partition unchanged.
5. **[ESC ACTION] Provide evidence**: assembled-board revision, exact BOM/datasheets, AM32 binary/configuration, flashing procedure, connector/cable drawing, motor/prop/battery current data, thermal test conditions, and rev3.2 current-sense sweep.
6. **[JOINT TEST] Validate propeller-off**: continuity and no-VBAT-at-FC check; reset/boot output state; DShot300 then DShot600 waveform; bidirectional telemetry; PWM fallback; each channel; loss of signal/ground; FC reset and ESC reset behavior.
7. **[JOINT TEST] Validate `/CURR`** at zero, low, mid and full throttle against a calibrated external current measurement. Do not use it for a safety decision until the rev3.2 hardware result is documented.
8. **[FREEZE GATE] Only after the above** freeze the FC connector pinout, ADC conditioning values, firmware output map, cable arrangement and schematic. PCB routing and the purchase BOM remain later-stage work.

### 11.10 Addendum conclusion

**[RECOMMENDATION]** Do not redesign the whole FC around the internal OpenESC gate-driver/MOSFET topology. Freeze the shared external contract only. The preferred system plan is: keep the custom bare H743 hybrid FC and separate CM5 power; use four H743 bidirectional-DShot/PWM-capable outputs; keep raw `+BATT` off the FC; treat ESC `/CURR` as optional until validated; and use either a direct OpenESC-compatible connector with pin 1 left NC or an interposer during first integration.

The current FC architecture therefore remains **[DECISION] unchanged**, while the exact FC-to-ESC connector/pinout, `/CURR` usage, cable/ground arrangement, firmware mapping and ESC revision remain **[OPEN]** for Stage 02.

## 12. BEC decision note for OpenESC integration

### 12.1 What “no BEC” means here

- **[VERIFIED]** The OpenESC README states `BEC: None`.
- **[VERIFIED]** The ESC still has internal regulated rails: the repository shows a battery-derived approximately `+10V` rail for the gate drivers and a `+3V3` rail for the four motor MCUs and current-sense amplifier. No user-facing 5 V accessory output is provided.
- **[DECISION]** No BEC is required for the ESC’s own motor-control operation, assuming the battery remains within the ESC input range and its internal rails are healthy.
- **[DECISION]** The FC remains powered from the project’s protected external `5V_FC` branch, and the CM5 remains on its separate 5.1 V-class branch. The FC must not power itself from the ESC J1 `+BATT` pin merely because the ESC has no BEC.

### 12.2 Advantages of keeping the ESC BEC-free

1. The high-current ESC PCB stays focused on motor switching, gate drive, local logic and current sensing.
2. The FC power source can be protected, filtered and monitored independently of the ESC board.
3. A BEC switching node is not added near the ESC’s sensitive current-sense and gate-drive circuitry.
4. A failure of an ESC-mounted BEC is less likely to pull down the FC, receiver and navigation power rail.
5. The FC power design can be sized for the actual receiver/GNSS/telemetry/lidar load instead of inheriting an arbitrary ESC BEC rating.
6. The CM5 cannot accidentally be powered from an undersized ESC BEC; its high transient load remains on its own branch.

### 12.3 Disadvantages of no BEC

1. The system needs a separate regulated 5 V source, such as a PDB/external UBEC or power module.
2. The wiring and power budget must be documented across more than one board.
3. A conventional FC that expects 5 V from an ESC connector cannot be connected as if J1 were a 5 V BEC output; OpenESC J1 pin 1 is `+BATT`, not 5 V.
4. Receiver, telemetry, GNSS and scalar-lidar power must be distributed from the FC or an external auxiliary-power branch.
5. If no independent regulated branch is provided, the FC/receiver could be underpowered or exposed to raw battery voltage.

### 12.4 Should a BEC be added?

**[RECOMMENDATION] Do not add an integrated BEC to the current OpenESC Rev3.3 board for this project.** Keep the ESC BEC-free and use this system-level tree:

```text
LiPo battery
  +--> PDB / ESC high-current path --> OpenESC --> motors
  +--> protected external UBEC/power module --> 5V_FC --> FC regulators and 5V_AUX ports
  +--> separate high-current regulated branch --> CM5 carrier
```

This matches the existing FC safety partition and avoids changing the exact OpenESC circuit or connector contract. The external 5 V source still needs proper input protection, current limiting, reverse-current/back-feed control, filtering, thermal analysis and a verified load budget.

### 12.5 If a BEC is later required

| Option | Assessment |
|---|---|
| External switching UBEC on the PDB/battery branch | **[RECOMMENDATION]** if a 5 V accessory supply is required. Keeps heat and switching noise away from the OpenESC PCB. |
| Separate BEC daughterboard beside the ESC/PDB | **[CANDIDATE]** useful when the PDB and FC harness need a dedicated power module; still requires output protection and cable validation. |
| Integrated switching BEC on a new ESC revision | **[CANDIDATE / NOT FOR CURRENT REV]** would require a new power stage, thermal/EMI review, protection, connector output definition and revised source/BOM. |
| Linear BEC from 6S to 5 V | **[DNP]** for FC/receiver/peripheral power except perhaps a very small, explicitly calculated load. Its dissipation is approximately `(Vin - Vout) x Iout`; at 25.2 V to 5 V and 1 A, that is about 20 W before other losses. |

An integrated BEC also cannot simply reuse J1 pin 1: that pin is already assigned to raw `+BATT`. A new BEC output would need a new connector pin, a repurposed currently unused pin, or a separate connector, each requiring a new interface contract. If a BEC is connected to the ESC’s post-shunt `+BATT` rail, its input current would also be included in the board-level current-sense measurement unless the power path is deliberately changed; this must be accounted for during calibration.

### 12.6 BEC information still open

- **[OPEN]** Total continuous and peak current for the receiver, GNSS/compass, telemetry, scalar-lidar, LEDs, buzzer and any servos.
- **[OPEN]** Final battery cell count and measured battery/PDB transients.
- **[OPEN]** Whether the PDB or another team already supplies a protected 5 V rail.
- **[OPEN]** Required 5 V connector, cable length, current rating, inrush behavior and back-feed policy.

Until these values are supplied, “no integrated ESC BEC” is the recommended architecture decision, while the exact external 5 V regulator remains a candidate rather than a final part selection.
