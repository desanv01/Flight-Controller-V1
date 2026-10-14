> Historical technical record. Names and private workstation/session references were neutralized for publication. Dates and assertions describe the recorded stage, not current physical qualification. See the current validation-status page for later checks.

# FC Drone FC Rev A - Stage 05 R18 control review

Date: 2026-09-09  
Disposition: VERIFIED CONDITIONAL PASS; Stage 05 is accepted at recommendation-grade schematic-capture scope. Stage 06 is not authorized by this review.

## Review outcome

- VERIFIED: the dedicated Stage 05 task produced and sealed `FC_REV_A_STAGE_05_POWER_TREE_PROTECTION_MONITORING_2026-09-08.md` as an R18 conditional-pass handoff.
- VERIFIED: `hardware/FC_REV_A/sheets/02_power.kicad_sch` now contains the protected POWER1 entry, hardware-default startup sequencing, `3V3_MAIN`, `5V_AUX`, `3V3_SENS`, `3V3_ANA`, informational fail-low `PWR_STATUS`, and the approved measurement access.
- VERIFIED: the root hierarchy connects only the approved `3V3_MAIN`, GND, `3V3_ANA`, and `PWR_STATUS` boundaries. The MCU-core delta is limited to three hierarchical labels and three short boundary wires; existing core records and the original MCU symbol are preserved.
- VERIFIED: camera and `VL53L5CX-SATEL` remain separately powered CM5 peripherals with no FC rail load. The retired `LIDAR_FC` interface consumes no circuit; PA0/PA1 remain reserved.
- VERIFIED: `VBAT_SENSE_3V3`, CAN2, and `ESC_CURR_DNP` remain DNP/reserved. USB, OpenESC J1-1/J1-4, and CM5 no-backfeed boundaries are unchanged.
- VERIFIED: no PCB file, Stage 06 circuit, fabrication release, order, or flight approval was created.

## Recommendation-grade implementation retained

- RECOMMENDATION: TPS259470LRPWR input eFuse with TPS3808G01DBVR startup supervisors.
- RECOMMENDATION: TPS62130ARGTR plus XAL4020-222MEC for `3V3_MAIN`.
- RECOMMENDATION: TPS552892RYQR plus XAL7070-682MEC for the locally regulated AUX buck-boost stage.
- RECOMMENDATION: TPS25940LRVCR as the latch-off AUX limiter.
- RECOMMENDATION: TPS73633DBVR for `3V3_SENS`, enabled by hardware input health and main power good.
- RECOMMENDATION: TPS3700DDCR monitors and SN74HCS11DR logic for informational fail-low `PWR_STATUS`.
- RECOMMENDATION: BLM18AG601SN1D as the populated `3V3_ANA` bead; the mutually exclusive zero-ohm bypass remains DNP.
- RECOMMENDATION: all exact magnetics, passives, packages, and footprints listed in the handoff remain subject to Stage 08 footprint/BOM review and later physical qualification. No item is promoted to production DECISION by this review.

## Independent verification

- VERIFIED: `qa/stage05-power/correction_r18/final_verify.py` independently reran successfully after the final metadata correction.
- VERIFIED: 118 real components total, including 89 Stage 05 components; 138 exported nets; 263 captured pin/net checks; 100 manufacturer-to-symbol IC pin checks; zero pin/net mismatches; zero PCB files.
- CONTROLLED ERC: 53 retained findings comprise 50 unconsumed MCU reservations, one official-required VCAP power-output pair, and two intentional aliases. The Stage 04 `3V3_ANA` and `PWR_STATUS` ownership findings are cleared. No new ERC suppression was added.
- VERIFIED: all 15 R18 analytical gates pass. Key results are `5V_AUX` 4.81255 V steady minimum at 1 A, 4.76255 V after the illustrative 50 mV droop allocation, 1.13948-1.35109 A settled AUX current limit, 0.31166 A first-5-ms input screen, and 95.0877 uA internal backfeed engineering allocation.
- VERIFIED: the corrected root render identifies Stage 05 R18 and states that the MCU core and power are captured while remaining sheets are unpopulated and the design is not for fabrication.
- VERIFIED: final full-sheet and close-up renders for input protection, main buck, AUX converter, AUX limiter, sensor/analog rails, status logic, root hierarchy, and MCU boundary were visually inspected and found readable.

## OPEN items carried forward

- OPEN: final POWER1 source-rise/source-impedance, module startup concurrency/capacitance, and board-ambient envelopes require contract confirmation and physical measurement.
- OPEN: complete AUX switched-network stability, startup SOA, transient response, short/latch behavior, prebias, removal, brownout, and restart require the assigned coupon/Stages 11-13 validation.
- OPEN: 55/70 degC board thermal behavior, converter/magnetic loss, EMI, and sensor-rail PSRR require PCB/prototype evidence.
- OPEN: the strictly below 100 uA assembled POWER1 backfeed requirement remains split between Stage 07 interface accounting and Stages 11-13 measurement. The 95.0877 uA Stage 05 figure is an engineering allocation, not a guaranteed assembled maximum.
- OPEN: Stage 06 must reconcile actual ICM-42688-P and BMP390 loads, sequencing, I/O back-power, and noise susceptibility with the captured 25/50 mA sensor screen and 100 mA reserve.
- OPEN: Stage 07 must enforce the 1 A aggregate AUX contract, the 0.5 A OpenRX allocation, the residual 0.5 A allowance, actual module startup behavior, connector-path resistance, and all independently powered interface paths.
- OPEN: Stage 08 must audit U2/U5 manufacturer land patterns and every recommendation footprint/MPN before any placement or production freeze.
- OPEN: the reported TPS552892 workbook was not located, and no FC-specific PSpice result is claimed. Under R18 this is supporting evidence, not a Stage 05 capture blocker.

## Stage 06 entry gate

Stage 05 is accepted and technically ready to hand off. Stage 06 may begin only after explicit human authorization. Its task must first read the R18 Stage 05 handoff, this control review, the current control state, the Stage 02 resource/port records, and the official current ICM-42688-P and BMP390 sources. Stage 06 is limited to the onboard IMU and barometer circuits and must not alter the accepted power topology, MCU resource map, external interfaces, PCB geometry, or begin Stage 07.

