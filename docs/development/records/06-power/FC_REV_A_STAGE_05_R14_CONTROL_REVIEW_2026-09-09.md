> Historical technical record. Names and private workstation/session references were neutralized for publication. Dates and assertions describe the recorded stage, not current physical qualification. See the current validation-status page for later checks.

# FC Drone FC Rev A - Stage 05 R14 Path A control review

Date: 2026-09-09, Asia/Kuala_Lumpur  
Result: **VERIFIED PATH A STOPPED STATE - STAGE 05 OPEN**  
Stage 06: **NOT AUTHORIZED**

## Outcome

Project control independently reviewed the R14 Path A handoff, reproduced its power calculations, full loop sweep, reduced follow-through and candidate pin audit, reran native KiCad verification, and visually inspected the loop plot and power-sheet render. TPS552892 removes TPS63070's simple output-capacitance limit, and a slower compensation route is analytically plausible, but the complete pre-capture evidence gate remains unproven. Stopping without capture or part freeze was correct.

An asynchronous stale-message interpretation created an erroneous clarification artifact early in the task. Project control corrected it during execution. The task preserved that material under `qa/stage05-power/correction_r14/superseded_error/`; R14 remained authoritative and the approved envelopes were used for the actual Path A handoff.

## Verified evidence

- R14 control SHA-256 matched at task entry: `ea2e0666c13c059d55b196f88316f15040cd28e623a2fcd1762b2c3aec4b9f07`.
- The R12 handoff was preserved byte-for-byte at `qa/stage05-power/history/FC_REV_A_STAGE_05_STOPPED_R12_2026-09-08.md`, SHA-256 `26bdcaecfa6435256f03597be9f6d742dcb5c3943561f551d302c8b480f9ae4f`.
- Independent reruns of `power_calculations.py`, `loop_analysis.py`, `loop_followthrough.py`, `pin_audit.py` and `verify.py` passed at their stated analysis/stopped-state scopes.
- The broad loop analysis reproduced 3,456 cases for each of four compensation networks. None passed every broad corner.
- The narrower 480-case follow-through reproduced zero target misses for candidate D (680 ohm, 2.2 uF, 4.7 nF), including 160 full-680 uF cases, but its modeled additional dynamic droop is 71.96 mV versus the 50 mV allocation and the model omits several nonlinear/hot/controller bounds.
- Ninety-seven controlled entry files were checked. Only the authorized canonical Stage 05 handoff changed.
- Five newly retained official-source PDFs passed recorded byte-size and SHA-256 verification. The official TI calculation-tool page was identified, but the XLSX download returned HTTP 403 and was not used.
- The KiCad design remains at the Stage 04 baseline: 29 netlisted components, 88 nets, 54 retained ERC findings, zero new findings and zero PCB files.
- Visual inspection confirms `02_power.kicad_sch` remains the empty foundation sheet. No circuit, symbol, footprint, test point or parent-sheet power connection was added.
- Stage 06 has not begun.

## Candidate disposition

- `TPS552892RYQR`: remains the leading AUX-converter **CANDIDATE** for Path A. Its documented 10-1000 uF effective range contains the explored 702-768 uF combined capacitance, but scalar capacitance range is not a switched-network stability proof.
- Compensation D (680 ohm/2.2 uF/4.7 nF): analytical **CANDIDATE** only. It passes the reduced follow-through margins but misses the present dynamic-droop allocation and lacks a complete vendor/hot/nonlinear model.
- `TPS25940ARVCR` / latch-off variant: settled current-limit and startup-current arithmetic pass, but startup transient thermal/SOA, VIN=0 maximum leakage and fail-low fault semantics remain unproven.
- `TPS25942LRVCR`: credible active-limiting alternative with the same principal startup-SOA and VIN=0 evidence gaps.
- `TPS259470LRPWR`: lower loss and improved current-limit indication, but low-voltage foldback prevents the approved 680 uF/1 A startup proof; VIN=0 leakage remains typical rather than guaranteed.
- `TPS25944LRVCR`: rejected as the sole AUX limiter because it permits overload until its circuit-breaker timer expires instead of regulating within the required 1.10-1.50 A interval.

## Decisive residual blockers

1. No supported complete TPS552892 model covers the selected local capacitance, switch/harness, full 680 uF load, alternating near-unity operation, temperature corners and nonlinear startup/removal/fault states.
2. No compensation/passive implementation yet proves both robust margins and the external 4.75 V dynamic floor over all approved cases.
3. No compared output-protection device has source-backed startup transient Ztheta/SOA evidence on a justified thermal structure at 55/70 degC.
4. No compared chain provides a guaranteed all-state leakage sum below 100 uA into unpowered POWER1, including control/status pull-ups, converter, input eFuse and external-I/O paths.
5. Reset-safe first-window restraint, complete fail-low `PWR_STATUS` translation, fault timing, hot total losses, source coordination and exact passives remain unqualified.

## Recommended next evidence step

Keep every approved envelope unchanged. First attempt read-only recovery of TI's official TPS552892 calculation workbook through an interactive browser and broaden the official-source output-protection search beyond the currently screened TI devices. Do not contact a manufacturer, capture a circuit or relax a requirement during this step. If official material still cannot close the model/SOA/leakage gaps, return a concise manufacturer-question and/or dedicated power-test-coupon proposal for explicit human approval.

Stage 05 remains OPEN. Stage 06 and PCB work remain locked.
