> Historical technical record. Names and private workstation/session references were neutralized for publication. Dates and assertions describe the recorded stage, not current physical qualification. See the current validation-status page for later checks.

# FC Drone FC Rev A
# Stage 01 Closeout and ESC Open Register

Date: 2026-09-07  
Stage result: CONDITIONAL PASS  
Next controlled stage: Stage 02 - interface, power-boundary, connector, and STM32H743 resource freeze

## 1. Authority and scope

The user's 2026-09-07 policy bundle controls this closeout. Historical embedded prompts are evidence, not authority. Status terms are preserved exactly: DECISION, RECOMMENDATION, CANDIDATE, ASSUMPTION, OPEN, VERIFIED, and DNP.

Stage 01 is accepted conditionally. Missing original ESC documents remain OPEN and do not block bounded Stage 02 work. This file does not release a cable, ESC manufacturing package, schematic, PCB, firmware, or flight configuration.

## 2. Records reconciled

The following required records were read and reconciled:

- `FC_REV_A_CONTEXT_ARCHIVE_INDEX_AND_UPLOAD_ORDER_2026-09-07.md`
- `FC_REV_A_MULTI_STAGE_EXECUTION_RULES_AND_NEW_CHAT_PROMPT_2026-09-07.md`
- `FC_REV_A_IMPLEMENTATION_TIMELINE_AND_STAGE_GATE_PLAN_2026-09-03.md`
- `FC_REV_A_STAGE_01_CIRCUIT_SELECTION_2026-08-28.md`
- `FC_REV_A_ESC_MATCHING_WITH_FC_RESEARCH_CHAT_SUMMARY_2026-09-07.md`
- `FC_REV_A_OPENESC_RESPONSES_COMBINED_2026-08-28.md`
- `FC_REV_A_DECISION_BASELINE_2026-08-27.md`
- directly relevant local OpenESC-30x30 source at `tmp/OpenESC-30x30`
- `FC_REV_A_OPENRX_LITE_UNIVERSAL_TRANSCEIVER_ANALYSIS_2026-09-02.md` for the fixed external receiver boundary

## 3. Evidence inventory

| Evidence | Result | Control status |
|---|---|---|
| Local OpenESC repository | Clean Git checkout; HEAD `1da7dbd046760160639fb9c3f470702250b4b2cb`; remote `main` reported the same commit on 2026-09-07 | VERIFIED |
| `hardware/4in1.kicad_sch` | SHA-256 `242BBDD87FA1A67C5FA7946B96585C172E668D3DB1651BBD8050D6206A851550` | VERIFIED |
| `hardware/4in1.kicad_pcb` | SHA-256 `02D502A1A5D3E41F21F755CDC80D69172581F84BC9525AA42C553BC491F28304` | VERIFIED |
| `README.md` | SHA-256 `9D1C7EACF26019D802A941838D89F6312F8FFF3E5A0290DDE53D4C70B71CA6DA` | VERIFIED |
| `[LOCAL_SOURCE]` | Not present | OPEN |
| `[LOCAL_SOURCE]` | Not present | OPEN |
| `[LOCAL_SOURCE]` | Not present | OPEN |
| As-built board photos, substitutions/ECOs, continuity record, and calibrated test logs | Not present | OPEN |

## 4. Reconciled decisions

- DECISION: STM32H743VIT6, LQFP100, remains the bare FC MCU.
- DECISION: ICM-42688-P remains onboard on a dedicated local SPI bus, quiet sensor rail, and interrupt provision.
- DECISION: BMP390 remains onboard with a protected vent.
- DECISION: OpenESC-30x30 remains an external module with a signal/ground-only FC boundary.
- DECISION: OpenESC J1 pin 1 is raw `+BATT` and must have no conductor, trace, pad connection, protection branch, ADC branch, test point, or other FC copper.
- DECISION: J1 pin 2 is the defined signal ground; J1 pin 4 is NC; J1 pins 5-8 are logical M1-M4.
- DECISION: first bench integration uses a passive interposer/harness.
- DECISION: FC power is externally regulated; CM5 power is separate.
- DECISION: microSD logging is required; the interface choice is Stage 02 work.
- DECISION: one CAN interface is required; a second must be evaluated visibly.
- DECISION: USB-C is a debug/configuration, self-powered-device interface with VBUS sensing and no backfeed.
- DECISION: `/CURR` circuitry is optional, DNP, informational, and non-safety-critical until calibrated.
- DECISION: ArduPilot is first target; PX4 remains an alternative.
- DECISION: qualification order is PWM, DShot300, bidirectional DShot300, DShot600, then bidirectional DShot600.
- DECISION: board outline, layer count, mounting, and connector placement remain OPEN for later stages.

## 5. Conflicts and dispositions

| Conflict | Disposition |
|---|---|
| Older conceptual `ESC_SIG` alternated four signals with four grounds; OpenESC J1 carries `+BATT`, one GND, `/CURR`, NC, and M1-M4. | DECISION: do not reuse the older direct pinout. Use the controlled interposer and exact J1 logical order. |
| Historical records alternately describe 20 mV/A/165 A and 10 mV/A/330 A. | VERIFIED local 30x30 source states two 0.2 mOhm shunts in parallel with gain 100, nominally 10 mV/A and about 330 A against 3.3 V. Calibration remains OPEN. |
| Local ESC text says 2S-8S while controlled planning notes qualify 3S-8S. | ASSUMPTION: 3S-8S planning range. 2S remains OPEN until measured. |
| Older bring-up order skipped a distinct bidirectional-DShot300 step. | DECISION: use the 2026-09-07 user-approved sequence. |
| Older Stage 02 gates expected final connector geometry; current policy leaves placement OPEN. | DECISION: freeze electrical/logical contracts now; retain mechanical placement and final connector release as OPEN. |

## 6. ESC open register at P0 exit

| ID | Topic | Status | Owner | Closure evidence / containment |
|---|---|---|---|---|
| A-01 | Exact OpenESC source revision | VERIFIED | FC control | Local clean checkout and remote `main` both `1da7dbd046760160639fb9c3f470702250b4b2cb`. |
| A-02 | Original controlled archive/interface response package | OPEN | ESC owner | Supply the original interface PDF, response document, BOM, checksums, and release identifier. Local Git revision is containment, not a substitute. |
| A-03 | As-built board parity and substitutions | OPEN | ESC owner / assembler | Dated top/bottom photos, assembly revision, substitution/ECO record, and continuity results. |
| B-01 | J1 connector identity and electrical pin order | VERIFIED | FC control | Local schematic/PCB identify `SM08B-SRSS-TB(LF)(SN)` and pins 1-8. |
| B-02 | J1 pin-1 orientation and view convention | OPEN | ESC owner / bench integrator | Containment: the interposer drawing uses connector-face pin numbers; obtain the physical board photograph and continuity check before power. |
| B-03 | Cable mate, order, length, gauge, shield, and return topology | OPEN | ESC owner / harness owner | Controlled cable drawing and 100% continuity report. First bench use is contained by the interposer. |
| B-04 | Connector shell/mount-pad relationship | OPEN | FC control | Local source verification shows P1/P2 tied to GND; as-built continuity remains unverified. Numbered pin 2 remains the only accepted signal return. |
| C-01 | ESC battery qualification | OPEN | ESC owner | ASSUMPTION for contained planning: 3S-8S. Supply accepted evidence before claiming 2S or releasing the flight envelope. |
| C-02 | ESC BEC output | VERIFIED | FC control | No user-accessible BEC. FC and CM5 remain separately powered. |
| C-03 | ESC-side input protection | OPEN | PDB/harness owner | Local source was VERIFIED to contain no system reverse-polarity, inrush, or hot-plug solution. System owner must provide and verify it. |
| C-04 | Hot-plug and bulk-capacitor procedure | OPEN | PDB/harness owner | Controlled 3S-8S procedure, required bulk capacitor, polarity check, fuse/current limit, and abort thresholds. |
| D-01 | `/CURR` nominal topology and scale | VERIFIED | FC control | Local source supports nominal 10 mV/A, ground-referenced, about 1 kOhm output path. |
| D-02 | FC `/CURR` circuitry | DNP | FC owner | Preserve optional PC1/ADC1 candidate and DNP protection/filter footprints; no safety use. |
| D-03 | `/CURR` calibration | OPEN | ESC owner / test owner | Hold all safety use; run a zero/low/mid/high sweep against calibrated external measurement. |
| D-04 | `/CURR` fault behavior | OPEN | ESC and firmware owners | Hold all safety use; run open/short/out-of-range tests and define firmware handling. |
| E-01 | PWM/DShot300/DShot600 actual-board waveform acceptance | OPEN | Joint FC/ESC test | Propeller-off captured waveforms and error-rate results in required order. |
| E-02 | Bidirectional DShot300/600 telemetry | OPEN | Joint FC/ESC test | Turnaround, return amplitude, decoded eRPM/EDT fields, and error-rate evidence. |
| E-03 | Reset/disarm/signal-loss behavior | OPEN | Joint FC/ESC test | FC-reset, ESC-reset, disconnect, and brownout tests with motors restrained and props removed. |
| E-06 | Telemetry-field and logging contract | OPEN | Firmware owner | Exact AM32 target/version/config and ArduPilot telemetry configuration. |
| F-01 | Reproducible ESC firmware package | OPEN | ESC firmware owner | Target, source commit, binary checksum, bootloader, configurator export, and Windows recovery procedure. |
| F-03 | Motor poles/KV/direction configuration | OPEN | Propulsion owner | Exact motor/prop set and saved AM32 parameters. |
| F-04 | Safe startup and shutdown proof | OPEN | Joint test owner | Bench sequence E-03 completed. |
| F-05 | Thermal foldback reliance | DNP | Project control | FC safety case must not rely on ESC foldback. |
| G-01 through G-05 | Current, thermal, cooling, and propulsion envelope | OPEN | Propulsion owner | Hold flight claims; obtain instrumented current-duration-temperature-airflow tests for the actual motor, prop, battery, and installation. |
| H-01 | ESC KiCad reproducibility and source parity | OPEN | ESC design owner | Supply a clean ERC/DRC/netlist/library audit for commit `1da7dbd...`; FC does not modify the ESC source. |
| H-03 | Mechanical/fabrication/assembly release | OPEN | ESC owner / manufacturer | Dimensioned drawing, stack, finish, assembly data, and accepted production package. |

## 7. P0 exit assessment

P0 result: CONDITIONAL PASS for Stage 02 entry with controlled OPEN items.

The safety boundary, J1 electrical order, interposer containment, corrected H743 package pins, and owners/closure evidence are recorded. The missing original ESC attachments and all bench/flight evidence remain OPEN. No direct cable, ESC fabrication package, safety use of `/CURR`, or flight claim is released.
