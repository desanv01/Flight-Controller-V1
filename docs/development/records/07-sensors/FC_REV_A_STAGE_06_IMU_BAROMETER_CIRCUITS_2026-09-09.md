> Historical technical record. Names and private workstation/session references were neutralized for publication. Dates and assertions describe the recorded stage, not current physical qualification. See the current validation-status page for later checks.

# FC Rev A — Stage 06 IMU and barometer circuits

Date: 2026-09-09  
Authority: CURRENT_CONTROL_STATE R24, Stage 06 only  
Disposition: **RECOMMENDATION CAPTURE COMPLETE; ELECTRICAL INTEGRATION OPEN.**  
This is a reviewable schematic/evidence handoff, not a Stage 06 acceptance, Stage 07 authorization, procurement release, manufacturing release or flight release.

## 1. Result and authority boundary

The ICM-42688-P and BMP390 circuits, required local signal isolation, local barometer slew support, and controlled symbols are captured. All original MCU/power source records and library symbols are preserved. Only minimum hierarchy additions connect the new sheet. Stage 05 regulator topology, compensation, protection and hardware enable logic were not changed. No other MCU resource, external connector, PCB, fabrication output or purchase was introduced.

**Integration remains OPEN for the BMP390 guaranteed minimum ramp, the IMU/direct-rail ramp and noise, actual sensor peak current, total LDO startup current including existing C41, partial-power waveforms, and exact-rail AUP thresholds.** These items cannot be closed by a successful export, nominal calculation, or ERC result. The captured local barometer solution is a conditional candidate, not proof that Bosch's minimum ramp is satisfied.

The preserved pre-change snapshot predates R24. Canonical KiCad hashes matched that snapshot before capture resumed. The current control document's R20-to-R24 change is an external project-control delta, not a Stage 06 edit. This task has not written CURRENT_CONTROL_STATE. Stage 02 pin/resource freeze, Stage 03 foundation, accepted Stage 04 core, accepted Stage 05 R18 capture/control review, CM5 change-control, net registry and EDA execution policy remain governing records.

Verified native result: **163 total real components, 155 nets, 45 new sensor-sheet components, 158 sensor pin/net checks, 68 independent source-to-symbol pin checks, nine frozen signal checks, and 413 preserved existing pin/net assignments.** Zero pin/net mismatches; zero PCB files.

Current evidence is verification_8 schematic PDF (private source record), final audit (private source record), calculation results (private source record), and source/pin audit (private source record). Earlier verification directories are development history, not the handoff baseline.

## 2. Frozen MCU boundary

| Net | H743 port / LQFP100 pin | Actual captured endpoint |
|---|---|---|
| SPI1_SCK | PA5 / 29 | U13 A1; U13 B1 to ICM pin13 |
| SPI1_MOSI | PA7 / 31 | U13 A2; U13 B2 to ICM pin14 |
| SPI1_MISO | PA6 / 30 | U19 A1; ICM pin1 through U14 then U19 |
| IMU1_CS | PE3 / 2 | U13 A3; U13 B3 to ICM pin12 |
| IMU1_DRDY | PE4 / 3 | ICM pin4 through U14/U19 |
| IMU1_INT2 | PE2 / 1 | ICM pin9 through U14/U19; optional firmware function |
| I2C2_SCL | PB10 / 46 | U17 B SCL; A SCL to BMP pin2 |
| I2C2_SDA | PB11 / 47 | U17 B SDA; A SDA to BMP pin4 |
| BARO_INT | PC13 / 7 | BMP pin7 through U18; optional firmware function |

PA0/PA1 retain their historical isolated LIDAR_FC labels and are not consumed. LSE remains DNP; PC13 is not combined with an enabled LSE configuration. SPI1 is dedicated: the buffered MISO path need not tri-state for another slave, and no additional SPI slave is authorized here.

Root changes add direct core-to-sensor hierarchical wires, MAIN/GND/SENS supply connections, and updated Stage 06 title/status text. The core gains nine wires and nine hierarchy labels. The power sheet gains one local label, one wire and one hierarchy label for the existing 3V3_SENS net. These are append-only changes in the core and power sheets; the audit checks every original parsed record remains present.

## 3. ICM-42688-P circuit and source basis

U12 is the genuine TDK InvenSense ICM-42688-P, LGA14, 2.5 × 3 mm. DS-000347 v1.9 is retained from the PDF linked in TDK's official product record. There is no invented REGOUT pin or exposed-pad connection. Physical pin identities are audited independently against the manufacturer table on page20; the 4-wire SPI reference and capacitor table are on pages21–22.

- Pins5 VDDIO and8 VDD connect directly to 3V3_SENS, with no slow switch in the IMU path.
- C51 100nF and C52 2.2uF are the VDD bypass/bulk pair. C53 10nF is VDDIO bypass. All are X7R, nominal ±10%, with 50V recommendations. Direct schematic conductors connect the bank to U12 supply pins; actual placement must put the correct capacitors beside their physical pins.
- Pin6 GND and reserved pin7 are grounded. Reserved pins2/3/10/11 are also grounded, which the manufacturer permits. Reserved pins are not arbitrary hidden NCs.
- Pins12/13/14 are CS/SCLK/SDI in 4-wire SPI. Pin1 is SDO. Native symbol alternates preserve AP_AD0, AP_SCL, AP_SDA and AP_SDIO without duplicating physical pins.
- Pin4 INT1 is the primary data-ready output. Pin9 INT2/FSYNC/CLKIN is retained as an optional interrupt function; the weak pulldown establishes the intended unused-FSYNC low state. Firmware must configure this function explicitly; no external clock is added.

U13 SN74AXC4T774PWR translates the three MCU outputs to the sensor supply domain. VCCA is MAIN, VCCB is SENS, DIR1–3 are high, DIR4 is low, and OE is grounded. A4 is NC and B4 is grounded. CS has a100k pull-up on each rail side; SCK/MOSI have100k pull-downs. These establish inactive levels during reset and isolation.

The return path is **ICM → U14 SN74AUP3G17DCUR on SENS → U19 SN74AXC4T774PWR → H743 on MAIN**. U14 provides low input leakage and Schmitt inputs; U19 provides dual-supply power-off isolation. U19 DIR1–4 are low, OE grounded, and its unused A4/B4 treatment matches U13. R39/R40/R53 are1.5M pulldowns at the lightly loaded IMU outputs; R54–R56 are22k pulldowns on the buffered return signals.

This extra input stage is deliberate: TDK specifies SDO/INT output levels with a1M load, while an AXC data input can draw4uA at85°C. Direct connection would not establish that lightly loaded output condition from the published maxima. The calculated IMU load is 2.791uA, below the conservative 2.940uA reference load at minimum VOH. U14 is on SENS so MAIN cannot directly source its inputs during sensor-off states. Buffered-side pulldowns bound AXC off leakage without loading the IMU itself.

TDK's monotonic10–90% ramp requirement is0.01–3ms. The **proposed qualification window is1–3ms** to limit incremental capacitor charging. This window is an acceptance target, not a measured property of Stage 05. The TDK10mVpp supply-noise figure is **typical**, not an absolute maximum. Verify sensor noise/aliasing under converter, radio, SD-card and motor activity before any performance claim.

## 4. BMP390 circuit and local slow rail

U16 is Bosch BMP390, LGA10, 2 × 2 mm. The source is BST-BMP390-DS002-07 revision1.7. Physical pins are audited against page46 and I2C wiring against Figure25/page48.

- Pins1 VDDIO and10 VDD use **BARO_3V3**, with a100nF bypass each (C62/C63).
- Pins3/8/9 VSS are grounded. Pin5 SA0/SDO is grounded for **7-bit address0x76**. Pin6 CSB is tied to local VDDIO for I2C. The Figure25 preference for a programmable CSB is recorded; no spare frozen GPIO is silently consumed, and SPI mode is not provided by this circuit.
- Pins2 SCL and4 SDA connect through U17 TCA9416DDFR. The DDF package pin table is used, not the differently numbered DTM package.
- U17 VCCA/OE use BARO_3V3; VCCB uses MAIN. Its internal10k pull-ups are local to each supply domain. R50/R51 add4.7k only on the barometer side. The manufacturer allows this rail/OE arrangement and either supply order; no requirement for A≤B is assumed.
- Pin7 INT crosses U18 SN74AXC1T45DBVR, A on BARO_3V3 and B on MAIN, DIR high. R52 is22k to ground, limiting worst-case off-state input lift while remaining a light BMP output load. The interrupt function remains optional in firmware.

Bosch page11 specifies a supply ramp of **at least10ms** and warns against interface-high conditions while VDDIO is off. A direct connection to the IMU ramp would conflict with that written requirement. U15 TPS22918DBVR therefore creates BARO_3V3 locally from 3V3_SENS, without changing Stage 05. C58 is input bypass, C59 is22nF C0G timing, C61 is local output bulk. QOD is tied to VOUT; R49 is a910Ω discharge/load resistor. R48/C60 provide an ON delay from SENS. There is no bypass link that can accidentally defeat the slow path.

TI gives the approximate relation SR=0.55×CT[pF]+30 us/V; its rise calculation already represents10–90%. With22nF, the nominal result is **40.029ms typical**. Capacitor/rail tolerance alone gives approximately37.257–42.849ms, but this is **not a guaranteed PVT range**: the datasheet does not bound the slew coefficient. The ON delay step screen is approximately7.86–49.12ms; retained charge and short restarts invalidate that simple calculation.

**The BMP390 integration remains OPEN. Do not energize the BMP390 until a support-circuit coupon verifies ≥10ms at its actual VDD/VDDIO pins across source/load/temperature/restart corners.** The nominal40ms result does not close this gate. If the candidate fails, only the affected local barometer support is to be revised under control; this handoff does not reopen Stage 05.

TPS22918 is not claimed to be a reverse-blocking switch. QOD requires valid operating conditions, and a charged ON capacitor can delay turn-off. MAIN-domain paths are isolated by U17/U18, local bleeders discharge stored charge, but abrupt input shorts, mid-rail states and restart waveforms still require direct measurement.

## 5. Quantitative budgets and limitations

The calculation script is reproducible and labels assumptions explicitly. MAIN uses the retained Stage05 range3.192792–3.417211V. Settled SENS uses3.267–3.333V from TPS736 ±1%, subject to its VIN headroom and ≥10mA load conditions. R41=300Ω provides at least10.573mA once SENS is in range, even before the delayed barometer rail turns on. It is a sensor-support load/discharge element, not an unrelated rail load.

| Sensor-boundary contribution | Screen mA |
|---|---:|
| R41 SENS 300R | 11.4536 |
| R49 BARO 910R | 3.7759 |
| IMU allocation NOT datasheet max | 4.0000 |
| BMP pressure peak max | 0.7300 |
| I2C A two low lines | 2.3510 |
| three buffer 22k pulldowns | 0.4686 |
| other bias and GPIO allocation | 0.3000 |
| support static allocation | 0.1500 |
| dynamic at 1MHz allocation | 0.3000 |

Total is **23.529mA**, leaving1.471mA within25mA. The IMU4mA item is an engineering allocation, **not a manufacturer maximum**; TDK gives0.88mA typical for six-axis low-noise operation. Bosch pressure peak is730uA maximum; its320uA temperature peak is a different measurement phase. The0.30mA dynamic allowance applies to1MHz bring-up, not unrestricted24MHz operation. Added MAIN load is allocated10mA within the existing MAIN budget, not an increase of that budget. The100mA sensor reserve is not permission to consume it.

With5uF maximum new direct capacitance and a1ms linear-ramp screen, incremental sensor startup is **40.194mA**, below50mA. However, **including existing Stage05 C41 at28uF gives 133.518mA at1ms and 60.192mA at3ms**. Therefore the total-LDO startup envelope is OPEN. If50mA includes C41 charging, this corner does not satisfy it even at the maximum IMU ramp. No silent reinterpretation or Stage05 component change has been made. The power/sensor owners must resolve the boundary interpretation and verify total LDO/input startup I(V,t), including source droop and concurrency.

The5uF aggregate also exceeds the4.567uF simple nominal×tolerance×X7R temperature upper sum. Individual effective-capacitance ranges in component fields remain assumptions pending manufacturer bias/aging curves. The ON-delay late screen uses1.3uF, superseding its component-field1.2uF assumption for this check. C59's manufacturer spec confirms22nF, ±5%,50V,C0G,30ppm/°C and no aging; the calculation uses±6% total. R41 dissipation is38.17mW, below the41.18mW half-rating screen after85°C resistor derating.

I2C starts at100kHz. With the internal and external pull-ups included, the conservative both-side low sink is1.631mA. Without crediting edge acceleration,1us rise-time capacitance limits are approximately338.2pF on A and94.4pF on B. Target≤50pF per side.400kHz requires tighter limits, actual VOL and waveform validation; it is not released by this capture.

SPI starts in mode0 at1MHz. TDK requires CS setup≥39ns, hold≥18ns, SDI setup≥13ns and hold≥8ns; its SDO valid maximum is21.5ns at20pF. Use≥1us CS guards for initial bring-up. An80ns round-trip engineering budget leaves420ns of the500ns half-cycle, but it is not exact static timing analysis.24MHz remains prohibited until both isolators, U14, PCB loading/skew and H743 receive timing are quantified and measured.

The AUP threshold table specifies discrete supply test points. The proportional3.0V-row screen has margin against the TDK output levels, but **it is not a manufacturer guarantee at the actual3.267–3.333V rail**. Obtain a written bound or characterize/replace the affected buffer before electrical qualification. Its leakage bounds and the threshold extrapolation are deliberately not conflated.

## 6. Reset, sequencing and partial-power contract

| State | Captured treatment | Remaining qualification |
|---|---|---|
| All rails off | Local discharge resistors; no external sensor connector | Residual-charge settling and leakage at hot corner |
| MAIN on, SENS off | U13/U19 supply isolation; U14 also off; sensor-side bias follows SENS | Off-pin excursions and internal coupling, including short restart |
| SENS on, MAIN off | U13/U19 isolate MAIN; U17/U18 protect barometer boundary | MAIN dead-rail lift and decay through actual assembled load |
| MAIN/SENS on, BARO off or ramping | U17 independent UVLO/isolation; U18 partial-power protection; baro pull-ups use local rail | Every BMP pin ≤VDDIO+0.3V through the full ramp/decay |
| MCU reset, rails valid | CS pulled high; SCK/MOSI low; IMU return and optional INT pins weakly low | Boot-ROM/pin-mode transition waveform; configure IRQ drive before use |
| Brownout / abrupt short | Stage05 hardware EN behavior retained; local isolation/discharge supports containment | Undefined intermediate supply bands are not covered by a zero-volt Ioff test |
| Normal operation | Direct IMU rail; delayed local BMP rail; common GND | Load/noise/timing/vibration/pressure tests |

At≤85°C AXC data Ioff is4uA maximum, TCA port Ioff0.5uA maximum, and AUP off-output leakage0.6uA maximum. The100k IMU-side bias lift screen is0.412V at4uA, below the ICM0.5V over-rail limit when the dead rail is near zero. The22k BMP INT lift is0.0906V, below0.3V. Buffered return pull-downs absorb leakage without placing that load on ICM outputs. A conservative100uA dead-rail allocation gives≤30.9mV SENS,≤93.73mV BARO and≤70.04mV MAIN from the bleeders alone. This is a **steady-state allocation**, not a measured board backfeed total or a guarantee through brownout. Full system reverse current remains part of the accepted Stage05/Stage07/physical-test obligations.

Firmware bring-up, after qualified supplies are stable:

1. Hold CS high and initialize SPI1 at1MHz mode0; disable unintended GPIO pulls on the return pins. Do not use IRQ edges before configuring sensor output drive.
2. Respect ICM's1ms power-up register-access delay. Read WHO_AM_I at0x75 and require0x47. Apply the documented DEVICE_CONFIG soft reset, wait1ms, verify identity again, then configure four-wire SPI and the required internal-interface disable settings from v1.9.
3. Configure INT1 push-pull and the chosen polarity before enabling data-ready. Configure INT2 explicitly only if used; otherwise preserve its inactive function. Default open-drain behavior is not the intended populated weak-pulldown IRQ operating mode. Observe the documented200us no-write interval after changing gyro/accelerometer power modes and their individual startup delays before accepting samples.
4. Wait the experimentally qualified barometer rail delay, then read BMP CHIP_ID0x00 and require0x60. Check STATUS.cmd_rdy, issue CMD0x7E=0xB6 when permitted, and recheck status/identity. Read compensation coefficients, enable pressure/temperature and set oversampling/ODR/IIR deliberately. A fixed500ms initial timeout may be used for development; it does not prove rail validity or authorize a safety decision.
5. Start I2C2 at100kHz with open-drain pins. Qualify clock stretching, NACK/timeouts, bus recovery and full power-cycle recovery. BMP INT is optional and must be configured before consuming events. Preserve monotonic timestamps and reject stale, saturated or uninitialized sensor data.

## 7. Physical guidance retained for later stages

No layout work was performed. Stage08/09 must reconcile the exact manufacturer land patterns and physical pin1/orientation before creating placement or copper. The ICM and BMP symbols have no invented EP; generic package-center features in a general assembly note do not authorize a center pad for these selected packages.

Use TDK AN-000393 v2.4 for package-specific mounting, solder and mechanical-stress treatment. Avoid vias/traces/copper features immediately under the IMU package as instructed; resolve the exact lower-plane treatment in layout review while preserving a common continuous ground system. Keep the IMU away from mounting/anchor strain, heat sources and switch nodes; maintain uniform solder joints, short local bus routing and adjacent bypasses. No split analog ground island is introduced. Confirm handling/cleaning/reflow restrictions for the selected MEMS package; do not assume ultrasonic cleaning is acceptable.

BMP390 requires a protected but unobstructed pressure path. Keep adhesive, conformal coating, solder flux/cleaning residue and liquids out of the port. Protect from dust and direct propwash without sealing it. Foam/membrane/gasket choices, adhesive migration, enclosure pressure lag, orientation and thermal gradients require qualification. Verify pressure accuracy after assembly and with processors/regulators/radios active. Neither sensor is cleared for flight by this schematic.

## 8. Symbols, sourcing and ERC disposition

Eight IC instances use seven new local symbol definitions. Pin number/name/type plus native alternate functions are audited independently; there are68 physical pins across unique definitions. Existing local symbols are byte-preserved. Native symbol and schematic SVG/PDF renders were inspected; iterative corrections removed supply-wire shorts and default-property overlaps before the final baseline.

The official KiCad KLC checker was run. Its modern parser required an audit-only envelope version and leading-zero numeric normalization; canonical old symbols were not upgraded or changed. The final report retains four explained KLC findings. The three S5.1 footprint warnings for ICM-42688-P, BMP390 and TCA9416DDFR are expected because final footprint assignment and validation remain Stage 08 work. The TPS22918DBVR S4.2 top-VIN placement is a documented non-electrical symbol-layout convention exception: TPS22918 is a load switch, while the checker assumes a power converter and explicitly permits ignoring this finding for other device classes. This exception does not change pin numbering, electrical types or connectivity. Text-size, pin-offset, metadata and footprint-filter issues were corrected. This is not described as a completely clean KLC run. Existing recommended footprints are checked for existence, not for production suitability.

ERC retains46 findings:41 unchanged isolated MCU reservations; the inherited required VCAP power-output pair; two inherited multiple-net-name warnings; and two new B4 bidirectional-to-GND warnings on U13/U19. The B4 pins are inputs with DIR4 hard low, and A4 is NC, as independently checked against the TI truth table. They are controlled mode-dependent warnings, not permission to drive an output against ground. No ERC rule severity, exclusion or broad suppression was added.

PCBParts was used for sourcing metadata only. It returned a Tokmas-labeled ICM-42688-P variant rather than the selected TDK device; **that result is rejected as a substitute**. BMP390 had no exact database match. Genuine manufacturer provenance and authorized-distributor availability for both sensors remain OPEN. TI exact-part metadata was found (TPS22918 C131941; TCA9416 C4364143; AXC4 C1849453; AXC1 C2677376; AUP3G17 C191827), but dated database stock is not an order or authenticity guarantee. All exact parts remain RECOMMENDATION. No purchase was placed.

Full parts: recommendation BOM (private source record). Sourcing record: PCBParts retained results (private source record). KLC report: KLC final report (private source record).

## 9. Required OPEN-item disposition

| ID | Open item / close criterion | Owner / gate |
|---|---|---|
| S06-01 | BMP supply≥10ms at both pins for full PVT/load/restart; no interface over-rail excursion | Sensor support owner; before BMP energization/integration |
| S06-02 | ICM direct rail monotonic1–3ms; actual noise and transient peaks characterized | Sensor/power owner; before sensor electrical acceptance |
| S06-03 | Resolve whether50mA includes C41; measure total LDO/input startup including capacitor corners and concurrency | Project control + power/sensor owners; before capture acceptance is promoted |
| S06-04 | Actual ICM maximum and dynamic support load fit25/50mA without claiming typical values as maxima | Sensor owner; coupon/bench gate |
| S06-05 | AUP thresholds at actual rail covered by written manufacturer bounds or validated replacement/qualification | Sensor owner; before return-path acceptance |
| S06-06 | MAIN/SENS/BARO off, brownout, prebias, hot restart and short tests meet every pin limit; whole-board backfeed retained | Sensor/power owners; Stages11–13 |
| S06-07 | Exact land patterns, pin1, vent, MEMS mechanics, decoupler bias/temperature/aging and assembly constraints | Stage08/09 owners; no layout release here |
| S06-08 | Genuine sensor sourcing; exact package/lifecycle/assembly feasibility and approved BOM | BOM owner; before procurement |
| S06-09 | H743 timing, SPI/I2C waveform, interrupt/reset/recovery and firmware configuration tests | Firmware/bench owner; before sensor data is trusted |
| S06-10 | Vibration, EMI, thermal gradients, pressure lag/propwash and assembled accuracy | Physical-test owner; before flight/production |

No item above is silently closed by this report. Stage07 stays locked until project-control review and new explicit authorization.

## 10. Reproduction and artifact index

Read-only verification commands from the workspace root:

```powershell
python -X utf8 qa/stage06-sensors/calculations.py
python -X utf8 qa/stage06-sensors/verify_capture.py 8
python -X utf8 qa/stage06-sensors/final_audit.py
```

The first two regenerate QA outputs; they do not change canonical schematics. Do not run the capture/boundary builders as a casual verification step. `build_sensors.py` writes guarded sensor/library files; `connect_boundaries.py` is a one-time guarded transaction. The final file manifest seals the released local handoff artifacts and current control hash. Native KiCad registry-access warnings were nonfatal; command return codes and output files were checked.

- Sensor schematic (private source record)
- Project root schematic (private source record)
- Local symbol library (private source record)
- Native netlist (private source record)
- Native ERC JSON (private source record)
- Retained ERC dispositions (private source record)
- Source manifest (private source record)
- Final scope audit (private source record)
- Entry snapshot manifest (private source record)

## 11. Manufacturer source manifest

- `hardware/FC_REV_A/docs/evidence/stage06-sensors/an000393.pdf` — AN-000393 v2.4, 2026-02-09; 1831116 bytes; SHA-256 `be0aa48f9f10fc2dcb0e647d8a6509a75636b3f5df0e714388784a53d9bde55b`. [Manufacturer source](https://d17t6iyxenbwp1.cloudfront.net/s3fs-public/2026-06/AN-000393%20TDK%20InvenSense%20IMU%20PCB%20Design%20and%20MEMS%20Assembly%20Guidelines%20v2.4.pdf?VersionId=0JJT_E0010fzx6pG58sIeAXICnPVAVgn).
- `hardware/FC_REV_A/docs/evidence/stage06-sensors/bmp390.pdf` — BST-BMP390-DS002-07 rev1.7, March2021; 1930878 bytes; SHA-256 `8dcf0f74449cb1627e865c7f24d328b76c204d8b9621091ede8c6869fb393e48`. [Manufacturer source](https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bmp390-ds002.pdf).
- `hardware/FC_REV_A/docs/evidence/stage06-sensors/icm42688p.pdf` — DS-000347 v1.9, 2024-11-12; 1402996 bytes; SHA-256 `9c6b57b0a2e45cf0251dd2423878573bd4da46e0cc2faa93dc558c28af51300a`. [Manufacturer source](https://d17t6iyxenbwp1.cloudfront.net/s3fs-public/2026-06/DS-000347%20ICM-42688-P%20v1.9.pdf?VersionId=XL060vOv88u6zsKx9dkBVJEyV452m0eq).
- `hardware/FC_REV_A/docs/evidence/stage06-sensors/kemet_22n.pdf` — Manufacturer specsheet generated 2026-09-09; 239972 bytes; SHA-256 `551f74b1cade8e1cb3dc85371f867ee59feca42f0bbfa3cecfa5c0d1109421bc`. [Manufacturer source](https://yageogroup.com/component-documentation/download/specsheet/C1206C223J5GACTU).
- `hardware/FC_REV_A/docs/evidence/stage06-sensors/murata_10n.pdf` — GRM188R71H103KA01-01, 2016-02-28 reference sheet; 870448 bytes; SHA-256 `f164fbe0a83fd244a413bda28141ba1f5b1bb5234b750e24b2268534cb634878`. [Manufacturer source](https://search.murata.co.jp/Ceramy/image/img/A01X/G101/ENG/GRM188R71H103KA01-01.pdf).
- `hardware/FC_REV_A/docs/evidence/stage06-sensors/murata_1u.pdf` — GRM31CR71H105KA61-01A, 2025-01-10 reference sheet; 1983959 bytes; SHA-256 `734541bb09e7fcff71b6415e4c5dd76cd1cab009dae308a7103d0df10acc4da6`. [Manufacturer source](https://search.murata.co.jp/Ceramy/image/img/A01X/G101/ENG/GRM31CR71H105KA61-01A.pdf).
- `hardware/FC_REV_A/docs/evidence/stage06-sensors/sn74aup3g17.pdf` — SCES765C, January2012; 867945 bytes; SHA-256 `74cd3588a32270e5c90505eaf98520193b033a7fe0c116e5db7f378054334083`. [Manufacturer source](https://www.ti.com/lit/ds/symlink/sn74aup3g17.pdf).
- `hardware/FC_REV_A/docs/evidence/stage06-sensors/sn74axc1t45.pdf` — SCES882E, December2023; 1840072 bytes; SHA-256 `41e03bd8f0740ae8bbdf92309e7c82bac1359a768556cbe68de41b0273e49f12`. [Manufacturer source](https://www.ti.com/lit/ds/symlink/sn74axc1t45.pdf).
- `hardware/FC_REV_A/docs/evidence/stage06-sensors/sn74axc4t774.pdf` — SCES898C, May2022; 2480293 bytes; SHA-256 `f45cd62a9675b9f6071519d149a060d4124f49944f3c3af44160a76796f3bf20`. [Manufacturer source](https://www.ti.com/lit/ds/symlink/sn74axc4t774.pdf).
- `hardware/FC_REV_A/docs/evidence/stage06-sensors/tca9416.pdf` — SCPS238A, August2021; 1272448 bytes; SHA-256 `5e5e534585edfbd7315cefc246f7e70ac8406a0fc82823743161a74c595020a5`. [Manufacturer source](https://www.ti.com/lit/ds/symlink/tca9416.pdf).
- `hardware/FC_REV_A/docs/evidence/stage06-sensors/tps22918.pdf` — SLVSD76C, July2017; 1072926 bytes; SHA-256 `1b28eb58003d28b18bf919a15734056f296a499bebee2bd493a1e4358c4dfb1c`. [Manufacturer source](https://www.ti.com/lit/ds/symlink/tps22918.pdf).
- `hardware/FC_REV_A/docs/evidence/stage06-sensors/yageo_1M5.pdf` — Manufacturer specsheet generated 2026-09-09; 56541 bytes; SHA-256 `9aa4a5ae53f18cb85aeca3f8ac3b4aeed30a54f33bf18b76aabe288ced33eae5`. [Manufacturer source](https://yageogroup.com/component-documentation/download/specsheet/RC0603FR-071M5L).
- `hardware/FC_REV_A/docs/evidence/stm32h743/stm32h743vi.pdf` — Existing source_manifest.json and Stage04/05 accepted handoffs; 7075281 bytes; SHA-256 `f6e620179006c8c4d497b477ba065edc89c6dd9ac24d9debb3362910651f42ee`.
- `hardware/FC_REV_A/docs/evidence/stm32h743/rm0433.pdf` — Existing source_manifest.json and Stage04/05 accepted handoffs; 40711860 bytes; SHA-256 `9ba54135736a47a302cdc28fdc7ca8f23c6eed5a646fa0a639af6ed2ad71336e`.
- `hardware/FC_REV_A/docs/evidence/stm32h743/an4938.pdf` — Existing source_manifest.json and Stage04/05 accepted handoffs; 1126615 bytes; SHA-256 `217b5dcbfdd27cec4f6013cf1f51930bf81c338ccbaf7bf8dce3fa69592bb8b3`.
- `hardware/FC_REV_A/docs/evidence/stage05-power/correction_r18/tps736.pdf` — Existing source_manifest.json and Stage04/05 accepted handoffs; 2682751 bytes; SHA-256 `f2da4943d86f038b91ae01bd0557005ed3668cd19deb5f9cf2643605a0a3c09a`.

## 12. Exact recommendation BOM

| Ref | Value | MPN | Manufacturer | Footprint recommendation |
|---|---|---|---|---|
| C51 | 100n | GRM188R71H104KA93D | Murata | Capacitor_SMD:C_0603_1608Metric |
| C52 | 2.2u | GRM31CR71H225KA88L | Murata | Capacitor_SMD:C_1206_3216Metric |
| C53 | 10n | GRM188R71H103KA01D | Murata | Capacitor_SMD:C_0603_1608Metric |
| C54 | 100n | GRM188R71H104KA93D | Murata | Capacitor_SMD:C_0603_1608Metric |
| C55 | 100n | GRM188R71H104KA93D | Murata | Capacitor_SMD:C_0603_1608Metric |
| C56 | 100n | GRM188R71H104KA93D | Murata | Capacitor_SMD:C_0603_1608Metric |
| C57 | 100n | GRM188R71H104KA93D | Murata | Capacitor_SMD:C_0603_1608Metric |
| C58 | 1u | GRM31CR71H105KA61L | Murata | Capacitor_SMD:C_1206_3216Metric |
| C59 | 22n | C1206C223J5GACTU | KEMET | Capacitor_SMD:C_1206_3216Metric |
| C60 | 1u | GRM31CR71H105KA61L | Murata | Capacitor_SMD:C_1206_3216Metric |
| C61 | 1u | GRM31CR71H105KA61L | Murata | Capacitor_SMD:C_1206_3216Metric |
| C62 | 100n | GRM188R71H104KA93D | Murata | Capacitor_SMD:C_0603_1608Metric |
| C63 | 100n | GRM188R71H104KA93D | Murata | Capacitor_SMD:C_0603_1608Metric |
| C64 | 100n | GRM188R71H104KA93D | Murata | Capacitor_SMD:C_0603_1608Metric |
| C65 | 100n | GRM188R71H104KA93D | Murata | Capacitor_SMD:C_0603_1608Metric |
| C66 | 100n | GRM188R71H104KA93D | Murata | Capacitor_SMD:C_0603_1608Metric |
| C67 | 100n | GRM188R71H104KA93D | Murata | Capacitor_SMD:C_0603_1608Metric |
| C68 | 100n | GRM188R71H104KA93D | Murata | Capacitor_SMD:C_0603_1608Metric |
| R38 | 100k | RC0603FR-07100KL | Yageo | Resistor_SMD:R_0603_1608Metric |
| R39 | 1.5M | RC0603FR-071M5L | Yageo | Resistor_SMD:R_0603_1608Metric |
| R40 | 1.5M | RC0603FR-071M5L | Yageo | Resistor_SMD:R_0603_1608Metric |
| R41 | 300 | RC0603FR-07300RL | Yageo | Resistor_SMD:R_0603_1608Metric |
| R42 | 100k | RC0603FR-07100KL | Yageo | Resistor_SMD:R_0603_1608Metric |
| R43 | 100k | RC0603FR-07100KL | Yageo | Resistor_SMD:R_0603_1608Metric |
| R44 | 100k | RC0603FR-07100KL | Yageo | Resistor_SMD:R_0603_1608Metric |
| R45 | 100k | RC0603FR-07100KL | Yageo | Resistor_SMD:R_0603_1608Metric |
| R46 | 100k | RC0603FR-07100KL | Yageo | Resistor_SMD:R_0603_1608Metric |
| R47 | 680 | RC0603FR-07680RL | Yageo | Resistor_SMD:R_0603_1608Metric |
| R48 | 100k | RC0603FR-07100KL | Yageo | Resistor_SMD:R_0603_1608Metric |
| R49 | 910 | RC0603FR-07910RL | Yageo | Resistor_SMD:R_0603_1608Metric |
| R50 | 4.7k | RC0603FR-074K7L | Yageo | Resistor_SMD:R_0603_1608Metric |
| R51 | 4.7k | RC0603FR-074K7L | Yageo | Resistor_SMD:R_0603_1608Metric |
| R52 | 22k | RC0603FR-0722KL | Yageo | Resistor_SMD:R_0603_1608Metric |
| R53 | 1.5M | RC0603FR-071M5L | Yageo | Resistor_SMD:R_0603_1608Metric |
| R54 | 22k | RC0603FR-0722KL | Yageo | Resistor_SMD:R_0603_1608Metric |
| R55 | 22k | RC0603FR-0722KL | Yageo | Resistor_SMD:R_0603_1608Metric |
| R56 | 22k | RC0603FR-0722KL | Yageo | Resistor_SMD:R_0603_1608Metric |
| U12 | ICM-42688-P | ICM-42688-P | TDK InvenSense | OPEN |
| U13 | SN74AXC4T774PWR | SN74AXC4T774PWR | Texas Instruments | Package_SO:TSSOP-16_4.4x5mm_P0.65mm |
| U14 | SN74AUP3G17DCUR | SN74AUP3G17DCUR | Texas Instruments | Package_SO:VSSOP-8_2.3x2mm_P0.5mm |
| U15 | TPS22918DBVR | TPS22918DBVR | Texas Instruments | Package_TO_SOT_SMD:SOT-23-6 |
| U16 | BMP390 | BMP390 | Bosch Sensortec | OPEN |
| U17 | TCA9416DDFR | TCA9416DDFR | Texas Instruments | OPEN |
| U18 | SN74AXC1T45DBVR | SN74AXC1T45DBVR | Texas Instruments | Package_TO_SOT_SMD:SOT-23-6 |
| U19 | SN74AXC4T774PWR | SN74AXC4T774PWR | Texas Instruments | Package_SO:TSSOP-16_4.4x5mm_P0.65mm |
