> Historical technical record. Names and private workstation/session references were neutralized for publication. Dates and assertions describe the recorded stage, not current physical qualification. See the current validation-status page for later checks.

# FC Drone FC Rev A - Stage 05 R8 correction control review

Date: 2026-09-08, Asia/Kuala_Lumpur  
Result: **VERIFIED SECOND STOPPED STATE - STAGE 05 OPEN**  
Stage 06: **NOT AUTHORIZED**

## Outcome

Project control independently reviewed the R8 correction handoff and reproduced its calculations and unchanged-KiCad verification. The corrected load buckets close the earlier allocation arithmetic, but no screened AUX pass-through combination establishes both the retained 4.75 V minimum and the approved guaranteed current-limit window. Stopping before capture was correct.

## Verified evidence

- R8 control hash matched at task entry and remained unchanged during the continuation.
- The R6 stopped handoff was preserved with its required SHA-256.
- Eighteen official TI PDFs are now retained across the Stage 05 evidence package; eight were added during R8 screening.
- `python -X utf8 qa/stage05-power/correction_r8/calculations.py` reproduces the reported path, load and thermal screens.
- `python -X utf8 qa/stage05-power/correction_r8/verify.py` passes with 92 entry files checked, only the authorized handoff replacement changed, 29 components, 88 nets, 54 retained ERC findings, zero new findings, zero PCB files and no capture.
- `02_power.kicad_sch`, the MCU core, local symbol library and frozen resource map remain unchanged. Stage 06 has not begun.

## Candidate disposition

- TPS2553 remains REJECTED.
- TPS25946 meets the current-limit accuracy direction but fails the simultaneous-envelope voltage screen.
- TPS25948 is the leading low-loss pass-through CANDIDATE, but its official datasheet does not establish the required guaranteed low-current limit interval near 1.25 A.
- TPS62903 is a preferred additional 3 A forced-PWM main-buck CANDIDATE, not selected.
- TPS7A2033 remains a sensor-LDO CANDIDATE; corrected load thermal screening is improved but reverse-current, decay, PSRR and sequencing remain OPEN.

## Mechanism proposal requiring approval

Evaluate `5V_FC_PROTECTED -> synchronous 5.0 V buck-boost -> default-on current-limited reverse-blocking switch -> 5V_AUX` within Stage 05. Retain 1 A aggregate, at least 4.75 V at the external boundary, the 1.10-1.50 A guaranteed current-limit window, informational status semantics, first-5-ms inrush control and every prohibited power boundary. The converter should be at least 2 A class so it does not prematurely limit before the AUX switch. Exact IC and circuit remain OPEN until official-source comparison, PCBParts evidence, loss/thermal/EMI/inrush/backfeed/sequencing calculations and symbol audits pass.

This proposal increases switching noise, area, startup energy and verification burden. It is not authorized by this review. Project control must record explicit human approval before the Stage 05 task evaluates or captures it.
