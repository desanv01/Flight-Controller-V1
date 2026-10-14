> Historical technical record. Names and private workstation/session references were neutralized for publication. Dates and assertions describe the recorded stage, not current physical qualification. See the current validation-status page for later checks.

# FC FC Rev A — Stage 08 Schematic, Symbol, Footprint and BOM Review

Date: 2026-09-10  
Stage: 08 — review-only schematic/BOM scope  
Disposition: **VERIFIED CONDITIONAL PASS — recommendation-grade review complete; one source-backed footprint-field correction applied; Stage 09 remains locked**

## 1. Executive disposition

The complete nine-sheet KiCad hierarchy passes Stage 08 at the authorized schematic-review scope. Fresh deterministic exports contain 326 components and 302 nets. The Stage 07 electrical topology is preserved, the frozen Stage 02 resource map is preserved, all 31 controlled local symbols and 376 audited physical pins pass their retained manufacturer-source audits, and the full-sheet and targeted-interface renders are pixel-identical to the accepted Stage 07 visual baseline.

One real footprint-field defect was found and corrected. J9's assigned KiCad USB4105 series footprint numbers all four shell stakes `SH`, while the controlled GCT symbol exposes physical shell pins `S1` through `S4`. That candidate could not map all symbol pins into PCB pads. Because the exact USB4105 shell-stake suffix and controlled production land pattern are still OPEN, the J9 instance footprint and the controlled symbol's default footprint were changed to blank. No pin, net, component, value, MPN, connectivity, annotation, status option, or visible schematic geometry changed.

After that correction, all 281 remaining assigned footprints resolve in the installed KiCad 10.0.6 libraries and their numbered pad sets cover every physical symbol pin. The 45 blank footprints are explicit OPEN, DNP, generic-foundation, or test-fixture matters; none is silently treated as production-ready.

This is not production approval, procurement approval, PCB approval, flight release, or physical validation. No `.kicad_pcb` exists. Stage 09 was not started.

## 2. Controlled inputs and baseline reproduction

The audit read and hashed the R28 control state, all Stage 01–07 handoffs/reviews named in the task, the execution and sourcing policies, `net_registry.csv`, and the retained status ledger. The exact list, byte counts, hashes, heading counts and controlled-state token counts are in `qa/stage08-review/governing_records_manifest.json`.

The historical Stage 07 correction closeout wrapper still seals the earlier R27 control-state hashes and therefore reports its expected `control state unchanged R27` assertion when run against R28. This is a historical-seal mismatch, not a schematic regression. The fresh Stage 07 interface exporter reproduced the accepted design before the Stage 08 correction at 326 components, 302 nets, 606 pin/net checks with no mismatches, the same 13 controlled ERC findings, frozen topology, and zero PCB files. The Stage 08 auditor then reran all exports and checks after the correction.

The accepted Stage 07 canonical hashes are recorded beside current hashes in `verification/canonical_file_audit.json`. Eight canonical schematic sheets and the root sheet remain byte-identical. Only the USB/debug child sheet and controlled local symbol library differ, exactly as authorized in Section 3.

## 3. Exact controlled changes

| File | Accepted Stage 07 SHA-256 | Stage 08 SHA-256 | Change |
|---|---|---|---|
| `hardware/FC_REV_A/sheets/07_usb_debug.kicad_sch` | `318b165f9a6d609a5782aa218c4172a90d344192b49463c9e072f109b286a342` | `f27be55f68d79aef8a2e13c96a891b908f7652053e85418b579f598d3e7750c6` | J9 footprint blanked; `Footprint_Status` records the `SH` versus `S1`–`S4` mismatch and exact-footprint requirement. |
| `hardware/FC_REV_A/libraries/FC_REV_A_Local.kicad_sym` | `b70e2acfecadf14e0af04ad701a553135d221ee00902641b13af7c84d0e1916d` | `24429fe5f12a74d88b9f00b5cbf25ef025c34ac61b850f226651bda2f68a26ca` | Default footprint for `USB4105-GF-A` blanked so the schematic copy matches the controlled library. |

The exact rationale and before/after file records are in `verification/authorized_stage08_changes.json`.

No change was made to:

- `FC_REV_A_CURRENT_CONTROL_STATE.md`;
- `hardware/FC_REV_A/docs/retained_status_ledger.md`;
- any pin name, pin number or electrical type;
- any wire, junction, label, hierarchical pin, net or sheet hierarchy;
- annotation or the 40 explicit DNP selections;
- any PCB, placement, routing, manufacturing, assembly or procurement artifact.

## 4. Manufacturer-source and hash audit

The consolidated evidence manifest contains 202 unique retained records. Of these, 194 currently resolve locally and match their recorded SHA-256 exactly. The eight explained exceptions are three Stage 05 URL-only calculation/reference downloads, three historical R27 control seals superseded by R28, and the two authorized Stage 08 J9 footprint-field edits above. There is no unexplained retained-source hash mismatch.

Key locally retained primary evidence includes:

| Device/family | Controlled source | Revision/date | Bytes | SHA-256 | Disposition |
|---|---|---:|---:|---|---|
| STM32H743VI | ST DS12110 / retained `stm32h743vi.pdf` | retained Stage 04 source | 7,075,281 | `f6e620179006c8c4d497b477ba065edc89c6dd9ac24d9debb3362910651f42ee` | VERIFIED source |
| ICM-42688-P | TDK DS-000347 | v1.9, 2024-11-12 | 1,402,996 | `9c6b57b0a2e45cf0251dd2423878573bd4da46e0cc2faa93dc558c28af51300a` | VERIFIED source |
| BMP390 | Bosch BST-BMP390-DS002-07 | rev. 1.7, March 2021 | 1,930,878 | `8dcf0f74449cb1627e865c7f24d328b76c204d8b9621091ede8c6869fb393e48` | VERIFIED source |
| TCA9416 | TI SCPS238A | August 2021 | 1,272,448 | `5e5e534585edfbd7315cefc246f7e70ac8406a0fc82823743161a74c595020a5` | VERIFIED source |
| GCT USB4105 | official drawing B4 | 2023-12-18 | 164,547 | `fb331fbabee8392ed2937ed757c1610cb0f174b84625147c0b580a18eea8c0e5` | VERIFIED drawing; exact suffix/footprint OPEN |
| GCT MEM2075 | official drawing A1 | 2020-09-10 | 144,177 | `9f1a621a3f7c649fd51f8ea49189e91ab2a4345eefcf7024382a072b782e90a3` | VERIFIED drawing; footprint OPEN |
| TI TPD4E05U06 | official datasheet | retained Stage 07 source | 2,801,466 | `c167cf1e72a5473a4d2c59b6a3c0251498701da05b7785919b9ceaae3b3e02c6` | VERIFIED source |

Current official product records were also checked: the [TDK ICM-42688-P product record](http[LOCAL_SOURCE] [Bosch BMP390 product record](http[LOCAL_SOURCE] [GCT USB4105 product record](http[LOCAL_SOURCE] [GCT USB4105 drawing](http[LOCAL_SOURCE] [GCT MEM2075 product record](http[LOCAL_SOURCE] [GCT MEM2075 drawing](http[LOCAL_SOURCE] and [TI TPD1E05U06 package record](http[LOCAL_SOURCE] These checks support package/drawing status only; they do not close sourcing, lifecycle, assembly or physical-test gates.

## 5. Controlled symbol audit

- Controlled local symbols: 31.
- Manufacturer/source-audited physical pins: 376.
- Failed pin-number, pin-name or pin-type checks: 0.
- Local symbols without a retained source-pin audit: 0.
- J1 remains a controlled sparse symbol with physical positions 2, 5, 6, 7 and 8 only.
- J1 positions 1 and 4 remain absent, not no-connect placeholders.
- J1 position 3 remains absent; the optional current contact is represented separately as DNP J2.
- USB4105 contact pins A/B and shell pins S1–S4 remain source-traceable. Only the incompatible footprint assignment was removed.

The pin-level evidence is in `verification/source_to_symbol_audit.csv`; the library inventory and aggregate result are in `verification/symbol_audit_summary.json`.

## 6. Footprint and package disposition

### 6.1 Audit totals

- Assigned footprints: 281; installed-library resolution PASS for all 281.
- Assigned-footprint symbol-pin/pad-number coverage: PASS for all 281.
- Blank footprints: 45; all 45 carry an explicit disposition.
- `VERIFIED CANDIDATE`: 241 populated records plus 32 DNP records.
- `RECOMMENDATION`: 8 test-point records.
- Official drawing verified but footprint OPEN: 11 device records plus two MEMS package records.
- Other explicit OPEN records: 29, including the sparse J1, DNP J2, corrected J9, J12, generic Stage 04 passives/test points/crystals, and unassigned exact-package devices.

`VERIFIED CANDIDATE` means the exact package/family name and pad-number set are consistent with the retained source and KiCad library. It does not approve placement, courtyard, solder mask, stencil, thermal-via strategy, assembly process or production release.

### 6.2 High-consequence results

| Item | Stage 08 disposition |
|---|---|
| U1 STM32H743VIT6 | KiCad LQFP-100 14 × 14 mm, 0.5 mm pitch candidate and 100-pad numbering VERIFIED CANDIDATE; placement/escape/assembly remain Stage 09. |
| U2 TPS259470LRPWR | TI RPW0010A asymmetric VQFN-HR drawing verified; no exact installed candidate found; footprint remains blank/OPEN. |
| U5 TPS552892RYQR | TI RYQ0021A land/stencil guidance verified; no exact installed candidate found; footprint remains blank/OPEN. |
| U6 TPS25940LRVCR | Installed Texas RVC0020A candidate resolves and covers all symbol pins; thermal-via/stencil/board validation remains OPEN. |
| U12 ICM-42688-P | Official package drawing verified; exact controlled land pattern, orientation, MEMS keepout and assembly constraints remain OPEN. |
| U16 BMP390 | Official 10-pin 2 × 2 mm LGA drawing/landing guidance verified; exact footprint, vent/port keepout and assembly constraints remain OPEN. |
| U17 TCA9416DDFR | Exact KiCad DDF0008A/SOT-8-thin candidate exists, but remains deliberately unassigned pending Stage 09 release. |
| U21/U23/U26/U29/U32/U35/U43/U53/U58/U61/U62 | TPD4E05U06 DQA 10-pad USON family and pin coverage verified as candidates; line routing, ground return, mask/paste and assembly remain OPEN. |
| U39/U40/U41/U46/U49/U52/U56/U60 | TI DYA0002A drawing verified. Generic KiCad `D_SOD-523` geometry is not the authoritative DYA land pattern; footprints remain blank/OPEN. |
| J1 | Intentionally blank. It must never receive an ordinary contiguous 8-pad JST SH footprint. Exact FC-side service/interposer termination remains OPEN. |
| J2 | Separate single optional `/CURR` service contact, wholly DNP and intentionally blank; no fictitious one-position connector selected. |
| J3–J8, J10–J11 | JST GH BMxxB-GHS-TBT family/pitch/contact numbering candidates verified; mating-face versus wire-entry view, exact mate/contact, harness, retention and loaded-voltage qualification remain OPEN. J8 and J11 remain DNP. |
| J9 | Existing KiCad series candidate REJECTED for assignment because footprint shell pads `SH` do not cover symbol pins `S1`–`S4`. Exact stake-length suffix and matching custom/controlled footprint remain OPEN. |
| J12 MEM2075-00-140-01-A | Official A1 component-side layout confirms contacts 1–8, normally-open card detect, shell/retention pads and keepouts. No exact controlled footprint is assigned; remains OPEN. |

The component-level disposition is in `verification/symbol_to_footprint_audit.csv`; assigned pad-map evidence is in `verification/assigned_footprint_resolution.csv`.

## 7. Connector/socket audit

- J1 contract is exactly positions `2=GND`, `5=M1`, `6=M2`, `7=M3`, `8=M4`; no other J1 positions exist.
- J2 remains separate, DNP, and connected only to the retained optional current branch; `/CURR` is not a safety input.
- ESC-side recommendation remains `SM08B-SRSS-TB` with `SHR-08V-S-B`; exact crimp terminal suffix, wire, applicator, keying proof and flight harness remain OPEN.
- JST GH candidates preserve circuit-1 numbering at the FC header. Separate housing wire-entry views must not be mirrored into the PCB view.
- USB is self-powered/data-only at the FC boundary. VBUS reaches only the sense/protection path; there is no VBUS-to-FC-rail power path.
- microSD uses exact source pin numbering and an explicit normally-open card-detect contact; socket land pattern remains OPEN.

The per-connector record is `verification/connector_socket_audit.csv`.

## 8. BOM and metadata audit

The BOM was regenerated from the current schematic netlist; no hand-maintained purchasing list was substituted.

- Components / unique references: 326 / 326.
- Grouped recommendation-grade BOM rows: 122.
- Explicit DNP components: 40.
- Excluded from BOM: 0.
- Excluded from board: 0.
- Blank footprints: 45 / 45 with explicit disposition.
- Blank MPN: 29; blank manufacturer: 38; blank datasheet: 35. Every blank is attached to a generic-foundation, OPEN, DNP or test-fixture record; no ordinary metadata omission requires another schematic edit.
- Duplicate references: 0.
- Conflicting exact MPN/footprint/status groups: 0.

All DNP references remain visible in design and BOM data: `C17, C18, C70, C83, C84, C86, C90, C91, C92, C93, C94, D1, J2, J8, J11, R27, R69, R70, R71, R98, R103, R104, R105, R106, R107, R114, R116, R130, TP5, U22, U23, U38, U41, U44, U48, U49, U50, U51, U52, Y2`.

The authoritative review outputs are `verification/complete_bom_audit.csv`, `verification/grouped_recommendation_bom.csv`, and `verification/bom_field_summary.json`.

## 9. ERC disposition

Fresh KiCad 10.0.6 ERC reports the same 13 accepted semantic findings after correction:

- Six `isolated_pin_label` warnings: `AUX_UART_RX`, `AUX_UART_TX`, `BUZZER`, `LIDAR_FC_TX`, `LIDAR_FC_RX`, and `VBAT_SENSE_3V3`. These are frozen one-ended reservations; no Stage 08 consumer is authorized.
- One `pin_to_pin` error: U1 VCAP pins 48 and 73 are both modeled power outputs on the same official VCAP capacitor node. Retain; this is not a short between independent rails.
- Two `pin_to_pin` warnings: U13 and U19 unused mode-dependent AXC B4 channels are intentionally tied to GND while their physical pins remain typed bidirectional.
- Three `multiple_net_names` warnings involving `3V3_REF` and `3V3_MAIN`: retain the controlled reference/sense alias; there is no independent regulator or power path.
- One `multiple_net_names` warning involving `5V_FC_IN_A` and `5V_FC_IN`: retain distinct POWER1 contact traceability where the two positive contacts intentionally join.

No ERC waiver was added. The machine-readable per-finding disposition is `verification/erc_disposition.json`.

## 10. Netlist, resource and prohibited-path audit

All of the following pass:

- 326 components, 302 nets, unique references and frozen pre-Stage08 pin topology.
- PD12–PD15 remain M1–M4 on TIM4; J1 positions 5–8 map in order.
- CAN1 remains populated; the entire CAN2 evaluation group remains DNP.
- PA0/PA1 remain reserved with only one-ended lidar labels; no active FC lidar circuit exists.
- Camera and lidar remain separately powered CM5 peripherals; no camera net or raw-battery net exists on the FC.
- USB VBUS does not power `3V3_MAIN`, `5V_AUX` or the FC input rail.
- J2 and its current-monitor branch remain wholly DNP.
- No raw battery, PCB, layout, fabrication, assembly or manufacturing file was introduced.

The exported netlists and focused rail membership are in `verification/netlist.xml`, `verification/netlist.kicadsexpr`, and `verification/rail_membership.json`.

## 11. Rendering and visual inspection

KiCad exported a fresh nine-page PDF and nine SVG sheets. All nine full-page PNGs and 15 targeted closeups were freshly rendered using the same matrices and crop boxes as the accepted Stage 07 verification set. All 24 image hashes are pixel-identical to the accepted baseline.

Manual inspection found no clipping, overlapping component labels, unreadable critical annotations, missing DNP crosses, broken hierarchy boundary, or unexpected visible topology change. The review sheets are `verification/all_sheets_contact.png` and `verification/targeted_closeups_contact.png`; the hash comparison and crop register are `verification/visual_equivalence.json` and `verification/visual_review.json`.

## 12. Remaining controlled status

### VERIFIED at Stage 08 scope

- Nine-sheet hierarchy, 326-component/302-net topology and Stage 02 resource ownership.
- Thirty-one local symbols and 376 retained manufacturer-source pin checks.
- All 281 assigned footprint names resolve and cover corresponding symbol pin numbers.
- BOM/reference/DNP/status consistency at recommendation-grade schematic scope.
- Exact J1/J2 sparse boundary and prohibited-path absence.
- Fresh ERC/netlist/PDF/SVG/PNG reproduction.
- J9 incompatible footprint assignment removed without electrical change.

### RECOMMENDATION / CANDIDATE only

- All populated ICs, passives, magnetics, connectors and ESD devices remain recommendation-grade until their assigned physical and production gates pass.
- LQFP100, RVC0020A, DDF0008A, JST GH, USB4105 series geometry, MEM2075 geometry, DQA and other installed/library package matches are evidence for candidate selection, not production-footprint approval.
- ESC-side JST SH header/housing and the Stage 07 five-conductor bench harness remain recommendations only.

### ASSUMPTION retained

- Stage 05 source edge, 680 µF post-switch capacitance envelope, 55/70 °C screens and corrected load buckets remain analytical contracts, not measured production facts.
- First-bench ESC cable remains no more than 150 mm; external UART/I2C harnesses no more than 300 mm; initial CAN harness no more than 1 m.
- OpenRX remains budgeted up to 0.5 A pending measurement; camera and lidar remain zero FC-rail load because they are separate CM5 peripherals.
- Remote-own-rail pull-ups, off-state leakage allocations, HSE stray capacitance and POWER1 contact sharing remain assumptions pending their recorded tests.

### OPEN

- Exact controlled/custom footprints for J1, J2, J9, J12, U2, U5, U12, U16, U17, the DYA ESD parts, early generic core passives/test points/crystals, and any other row marked OPEN in the footprint audit.
- USB4105 exact 060/095/120 shell-stake suffix, pad numbering strategy, through-hole process, keepout, paste/mask and assembly drawing.
- MEM2075 pad geometry, keepout, card insertion envelope, detect mechanics and assembly drawing.
- MEMS orientation, keepout, vent/port, stress, reflow, vibration and acoustic/pressure effects.
- POWER1 exact connector/MPN, current derating, unequal sharing, wire/crimp, loaded drop, temperature rise and vibration retention.
- All Stage 04–06 physical, electrical, thermal, EMI, startup, backfeed, sourcing and firmware validation items.
- S07-01 through S07-12 at their assigned harness, private-firmware, waveform, carrier, electrical, footprint, USB, CAN, microSD and system-test gates.
- Final genuine-production sourcing/lifecycle/availability evidence and supplier authorization.

### DNP retained

- LSE population, SWO test option, optional current-monitor branch, CAN2 evaluation path, optional port-power/reference paths, optional PPS/BOOT/status/termination choices and every other DNP reference listed in Section 8 remain DNP. Nothing in Stage 08 authorizes population.

## 13. Human approvals still required

1. Project control must explicitly accept this conditional Stage 08 handoff and the two-file J9 footprint-field correction.
2. Project control must explicitly authorize Stage 09; Stage 08 completion alone does not start it.
3. Before placement, a human reviewer must approve every exact custom/controlled footprint still OPEN, including J1/J2/J9/J12 and the power/MEMS/DYA devices, against component-side manufacturer drawings and assembly constraints.
4. Any proposal to populate CAN2, add an FC camera/lidar path, alter the frozen resource map, change DNP policy, change power requirements, order parts, fabricate hardware or claim flight/production readiness requires separate explicit authority.

## 14. Exact Stage 09 entry criteria

Stage 09 may begin only after all of the following are true:

1. An authorized human reviewer accepts this handoff as a Stage 08 **VERIFIED CONDITIONAL PASS**.
2. The reviewer explicitly accepts the J9 candidate rejection and the resulting blank footprint/default.
3. The exact footprint worklist is approved for controlled implementation or remains explicitly blocked; no approximate footprint may be silently substituted.
4. The 13 ERC findings, 40 DNP components, 45 blank footprints, and all carried OPEN/ASSUMPTION items are acknowledged without false closure.
5. Stage 09 receives a new explicit scope release. Until then there is no authority to define board outline/stackup, place, route, generate fabrication/assembly outputs, procure, fabricate or start physical work.

**Stop here. Stage 09 remains locked and was not started.**

## 15. Verification package

Primary Stage 08 artifacts are under `qa/stage08-review/verification/`:

- `stage08_summary.json` — top-level deterministic result and invariant checks;
- `authorized_stage08_changes.json` and `canonical_file_audit.json` — exact controlled deltas;
- `complete_bom_audit.csv`, `grouped_recommendation_bom.csv`, `bom_field_summary.json`;
- `source_manifest.csv`, `source_manifest_summary.json`, `source_to_symbol_audit.csv`, `symbol_audit_summary.json`;
- `symbol_to_footprint_audit.csv`, `assigned_footprint_resolution.csv`, `connector_socket_audit.csv`;
- `erc.json`, `erc_disposition.json`, `netlist.xml`, `netlist.kicadsexpr`, `rail_membership.json`;
- `schematic.pdf`, `svg/`, nine full-page PNGs, 15 targeted closeups, two contact sheets, `visual_equivalence.json`, and `visual_review.json`;
- `commands.json` — exact KiCad CLI command results.

The deterministic generator is `qa/stage08-review/stage08_audit.py`.
