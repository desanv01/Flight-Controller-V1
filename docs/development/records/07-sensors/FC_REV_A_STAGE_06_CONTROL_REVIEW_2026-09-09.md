> Historical technical record. Names and private workstation/session references were neutralized for publication. Dates and assertions describe the recorded stage, not current physical qualification. See the current validation-status page for later checks.

# FC Drone FC Rev A — Stage 06 control review

Date: 2026-09-09  
Reviewed handoff: `FC_REV_A_STAGE_06_IMU_BAROMETER_CIRCUITS_2026-09-09.md`  
Control disposition: **VERIFIED CONDITIONAL PASS at recommendation-grade sensor schematic-capture scope**  
Next stage: Stage 07 remains locked pending separate human authorization.

## 1. Review conclusion

Project control accepts Stage 06 as complete at its authorized schematic-capture and evidence scope. The onboard ICM-42688-P and BMP390 circuits, partial-power containment, local BMP390 slew candidate, controlled local symbols, source evidence, load calculations and deterministic verification are present and reviewable.

This acceptance does not promote any exact support IC, passive, package or footprint to a production DECISION. It does not prove sensor electrical integration, PCB behavior, environmental performance, fabrication readiness or flight readiness. Every OPEN item in the Stage 06 handoff remains mandatory at its assigned gate.

## 2. Independently verified results

- VERIFIED: the required handoff exists and was read completely.
- VERIFIED: independent reruns of `calculations.py`, `verify_capture.py 8` and `final_audit.py` all exited zero.
- VERIFIED: 163 real components and 155 nets are exported; Stage 06 adds 45 sensor-sheet components.
- VERIFIED: 158 captured sensor pin/net checks report zero errors.
- VERIFIED: 68 source-to-symbol physical-pin checks, nine frozen MCU-signal checks and 413 preserved existing pin/net assignments pass.
- VERIFIED: the original local-library symbols are unchanged; seven new controlled symbol definitions support eight new IC instances.
- VERIFIED: MCU/core and Stage 05 power changes are append-only hierarchy-boundary connections: nine wires plus nine hierarchical labels on the MCU core and one label, wire and hierarchical label on the power sheet.
- VERIFIED: no `.kicad_pcb` file, Stage 07 circuit, manufacturing output, order or fabrication authorization exists.
- VERIFIED: the post-review 84-artifact Stage 06 package was resealed after the independent verifier regenerated QA outputs, and every sealed path/hash/byte count matched.

## 3. Visual review

Project control inspected:

- the complete Stage 06 sensor sheet;
- the ICM-42688-P block and its return-path buffering;
- the MCU-to-sensor SPI isolation/bias block;
- the TPS22918 local BMP390 slow-rail block;
- the BMP390 and TCA9416 I2C block;
- the optional barometer interrupt block;
- the root hierarchy;
- the STM32H743 sensor-interface boundary.

The final iteration is readable, separated into controlled functional blocks and visibly marked RECOMMENDATION / OPEN physical validation / not for fabrication. No obvious wire short, property overlap, prohibited camera/lidar circuit, PA0/PA1 reuse, Stage 07 circuit or PCB work was found.

## 4. Controlled ERC and KLC disposition

- CONTROLLED ERC: 46 findings remain: 41 inherited one-ended MCU reservations, the official-required VCAP power-output pair, two inherited multiple-net-name warnings and two new U13/U19 B4 bidirectional-to-GND mode warnings. The latter are contained because DIR4 is fixed low and A4 is NC. No broad suppression or severity change was introduced.
- CONTROLLED KLC: four findings remain and are explicitly explained. Three S5.1 warnings result from deliberately unassigned final footprints for ICM-42688-P, BMP390 and TCA9416DDFR; final land-pattern approval belongs to Stage 08. The TPS22918 S4.2 item is a non-electrical layout-convention exception caused by the checker treating a load switch as a converter. Pin numbers, pin types and connectivity are unaffected.

## 5. Architecture and implementation status

- DECISION retained: ICM-42688-P is the onboard IMU on the frozen dedicated SPI1 allocation and `3V3_SENS`.
- DECISION retained: BMP390 is the onboard barometer with a protected pressure vent and the frozen I2C2 allocation.
- RECOMMENDATION: SN74AXC4T774, SN74AUP3G17 and the associated bias networks provide the captured IMU partial-power containment.
- RECOMMENDATION: TPS22918 creates delayed `BARO_3V3`; TCA9416 isolates/translates I2C; SN74AXC1T45 isolates the optional barometer interrupt.
- RECOMMENDATION: the calculated TPS22918 nominal 10–90% rise is about 40.029 ms.
- OPEN: the Bosch minimum 10 ms ramp is not guaranteed over PVT/restart by the published typical slew relation. Do not energize/integrate the BMP390 until coupon or prototype waveforms qualify the actual VDD/VDDIO pins.
- OPEN: exact sensor/support IC sourcing, production passives and all footprints remain unapproved.

## 6. Load and sequencing disposition

- VERIFIED calculation: the Stage 06 steady screening total is 23.529 mA, leaving 1.471 mA against the 25 mA planning screen.
- ASSUMPTION: the 4 mA IMU allowance is an engineering allocation, not a manufacturer guaranteed maximum.
- VERIFIED calculation: new direct sensor capacitance gives a 40.194 mA startup screen at the assumed 1 ms ramp, below the 50 mA transient target.
- OPEN discrepancy: including existing Stage 05 C41 produces approximately 133.518 mA at 1 ms or 60.192 mA at 3 ms. Project control must resolve whether the 50 mA screen includes C41 and validate total LDO/startup `I(V,t)`; no Stage 05 value is silently changed.
- OPEN: actual ICM maximum/dynamic consumption, direct-rail 1–3 ms monotonic ramp, sensor-rail noise, exact AUP thresholds at the real rail, partial-power/brownout/restart behavior and assembled backfeed require later evidence.

## 7. Retained OPEN items

The authoritative Stage 06 OPEN register is S06-01 through S06-10 in the handoff:

1. BMP390 minimum-ramp and interface-overrail qualification.
2. ICM direct-rail ramp, noise and transient qualification.
3. C41/50 mA boundary interpretation and total startup measurement.
4. Actual ICM maximum/dynamic load.
5. AUP threshold evidence or qualified replacement.
6. All-state partial-power, brownout, prebias, hot-restart, short and backfeed testing.
7. Final land patterns, pin-1, MEMS/vent mechanics, decoupler derating and assembly constraints.
8. Genuine sensor sourcing and approved BOM.
9. H743/SPI/I2C/interrupt/reset/recovery firmware and waveform validation.
10. Vibration, EMI, thermal-gradient, pressure-lag/propwash and assembled-accuracy validation.

Stage 05 deferred OPEN items also remain unchanged. None is closed by ERC, export, calculation or this control review.

## 8. Stage gate

Stage 06 exit gate: **PASSED CONDITIONALLY for recommendation-grade schematic capture.**

Stage 07 may begin only after a new explicit human authorization and must first read the Stage 06 handoff, this control review, the current control state and the retained status ledger. Stage 07 must not reinterpret the Stage 06 recommendations as production-approved parts and must carry S06-01 through S06-10 to their assigned owners.

No Stage 07 implementation, PCB work, fabrication, ordering or flight approval is authorized by this review.
