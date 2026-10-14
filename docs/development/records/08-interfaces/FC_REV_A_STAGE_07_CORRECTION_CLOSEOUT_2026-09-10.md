> Historical technical record. Names and private workstation/session references were neutralized for publication. Dates and assertions describe the recorded stage, not current physical qualification. See the current validation-status page for later checks.

# FC Drone FC Rev A — Stage 07 Correction Closeout

Date: 2026-09-10  
Control basis: `FC_REV_A_CURRENT_CONTROL_STATE.md`, revision R27  
Baseline implementation handoff: `FC_REV_A_STAGE_07_ESC_EXTERNAL_INTERFACES_2026-09-09.md`  
Baseline independent review: `FC_REV_A_STAGE_07_CONTROL_REVIEW_2026-09-10.md`  
Result: **ANALYTICAL CORRECTION COMPLETE; Stage 07 remains VERIFIED CONDITIONAL PASS; S07-01 through S07-12 remain OPEN at their stated physical, firmware, carrier, footprint, or system gates.**  
Stop boundary: **Stage 08 remains locked and was not started.**

## 1. Purpose and controlled outcome

This closeout evaluates the user-supplied ESC update, answers the connector-boundary question, corrects the harness and AUX-drop analysis, and expands the closure instructions for S07-01 through S07-12. It does not promote screenshot evidence into native-design proof and does not claim any physical or firmware test.

The accepted R27 KiCad baseline already contains the explicitly approved `5V_AUX` hierarchical output and short wire on `02_power.kicad_sch`, plus the matching root-sheet pin and connection. The user's later approval therefore required no additional edit. All ten canonical schematic/library files remain byte-identical to the accepted Stage 07 manifest. No PCB file exists.

This correction does not edit:

- `FC_REV_A_CURRENT_CONTROL_STATE.md`;
- `hardware/FC_REV_A/docs/retained_status_ledger.md`;
- the original Stage 07 handoff or control review;
- either original user-supplied evidence file or any extracted archive member;
- any canonical KiCad schematic or symbol library;
- PCB geometry, footprints, placement, routing, stackup, Gerbers, drills, CPL, fabrication, procurement, or manufacturer communication.

## 2. User evidence boundary

The evidence is retained at `hardware/FC_REV_A/docs/evidence/stage07-correction/user-supplied/`. The two originals were read and hashed without modification.

| Original | Bytes | SHA-256 |
|---|---:|---|
| `Thank you for the detailed review..txt` | 2,691 | `eab50fcab258d2f2af1e4e844857dd3dd7e318c484c8e540199e5e711fbc0343` |
| `escdesignupdate.zip` | 778,633 | `0ad0c2de74d8f2399b64ce441d7facb2af63bb3990ce22bb70dc868d543de80c` |

The ZIP contains only the following seven members. It contains no Gerbers, drills, native KiCad project, netlist, fabrication drawing, firmware, bootloader, private AM32 fork, connector assembly drawing, continuity record, oscilloscope capture, or as-built photographs.

| Extracted member | Bytes | SHA-256 |
|---|---:|---|
| `3d view bottom.png` | 343,198 | `9324e9b380abfd2acd529f0010a9a52d09d05aa10ebb4f1c46147742f615ec4f` |
| `3d view top.png` | 258,504 | `9ac388fc8d52b693f8a48936ae54de48bd4e3fcf2a69b515596652586c45911d` |
| `4in1_ESC_BOM.csv` | 1,855 | `abfe3a9967fbd1b22c978da0d25aa284edf61f2cc73bbef1c42b50708208e8fb` |
| `DRC.png` | 49,300 | `a5de5332816123056b1d0960b13053c6f679eca346bef612dda89d21a924df5a` |
| `ERC.png` | 26,240 | `f06e2ef5d18df679d98f3f9430b608e627cd9af24c83edfe0768465d22782961` |
| `ESC schematic.png` | 55,759 | `d86684f57dd424e28e570cf0684f2a84078ce483e40db34a67c78b3c92788718` |
| `Overview ESC schematic.png` | 67,745 | `ff71ff9b18085cb3917036490ec6e7653832d0dee061f1768dff19c616843566` |

The screenshots support only what is visibly shown:

- The overview schematic depicts J1 as `SM08B-SRSS-TB`, with pin 1 `+BATT`, pin 2 GND, pin 3 `CURR`, pin 4 visually unconnected, and pins 5–8 M1–M4.
- The ERC screenshot reports 0 errors, 329 warnings, 49 exclusions, and four ignored test categories.
- The DRC screenshot reports 0 errors, 26 warnings, 15 ignored tests, and states that schematic parity was not run.
- The two 3D images are CAD renders. They are not as-built or inspection photographs.
- The BOM identifies J1 `SM08B-SRSS-TB`, LCSC `C160407`, and four `AT32F421G8U7` devices. A BOM does not prove authentic procurement, placement, soldering, or programmed firmware.

Those screenshot totals are not substituted for native ERC/DRC evidence. There is no native ESC source in the supplied update, so independent re-export or parity checking of that archive is impossible.

## 3. Why J1 positions 1 and 4 are absent

This is an **FC cable/interposer safety boundary only**. It requests no change to the ESC board.

- ESC J1-1 is raw `+BATT`. The FC's ESC interface is signal/GND only. Allowing a terminal or conductor at cavity 1 would place raw battery voltage in the FC-side cable assembly, where a repin, damaged harness, solder bridge, or unintended termination could defeat that boundary.
- ESC J1-4 is unused/NC in the supplied screenshot and retained upstream netlist. It is intentionally prohibited so that a future board variation, mistaken repin, or accidental contact cannot silently create an unreviewed function.
- At the FC termination there shall be no contact, crimp, wire, copper, via, pad, test point, net, or connector pin corresponding to ESC J1-1 or J1-4.
- The ordinary ESC board connector remains the populated eight-position `SM08B-SRSS-TB`. The absence rule applies to the mating harness and the FC-side termination.
- The default harness also omits J1-3 because `/CURR` is DNP, informational, disabled by default, and prohibited as a safety input. A later current-sense trial may use the separate DNP J2 path only after range, calibration, powered-state, and fault review.

## 4. S07-01 — Controlled ESC harness and passive interposer

### 4.1 Exact logical map

| ESC board J1 | ESC meaning | Harness population | FC-side destination | Status |
|---:|---|---|---|---|
| 1 | raw `+BATT` | **NO terminal, crimp, wire, splice, shield drain, or test lead** | no FC contact/pad/net | PROHIBITED |
| 2 | GND | populated | FC J1-2 / GND | REQUIRED |
| 3 | `CURR` | absent in default assembly | optional separate J2 DNP path only | DNP |
| 4 | NC/prohibited | **NO terminal, crimp, wire, splice, shield drain, or test lead** | no FC contact/pad/net | PROHIBITED |
| 5 | M1 | populated | FC J1-5 / `ESC_M1_PORT` | REQUIRED |
| 6 | M2 | populated | FC J1-6 / `ESC_M2_PORT` | REQUIRED |
| 7 | M3 | populated | FC J1-7 / `ESC_M3_PORT` | REQUIRED |
| 8 | M4 | populated | FC J1-8 / `ESC_M4_PORT` | REQUIRED |

The FC netlist independently contains only J1 pins 2, 5, 6, 7, and 8. The current-sense experiment is a separate DNP contact and is not part of the default motor harness.

### 4.2 Connector identity and orientation control

- ESC board header confirmed by the user and BOM: JST SH 1.0 mm, `SM08B-SRSS-TB` side-entry.
- Mating housing confirmed by the user: `SHR-08V-S-B`.
- The user's terminal identification is `SSH-003T-P0.2`. The retained current JST SH catalogue lists the tin contact as `SSH-003T-P0.2-H`; procurement must verify the exact suffix and approved applicator before release.
- JST rates the SH family at 1 A with AWG28, 50 V, and AWG32–28 wire; initial contact resistance is 20 mΩ maximum, rising to 40 mΩ after environmental testing in the current catalogue. This connector rating does not release the vehicle harness.
- Numbering shall be taken from JST's official circuit-1 datum and verified against the actual molded housing/header marks. Assemblers may not infer numbering from apparent left/right orientation, wire color, a screenshot, or PCB silkscreen alone.
- The harness drawing shall show two views: the ESC header viewed from the connector mounting/mating reference defined by the JST drawing, and the housing wire-entry view. Both shall mark circuit 1, the latch/key, cavities 1–8, and the three unpopulated cavities 1, 3, and 4.

### 4.3 Wire, length, retention, and construction recommendation

- Initial bench interposer: maximum 150 mm one-way, AWG28 stranded wire, five populated conductors only, with the GND conductor routed adjacent to the four motor signals. The SH catalogue permits AWG28 and it is the lowest-resistance permitted gauge in that family.
- Candidate flight assembly: retain the same maximum 150 mm and AWG28 until waveform, crosstalk, vibration, and retention testing justifies a change. This is a recommendation, not a released flight cable.
- Use a labeled sleeve at both ends and a keyed, unique eight-position housing. Do not use loose individual jumpers in flight.
- Provide service slack without a loop that can contact rotating parts. Anchor the loom to the vehicle structure so connector contacts carry no cable tensile load. Final anchor distance, sleeving, potting, bend radius, pull force, and vibration profile remain OPEN.
- The ESC harness carries only logic and its return. It carries no `5V_AUX` and no raw battery conductor by design.

### 4.4 Mandatory continuity jig and acceptance record

Before any energized connection, use a keyed passive fixture that exposes ESC cavities 1–8 and all FC-side contacts. The signed record must include serial number, harness revision, operator, instrument ID/calibration date, and both connector-orientation photographs.

1. Verify circuit 1 from the molded/drawing datum before testing.
2. Verify J1-2 to FC GND and J1-5/6/7/8 to the matching M1/M2/M3/M4 contacts. Each must be less than 0.25 Ω after subtracting fixture-lead resistance.
3. Verify cavities 1, 3, and 4 contain no terminal or wire by visual inspection and back-light/probe inspection.
4. Verify each of cavities 1, 3, and 4 is greater than 10 MΩ to every populated FC contact and to FC GND at the fixture's safe test voltage.
5. Verify every unintended pair among GND and M1–M4 is greater than 10 MΩ.
6. Apply a 100 mA fixture current through the GND conductor and require less than 50 mV total harness drop after fixture subtraction. Record the actual value; this screen is for workmanship and does not establish the final flight return-current requirement.
7. Perform 100% pin-map recheck after strain relief is installed and after the prescribed vibration/retention exposure.

Bench use is limited to a current-limited source, props removed, motor outputs inhibited at power-up, ground-first connection, and the passive interposer. Direct flight use remains OPEN until the final drawing, pull/retention, vibration, continuity, and bidirectional waveform records are reviewed and accepted.

## 5. S07-02 — ESC protocol, firmware identity, and safe shutdown

The public AM32 repository at commit `e6991d583dd1588ea4e02f421b7b617076c5eeb3` states generic support for servo PWM, DShot300/600, bidirectional DShot, and AT32F421 devices. It also states that the bootloader depends on the MCU and signal input pin. This does **not** identify or validate the private `OPENESC_20_F421` target.

The required private fork, exact source commit, build configuration, compiler/toolchain version, produced binary hash, bootloader hash, fuse/option-byte configuration, input-pin mapping, dead-time, current/voltage scaling, motor-direction default, startup tones, and failsafe behavior were not supplied. `OPENESC_20_F421` therefore remains OPEN and blocks firmware-specific release.

The controlled bring-up sequence remains:

1. Props removed, current-limited supply, motor outputs held inactive through boot/reset, and PWM only for channel identity, safe idle, direction, and shutdown tests.
2. DShot300 command and no-command testing.
3. Bidirectional DShot300 return waveform, timing, error-rate, and missing/malformed response behavior.
4. DShot600, then bidirectional DShot600, only after the lower-rate steps pass.

ArduPilot's official DShot guidance says DShot should be used only with a known-compatible ESC, most compatible ESCs also accept normal PWM, DShot150 is the conservative choice for long leads, and DShot300/600 are preferred for bidirectional operation. The project retains its already-approved PWM → DShot300 → bidirectional DShot300 → DShot600 sequence because the candidate harness is short; DShot150 may be evaluated only through a controlled firmware/test change if cable results require it.

Required safe-state tests remain OPEN: power-up, reset, watchdog, FC brownout, ESC brownout, signal open, signal short-to-ground, signal stuck-high, malformed frames, lost bidirectional telemetry, and cable disconnect/reconnect. No missing or malformed telemetry may itself arm a motor, and `/CURR` may not affect arming, failsafe, or shutdown.

## 6. S07-03 — Remote pull-ups, clamps, level domains, capacitance, and backfeed

The captured UART outputs are open-drain through `SN74LVC2G07`; each remote device or adapter must supply the pull-up from the remote device's own switched 3.3 V logic rail. A 2.2 kΩ +3% pull-up with 100 pF reaches 70% in approximately 272.8 ns. That is comfortably shorter than a 420 kbaud CRSF bit period of 2,381 ns; 921600 baud has only 1,085 ns per bit and remains a waveform/error-rate test.

Incoming UART/handshake lines use power-off-tolerant LVC input buffers and local pull-downs. GNSS I2C uses a disabled-when-off TMUX path; remote-owned 2.2 kΩ pull-ups are required. The 30–70% I2C rise screen is approximately 192.0 ns at 100 pF, below the 300 ns Fast-mode limit. The corresponding worst stated pull-up sink screen is about 1.60 mA. Actual module pull-up values, duplicate pulls, cable capacitance, thresholds, powered-off clamp currents, and ground sequencing remain OPEN.

- OpenRX: its selected adapter must expose a switched 3.3 V logic node for the two 2.2 kΩ pulls. `5V_AUX` is power only; it may not be used as a signal pull-up.
- GNSS/compass carrier: provide its own regulated logic rail, local UART/I2C pulls, measured capacitance, and powered-state truth table.
- RFD900x: the main header does not provide an ordinary 3.3 V output. A qualified adapter may use a verified switched logic node; an always-on auxiliary rail is prohibited because it defeats the off-state policy. No internal radio modification is released.
- CM5: use the CM5 carrier's own 3.3 V domain and GPIO_VREF configuration. The FC reference contact is omitted by default; if fitted, it is a high-impedance monitor only and cannot power the CM5 or its GPIO rail.

Ground-referenced TPD ESD devices have no VCC steering rail and avoid a direct clamp-to-FC-rail backfeed path. They are transient clamps, not protection against sustained 5 V, battery, open-ground, or connector-sequencing faults. Actual device/cable capacitance and IEC performance remain layout and physical gates.

The conservative all-option off-state allocation remains 222.9 µA. Removing optional GPS PPS allocation, three DNP LM66100 power paths, and DNP CAN2 produces a default-populated arithmetic estimate of 176.8 µA. The corresponding 680 Ω +3% MAIN-bleed voltages are about 0.1561 V and 0.1238 V. Neither allocation proves the required less-than-100 µA reverse current at POWER1 because individual leakage limits do not define the assembled injection path. Measure reverse current separately into AUX, MAIN, and POWER1 across all states; the requirement remains OPEN.

## 7. S07-04 — Recomputed `5V_AUX` cable drop

The correction preserves the hard 4.75 V remote floor. It does not hide cable/contact loss inside the earlier 25 mΩ internal-path allowance.

Assumptions, all explicitly analytical:

- source floor 4.90155 V;
- 64 mΩ limiter plus 25 mΩ retained shared internal path;
- 125 mΩ LM66100 envelope;
- copper resistance at 20 °C: AWG26 0.1339 Ω/m, AWG28 0.2129 Ω/m, AWG30 0.3386 Ω/m;
- copper temperature factor at 85 °C: 1.25545;
- GH contact screen: 30 mΩ each initial and 50 mΩ each after environmental testing;
- default concurrency: receiver 0.50 A plus GPS carrier 0.15 A.

| Case | Remote floor before dynamic allowance | With additional 50 mV dynamic allowance | 4.75 V result |
|---|---:|---:|---|
| Receiver, AWG26, 150 mm, 20 °C, initial contacts | 4.7311 V | 4.6811 V | FAIL |
| Receiver, AWG26, 150 mm, 85 °C, after-test contacts | 4.7060 V | 4.6560 V | FAIL |
| Receiver, AWG28, 150 mm, 85 °C, after-test contacts | 4.6911 V | 4.6411 V | FAIL |
| Receiver, AWG30, 150 mm, 85 °C, after-test contacts | 4.6674 V | 4.6174 V | FAIL |
| GPS, AWG26, 300 mm, 85 °C, after-test contacts | 4.7948 V | 4.7448 V | PASS before, FAIL after dynamic allowance |

With GPS held at 0.15 A, the calculated maximum receiver current that preserves 4.75 V before any dynamic allowance is approximately 0.440 A with zero wire, 0.398 A at 100 mm AWG26, and 0.379 A at 150 mm AWG26 under the stated aged/85 °C assumptions.

The closest compliant arrangement within the captured architecture is the shortest practical AWG26 GH assembly, no more than 150 mm, with a measured worst-case receiver peak no greater than the applicable calculated limit and a measured dynamic floor at or above 4.75 V. Because JST GH accepts AWG26 and SH does not, this recommendation applies to AUX-powered GH module cables, not the ESC SH signal harness. If the receiver needs the full 0.5 A reserve, the power path or connector must be redesigned under change control. The 0.5 A planning reserve and 4.75 V requirement remain unchanged.

## 8. S07-05 — Complete power-state matrix

| Interface | FC on / remote off | FC off / remote on | Both on | Reset, brownout, removal, hot plug | Remaining proof |
|---|---|---|---|---|---|
| ESC | FC biases inactive; actual AT32 input/injection behavior unknown | TMUX isolation allocation only | Signal/GND, M1–M4; no power contact | no commands through boot/reset; ground-first fixture | private build, injection, waveform, faults OPEN |
| OpenRX | open-drain output cannot source remote rail; remote pulls disappear | LVC Ioff and LM66100 block are analytical | 5V_AUX/GND, PC6 TX→RX, receiver TX→PC7 RX | no-frame must remain safe; powered insertion excluded until tested | own-rail pulls, current, backfeed OPEN |
| GPS carrier | UART/I2C remote pulls disappear; PPS DNP | LVC/TMUX/LM paths only | UART 115200, I2C ≤400 kHz, optional PPS | bus unlock, false-edge, insertion surge OPEN | carrier rail, pulls, capacitance, current OPEN |
| RFD900x | TX/RTS open-drain; input pulls low | input Ioff only; FC power path absent | external radio power; full handshake | stale frames ignored; RTS/CTS reset timing OPEN | adapter logic rail and error-rate OPEN |
| CM5 | reference omitted by default; no FC power | LVC Ioff; optional reference blocker only | advisory UART7 on CM5's 3.3 V domain | CM5 restart/loss must not affect stabilization or motor generation | host isolation and stale-data tests OPEN |
| CAN1 | transceiver must meet powered-off bus loading | no AUX output by default | populated classic CAN 1 Mbit/s | recessive reset, UVLO, thermal, bus fault testing | topology, termination, EMC/fault OPEN |
| CAN2 | wholly DNP | wholly DNP | prohibited without approval | remains physically absent | later approval required |
| USB-C | self-powered FC controls pull-up according to VBUS | host VBUS reaches sense buffer only | FS device, both CC resistors | USB-only cannot boot FC; attach/detach/brownout OPEN | both orientations and ROM DFU OPEN |
| SWD/recovery | only qualified off-tolerant probe | reference blocker prevents probe-to-MAIN feed | target-powered debug; local BOOT shunt DNP | disconnect unqualified probe; shunt power-off only | probe threshold/off-state testing OPEN |
| microSD | card shares MAIN | independently powered emulator prohibited | 3.3 V four-bit SDMMC1 | detect bounce, write interruption, removal and corruption tests | exact card/current/timing OPEN |

Camera and `VL53L5CX-SATEL` lidar remain CM5-only loads and are excluded from all FC AUX states and budgets. `LIDAR_FC` remains retired; PA0/PA1 remain reserved. CM5 is independently powered and advisory only.

## 9. S07-06 — AUX startup and concurrency

The default active allocation remains 0.65 A: 0.50 A receiver plus 0.15 A GPS carrier. Camera and lidar contribute zero FC current. TELEM and CAN connector-power options remain DNP. The aggregate continuous AUX ceiling remains 1.00 A.

The retained default capacitance allocation is 320.6 µF. At the 5.093115 V screen, its ramp contribution is approximately 48.0 mA at 34 ms and 30.8 mA at 53 ms, giving total startup screens of 0.6980 A and 0.6808 A. The full permitted 1.00 A active plus 680 µF case is approximately 1.1019 A at 34 ms and 1.0653 A at 53 ms, below the 1.139477 A limiter-minimum screen by only 37.6 mA in the fastest case.

The calculation shows compatibility of the planning envelope only. Each selected module must provide measured cold-start and powered-insertion `I(V,t)`, actual effective input capacitance, reset/brownout behavior, and concurrency. The total post-switch capacitance must remain no more than 680 µF and active startup load no more than 1 A. A capacitor is not an inrush limiter. Physical closure remains OPEN.

## 10. S07-07 — Footprints, pin 1, and orientation disposition

No footprint field was changed in this correction because production geometry belongs to Stage 08/09 and the present schematic is recommendation-grade.

| Item | Official-source disposition | Current action |
|---|---|---|
| ESC board `SM08B-SRSS-TB` | JST SH side-entry, 1.0 mm, circuit-1 datum in official drawing | board identity confirmed; no ESC edit |
| FC sparse J1 | must have only 2,5,6,7,8 and cannot use an ordinary 8-pad footprint | footprint remains blank; custom interposer/termination required |
| GH ports | official header/mate/contact family retained; AWG30–26 and contact limits apply | KiCad candidates remain recommendations |
| GCT USB4105-GF-A | official B4 drawing dated 2023-12-18; component-side recommended layout | existing KiCad footprint remains candidate, geometry review OPEN |
| GCT MEM2075-00-140-01-A | official A1 drawing dated 2020-09-10; 8 contacts plus CD and shell terminations | footprint remains blank; exact custom footprint required |
| TPD4E05U06 DQA | official TI DQA package drawing retained | existing USON-10 candidate remains recommendation |
| TPD1E05U06 DYA | official TI DYA is two-pin SOD-523 | installed `Diode_SMD:D_SOD-523` is a candidate; field remains blank pending pad/assembly review |

Stage 08 must compare every land pattern against the official component-side drawing, verify pin-1/orientation markers and paste/mask/courtyard rules, and render the assembled orientation. No approximate MEM2075 or sparse-J1 footprint may be invented.

## 11. S07-08 — USB-C, CC, VBUS, ESD, orientation, and ROM DFU

The captured USB-C contract remains data/debug only:

- USB4105 A1/A12/B1/B12 to GND; A4/A9/B4/B9 to `USB_VBUS_PORT`; A6/B6 D+; A7/B7 D−; A5 and B5 receive independent 5.1 kΩ Rd resistors; SBU contacts are NC; shell tabs use the prototype 0 Ω ground bond.
- VBUS has no diode, switch, or copper path to `5V_FC`, `5V_AUX`, `3V3_MAIN`, or the MCU supply. It enters only a 1 kΩ / 47 kΩ sense path and tolerant buffer. At 5.5 V the nominal buffer-pin voltage is about 5.385 V and divider current about 114.6 µA.
- TPD4E05U06/TPD1E05U06 ground-referenced protection avoids rail-steering backfeed but does not prove sustained-overvoltage immunity.
- USB-only connection cannot power or boot the FC. External FC power is required for enumeration and ROM DFU.
- No external D+ pull-up is added in parallel with the MCU-controlled pull-up.

Required bench closure: enumerate with both plug orientations, verify D+/D− polarity and full-speed eye/waveform, measure VBUS attach/detach and PA9 timing, verify no reverse current to the host for all FC states, exercise reset/brownout and STM32 ROM DFU, and review shell/ground EMC. All remain OPEN.

## 12. S07-09 — CAN1 and CAN2

CAN1 remains populated on PD1 TX / PD0 RX with TCAN332DCNR, classic CAN 1 Mbit/s, and a vehicle-harness target no longer than 1 m. CAN2 on PB6/PB5 remains wholly DNP, including transceiver, connector, bypass, termination, and AUX-power option.

- Use one twisted CANH/CANL pair with an adjacent/common ground conductor. Do not use the AUX pin by default.
- Fit the 120 Ω termination only when the FC is physically at one end of the bus, with exactly two end terminations total. The captured resistor is DNP.
- TCAN332 integrated ESD, ±12 V common-mode operating range, TXD timeout, UVLO, and thermal shutdown support the recommendation but do not prove a battery short, open-ground event, repeated fault, or vehicle EMC result.
- Preserve separate 0 Ω common-mode-choke bypasses. Select and populate a choke only after waveform/EMI evidence; avoid an unreviewed footprint substitution.
- Test powered/unpowered bus loading, dominant timeout, recessive reset, brownout/restart, CANH/CANL short together, each line short to ground and supply within a controlled fault fixture, temperature rise, common-ground offsets, ESD, radiated/conducted emissions, and communication error rates.

CAN1 physical and EMC closure remains OPEN. CAN2 may not be populated without explicit later approval.

## 13. S07-10 — microSD

The recommendation remains GCT `MEM2075-00-140-01-A`, 3.3 V SDMMC1 four-bit, with pin map 1 DAT2, 2 DAT3, 3 CMD, 4 VDD, 5 CLK, 6 VSS, 7 DAT0, 8 DAT1, normally-open CD closing to ground on insertion, and shell/ground terminations per the official drawing.

Use a qualified 16 GB or 32 GB SDHC Class 10/U1 card formatted FAT32 for initial bring-up. This is a test-card recommendation, not a frozen procurement item. The official SD Association page identifies Physical Layer Simplified Specification 9.10 dated 2023-12-01; the exact downloadable specification remained behind its terms flow, so the retained artifact is honestly labeled HTML. ArduPilot's logging guidance supports FAT32/vFAT and card-dependent validation.

- Bring up at 3.3 V, four-bit Default Speed no higher than 25 MHz after low-speed identification. Do not enable 1.8 V UHS switching in the initial configuration.
- Preserve the 300 mA insertion/startup allocation, 22 µF plus 100 nF local bypass, 47 kΩ CMD/data pulls, 22 Ω clock damping, and rail-less ESD arrays.
- Debounce CD in firmware; do not begin transactions until supply/detect are stable.
- Stop and flush logging before commanded removal. Test removal during idle/read/write, repeated insertion, card full, filesystem repair, FC brownout, watchdog reset, and power interruption during worst-case write.
- Record the exact card MPN/capacity, current waveform, clock/data waveforms, error counts, sustained logging rate, temperature, and corrupted/recovered files.

Exact socket footprint, card choice, current, timing, removal, and brownout integrity remain OPEN.

## 14. S07-11 — GNSS/compass carrier

The preferred architecture remains a custom external carrier using u-blox `MAX-M10S-00B` plus IST8310: GPS1 UART on PD8/PD9 at 115200 initially, I2C4 on PB8/PB9 at no more than 400 kHz, and optional PPS on PD10 through the DNP path. The carrier must regulate locally from its AUX input, own all UART/I2C pull-ups on its switched 3.3 V rail, and prove cable capacitance, startup current, minimum input voltage, backfeed, reset, and navigation/compass behavior.

The retained u-blox integration manual is R05 dated 2026-04-28. An official full IST8310 source was not obtained; the previous manufacturer URL returns 404. No IST8310 pin table, footprint, carrier BOM, or release claim is invented. The MMC5983MA remains only a candidate alternate. S07-11 remains OPEN pending official IST8310 evidence or an explicitly approved replacement, complete carrier schematic/BOM, and physical test.

## 15. S07-12 — RFD900x and companion interface

RFD900x remains the preferred TELEM1 radio with external regulated power by default and full hardware handshake. From RFDesign datasheet V1.2:

| FC J5 contact | FC signal | RFD900x main-header pin | Direction at radio |
|---:|---|---:|---|
| 2 | GND | 1 or 2 | ground |
| 3 | FC TX | 7 RX | input to radio |
| 4 | FC RX | 9 TX | output from radio |
| 5 | FC CTS input | 11 RTS | output from radio |
| 6 | FC RTS output | 3 CTS | input to radio |

RFD pin 4 receives the external regulated supply. Do not bridge radio USB-power pins 5/6 or use the FC power contact by default. The radio's approximately 1 A transmit peak and 5 V minimum input are incompatible with claiming the current FC AUX allocation as proven. Its 3.5 V serial absolute maximum is not permission for 5 V logic.

Bring up at 57600 baud with RTS/CTS, then qualify 115200 and 921600 only after rise/fall, overshoot, BER, long-frame, reset, handshake-stall, no-frame, cable-variant, and hot-plug tests. Verify that stale or malformed radio/CM5 data is ignored and neither interface can affect stabilization, failsafe, safe shutdown, or motor-waveform generation. CM5 uses UART7 on its own power/domain and remains advisory. Optional status LED visibility remains DNP/OPEN.

## 16. Sources and revisions

New correction sources were retained with SHA-256 in `hardware/FC_REV_A/docs/evidence/stage07-correction/source_manifest.json`:

| Source | Revision/identity | Bytes | SHA-256 |
|---|---|---:|---|
| AM32 README | commit `e6991d583dd1588ea4e02f421b7b617076c5eeb3` | 4,521 | `e24970784df60cdf171b9f3ae732c4205dc1e4a79b382fc565f329d6c99bb204` |
| ArduPilot DShot documentation source | wiki commit `3c32dea0717100fc8eb16f4bcc779674ff9425ab` | 12,384 | `f713f4669b41e5ffbf965c62730e63f3a5dc3aae873491c95d3d7365685d6d3b` |
| ArduPilot logging documentation source | same wiki commit | 52,397 | `565d360e4644406e0b9c653e423ab2217203e18455719457ed17dae7efcf7af0` |
| SD Association simplified-specifications page | retrieved 2026-09-10; lists Physical Layer 9.10, 2023-12-01 | 78,298 | `fce16fa99aa39185430eba660aef7673e864f9160aaeba2b363d4fd8184f8c81` |
| GCT USB4105 product specification | A3, 2023-02-27 | 358,821 | `372fe1bc0e0b1b4ce7e18b61514e967c7c2f883f0c7fe1f4586b567785ee9cd2` |

Retained Stage 07 official PDFs reused by hash include JST SH `ea3071ca…`, JST GH `b1dcb317…`, GCT USB4105 drawing B4 `fb331fba…`, GCT MEM2075 drawing A1 `9f1a621a…`, TI TPD4/TPD1 `c167cf1e…`, u-blox MAX-M10S R05 `5a7510ef…`, RFDesign RFD900x V1.2 `988483fe…`, and Artery AT32F421 V2.03 `95340995…`. Exact URLs, byte counts, and full hashes are in the manifest.

## 17. Verification and visual inspection

KiCad 10.0.6 regenerated the hierarchical netlist, ERC JSON, nine SVG sheets, nine-page PDF, nine complete-sheet PNGs, and fifteen enlarged close-up PNGs. Results:

- 326 components and 302 nets;
- 606 captured pin/net checks, zero mismatch;
- frozen pre-Stage07 topology preserved;
- 432 independent release checks passed;
- 108 local symbol pins audited against retained source tables;
- zero PCB files;
- 13 ERC findings: six `isolated_pin_label`, three `pin_to_pin`, and four `multiple_net_names`, all matching the accepted classified set;
- no new unclassified ERC category;
- all 24 regenerated renders are SHA-256 identical to the accepted `verification_final` images.

Every one of the nine complete sheets and fifteen close-ups was visually inspected during this correction. No new clipping, collision, dangling hierarchy boundary, unexpected population, or changed graphical/net content was observed. `visual_review.json` and `visual_equivalence.json` retain the record. Pixel identity and ERC do not prove physical correctness.

Canonical proof: all ten files in `canonical_baseline_manifest.json` match the accepted Stage 07 SHA-256 values. The root schematic remains `93e492dd372b24c8cf3565ff0c0aab43349deb75000ef1c435c4cedca315cd56`; `02_power.kicad_sch` remains `9c8e100c1f266553f893a62ec2f31bf7fc552eb91a52835763a4fbc25535501c`. The R27 control state remains `1ebd6c9897c35bfaabb2fc3ba262e9234a33376c20a163c9062cfc5793d7af5d`; the retained ledger remains `38fdafa37e6cb59e53a651bcccfcf6fd58be5366a240c7f03be54a0ec5ba0817`.

## 18. Files created by this correction

No existing controlled handoff, control-state, ledger, user-evidence, or canonical KiCad file was overwritten.

- `FC_REV_A_STAGE_07_CORRECTION_CLOSEOUT_2026-09-10.md`
- `qa/stage07-correction/download_sources.ps1`
- `qa/stage07-correction/calculate_closeout.py`
- `qa/stage07-correction/audit_release_closeout.py`
- `qa/stage07-correction/verify_closeout.py`
- `qa/stage07-correction/calculations.json`
- `qa/stage07-correction/canonical_baseline_manifest.json`
- `qa/stage07-correction/user_evidence_manifest.json`
- `qa/stage07-correction/protected_control_manifest.json`
- `qa/stage07-correction/source_manifest.json`
- `qa/stage07-correction/verification/` and its copied evidence package at `hardware/FC_REV_A/docs/evidence/stage07-correction/verification/`
- five retained source artifacts plus `download_manifest.json` under `hardware/FC_REV_A/docs/evidence/stage07-correction/sources/`
- `hardware/FC_REV_A/docs/evidence/stage07-correction/visual_review.json`

The verification run also created `qa/stage07-interfaces/verification_correction_closeout/` as a fresh export workspace. It does not alter the accepted `verification_final` baseline.

## 19. Human approvals and unresolved decisions

The user authorized the minimal `5V_AUX` hierarchy boundary. That boundary was already present in the accepted R27 baseline and was verified without another edit. No approval has been granted for Stage 08, production footprint freeze, PCB work, a flight harness, fabrication, procurement, or physical release.

All S07-01 through S07-12 identifiers remain OPEN because their remaining evidence depends on physical articles, private firmware, a completed carrier, exact footprint review, or system tests. This closeout sharpens their test instructions and resolves analytical ambiguities; it does not relabel an unperformed test as complete.

## 20. Exact Stage 08 entry criteria and instructions

Stage 08 may start only after an authorized human reviewer explicitly accepts this correction closeout and explicitly authorizes Stage 08. That authorization must acknowledge that S07-01 through S07-12 remain carried OPEN and that Stage 08 cannot close firmware or physical gates by drawing review alone.

Before the first Stage 08 edit, the executor shall:

1. Re-read R27, the original Stage 07 handoff, the Stage 07 control review, and this correction closeout.
2. Verify the ten canonical hashes against `canonical_baseline_manifest.json`, plus the control-state and retained-ledger hashes against `protected_control_manifest.json`.
3. Preserve J1 as a sparse FC boundary with only contacts 2,5,6,7,8; never assign the ordinary eight-pad SH footprint to that sparse FC symbol.
4. Preserve J1-1 and J1-4 as absent from the FC assembly and keep J1-3 `/CURR` DNP/separate.
5. Preserve OpenRX wiring, MAX-M10S + IST8310 carrier recommendation, RFD external-power default, CM5 independent/advisory status, camera/lidar CM5-only status, retired `LIDAR_FC`, CAN1 populated, CAN2 wholly DNP, USB data-only/no-power, and SDMMC1 four-bit.
6. Treat USB4105, MEM2075, TPD DYA/DQA, GH, and every other footprint as a recommendation until official drawing, pin-1, orientation, courtyard, paste, mask, and assembly review passes. MEM2075 and sparse J1 require exact custom geometry; TPD1 DYA may use the installed SOD-523 candidate only after pad review.
7. Do not fabricate, order, contact a manufacturer, or create Gerbers/CPL/manufacturing outputs unless separately authorized by the active control stage.
8. Carry every Stage 04–06 OPEN item and S07-01 through S07-12 forward without silent closure.

**Stop here. Stage 08 remains locked.**
