> Historical technical record. Names and private workstation/session references were neutralized for publication. Dates and assertions describe the recorded stage, not current physical qualification. See the current validation-status page for later checks.

# FC Drone FC Rev A — Stage 09 control review

Date: 2026-09-10  
Reviewed handoff: `FC_REV_A_STAGE_09_PCB_SETUP_PLACEMENT_2026-09-10.md`  
Dedicated task: `FC FC Rev A — Stage 09 PCB Setup and Placement`, thread `[PRIVATE_SESSION]`  
Disposition: **VERIFIED CONDITIONAL PASS — recommendation-grade PCB setup, controlled footprints, provisional geometry and placement**

## Project-control decision

Stage 09 is accepted within its authorized, unrouted scope. The canonical PCB now provides a controlled basis for a later routing stage, but it is not a production, procurement, fabrication, assembly or flight release.

Stage 08 remains accepted. No electrical topology, value, net name, MCU resource, DNP decision or prior-stage circuit was reopened. Stage 10 remains locked pending a new explicit project-control authorization.

## Independently verified result

Project control reran `qa/stage09-pcb/verify_stage09.py` with the KiCad 10.0.6 Python runtime and reran native `kicad-cli pcb drc --schematic-parity` into `qa/stage09-control/drc_control_final.json`.

The independent result is:

- 326 schematic components and 302 nets, unchanged from Stage 08;
- 321 electrical PCB footprints plus four board-only mounting holes;
- all PCB electrical pads match the accepted schematic netlist;
- 40 schematic DNP items and 36 board DNP footprints, with the difference fully explained by intentional footprintless provisions;
- four copper layers and nominal 1.6 mm prototype thickness;
- four 2.2 mm NPTH mounting holes on exact 20 mm × 20 mm centers;
- eight mechanical/routing keepout rule areas;
- zero tracks, zero vias and zero final copper zones;
- zero PCB-rule violations;
- 499 expected unconnected items because routing is outside Stage 09;
- the same 13 classified schematic ERC findings;
- zero ordinary schematic-to-PCB field or attribute mismatches;
- exactly five controlled missing-footprint warnings: C17, C18, Y2, J1 and J2.

The recurring KiCad HKCU registry-access messages are the previously controlled local-environment diagnostic. KiCad completed the checks, returned a valid report and recorded the results above; the warning did not alter the PCB or invalidate the DRC result.

## Control-review correction

The dedicated task's original net/pad/DNP verifier passed, but project control additionally enabled KiCad's native schematic-parity check. The first native report exposed 199 blank PCB Datasheet fields, 15 test-point BOM-attribute mismatches and five intentional missing footprints. After correcting those exact metadata references, KiCad revealed another 90 Datasheet-field mismatches that had not appeared in its initial report.

The existing Stage 09 task corrected both exact-reference sets. In total:

- 289 PCB Datasheet fields now match the authoritative schematic properties;
- TP1–TP15 PCB `Exclude from bill of materials` attributes now match the schematic;
- no schematic file, geometry, position, orientation, UUID, value, footprint assignment, DNP state, net, pad map, route, zone or keepout changed;
- final native parity contains only the five intentional footprintless references.

The before/after hashes, both native reports and all 304 metadata edits are retained in `qa/stage09-pcb/parity_correction.json`, `parity_before.json` and `parity_after_first_pass.json`. The deterministic verifier now asserts the corrected metadata and the exact five-warning disposition.

## Geometry, placement and visual review

The accepted prototype study uses a provisional 65 mm × 65 mm outline and a four-layer role assignment:

- L1: primary components, signals and local power loops;
- L2: intended continuous common ground reference;
- L3: power distribution and lower-speed signals;
- L4: secondary components and signal/service access.

This is a recommendation, not a manufacturer-approved stackup. Dielectrics, copper weights, impedance, material and fabrication capability remain OPEN.

Project control inspected the front, back, top-3D, bottom-3D and controlled-footprint gallery outputs. The study is visually coherent at recommendation-grade scope:

- USB-C and microSD entry/ejection directions reach the lower edge;
- external connectors are placed along accessible edges;
- the STM32H743 is central and its decoupling/clock neighborhood is compact;
- power-entry and converter regions are grouped on the left;
- the ICM-42688-P and BMP390 occupy the upper quiet region away from the main switching cluster;
- IMU and barometer underside exclusions are clear after thirteen recorded relocations;
- the BMP390 vent datum and IMU no-trace/no-via/no-pour intent remain visible;
- the initial USB backside collision and U6/U20 silkscreen-only overlap were corrected without changing connectivity.

The custom/unavailable 3D bodies are explicitly simplified envelopes. Final mating-part sweeps, enclosure fit, standoff stack, assembly access, thermal clearance and vibration suitability remain OPEN.

## Controlled footprint disposition

Forty of the 45 Stage 08 blank-footprint entries now have source-backed recommendation-grade assignments. The controlled J9 USB4105, J12 MEM2075, TI RPW/RYQ/DDF/DYA packages, ICM-42688-P, BMP390 and other required patterns passed pad-map and source audits.

The five remaining blank references are intentional:

- C17, C18 and Y2: LSE provisions remain DNP and no speculative package is assigned;
- J1: the sparse OpenESC logical boundary remains footprintless; positions 1 and 4 have no FC contact or copper;
- J2: optional `/CURR` / `ESC_CURR_DNP` remains DNP and footprintless.

The native ESC evidence remains identified as `SM08B-SRSS-TB(LF)(SN)`. The supplied G-version catalog is geometry-family evidence only and was not substituted.

## Retained OPEN items

This acceptance does not close:

- the physical POWER1 connector, mate, loaded-contact derating, crimp/wire system, unequal sharing, voltage drop, temperature rise or vibration qualification;
- the final FC-to-ESC harness/interposer termination, continuity and flight release;
- manufacturer-selected stackup, impedance, copper weights, material or board capability;
- production footprint, stencil, paste, thermal-via, assembly-process or exact 3D-body approval;
- enclosure, USB-plug, microSD-card, harness-bend, standoff and ESC-stack mechanical fit;
- Stage 05 stability, startup SOA, thermal, EMI, transient, sequencing, backfeed and source qualification;
- S06-01, S06-02 and S06-04 through S06-10;
- S07-01 through S07-12;
- all later routing, plane, signal-integrity, thermal, manufacturing and prototype-test gates.

These remain mandatory at their assigned later gates and must not be relabelled VERIFIED.

## Stage 10 entry criteria

Stage 10 requires a new explicit authorization. Its release must define the recommendation-grade routing and copper scope, including continuous L2 ground intent, power/current-path handling, USB differential-pair treatment, sensor/oscillator constraints, via and return-path policy, zone policy and post-route DRC/visual verification.

Before Stage 10 is released, project control must also state whether POWER1 and the sparse ESC boundary are to remain intentionally unrouted/footprintless in the routing study or provide separately approved physical termination definitions. No speculative connector may be introduced to make routing appear complete.

Stage 10 must not generate manufacturing outputs or begin Stage 11 unless separately authorized.

## Control-state action

Update `FC_REV_A_CURRENT_CONTROL_STATE.md` to revision R31 with Stage 09 as the latest completed stage and no active stage. Preserve all deferred OPEN items. Keep Stage 10, manufacturing, procurement, fabrication and flight approval locked.
