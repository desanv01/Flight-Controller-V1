> Historical technical record. Names and private workstation/session references were neutralized for publication. Dates and assertions describe the recorded stage, not current physical qualification. See the current validation-status page for later checks.

# FC Drone FC Rev A - Stage 05 R16 control review

Date: 2026-09-09, Asia/Kuala_Lumpur  
Result: **VERIFIED R16 STOPPED STATE - STAGE 05 OPEN**  
Stage 06: **NOT AUTHORIZED**

## Outcome

Project control independently reviewed the R16 handoff, reran the calculation, model-audit and stopped-state verification scripts, and visually inspected the full and close-up power-sheet renders. The official encrypted TPS552892 PSpice package was recovered and integrity-checked, but the calculation workbook remained inaccessible and no compatible PSpice runtime was available. Official evidence still does not close the required switched-network dynamics, startup SOA, all-state leakage/backfeed, fail-low status, hot-loss, sensor-LDO or input-protection gates. Stopping before schematic capture or exact-part freeze was correct.

## Verified evidence

- R16 control SHA-256 matched task entry: `d2dcf5bf483b11270551d3e220b81fc31ddba42bffcbc133788bdc98ade8b1ae`.
- The R14 handoff was preserved byte-for-byte at `qa/stage05-power/history/FC_REV_A_STAGE_05_STOPPED_R14_2026-09-09.md`, SHA-256 `63d434a278cccdf7392cb4676704510fdf84fa2012c6f485f5e93536193c935a`.
- The canonical R16 handoff SHA-256 is `67bd50cb800e131aaa5546e072e603700868fedccd31f2c877891d757ef02990`.
- The official TI SLVME05 TPS552892 encrypted PSpice package was recovered as 252855 bytes, SHA-256 `b6e087f603ce774de0a6b2ec197d733b8e2723e0a3160ee7509142f5a658c525`; ZIP CRC and 23 extracted-member hashes passed.
- The official TPS552892 calculator page identifies V1.0, 2023-08-04, 238 K and published checksum `ff16420f6b2c639158584121a4ba6d3ce8707bc5388962cff67f8b404581862d`. The workbook download returned HTTP 403 and Chrome `ERR_BLOCKED_BY_CLIENT`; no workbook bytes or formulas were obtained and no barrier was bypassed.
- The supplied model project is a 5 V input, 9 V output, 1 A, 120 uF reference, not the FC 5 V/680 uF network. Its bundled aborted/convergence logs are vendor historical logs, not local simulation results.
- Independent reruns of `qa/stage05-power/correction_r16/calculations.py`, `audit_model.py` and `verify.py` passed at their stated arithmetic, static-audit and stopped-state scopes.
- The stopped-state verifier checked 99 entry files; only the authorized canonical handoff replacement changed. It reports 29 components, 88 nets, 54 retained ERC findings, zero new findings, zero PCB files, no Stage 05 capture and no Stage 06 work.
- Visual inspection of `power_full.png` and `power_closeup.png` confirms the power sheet remains the empty Stage 03 foundation with its original warnings. No circuit, symbol, footprint, test point or parent-sheet power connection was added.
- `hardware/FC_REV_A/sheets/02_power.kicad_sch` remains SHA-256 `df3a44d1c74c0a83a15320c8d035478d4498e8239660a2618ac2a086420b1500`.

## Decisive residual blockers

1. The official TPS552892 model has not been run for the FC network. A compatible PSpice runtime is absent, and the official workbook is inaccessible.
2. No official-model-supported common-corner proof covers VIN 4.72-5.5 V, local plus 680 uF capacitance, ESR, switch/harness impedance, 55/70 degC, near-unity operation, startup, steps, limiting, short, prebias, source removal, brownout and restart while guaranteeing the 4.75 V AUX boundary.
3. TPS25940/42 and other screened protection devices still lack sufficient source-backed startup transient SOA/Ztheta and guaranteed VIN=0/all-control-state leakage evidence. TPS259470 foldback does not close the approved full-capacitance/full-load startup envelope.
4. The strict below-100 uA POWER1 backfeed sum remains unprovable until guaranteed maxima exist for the converter, protection chain, status/control paths and every externally powered interface.
5. TPS3700 cannot simultaneously guarantee deassertion by 4.75 V and assertion at the present 4.842416 V minimum DC screen. A tighter monitor, improved headroom or explicit health-threshold policy is required.
6. Exact input-eFuse behavior, first-5-ms timing, reset/restart coordination, main-buck hot loss, TPS7A2033 reverse/PSRR/sequencing, exact passives/magnetics and EMI remain OPEN.
7. The Stage 04 `3V3_ANA` parent-hierarchy ERC finding remains OPEN because capture was correctly withheld.

## Candidate disposition

- `TPS552892`: remains the leading AUX-converter **CANDIDATE**, not approved for capture.
- `TPS25940L` / `TPS25942L`: latch-off **CANDIDATES**; current-window arithmetic is promising, but startup SOA and VIN=0 leakage remain OPEN.
- `TPS259470L`: lower-loss **CANDIDATE**, but low-voltage foldback and maximum leakage evidence remain OPEN.
- `TPS26630` plus external reverse FET: alternate **CANDIDATE** only; exact current accuracy, SOA, leakage and status remain OPEN.
- `MAX17613`: rejected for this chain because its loss/headroom evidence does not meet the approved boundary.
- `TPS3700`: monitor **CANDIDATE** only; current threshold and power-collapse behavior do not meet the complete fail-low contract.
- All exact converter, switch, eFuse, regulator, LDO, magnetic, capacitor, compensation, monitor and footprint choices remain CANDIDATE/OPEN.

## Required next authorization

The prepared `qa/stage05-power/correction_r16/manufacturer_questions_and_coupon.md` contains three separate packages. Project control recommends:

1. authorize installation and controlled use of PSpice for TI with the retained official SLVME05 project, plus another allowed attempt to obtain the exact official workbook;
2. authorize sending the prepared technical questions to the relevant manufacturers, without changing any approved envelope;
3. authorize detailed power-test-coupon design only if simulation and manufacturer responses still cannot close the mandatory guarantees. Coupon fabrication, ordering and production remain separate human decisions.

Software installation and external manufacturer communication require confirmation immediately before those actions. Until an approved evidence path closes every mandatory gate, Stage 05 remains OPEN and Stage 06 remains locked.
