> Historical technical record. Names and private workstation/session references were neutralized for publication. Dates and assertions describe the recorded stage, not current physical qualification. See the current validation-status page for later checks.

# FC Drone FC Rev A - Stage 05 R12 continuation control review

Date: 2026-09-08, Asia/Kuala_Lumpur  
Result: **VERIFIED STOPPED STATE - STAGE 05 OPEN**  
Stage 06: **NOT AUTHORIZED**

## Outcome

Project control independently reviewed the R12 handoff, reproduced the calculations and candidate pin audit, reran native KiCad verification, and visually inspected the full and close-up power-sheet renders. The approved R10 continuation envelopes remain intact, but the complete pre-capture evidence gate did not pass. Stopping without capture or part freeze was correct.

## Verified evidence

- The R12 control-state SHA-256 matched at continuation entry.
- The R10 handoff was preserved byte-for-byte as `qa/stage05-power/history/FC_REV_A_STAGE_05_STOPPED_R10_2026-09-08.md`, SHA-256 `4349051668820b141e8b00bd18f8874efc1e2c2f9e6681e89dd8b803994e2fde`.
- Independent reruns of `calculations.py`, `pin_audit.py`, and `verify.py` passed at their stated stopped-state scope.
- Ninety-five controlled entry files were checked. Only the authorized canonical Stage 05 handoff changed.
- Nine newly retained official manufacturer PDFs passed recorded byte-size and SHA-256 verification. Failed support-page retrievals remain explicitly marked and were not treated as specifications.
- The KiCad design remains at the Stage 04 baseline: 29 netlisted components, 88 nets, 54 retained ERC findings, zero new findings and zero PCB files.
- Full and close-up power-sheet renders show the sheet remains the empty foundation sheet. No symbols, circuits, test points or parent-sheet power connections were added.
- Stage 06 has not begun.

## Decisive blockers

1. **Switched-load stability:** the approved 680 uF external allowance plus the minimum 15 uF local capacitance gives 695 uF in the direct-connected approximation, exceeding TPS63070's published 470 uF maximum. The intervening switch/harness may alter the impedance, but no retained source or complete loop model proves stability over line, load and temperature.
2. **Startup SOA/temperature:** the approved startup envelope calculates up to 5.548 W peak and 143.737 mJ in TPS25940. Required transient thermal-impedance bounds are no more than 12.617 degC/W at 55 degC or 9.913 degC/W at 70 degC before preheating. Guaranteed application data establishing those limits is unavailable.
3. **Hot continuous loss:** available room-temperature efficiency and switch-resistance data do not bound total loss at 55/70 degC on the eventual FC layout. No unsupported 90% efficiency assumption was used.
4. **Unpowered leakage/status:** published TPS25940 reverse-leakage conditions do not prove total system backfeed below 100 uA for VIN=0 and all external-power states. Its fault output can release below internal undervoltage, so a main-powered pull-up alone cannot guarantee fail-low status during input removal.
5. **Fault/source coordination:** the candidate input-eFuse limit can span approximately 4.10-5.02 A. This is not yet coordinated with the 3 A continuous/4 A for 100 ms POWER1 contract, source collapse, blanking, thermal response or restart behavior.

## Source/model findings

- PCBParts' TPS63070 pin record omits physical pins 8/VOUT and 13/VIN; the manufacturer datasheet is the pin authority. No catalog model was imported.
- The TPS63070 EVM guide contains a 0.1 pF/0.1 uF VAUX-capacitor inconsistency. The datasheet and BOM identity support 100 nF; the drawing was not copied blindly.
- `TPS63070RNMR + TPS25940ARVCR` remains a **CANDIDATE**, not an approved capture or BOM choice.
- `TPS552892RYQR` remains a permitted analysis alternative with external compensation; it may help address the capacitance constraint but does not close TPS25940 thermal/backfeed/status gaps.

## Safe continuation paths

- **Path A - preserve the 680 uF contract:** perform a full TPS552892 switched-network compensation/stability analysis and seek source-backed or manufacturer application evidence for startup Ztheta/SOA, hot losses, VIN=0 leakage and fault/status behavior. No external contact is authorized merely by this review.
- **Path B - reduce the AUX capacitance contract:** adopt `C_attached <= 470 uF - C_local,max` if retaining TPS63070's published direct-capacitance envelope. For example, a proven 100 uF local maximum would restrict attached effective capacitance to 370 uF. This is a material contract change and still does not close thermal, leakage or status gates.

Project control recommends Path A first because it preserves the approved external-module allowance. If Path A cannot produce source-backed closure, return with the exact residual gaps before considering Path B. Stage 05 remains OPEN and Stage 06 remains locked.
