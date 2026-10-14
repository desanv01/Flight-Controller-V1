> Historical technical record. Names and private workstation/session references were neutralized for publication. Dates and assertions describe the recorded stage, not current physical qualification. See the current validation-status page for later checks.

# FC Drone FC Rev A — Stage 08 control review

Date: 2026-09-10  
Reviewed handoff: `FC_REV_A_STAGE_08_SCHEMATIC_REVIEW_SYMBOLS_FOOTPRINTS_2026-09-10.md`  
Dedicated task: `FC FC Rev A — Stage 08 Schematic and BOM Review`, thread `[PRIVATE_SESSION]`  
Disposition: **ACCEPTED — VERIFIED CONDITIONAL PASS at recommendation-grade schematic, symbol, footprint and BOM-review scope**

## 1. Control disposition

Project control accepts the Stage 08 handoff and its single source-backed correction. Stage 08 is complete at the authorized review-only scope. This acceptance does not approve production footprints, procurement, PCB geometry, placement, routing, fabrication, flight use or any physical-validation claim.

Stage 09 remains locked. A new explicit human authorization is required before any PCB setup or placement work.

## 2. Independent verification

Project control independently reran:

`python -X utf8 qa/stage08-review/stage08_audit.py`

The final rerun returned PASS and reproduced:

- KiCad 10.0.6;
- 326 components and 302 nets;
- 31 controlled local symbols and 376 passing source-pin checks;
- 281 assigned footprints, all resolving in the installed library and covering their corresponding symbol pin numbers;
- 45 blank footprints, all explicitly classified OPEN, DNP, generic-foundation or test-fixture matters;
- 122 grouped recommendation-grade BOM rows and 40 explicit DNP components;
- 13 retained and classified ERC findings, with no broad waiver added;
- exact preservation of the pre-Stage08 electrical topology and frozen resource ownership;
- exact preservation of the sparse J1 boundary, J2 current branch DNP, CAN2 DNP, USB no-power-path rule, PA0/PA1 reservation and absence of an FC camera/lidar path;
- zero PCB files and no Stage 09 work.

All nine full-sheet renders and all 15 targeted close-ups were inspected by project control. They are pixel-identical to the accepted Stage 07 visual baseline and show no clipping, broken hierarchy, missing DNP marking or out-of-scope topology.

## 3. Accepted Stage 08 correction

The review found that the installed KiCad candidate footprint `Connector_USB:USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal` numbers all four USB shell stakes `SH`, while the controlled GCT USB4105 symbol represents the source drawing's shell stakes as `S1` through `S4`. The candidate therefore could not map all physical symbol pins into PCB pads.

Project control accepts the conservative correction:

- blank J9's instance footprint in `hardware/FC_REV_A/sheets/07_usb_debug.kicad_sch`;
- blank the default footprint of `USB4105-GF-A` in `hardware/FC_REV_A/libraries/FC_REV_A_Local.kicad_sym`;
- retain the exact USB4105 stake-length suffix, matching pad-number strategy and controlled footprint as OPEN.

No pin, net, component value, MPN, status, annotation or visible schematic connection changed. The two file hashes and the authorized delta are recorded in `qa/stage08-review/verification/authorized_stage08_changes.json` and `canonical_file_audit.json`.

## 4. Accepted status boundaries

The following are VERIFIED only at Stage 08 review scope:

- hierarchy, reference and recommendation-grade BOM consistency;
- local-symbol source-pin coverage;
- installed candidate-footprint resolution and pad-number coverage;
- deterministic ERC/netlist/render reproduction;
- prohibited-path absence and frozen-resource preservation.

The following remain RECOMMENDATION, ASSUMPTION, DNP or OPEN as recorded in the handoff:

- exact/custom footprints for J1, J2, J9, J12, U2, U5, U12, U16, U17, the DYA ESD devices and other explicitly classified rows;
- USB4105 exact suffix and manufacturing land pattern;
- MEM2075 socket land pattern and insertion/keepout mechanics;
- MEMS orientation, keepout, vent, stress, vibration and assembly requirements;
- POWER1 connector/harness qualification;
- S07-01 through S07-12;
- all deferred Stage 04–06 electrical, thermal, EMI, startup, backfeed, sourcing and firmware validation;
- genuine production sourcing, lifecycle, assembly and prototype evidence.

No estimate or candidate package is promoted to production approval by this review.

## 5. Stage boundary

Stage 08 is complete. Stage 09 is not authorized by this record and was not started.

Before Stage 09 may begin, project control requires a new explicit release covering PCB outline constraints, mounting pattern, layer count/stackup, placement rules, controlled footprint implementation and the disposition of all 45 currently blank footprints. No approximate footprint may be silently substituted.

