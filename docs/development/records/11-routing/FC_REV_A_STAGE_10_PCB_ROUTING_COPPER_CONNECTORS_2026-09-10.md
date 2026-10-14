> Historical technical record. Names and private workstation/session references were neutralized for publication. Dates and assertions describe the recorded stage, not current physical qualification. See the current validation-status page for later checks.

# FC Rev A Stage 10 — PCB routing, copper and connectors

Date: 2026-09-10. Disposition: **VERIFIED STOPPED / CONTINUATION; STAGE 10 NOT COMPLETE — HOLD STAGE 11**.

The canonical board has 325 electrical footprints plus four mounting holes, 4880 track segments, 663 vias, 12 copper zones and 10 rule areas. Native connectivity reports **153 unconnected links**, comprising at least 153 links between physical pad islands; remaining differences are conductive-item islands. These are not hidden or waived.

Independent invariant checks: **25/25 pass**. Native DRC classification:

| Severity | Type | Count |
|---|---|---:|
| warning | track_dangling | 36 |
| warning | via_dangling | 33 |

Native DRC unconnected-list entries: 153; full native count above controls. Native parity findings: 3. ERC findings: 13.

Detailed findings, every physical pad island and route metrics are retained in qa/stage10-pcb/connectivity_accounting.md (private source record), qa/stage10-pcb/connectivity_accounting.json (private source record), qa/stage10-pcb/routing_metrics.json (private source record) and qa/stage10-pcb/drc_final.json (private source record).

## Exact implementation and retained decisions


## Scope and disposition

This is a VERIFIED STOPPED / CONTINUATION checkpoint of the Stage 10 implementation. Stage 10 is NOT complete while active routing remains open. It does not authorize manufacture, procurement, power-up or flight. Any remaining native unconnected links are design work, not waived findings. The final report's measured routing and DRC counts control the disposition; incomplete active circuits hold Stage 11 entry.

Stage 09 was the accepted conditional baseline. Stage 10 adds physical POWER1 and ESC connectors, the two authorized DNP LSE capacitor footprints, bounded placement refinements, common ground, power copper, USB pair geometry, routing and verification. Existing electrical topology, MCU resources, component values and DNP state are preserved. No broad DRC/ERC waiver was added. Root current control and historical handoffs are unchanged; independent main-control review is required.

## Mechanical and provisional stackup

Board edge centerline is exactly 65×65 mm. Four Ø2.2 mm NPTH at (30,25), (50,25), (30,45), (50,45) mm preserve the 20×20 mm pattern. Nominal total thickness is 1.6 mm; four copper layers remain F.Cu, In1.Cu named GND, In2.Cu named POWER_SLOW, and B.Cu. The geometric edge bounding box includes the 0.05 mm drawing stroke and is 65.05×65.05 mm; this is not a change to board size.

L1 carries primary components, local power copper and signal escapes. L2 is the common GND reference with no signal tracks. L3 carries the rail regions and routed signals, including the geometric USB pair trunks. L4 carries secondary components and signal access. **L3 USB impedance and its reference spacing are OPEN**: the layer name and pair spacing do not establish controlled impedance. No dielectric thickness/material/copper weight has been promoted to a fabricator-approved stackup. The power calculations retain provisional 35 µm copper and 25 µm via plating as assumptions only.

Planning constraints remain 0.15 mm minimum track/clearance, 0.3 mm edge clearance, 0.6/0.3 mm through vias, and the accepted mask settings. Ordinary routes target 0.2 mm; legal local necking reaches 0.15 mm. The power netclass targets 0.8 mm; broad rail pours and source-via banks provide intended distribution. Narrow power escapes require current-specific review and do not prove 3 A capability. USB trunks use 0.2 mm width and 0.2 mm nominal coupled gap. Pad escapes, bends, transitions, branches and actual stackup require SI verification.

Placement changes are listed exactly in `final_geometry_model_audit.json`. POWER1 faces outward at the top edge, first contact row y=9.6 mm. J_ESC_FC faces outward at the left edge at (3.7,48), 270°. Nearby R4, FB1, R36, R37, R62, C33 and TP9 were moved for connector clearance; C19/C20 moved only to y=16.25. C20 is the eFuse DVDT timing capacitor, not a supply bypass. U4 was rotated 180 degrees toward L1. L2 was moved to (17.4,37.8), rotated 90 degrees; C28/C29 were moved to the back at (8.3,33.2)/(12.3,33.2), with supporting feedback/decoupling placement refined. MAIN_SW and both AUX switch nets now connect through 0.8 mm load trunks with short 0.25 mm pad necks; 0.2 mm bootstrap branches are separate from those trunks. Y1 was rotated to 270 degrees and C15/C16 repositioned to remove crossed HSE paths. Both HSE nets now connect on F.Cu without vias. These changes resolve the earlier open switch/HSE geometry defects; thermal and loop-performance qualification remains open.

## Connector and harness definition

POWER1 header: Molex Micro-Fit 3.0 **43045-0600**, right-angle, shrouded, polarized, six factory contacts. Cable housing **43025-0600**, terminals **43030-0038**, 18 AWG stranded tinned copper. Circuit 1=+5 V A, 2=GND A, 3=+5 V B, 4=GND B. Both positive branches join the existing 5V_FC_IN_A native net; both grounds join common /GND. These aliases preserve the accepted topology.

Physical 5 and 6 have **no cable terminals, no electrical pads, no nets, no traces, no vias and no zone copper**. Their unavoidable header tails pass through unnumbered 1.02 mm NPTH clearance holes with all-layer exclusions. The 3 mm locator is also NPTH. This deliberate controlled footprint differs from the manufacturer's ordinary six-electrical-circuit land pattern and requires physical fit/retention review. No sense/status or VBAT contact has been introduced.

The manufacturer's 10.16 mm maximum first-row-to-edge requirement is met geometrically at 9.6 mm. Nominal mating height is 10.29 mm; recommended PCB thickness 1.57 mm versus nominal 1.6 mm remains a fit gate. Pin 1 marking, pad numbering, courtyard and cable-exit direction were reviewed. Equal-length positive branches and equal-length ground branches are recommended, ≤100 mm one-way; 150 mm is bench fallback only after voltage-drop testing. Design basis: 3 A continuous, 4 A for 100 ms. Balanced current sharing, single-lead faults, crimp pull force, contact heating, latch retention, bend radius and vibration are OPEN. Anchor cable jackets to the frame/bracket; do not load solder joints.

FC physical ESC connector **J_ESC_FC / JST SH SM05B-SRSS-TB** is separate from logical J1. FC housing recommendation **SHR-05V-S-B**; ESC native connector **SM08B-SRSS-TB(LF)(SN)** and housing **SHR-08V-S-B**. FC 1 GND→ESC 2; FC 2 M1→ESC 5; FC 3 M2→ESC 6; FC 4 M3→ESC 7; FC 5 M4→ESC 8. Only five conductors. ESC 1 +BATT, 3 /CURR and 4 NC have no FC harness conductors. J2 remains DNP and footprintless. The archive's SSH-003T-P0.2 versus catalog SSH-003T-P0.2-H contact suffix remains OPEN for exact procurement/crimp qualification. The supplied G-variant is family evidence, not an adopted substitute.

Native ESC board and documentation identify Rev 3.3 although the ZIP is named Rev3.4. The native J1 pin map controls. The native eSR datasheet link is a family mismatch; official eSH controls SH geometry. ESC has no BEC; its 30.5×30.5 mm / Ø4 mm mounting differs from FC 20×20 / Ø2.2 mm. Direct stacking is not qualified.

## Battery and UBEC basis

DOGCOM 1380 mAh 160C 6S1P: 22.2 V nominal, 25.2 V full, XT60 discharge, JST-XHR balance, approximately 36×39×80 mm and 221 g. Matek BEC12S-PRO is the primary recommendation: 9–55 V input, default 5.2 V output, 5 A continuous/9 A peak, no reverse-input protection. Holybro SKU 15034 at 5.2 V remains fallback only. These figures are design inputs, not assembled-system ratings.

Battery XT60 supplies ESC raw input separately. The BEC branch needs upstream reverse-polarity protection and fuse/eFuse, then regulated 5.2 V to POWER1 and the Stage 05 FC protection. Raw battery never enters POWER1 or an FC ESC connector. CM5 power and camera/lidar remain independent of the FC architecture.

## Footprint and model dispositions

| Item | Disposition |
|---|---|
| C17/C18 | Authorized local 0603 recommendation footprints assigned; values remain TBD DNP. No crystal/load-cap value invented. |
| Y2 | Still DNP and footprintless; source/value/implementation unresolved. |
| J1 | Sparse eight-position logical ESC boundary remains footprintless; separate audited five-way J_ESC_FC provides physical termination. |
| J2 | Current contact remains DNP and footprintless; no current conductor added. |
| J9 USB4105 | Stage 09 controlled pad geometry, S1–S4 stake mapping and model preserved. Official retained B4 drawing remains controlling over supplied older B3. |
| J12 MEM2075 | Controlled source-backed Stage 09 pad geometry, insertion reservation and envelope preserved; card access/removal and data integrity OPEN. |
| Existing custom/DYA footprints | Existing pad dimensions, drill, relative geometry and nets preserved; C28/C29 have explicitly audited F-to-B side changes. No similar-package substitution. |

All referenced model files resolve. Molex uses a simplified source-dimensional CadQuery envelope (body, tails, locator), **not a manufacturer STEP or detailed mating/latch model**. Existing envelope models remain envelopes. Top/bottom 3D views show no obvious component-body collision; this is a visual screening, not tolerance, enclosure, tool-access or mated-harness qualification. Mounting hardware and the external frame are not modeled as a validated assembly.

KLC footprint checks retain four F9.3 local-model-path style findings, two per new connector, because portable `${KIPRJMOD}` paths intentionally replace global library paths. New POWER1 symbol check is clean. ESC symbol retains one S4.4 error and one S4.2 warning: passive connector GND and physical-number-order pin layout. These are explicitly classified local connector-symbol conventions; they are not hidden by ERC waivers. The checker ran on a schema-header-only diagnostic copy because its parser requires a newer header; canonical symbol-library schema was preserved.

## Verification interpretation and remaining gates

Native export/parity and independent pad/net checks are authoritative. Three intentional footprintless parity findings remain J1, J2 and Y2. Named J_ESC_FC can produce an annotation advisory during export; it is the explicitly requested physical reference. All 40 schematic DNP states and all existing values, UUIDs, properties and net memberships are preserved. Board DNP count is 38 because J2 and Y2 have no footprints. CAN2, ESC current, VBAT_SENSE_3V3, PA0/PA1 reservation, retired LIDAR_FC, USB no-power, OpenRX, GNSS/telemetry boundaries and CM5/camera/lidar architecture remain unchanged.

The 13 baseline ERC findings remain classified: six isolated labels (AUX_UART TX/RX, retired LIDAR_FC TX/RX, BUZZER, VBAT_SENSE), one VCAP power-output finding, two AXC unused B4/GND warnings and four aliases. No new electrical ERC finding is accepted. Final native DRC counts, full connectivity groups and explicit unresolved routes are appended by the final handoff generator. A dangling escape or an unconnected active net is OPEN, not a successful connection. DNP-only islands are identified separately; forbidden current nets are deliberately not routed.

Power-region review is recommendation only: reworked converter switch trunks are connected, while local bypass/feedback/compensation returns, source-via sharing, remaining rail links, copper necks and thermal spreading need review against actual load and the final stackup. No DC-resistance or temperature qualification is inferred from pour area. USB/CAN/SDMMC/sensor routing metrics are geometric, and branch-length totals are not point-to-point timing results. Continuous GND is retained, but return-current paths and EMI require engineering/bench review.

Carry forward OPEN: UBEC ripple/transient/thermal/EMI; Stage 05 converter stability, startup SOA, brownout/prebias/source removal/restart; 55 °C continuous and 70 °C screening thermal tests; assembled-system backfeed <100 µA; POWER1/crimp/harness and ESC continuity/vibration/DShot waveforms; USB SI/ESD/DFU; CAN bus/ESD/termination; microSD removal/timing/data integrity; sensor orientation/vibration/venting/powered-off leakage; genuine-device/lifecycle/production sourcing; final stackup/impedance and process capability; manufacturing and flight qualification.

## Stage 11 entry and instructions

**Do not begin Stage 11 automatically.** Main control must independently verify this handoff and canonical hashes, explicitly accept or return Stage 10, and update root current control itself. Before any manufacturing-oriented transition, close every active unrouted connection and blocking DRC issue, verify converter/rail current paths and USB/CAN/SD/sensor constraints, resolve the required physical connector/stackup/source gates, and repeat native parity/ERC/DRC plus renders. DNP/retired omissions must remain explicitly classified.

When separately authorized, Stage 11 must start from the accepted canonical board and this exact audit package, preserve all frozen resources/topology/DNP states, resolve only its approved scope, and retain physical bench gates. This handoff grants no authority to generate Gerbers, drills or CPL, place orders, fabricate, claim production footprints, or approve flight. No Stage 11 work was performed here.


## Official source provenance


Retrieved/reviewed 2026-09-10. File hashes, sizes and page counts are in `hardware/FC_REV_A/docs/evidence/stage10-pcb/retained_pdf_manifest.json`; native ESC extraction is in `native_esc_connector_audit.json`. These are design recommendations, not physical qualification.

| Subject | Controlling evidence | Disposition |
|---|---|---|
| POWER1 header | Molex 43045-0600, SD-43045-001 PSD001 (historical source reference)(SN): 1 +BATT, 2 GND, 3 /CURR, 4 NC, 5–8 M1–M4. Only 2 and 5–8 enter the five-wire FC harness. Native eSR link is a family mismatch; eSH controls connector-family geometry. |
| USB | Supplied USB4105 B3 2023-02-24; retained Stage 09 official B4 2023-12-18 | Controlled Stage 09 J9 geometry and S1–S4 remain. Supplied older revision does not supersede B4. |
| microSD | Supplied MEM2075 specification; retained Stage 09 drawing A1 2020-09-10 | Controlled J12 geometry and models preserved. |
| Battery/BEC architecture | Dogcom 6S battery (historical source reference)(SN).pdf | 152648 | `f1ae56031598bddeca94cae278a3807cfd90ba330e9f835f8e277df8cd10878a` |
| USB4105 - Product Drawing.pdf | 452595 | `aff194b6a5926126b9ec863396f0540dfc0aa908907bb5e646e59777f103541f` |

OpenESC archive: 19,212,394 bytes; SHA-256 `a9cf0e3f0e84c78ac6b60a68b79d761cf84910aecb76184da6f00a3a22fd7ef8`. Native board member SHA-256 `683125806b93f808d9c5cc2e10956f470e8ec7e537db047b83ab7524e60463e2`. Originals were preserved.

## Files and reproducibility

Canonical modified files:
- hardware\FC_REV_A\FC_REV_A.kicad_pcb
- hardware\FC_REV_A\FC_REV_A.kicad_prl
- hardware\FC_REV_A\sheets\01_mcu_core.kicad_sch
- hardware\FC_REV_A\sheets\02_power.kicad_sch
- hardware\FC_REV_A\sheets\04_esc.kicad_sch
- hardware\FC_REV_A\libraries\FC_REV_A_Local.kicad_sym

New controlled artifacts: J_POWER1 and J_ESC_FC local footprints and models, connector symbols in the existing local symbol library, retained source PDFs and QA evidence. `final_design_manifest.json` records every canonical design/library/model/source file hash. `entry_manifest.json` and `entry_library_manifest.json` retain the entry-state hashes. Scripts and isolated routing trials are under `qa/stage10-pcb`; no trial is manufacturing output.

Native views: `qa/stage10-pcb/board_views/` has front/back, each copper layer, ground/power and POWER1/ESC/USB/sensor/CAN/SDMMC/MCU-clock/power-converter close-ups. `refined_3d_top.png` and `refined_3d_bottom.png` show the reviewed current top/bottom 3D placement, including converter and clock refinements. `harness_review.svg` and `.png` show both cable mappings and mechanical gates. `schematic_views/` contains the native schematic renders and connector crops.

The native headless Specctra import helper returned False. The audited SES route subset was decoded into native KiCad track/via objects using explicit um/10 resolution, layer names and the sole 0.6/0.3 mm via definition; footprints, schematic nets and zones were preserved. Native DRC and independent geometry/net audits then checked the result. Illegal router neck widths were raised to the board minimum and conflicting unlocked escape pieces removed; no board rule was weakened. Stalled task-local router processes were terminated without altering the last validated native board.

## Final region review and explicit blockers


**VERIFIED STOPPED / CONTINUATION: Stage 10 is not complete.** Native copper DRC is clean, but mandatory routing remains unfinished. The exact remaining net/pad groups and native endpoint pairs are in `continuation_state.json` and `connectivity_accounting.json`.

Reviewed the refreshed native planar front/back, common-ground and power/signal views and region close-ups, plus current refined top/bottom 3D placement. Back planar geometry uses board coordinates, not mirrored assembly coordinates.

| Region | Current finding |
|---|---|
| POWER1 / ESC | Controlled electrical/NPTH maps, exclusion geometry and outward placement remain verified. Cable mating, crimp, continuity, retention and vibration qualification remain open. |
| Power converters | U4 rotation and L2 relocation replace prior thin/long switch routes with 0.8 mm load trunks and short 0.25 mm pad necks. MAIN_SW, AUX_SW1/2 and bootstrap nets are connected. Bootstrap branches use 0.2 mm. Actual current, loop performance, thermal spreading and remaining rail connections require review. |
| Clock | Y1 rotation and C15/C16 repositioning close both HSE nets on F.Cu without vias. Oscillator startup/load/EMI still require verification. |
| USB | Both main and port DP/DM nets are connected. Main geometric pair length is DP 44.173 mm / DM 44.159 mm, two vias each. Actual impedance, connector branch tuning and SI/ESD/DFU remain open. |
| Ground / rails | Common L2 ground contains no signal tracks. L3 rail distribution regions coexist with signals. Remaining supply/ground islands and neck/current paths are explicitly listed, not waived. |
| Sensors / CAN / ESC | Frozen placements, resource maps and DNP states remain. Additional signal connections were closed; every still-open net is accounted for below. Return paths, noise, bus termination and bench verification remain open. |
| 3D | All 310 referenced models resolve; current top/bottom placement shows no obvious component-body overlap. Simplified models do not validate mated harness, mounting hardware, enclosure or tolerance stackup. |

SDMMC MCU-net state:

| Net | Pad islands |
|---|---:|
| /SDMMC1_CLK | 1 |
| /SDMMC1_CMD | 1 |
| /SDMMC1_D0 | 1 |
| /SDMMC1_D1 | 1 |
| /SDMMC1_D2 | 1 |
| /SDMMC1_D3 | 1 |

Native DRC: **0 copper errors; 153 unconnected links**. Dangling warnings: {'track_dangling': 36, 'via_dangling': 33}. Three intentional footprintless parity findings remain J1, J2 and Y2. All 25 invariant checks pass.

The general router completed and its clean result was accepted. Bounded local grid closures were then accepted only after native DRC. Trial narrow supply connections were removed. Unsuccessful SD layer-bridge trials were not promoted as completed connections. No power-up, manufacture or Stage 11 readiness is claimed.


## Preserved DNP references

C17, C18, C70, C83, C84, C86, C90, C91, C92, C93, C94, D1, J11, J2, J8, R103, R104, R105, R106, R107, R114, R116, R130, R27, R69, R70, R71, R98, TP5, U22, U23, U38, U41, U44, U48, U49, U50, U51, U52, Y2.

No Gerbers, drills, CPL, manufacturing release, orders or fabrication were produced. Root current control remains untouched. Stage 11 is held for independent review and resolution of active routing/layout gates.
