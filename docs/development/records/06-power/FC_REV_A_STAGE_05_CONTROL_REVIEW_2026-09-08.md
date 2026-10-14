> Historical technical record. Names and private workstation/session references were neutralized for publication. Dates and assertions describe the recorded stage, not current physical qualification. See the current validation-status page for later checks.

# FC Drone FC Rev A - Stage 05 control review

Date: 2026-09-08, Asia/Kuala_Lumpur  
Review result: **VERIFIED STOPPED STATE - STAGE 05 OPEN, NOT PASSED**  
Stage 06: **NOT AUTHORIZED**

## Outcome

Project control reviewed the dedicated task handoff `FC_REV_A_STAGE_05_POWER_TREE_PROTECTION_MONITORING_2026-09-08.md`, its source archive, PCBParts snapshots, calculation script/output, native KiCad exports and baseline render. The task correctly stopped before schematic capture because the approved pre-capture gate was not satisfied. This review accepts the stopped-state evidence; it does not accept Stage 05 as complete and does not approve any production part.

## Independently verified

- Ten official TI PDFs are retained with official URLs, revisions, sizes and SHA-256 hashes under `hardware/FC_REV_A/docs/evidence/stage05-power/`.
- `python -X utf8 qa/stage05-power/calculations.py` reproduces the recorded screening values.
- `python -X utf8 qa/stage05-power/verify_stopped_state.py` returns `PASS - unchanged baseline only` with 66 unchanged entry files, 29 components, 88 nets, 54 retained ERC findings, zero PCB files, no power capture and no Stage 06 work.
- The verification harness compares the known KiCad `multiple_net_names` diagnostic by stable type, description and item descriptions because a repeated KiCad CLI run regenerated one internal label UUID while the canonical source files and diagnostic semantics remained unchanged. All other retained ERC findings remain UUID-strict.
- Visual inspection confirms `02_power.kicad_sch` is still the empty foundation sheet and contains no Stage 05 circuit.
- The Stage 04 core sheet and project-local symbol remain unchanged. No MCU resource, prohibited ESC/USB/CM5 power boundary, CAN2 DNP state or PCB state changed.

## Blocking findings

1. TPS25947 plus TPS2553 screens to approximately 4.675 V at the approved 4.9 V minimum input and 1 A auxiliary load before other losses, below the 4.75 V target.
2. TPS2553 with 1% programming resistance has no resistor interval that guarantees both at least 1.1 A and at most 1.25 A across the retained limit equations.
3. The full provisional rail allocations screen to approximately 2.235 A with assumed 90% buck efficiency and 20% margin, above the 2 A continuous POWER1 contract. Exact MCU, storage, CAN, indicator and external-module envelopes are not yet bounded.
4. TPS7A2033 DBV thermal/reverse-current behavior is not yet acceptable across the provisional load/temperature envelope.
5. Exact eFuse variant behavior, UVLO/OVLO reset behavior, inrush capacitance/load onset, all-power-state `PWR_STATUS` truth, reverse leakage, exact magnetics/capacitors and `VBAT_SENSE_3V3` source impedance remain OPEN.
6. JST XH is only a connector shortlist. The official original was not archived, and loaded-contact derating, crimp/wire, unequal sharing, temperature rise, pulse and vibration evidence remain OPEN.

## Control disposition

- ACCEPT the handoff as a VERIFIED stopped-state record.
- KEEP Stage 05 OPEN at its pre-capture gate.
- RETAIN all thirteen approved Stage 05 architecture policies and all existing OPEN/RECOMMENDATION/ASSUMPTION/DNP labels.
- Do not promote TPS25947, TPS62130A, TPS7A2033, TPS2553, TPS62902, TPS22950, JST XH or any passive to DECISION.
- Resume Stage 05 only after project control records the required operating/load envelopes and any approved target/mechanism changes.
- Do not begin Stage 06 until a completed power schematic, calculations, source/symbol audits, ERC/netlist checks, renders and final Stage 05 handoff are reviewed and explicitly accepted.

## Required next evidence or approval

- A bounded STM32H743 operating envelope: silicon revision assumption, maximum clock, enabled high-current blocks, workload and maximum design ambient/board temperature.
- Exact module/card current and inrush data, or enforceable aggregate budgets and allowed concurrency for microSD, CAN1, indicators and 5V_AUX ports.
- A lower-loss auxiliary path meeting at least 4.75 V at the permitted load, plus a reviewed current-limit tolerance window; otherwise an explicit target/mechanism change.
- Exact eFuse variant/fault/status policy and an all-power-state truth table.
- Sensor-rail load/thermal/PSRR/reverse-current envelope and exact package approach.
- POWER1 connector source archive and current/temperature/crimp/wire/vibration evidence.

The next implementation action is a Stage 05 continuation. Stage 06 remains locked.
