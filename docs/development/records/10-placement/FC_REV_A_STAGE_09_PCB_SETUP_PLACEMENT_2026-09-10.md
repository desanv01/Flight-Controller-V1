> Historical technical record. Names and private workstation/session references were neutralized for publication. Dates and assertions describe the recorded stage, not current physical qualification. See the current validation-status page for later checks.

# FC FC Rev A — Stage 09 PCB setup and placement

Date: 2026-09-10. Status: **IMPLEMENTED — recommendation-grade placement study; verification passed within the unrouted scope. Project-control acceptance remains pending.**

This handoff does not release Stage 10, production parts, manufacture or flight. The R30 control state and retained status ledger were not edited. Stage 08 remains the accepted VERIFIED CONDITIONAL PASS; no electrical circuit was reopened or changed.

## Deliverables and verification

The canonical board is `hardware/FC_REV_A/FC_REV_A.kicad_pcb`. It contains a provisional 65 × 65 mm outline, four copper layers, 1.6 mm nominal thickness, 321 electrical footprints and four board-only mounting holes. All assignments resolve in `hardware/FC_REV_A/libraries/FC_REV_A_Local.pretty`; models are retained in the adjacent `FC_REV_A_Local.3dshapes` directory.

| Check | Result |
|---|---|
| Accepted schematic population | 326 components, unchanged |
| Complete net membership | 302 nets, identical to Stage 08 |
| Values, non-footprint properties, UUIDs, DNP | Unchanged |
| Schematic DNP / board DNP | 40 / 36; four DNP provisions intentionally have no footprint |
| Assigned / intentionally blank | 321 / 5 |
| Board pad-to-net comparison | All electrical pad assignments match the native schematic netlist |
| Copper layer count | Four |
| Tracks / vias / final copper zones | 0 / 0 / 0 |
| Routing/mechanical rule areas | Eight, all keepouts; no filled power or GND planes |
| KiCad 10.0.6 DRC | Zero violations; 499 expected unconnected items |
| Native DRC with schematic parity, after control-review correction | Zero ordinary field/attribute mismatches; only five controlled missing-footprint warnings |
| KiCad 10.0.6 ERC | Same 13 retained findings |
| Control state, ledger, local symbols, net registry | Preserved |

The exact checks and counts are in `qa/stage09-pcb/verification_summary.json`, `pad_audit.json`, `drc_final.json`, `erc_final.json` and `footprint_assignments.json`. `verify_stage09.py` compares every net member and every retained component property. It also verifies that removing only the Footprint property values makes every changed schematic sheet identical to its entry snapshot. Board pad nets and native DNP attributes are checked separately. DRC has no exclusions or suppressions; the 499 unrouted connections are retained, not waived as completed routing.

The unchanged ERC set comprises the VCAP power-output conflict, six isolated historical labels, the two AXC B4 ground-direction warnings, and the four retained hierarchy alias findings. The electrical parity check is stronger than relying on the unchanged count alone.

Visual review outputs are `qa/stage09-pcb/front.png`, `back.png`, `board_3d_models.png`, `board_3d_bottom.png`, and the nine individual numbered footprint views in `footprint_views/`. Native SVGs and renderer logs accompany them. The two internal copper-layer plots deliberately show no routed copper or filled plane. The additional small `.kicad_pcb` files under QA are footprint diagnostic canvases, not alternative assembly boards.

## Controlled footprint disposition

### Control-review parity correction — 2026-09-10

Independent native `pcb drc --schematic-parity` exposed metadata that the original pad/net/DNP verifier did not check. Its first report contained 219 parity warnings: 199 blank PCB Datasheet fields, 15 mismatched test-point BOM exclusion attributes, and five intentional missing footprints. The first correction was restricted to those exact reported references. The next native run exposed another 90 Datasheet mismatches; project control explicitly authorized that second, exact-reference pass. The initial report evidently capped or deferred those additional instances.

**Final correction totals: 289 PCB Datasheet fields copied from the authoritative schematic properties, plus TP1–TP15 BOM-exclusion attributes matched to the schematic.** The test points remain the same approved service-access pads; only their PCB `Exclude from bill of materials` attributes changed. No schematic file, other PCB property, value, footprint assignment, DNP attribute, UUID, net name, pad map, position, orientation, route, zone or mechanical geometry changed. The complete board text compares identically after removing only the authorized Datasheet text and BOM-attribute differences.

Final native results: **0 PCB-rule violations; 499 expected unrouted connections; 0 ordinary field/attribute parity mismatches; 5 controlled missing-footprint warnings.** Their exact disposition is:

| Missing reference | Retained disposition |
|---|---|
| C17, C18, Y2 | DNP, unspecified LSE provisions; intentionally footprintless |
| J1 | Intentionally footprintless sparse OpenESC boundary; no contacts/copper added |
| J2 | Optional `/CURR` / `ESC_CURR_DNP` boundary; DNP and intentionally footprintless |

`qa/stage09-pcb/parity_before.json` retains the initial report; `parity_after_first_pass.json` retains the newly exposed 90; `parity_correction.json` records all 304 metadata edits and before/after hashes. The final `drc_final.json` includes native schematic parity. The full deterministic verifier now asserts the corrected fields, test-point attributes, and exactly these five remaining missing footprints. All earlier checks still pass: 326 schematic components, 302 unchanged nets, 40 schematic DNP / 36 board DNP, zero tracks, zero vias and zero final copper zones. Eight keepout rule areas remain unchanged.

Existing renders are retained because only hidden Datasheet text and BOM attributes changed, and the non-metadata board content is byte-equivalent. No affected visible geometry requires regeneration. The evidence index, visual-review provenance and final hash manifest were refreshed. No manufacturing output was generated. This correction ends at the Stage 09 handoff; Stage 10 remains locked.

The accepted 281 nonblank assignments were localized from the installed KiCad 10 libraries with source-file hashes. Forty of the 45 entry blanks now have recommendation-grade assignments. Five remain blank by design: **J1, J2, Y2, C17 and C18**.

| References | Implemented treatment | Source / retained limitation |
|---|---|---|
| U2 | TI RPW0010 HotRod 2 × 2 mm, ten electrical pad numbers, compound corner lands and long pads 5/6 | TI drawing 4225183/A, 08/2019, TPS25947 pp. 72–74; no invented center EP |
| U5 | TI RYQ0021 HotRod 5 × 3 mm, 21 electrical pad numbers, five long power lands and segmented paste windows | TI 4226658/A, 04/2021, TPS552892 pp. 40–42; pin 21 remains EXTVCC and NC |
| U12 | TDK ICM-42688-P LGA14, 3 × 2.5 mm component-side orientation | DS-000347 v1.9 pp. 54–55 and AN-000393 v2.4; nominal 0.475 × 0.25 mm terminal-sized lands |
| U16 | Bosch BMP390 LGA10, 2 × 2 mm, no EP | BST-BMP390-DS002-07 rev. 1.7 p. 49; top-view pin 1 is upper right; vent datum retained |
| U17 | TI DDF0008 SOT-23-THIN-8 | TCA9416 DDF drawing pp. 26–28; not the unrelated DTM package |
| U39/U40/U41/U46/U49/U52/U56/U60 | TI DYA0002 two-pad pattern | TPD1E05U06 drawing 4224978/B, 09/2021, pp. 24–26 |
| J9 | Local USB4105-GF-A default 0.95 mm stake recommendation; 16 electrical contact identities plus S1–S4 | Supplied GCT B3 and retained official B4; full A/B identity preserved despite four shared physical power/ground lands |
| J12 | MEM2075-00-140-01-A, normally-open detect, two locating holes and four shell lands | GCT A1 component-side land drawing; numeric 1–8 map directly to drawing P1–P8, with CD and SH retained |
| Y1 | Localized Abracon ABM3B four-pad 5 × 3.2 mm pattern | Abracon Rev U; oscillator pins 1/3, grounded case pads 2/4; never substituted with a two-pad ABM3 |
| C1–C16, R1 | Provisional 0603 metric patterns | Generic captured components have no frozen production MPN. These are explicit package recommendations, not an assertion of exact-part or effective-capacitance qualification |
| TP1–TP7 | 1.0 mm exposed service pads | Recommendation-grade probe access; existing later-stage test-point footprints retained |
| J1/J2 | No footprint and no newly invented physical pads | Sparse ESC boundary, with optional current input separate and DNP |
| Y2/C17/C18 | No footprint | Unspecified LSE parts remain DNP; no speculative crystal package |

`stage09_footprints.py` and `stage09_footprint_parameters.json` are co-located with the library. The official KiCad library generator repository is retained at `qa/stage09-pcb/tools/kicad-library-tools`, commit `475bd27b9a521418c3732ff2ee5efea98525d2c7`. A dedicated virtual environment and dependency lock are retained. Custom geometry was generated with KicadModTree. `finish_geometry.py` applies the TI drawings' 0.05 mm rounded corners, the final mask setting, and the documented U6 fab-only outline adjustment.

U2/U5 must not acquire a conventional central grounded thermal pad. Their long electrical lands are part of the HotRod package's electrical and thermal structure. U5 pin 21 is EXTVCC; neither its pad number nor net has been repurposed. The TI stencil examples are represented as a prototype starting point, including the three-window long-pad pattern on U5. Stencil thickness, paste process, thermal copper and any later thermal vias remain an assembly/layout qualification item. U4 and U6 retain their actual numbered EP connections; no production vias were added.

All eight JST-GH connector footprints retain the installed `MP` mechanical land identity without adding an electrical signal or GND connection. Their electrical pin sets match the schematic. J9's S1–S4 pads all match the accepted USB_SHIELD net; the existing shield-to-GND circuit remains unchanged. The stock connector's A/B coincident power lands retain both required electrical identities and match the same respective nets.

## Source identity and provenance

Entry hashes and source copies are retained in `qa/stage09-pcb/entry_manifest.json`, `entry/`, and `hardware/FC_REV_A/docs/evidence/stage09-pcb/`. The supplied-source manifest records sizes, SHA-256 hashes and archive members.

* `USB4105 - Product Drawing.pdf`: 452,595 bytes; SHA-256 `aff194b6a5926126b9ec863396f0540dfc0aa908907bb5e646e59777f103541f`. This is B3, 24/02/23. The blank stake suffix means 0.95 ± 0.15 mm; `-060` and `-120` are distinct alternatives. The retained official drawing is B4, 2023-12-18. The prototype uses the unsuffixed recommendation already captured as USB4105-GF-A. No 060/120 catalog result silently changes that MPN. Actual procurement suffix and sample fit remain OPEN.
* `MEM2075-00-140-01A.pdf`: 262,654 bytes; SHA-256 `95ffcfa42a69fc6326429e06df6e4bc60b5b3413c5f192b6d11889af2cd1f828`. This is the six-page product specification, not the dimensioned land drawing. The retained GCT A1 drawing, dated 2020-09-10, controls geometry. The specification's filename does not override the drawing's ordering grid.
* `SM08B-SRSS-G-TB(LF)(SN).pdf`: 152,648 bytes; SHA-256 `f1ae56031598bddeca94cae278a3807cfd90ba330e9f835f8e277df8cd10878a`. The supplied catalog is geometry/context evidence only. It does not replace the native ESC connector identity.
* `OpenESC-30x30-rev3.4.zip`: 19,212,394 bytes; SHA-256 `a9cf0e3f0e84c78ac6b60a68b79d761cf84910aecb76184da6f00a3a22fd7ef8`. Its native board reports Rev3.3 and identifies `SM08B-SRSS-TB(LF)(SN)`. The native `hardware/4in1.kicad_pcb` hash is `683125806b93f808d9c5cc2e10956f470e8ec7e537db047b83ab7524e60463e2`. The archive-name/native-revision discrepancy remains visible; neither proves an as-built ESC identity or FC mounting compatibility.

Previously retained TI, TDK, Bosch, Abracon and JST official sources are reused by path and hash in the evidence index. PCBParts search responses dated 2026-09-10 are retained as sourcing evidence in `pcbparts_2026-09-10.json`. Catalog availability, alternative stake variants and unsuccessful sensor searches are not electrical substitutions, genuine-part proof or approval to purchase. Manufacturer drawings control land geometry.

## Mechanical and layer study

The four mounting centers are **(30,25), (50,25), (30,45), (50,45) mm** in the 65 × 65 mm local board coordinates. This is exactly 20 × 20 mm, deliberately independent of the ESC archive's mounting geometry. **2.2 mm NPTH holes and a 6 mm diameter fastener/tool clearance are assumptions for M2 hardware**, not a frozen mechanical contract. The MCU's body and lead geometry fit between these centers; the coarse square courtyard bounding box alone is not used to reject the corner mounting spaces. Final fastener, washer, vibration isolator, standoff height, chassis fit and tolerance verification remain OPEN.

The outline is a compact first study for this 326-component circuit and its external connectors, not a proven global minimum. It uses both sides and keeps actual connector mouths and locating holes on-board. Reducing it further requires a new placement/routing-density and harness-access review rather than assuming the 20 mm mounting pitch is the board size.

| Layer | Provisional role |
|---|---|
| L1 / F.Cu | Primary components, critical local signals and power loops |
| L2 / In1.Cu, named GND | Intended continuous common GND reference; unfilled at this stage |
| L3 / In2.Cu, named POWER_SLOW | Power distribution and lower-speed signals |
| L4 / B.Cu | Secondary components, signal access and service pads |

Only nominal total thickness is assigned. Dielectric thicknesses, copper weights, material, controlled impedance and fabricator capabilities remain OPEN; no invented stackup is presented as supplier-approved. The project stores provisional 0.15 mm minimum copper clearance/track constraints, 0.3 mm copper-to-edge clearance, 0.6/0.3 mm planning via geometry, 0.05 mm mask expansion and 0.05 mm mask web. All netclasses use the 0.15 mm provisional clearance compatible with the source-backed fine-pitch lands. Power width and USB differential parameters are planning placeholders, not ampacity or impedance calculations. USB's approximately 0.194 mm pad-to-locating-hole clearance is retained from the manufacturer-matched library geometry; the provisional minimum hole clearance is 0.15 mm. Fabricator/process acceptance remains OPEN.

## Placement rationale and review

The power section occupies the left side; U4/L1 and U5/L2 have separate placement neighborhoods. Input protection is near the reserved POWER1 area. Bypass, bootstrap, feedback and compensation components were prioritized before general interface packing. No switching-node copper, loop routing or thermal spreading is claimed complete. U5/L2 distance, actual switched-loop area and the R18 compensation/layout assumptions must be checked against the routed board in Stage 10 and measured later.

U1 is between the mounting centers. Its local supply capacitors are anchored to the corresponding physical supply pins, with Y1/C15/C16 beside the oscillator pins. C7/C8 remain only the approved shared-VCAP capacitors; no VCAP or oscillator test point exists. Some capacitors and support circuits use the back side, so layer transitions, inductance and short return paths remain a routing-review obligation.

U12 and U16 occupy the upper quiet region, separated from the converters and the tall XAL7070. Sensor decouplers have placement priority. The IMU's interior top surface has a no-trace/no-via/no-pour rule area. Both sensor backs have explicit component/pad/via keepouts extending 1 mm beyond their courtyards; thirteen initially conflicting backside components were relocated and DRC rechecked. Common L2 GND is not split. The IMU assembly guidance's surface-flatness and mask conditions, package stress, solder process and vibration sensitivity remain OPEN physical checks; the presence of a rule area is not a MEMS qualification.

The BMP390 vent datum is shown on the footprint. Its top must remain open to the later protected pressure path: no adhesive, coating, connector harness or enclosure member may cover it. Foam, airflow shielding, pressure response and thermal accuracy are not qualified here. Backside component exclusion also avoids a direct local heat/stress source under the package.

J3–J6 serve the retained RC/GPS/TELEM/COMPANION contracts. J7 is populated CAN1; J8 and its CAN2 evaluation circuitry remain native DNP. Connector access is toward the upper/right edges. J9 USB and J12 microSD mouths meet the lower edge; their reverse-side locating/through-hole envelopes are reserved. J10/J11 remain debug/service, with J11 DNP. Card push/lock/eject travel and cable latch/finger access require the final enclosure/harness model. No CM5 camera or lidar connector, power load or reassignment of PA0/PA1 was introduced.

**POWER1 remains physically OPEN.** The frozen schematic does not supply a released six-contact physical connector footprint. An 18 × 10 mm corner area is reserved; no speculative JST-GH/XH part or extra contact was added. The required two positive/two ground contacts, six-pin contract, 3 A continuous/4 A pulse capability, unequal sharing and loaded 4.9–5.5 V pad contract still govern. Connector capture/assignment must return to project control before that boundary can be physically completed.

**ESC physical termination remains OPEN.** J1 stays footprintless with only the accepted logical contacts 2 and 5–8. Positions 1/4 have no FC copper or conductor, and optional position 3 remains separate DNP J2. The reserved bench-boundary area does not create a cable release or a usable physical termination. The passive interposer and final signal-only FC contact arrangement still need controlled definition. No raw battery, ESC power or current-safety connection was introduced.

The initial DRC exposed a USB shell through-hole/backside U8 collision. The opposite-side connector reservations removed it. A later silk-only U6/U20 clearance was resolved by moving U6's outline graphics to F.Fab in both the controlled library and board. No copper geometry or electrical net was changed to conceal a placement collision.

## 3D and physical limitations

Installed KiCad models are localized with hashes. Seven custom patterns use explicitly simplified package/body envelopes; the unavailable installed U4 STEP was replaced with a clearly marked 3 × 3 × 1 mm body envelope. These envelopes do not contain exact leads, internal socket structure or mating parts. The USB model remains a generic family model and does not qualify the 0.95 mm stake tolerance. The final top/bottom renderer views were inspected for modeled-body interference, gross orientation, edge access and mounting-space conflicts; this is not a formal manufacturer-CAD collision proof.

No enclosure, ESC stack, exact standoff, harness bend model, USB plug or microSD card travel solid has been approved. Actual 3D fit, underside service access, tallest-component clearance, vibration and assembly fit remain OPEN. The board is not ready to fabricate merely because DRC and modeled-body review passed.

## Retained gates and reproduction

All earlier physical/sourcing/firmware/flight gates remain in force. Specifically retain Stage 05 stability, startup SOA, 55/70 °C thermal behavior, inrush, EMI, backfeed, sequencing and POWER1 qualification; S06-01/02 and S06-04–10; and S07-01–12. S06-03's incremental-versus-upstream budget interpretation remains resolved, while measured startup current remains OPEN. Footprint implementation advances the land-pattern work but does not close the broader assembly, genuine-sourcing, vent, MEMS, harness or electrical validation items.

The reproduction order is: `preflight.py` once only; `stage09_footprints.py`; `assign_footprints.py`; native netlist export; `models.py`; `add_missing_model.py`; `build_board.py`; `finalize_setup.py`; `clear_sensor_backs.py`; `finish_geometry.py`; native ERC/DRC exports; `verify_stage09.py`; then diagnostic renders. Use the retained KiCad Python for board scripts and the dedicated library-generator environment for footprint/CadQuery scripts. Run from the project root. Source PDFs and the ESC archive remain read-only evidence. `preflight.py` intentionally refuses to replace an existing entry manifest.

For the corrected metadata state, insert the native schematic-parity check and `correct_parity.py` before the final verifier: retain the initial report as `parity_before.json`, apply its exact-reference first pass, retain the next report as `parity_after_first_pass.json`, and apply `correct_parity.py --second-pass`. Run native DRC with `--schematic-parity` again into `drc_final.json`, then the full verifier and `package_evidence.py`. The correction scripts assert the recorded reference counts and refuse an unexpected edit population; they are not unrestricted field synchronization.

The native board and final hashed package are the review authority; the placement search is a functional-anchor/courtyard study, not an autorouter. No Gerbers, drill files, CPL, production BOM, fabrication order, manufacturer contact, routing, production vias or final zones were produced. **Stage 10 remains locked pending explicit project-control release.**

