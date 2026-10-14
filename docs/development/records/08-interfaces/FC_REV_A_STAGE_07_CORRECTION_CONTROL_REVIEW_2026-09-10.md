> Historical technical record. Names and private workstation/session references were neutralized for publication. Dates and assertions describe the recorded stage, not current physical qualification. See the current validation-status page for later checks.

# FC Drone FC Rev A — Stage 07 correction control review

Date: 2026-09-10  
Reviewed handoff: `FC_REV_A_STAGE_07_CORRECTION_CLOSEOUT_2026-09-10.md`  
Dedicated task: existing `FC FC Rev A — Stage 07 ESC and External Interfaces`, thread `[PRIVATE_SESSION]`, continued using `gpt-5.6-sol` with high reasoning  
Disposition: **VERIFIED CONDITIONAL PASS — analytical correction/closeout accepted; Stage 08 entry authorized by the user's conditional release**

## Control conclusion

The correction closeout passes project-control review. It preserves the accepted Stage 07 schematic, strengthens the ESC evidence boundary, defines the sparse FC-to-ESC harness recommendation and continuity-jig criteria, corrects the AUX cable-drop screen, expands the S07-01 through S07-12 analytical dispositions, and retains every firmware- or hardware-dependent result as OPEN.

No canonical schematic or symbol-library file changed. No PCB file, geometry, placement, routing, manufacturing output, procurement action, fabrication authorization or Stage 08 implementation was created by the Stage 07 correction task.

The user explicitly authorized Stage 08 only after this handoff passed project-control review. That condition is now satisfied. Stage 08 may start at schematic/BOM-review scope only. Stage 09 remains locked.

## Supplied ESC evidence disposition

- VERIFIED: the two supplied originals are preserved unchanged under `hardware/FC_REV_A/docs/evidence/stage07-correction/user-supplied/`.
- VERIFIED: `Thank you for the detailed review..txt` is 2,691 bytes with SHA-256 `eab50fcab258d2f2af1e4e844857dd3dd7e318c484c8e540199e5e711fbc0343`.
- VERIFIED: `escdesignupdate.zip` is 778,633 bytes with SHA-256 `0ad0c2de74d8f2399b64ce441d7facb2af63bb3990ce22bb70dc868d543de80c`.
- VERIFIED: the ZIP contains one BOM CSV and six screenshots only. It contains no Gerbers, drills, native KiCad source, netlist, firmware, bootloader, private AM32 fork or as-built photographs.
- VERIFIED SCREENSHOT FACT: the ESC overview depicts `SM08B-SRSS-TB`, J1-1 raw `+BATT`, J1-2 GND, J1-3 `CURR`, J1-4 visually unconnected and J1-5 through J1-8 as M1 through M4.
- CONTROLLED LIMITATION: the supplied ERC screenshot shows zero errors, 329 warnings and 49 exclusions; the DRC screenshot shows zero errors, 26 warnings, 15 ignored tests and no schematic-parity run. These images are not independently rerunnable ESC verification.

## Accepted analytical corrections

- DECISION CLARIFICATION: J1-1 and J1-4 absence is an FC harness/interposer boundary, not a requested ESC-board modification. The FC assembly has no terminal, crimp, wire, pad, copper, via, test point or net for either position. Default J1-3 `/CURR` also remains absent/DNP.
- RECOMMENDATION: ESC-side `SM08B-SRSS-TB`, mating `SHR-08V-S-B`, and a verified JST SH terminal suffix. The retained JST catalogue lists `SSH-003T-P0.2-H`; exact procurement suffix and applicator remain OPEN.
- RECOMMENDATION: a five-conductor signal/GND interposer or harness with AWG28, maximum 150 mm initial one-way length, controlled circuit-1/key views, strain relief, and 100% continuity/isolation inspection. Flight release remains OPEN.
- VERIFIED ANALYTICAL RESULT: the prior 0.5 A OpenRX reserve does not analytically preserve the 4.75 V remote floor through the screened GH AUX path. With the stated aged-contact, 85 °C, AWG26 assumptions and 0.15 A GPS load, the calculated receiver ceiling is approximately 0.379 A at 150 mm, 0.398 A at 100 mm and 0.440 A with zero wire before the separate dynamic allowance.
- DECISION: the 4.75 V requirement and 0.5 A planning reserve are not reduced. Stage 08 may review the connector/footprint/BOM implications, while any power-path redesign remains controlled and physical voltage/current evidence remains OPEN.
- RECOMMENDATION: retain the existing PWM → DShot300 → bidirectional DShot300 → DShot600 bring-up order. The private `OPENESC_20_F421` source/build, bootloader, binary hashes, option bytes, mapping and all real waveforms remain OPEN.
- VERIFIED ANALYTICAL RESULT: default active AUX allocation remains 0.65 A and default planned post-switch capacitance remains 320.6 µF; camera and lidar remain excluded because they are CM5-only loads. The 680 µF, 1 A startup and 1 A continuous contracts remain unchanged.
- VERIFIED ANALYTICAL SCREEN: default-populated interface leakage arithmetic reduces from the all-option 222.9 µA envelope to about 176.8 µA after removing stated DNP allocations. This still does not prove less than 100 µA reverse current into POWER1; assembled measurement remains OPEN.

## Independent verification

Project control reran:

`python -X utf8 qa/stage07-correction/verify_closeout.py`

Result: **PASS — analytical Stage 07 correction closeout only**.

- 33 correction-control checks passed.
- 326 components and 302 nets reproduced.
- 606 pin/net checks passed with zero mismatches.
- 432 independent release checks passed.
- 108 controlled local-symbol pins audited.
- Frozen pre-Stage07 topology remained unchanged.
- All ten canonical schematic/library hashes matched the accepted Stage 07 baseline.
- J1 exported only pins 2 and 5–8; J1-2 is GND and J1-5 through J1-8 are M1 through M4.
- Thirteen previously classified ERC findings remained; no new ERC class appeared.
- Zero `.kicad_pcb` files existed.
- All nine complete-sheet and fifteen close-up renders were regenerated and hash-identical to the accepted Stage 07 visual baseline.
- Project control inspected all 24 images and observed no clipping, collision, dangling hierarchy boundary, unexpected population or out-of-scope change.
- The misleading SD `.pdf` response was correctly retained and identified as an HTML landing/terms page, not falsely represented as a PDF.

## Remaining OPEN items

S07-01 through S07-12 remain OPEN at their assigned physical, firmware, carrier, footprint or system gates. This includes flight-harness retention/vibration/continuity, private ESC firmware identity, PWM/DShot waveforms, remote-module powered-off behavior, 4.75 V loaded-cable verification, assembled backfeed below 100 µA, AUX startup/insertion, final land patterns, USB operation, CAN topology/EMI, microSD timing/data integrity, GNSS carrier evidence and high-rate telemetry behavior.

All Stage 05 and Stage 06 physical-validation items remain OPEN. None is promoted to VERIFIED by this analytical closeout.

## Stage 08 release boundary

Stage 08 is authorized using `gpt-5.6-sol` with high reasoning. It is limited to schematic-wide review, symbol provenance/pin audits, footprint and connector drawing review, BOM-field/MPN/status consistency, netlist/ERC checks, reference/annotation cleanup and controlled rendering/visual inspection.

Stage 08 must preserve every frozen invariant, recommendation/open status and the sparse ESC boundary. It may not define the PCB outline or stack, place or route, create fabrication/assembly outputs, populate CAN2, restore `LIDAR_FC`, connect camera/lidar to the FC, alter the Stage 02 resource map, approve production, or begin Stage 09.

