> Historical technical record. Names and private workstation/session references were neutralized for publication. Dates and assertions describe the recorded stage, not current physical qualification. See the current validation-status page for later checks.

# FC Drone FC Rev A - Stage 05 R10 buck-boost evaluation control review

Date: 2026-09-08, Asia/Kuala_Lumpur  
Result: **VERIFIED ANALYSIS-ONLY STOP - STAGE 05 OPEN**  
Stage 06: **NOT AUTHORIZED**

## Outcome

Project control independently reviewed the R10 continuation handoff and reproduced its sensitivity model and stopped-state KiCad verification. The proposed synchronous 5.0 V buck-boost mechanism remains viable for further investigation, but no candidate chain has passed the complete Stage 05 evidence gate. Stopping before capture was correct.

## Verified evidence

- `python qa/stage05-power/correction_r10/sensitivity.py` and `report_sweeps.py` reproduced 1,136 conditional grid cases and the published report.
- `python qa/stage05-power/correction_r10/verify.py` returned `PASS - R10 stopped state only`.
- Ninety-three controlled entry files were checked. Only the authorized canonical Stage 05 handoff changed from its preserved R8 version.
- The KiCad design remains at the Stage 04 baseline: 29 netlisted components, 88 nets, 54 retained ERC findings, zero new ERC findings and zero PCB files.
- `hardware/FC_REV_A/sheets/02_power.kicad_sch` remains byte-identical to entry and visually remains the empty Stage 03 foundation sheet.
- Fifteen newly retained official-source PDFs passed their recorded byte-size and SHA-256 checks. Failed retrievals are explicitly marked and were not used as evidence.
- Stage 06 has not begun.

## Candidate disposition

- `TPS63070RNMR + TPS25940ARVCR` is the leading **CANDIDATE** screening chain, not an approved capture or BOM selection.
- `TPS552892RYQR + TPS25940ARVCR` remains a larger alternative requiring compensation and application-current work.
- `TPS259470ARPWR` offers a lower-loss output path but its startup foldback prevents use of the normal current-limit equation as a startup guarantee.
- `TPS63060DSCT` remains a comparison only because its available evidence does not establish sufficient worst-case current margin.
- Exact converter, switch, magnetics, passives, footprints and timing/status circuitry remain **OPEN/RECOMMENDATION** pending a complete gate.

## Unresolved evidence gates

1. **POWER1 edge/inrush:** the first-5-ms current requirement cannot be proven without a controlled source-edge definition and a qualified reset-safe sequencing circuit. A 220 nF pre-eFuse analysis capacitor needs at least a 1.412 us linear edge in the idealized zero-resistance model; a 2 us screening edge calculates 0.735 A including the model's 0.10 A reserve. These are assumptions, not source qualifications.
2. **POWER1 source behavior:** the pad-level 4.9-5.5 V contract remains authoritative. Any separate source-impedance limit must be tied to an actual source model and must not double-count voltage drop already included at the FC pads.
3. **AUX startup envelope:** a TPS25940 100 nF dV/dt example screens 680 uF effective total capacitance and 1 A startup load at 1.099 A, but actual accessory `I(V,t)`, constant-power behavior, transient SOA and ramp tolerance are not bounded.
4. **Thermal envelope:** no maximum board ambient or guaranteed converter efficiency/cooling model is approved. The reported ambient limits are sensitivity slices, not qualification.
5. **All-state behavior:** reverse leakage/backfeed, startup/hot-restart, fault timing, `AUX_OFF`, and the complete `PWR_STATUS` truth table are not proven for every powered/unpowered state.
6. **Remaining Stage 05 circuits:** input eFuse thresholds/thermal coordination, main regulator/passives, sensor-LDO PSRR/reverse-current behavior, analog filtering, ADC open-safe conditioning and connector qualification remain OPEN.

## Recommended next control decisions

- Preserve the first-5-ms limit, but define a measurable POWER1 source-edge contract and require a hardware-only reset-safe delay; do not count an ideal instantaneous connector step as a qualified source.
- Keep the authoritative voltage requirement at the FC pads; treat source impedance as qualification evidence for the selected UBEC/harness rather than a second independent drop allowance.
- Adopt an interim external AUX contract of no more than 680 uF effective total post-switch capacitance, no more than 1 A aggregate startup load, and compatibility with an approximately 34-53 ms 0-to-5 V ramp. Require Stage 07 to verify every selected module's startup `I(V,t)` and concurrency before population.
- Use 55 degC as the minimum continuous board-ambient design target, with 70 degC preferred screening and measured prototype thermal validation later. Stage 05 must use source-backed loss curves and transient thermal evidence rather than assuming 90% efficiency.
- Continue comparing both TPS25940 and TPS25947-class output protection only after all-state reverse-current and startup-SOA evidence is available. No capture is permitted while any approved gate remains unsupported.

These recommendations are not decisions until explicitly approved by the user. Stage 05 remains OPEN and Stage 06 remains locked.
