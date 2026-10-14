> Historical technical record. Names and private workstation/session references were neutralized for publication. Dates and assertions describe the recorded stage, not current physical qualification. See the current validation-status page for later checks.

# FC Drone FC Rev A
# Stage 02 Interface and Resource Freeze - Main Handoff

Date: 2026-09-07  
Stage result: CONDITIONAL PASS  
Active work completed: Stage 02 only

## 1. Outcome

Stage 02 has a conflict-free H743 interface/resource candidate and bounded electrical contracts for all required ports. The deterministic ArduPilot hwdef parser accepted the complete assignment and generated timer, DMA, DMAMUX, SDMMC, FDCAN, SPI, UART, and ADC definitions.

The stage result remains CONDITIONAL PASS because original ESC attachments, final physical cable evidence, external module MPNs, final connector mechanics/placement, and runtime/bench results remain OPEN and require project-control acceptance. No KiCad project, schematic circuit capture, PCB, ERC, or DRC was created or run.

## 2. Work completed

- Reconciled the required control records and current user policy.
- Recorded P0 as CONDITIONAL PASS and created a controlled ESC OPEN register.
- Verified the local OpenESC source is a clean Git checkout at upstream `main` commit `1da7dbd046760160639fb9c3f470702250b4b2cb`.
- Confirmed the original ESC interface PDF, response document, and BOM are absent and kept them OPEN.
- Froze OpenESC J1-1 and J1-4 as no-conductor/no-copper NC positions.
- Defined a passive first-bench interposer/harness and its continuity/isolation tests.
- Froze four motor allocations on PD12-PD15 / TIM4_CH1-CH4 as DECISION entries; parser evidence is recorded separately as VERIFIED.
- Selected SDMMC1 4-bit microSD because the full resource map remains conflict-free and ArduPilot provides native H743 SDMMC support.
- Froze CAN1 on PD0/PD1 and visibly reserved CAN2 on PB5/PB6 with its transceiver/connector DNP.
- Froze USB-C as self-powered USB FS device/debug with VBUS sense and enforced no-backfeed.
- Froze the FC input contract at 5.2 V nominal, 4.9-5.5 V operating, at least 2 A continuous / 3 A for 100 ms at the connector.
- Shortlisted exact external FC module Holybro `UBEC 5A (3-14S)`, SKU `15034`, configured 5.2 V, as RECOMMENDATION.
- Assigned dedicated SPI1 to ICM-42688-P, I2C2 to BMP390, and non-conflicting UARTs to OpenRX, GNSS, telemetry, CM5, lidar, and AUX.
- Reconciled ICM-42688-P sourcing to TDK's current official product record, which lists DS-000347 Version 1.9; the retired v1.5 link is no longer used as an authority.
- Ran the official ArduPilot H743 hwdef generator at commit `12f1c264f2536c4c9565eec910fa028579845d36`; it exited 0.

## 3. Files created or modified

- `FC_REV_A_STAGE_01_CLOSEOUT_AND_ESC_OPEN_REGISTER_2026-09-07.md`
- `FC_REV_A_ESC_FC_INTERFACE_BASELINE_2026-09-07.md`
- `FC_REV_A_STAGE_02_ENTRY_BRIEF_2026-09-07.md`
- `FC_REV_A_STAGE_02_INTERFACE_RESOURCE_FREEZE_2026-09-07.md`
- `FC_REV_A_STAGE_02_H743_PIN_TIMER_DMA_MATRIX_2026-09-07.md`
- `FC_REV_A_STAGE_02_PORT_CONTRACT_2026-09-07.md`
- `FC_REV_A_ESC_OPEN_ITEM_REGISTER_2026-09-07.md`
- `FC_REV_A_STAGE_03_ENTRY_BRIEF_2026-09-07.md`
- `output/pdf/FC_REV_A_STAGE_02_ESC_CABLE_INTERPOSER_DRAWING_2026-09-07.pdf`
- `qa/stage02-hwdef-validation/hwdef.dat`
- `qa/stage02-hwdef-validation/defaults.parm`
- generated parser evidence under `qa/stage02-hwdef-validation/generated/`

The shallow official ArduPilot evidence checkout under `tmp/ardupilot-stage02/` is an analysis dependency, not a deliverable or canonical project.

## 4. Confirmed decisions

- DECISION: exact MCU is STM32H743VIT6 LQFP100.
- DECISION: ICM-42688-P is local on dedicated SPI1 with quiet rail and interrupts.
- DECISION: BMP390 is onboard on local I2C2 with protected vent.
- DECISION: OpenESC remains external; J1-1 raw battery and J1-4 are electrically NC at the FC.
- DECISION: initial integration uses the controlled passive interposer.
- DECISION: M1-M4 map in logical order to PD12-PD15 / TIM4_CH1-CH4.
- DECISION: microSD uses SDMMC1 4-bit, not SPI, for Rev A.
- DECISION: CAN1 is populated on FDCAN1; CAN2 is a reserved DNP evaluation path on FDCAN2.
- DECISION: USB-C is device/debug only, senses VBUS, and cannot power/backfeed FC rails.
- DECISION: `/CURR` is optional DNP/informational on PC1/ADC1 and disabled by default.
- DECISION: OpenRX Lite-UFL uses full-duplex uninverted CRSF on USART6.
- DECISION: CM5 uses a data-only UART7 link and remains separately powered/non-essential.
- DECISION: ArduPilot is first target; PX4 remains a compatible alternative to be checked later.
- DECISION: qualification order is PWM, DShot300, bidirectional DShot300, DShot600, bidirectional DShot600.

## 5. Recommendations and candidates

- RECOMMENDATION: Holybro UBEC 5A SKU 15034 at 5.2 V for the external FC source, subject to ripple/transient/thermal/harness validation.
- RECOMMENDATION: JST-GH 1.25 mm keyed/latching family for low-current flight ports, without claiming Pixhawk compatibility.
- RECOMMENDATION: TI TCAN332DCNR for populated CAN1; same footprint/function may be retained DNP for CAN2.
- RECOMMENDATION: ST USBLC6-2SC6 as the USB D+/D- ESD candidate.
- CANDIDATE: LSE population, GNSS PPS, SWO, auxiliary UART, and CAN2.
- CANDIDATE: exact USB-C receptacle, microSD socket, external-module connectors, and ESD parts remain for schematic/mechanical stages.

## 6. Assumptions

- ASSUMPTION: first-bench ESC cable is at most 150 mm and the motor/return bundle is kept together.
- ASSUMPTION: OpenESC planning input is 3S-8S; 2S remains unqualified.
- ASSUMPTION: `5V_AUX` total continuous external load is limited to 1.0 A until measured budgets are available.
- ASSUMPTION: UART/I2C/CAN external cable lengths are at most 300 mm except CAN, which is bounded to 1 m for the initial vehicle.
- ASSUMPTION: HSE is 8 MHz for the parser-only board definition; oscillator choice remains OPEN for Stage 04.

## 7. OPEN items and unresolved errors

- OPEN: original `OpenESC-30x30-Interfaces.pdf`, ESC response document, and rev3.3 BOM are missing.
- OPEN: actual assembled ESC revision, substitutions, photographs, and continuity.
- OPEN: final ESC harness/contact/wire/crimp identity and direct-flight cable release.
- OPEN: `/CURR` calibration and fault behavior.
- OPEN: AM32 exact target/binary/configuration/bootloader and the upstream April 2026 stale-bidirectional-telemetry issue applicability to the selected target/release.
- OPEN: receiver current/range/failsafe, GNSS/compass module, telemetry radio, scalar lidar, and CM5 carrier exact MPNs.
- OPEN: Holybro UBEC output ripple/tolerance, temperature, transient and EMI performance in this airframe.
- OPEN: exact connector headers/mates, pin-1 views, board placement, board outline, mounting, and layer count.
- OPEN: runtime ArduPilot build/bootloader/board ID, PX4 target, sensor orientation, and all hardware measurements.
- OPEN: exact ESD, protection, load-switch, regulator, microSD socket, and USB-C MPN/footprints.
- OPEN: full DS-000347 Version 1.9 PDF review for ICM-42688-P pin-level, timing, register, and reference-circuit details before Stage 04 capture.

No unresolved parser error remains. The first hwdef run stopped only because a non-release validation file did not embed a bootloader; the validation definition was explicitly configured with bootloader flashing disabled, and the repeated command exited 0. This is recorded as a resolved test-fixture issue, not a product decision.

## 8. Verification results

| Check | Result |
|---|---|
| Local OpenESC Git identity | VERIFIED clean at `1da7dbd...`, matching remote main on 2026-09-07 |
| J1 MPN and nets in local schematic/PCB | VERIFIED |
| ST LQFP100 package/core pins | VERIFIED against DS12110 Rev 11 |
| Alternate functions for assigned peripherals | VERIFIED by ST datasheet and ArduPilot H743 table |
| Duplicate/incompatible pin assignment | VERIFIED: none found; ArduPilot parser accepted the map |
| Motor timer/DMA/DMAMUX | VERIFIED: TIM4 group plus DMA1 Stream 2 / DMAMUX TIM4_UP generated; input-capture request macros generated for all four channels |
| SPI1 IMU DMA isolation | VERIFIED: separate DMA1 streams 0/1; `DMA_NOSHARE SPI1*` accepted |
| SDMMC feasibility | VERIFIED: SDMMC1 D0-D3/CK/CMD accepted, no conflict; FATFS hwdef generated |
| FDCAN feasibility | VERIFIED: CAN1 and CAN2 pins accepted together |
| USB/SWD/core recovery conflict | VERIFIED: none found |
| ICM-42688-P current source record | VERIFIED: TDK product page lists DS-000347 Version 1.9, production status, package, and SPI support; full Version 1.9 PDF circuit-detail review remains OPEN |
| Bench/runtime validation | OPEN: not performed |

## 9. ERC/DRC and scope status

- ERC: NOT APPLICABLE - no KiCad schematic exists for this stage.
- DRC: NOT APPLICABLE - no KiCad PCB exists for this stage.
- KiCad project creation/capture: NOT STARTED by policy.
- PCB placement/routing/manufacturing decisions: NOT STARTED by policy.

## 10. Required human approvals

Project control must explicitly accept:

1. this CONDITIONAL PASS and its remaining OPEN items;
2. 5.2 V POWER1 contract and Holybro UBEC 5A shortlist;
3. SDMMC1 microSD decision;
4. TIM4 PD12-PD15 motor group;
5. populated CAN1 plus DNP/reserved CAN2 policy;
6. bench-only interposer drawing and prohibition on direct-flight use;
7. proceeding to Stage 03 while final board geometry and connector placement remain OPEN.

## 11. Exact Stage 03 entry criteria

Stage 03 may begin only after project-control acceptance of the seven items above. The following must be treated as inputs, not silently changed:

- use this exact pin/resource matrix unless a documented Stage 02 change request is approved;
- preserve J1-1 and J1-4 as true no-copper NCs;
- preserve external-only FC power and separate CM5 power;
- implement SDMMC1 microSD and required CAN1; retain CAN2 as DNP/reserved;
- implement USB device-only VBUS sensing/no-backfeed;
- show `/CURR` as DNP/informational and disabled by default;
- keep board outline, layer count, mounting, and connector placement OPEN;
- create only the KiCad project foundation/hierarchy, libraries, rules, revision metadata, and documentation structure assigned to Stage 03.

## 12. Exact next-stage instructions

Create the Stage 03 KiCad foundation without capturing detailed circuits or routing. Establish the hierarchical sheet plan and controlled net names from the port contract; create library tables and design-rule placeholders; register KiCad/tool versions; add revision metadata; and write the Stage 03 handoff. Do not alter the Stage 02 pin map, select final connector footprints, set the board outline/layer stack, capture detailed MCU/power/sensor circuits, or begin PCB placement. Any required change returns to Stage 02 project control.

## 13. Project-control acceptance addendum

VERIFIED: on 2026-09-07 the user explicitly approved all seven items in section 10. Stage 02 is accepted as PASS FOR STAGE 03 ENTRY, with every recorded OPEN item retained.

- DECISION: POWER1 contract is approved. Holybro SKU `15034` remains a RECOMMENDATION/test-shortlist item only, not a production module or BOM decision.
- DECISION: SDMMC1 microSD and TIM4 PD12-PD15 motor allocations are approved; physical runtime validation remains OPEN.
- DECISION: CAN1 is populated and CAN2 remains reserved DNP; CAN2 cannot be populated without later approval.
- DECISION: the interposer is bench-only, J1-1/J1-4 have no contact/conductor/copper, and no direct-flight cable is approved.
- DECISION: Stage 03 foundation entry is approved while board geometry and connector mechanics/placement remain OPEN.

Evidence reconciliation after handoff review: `ESC_Integration_Confirmation_FC_Team_v3.docx` was recovered and checksum-verified. Its JST SH connector evidence is usable, but its raw-battery J1-1 self-power instruction is superseded and prohibited. The missing-originals and as-built evidence OPEN items are narrowed, not closed.
