> Historical technical record. Names and private workstation/session references were neutralized for publication. Dates and assertions describe the recorded stage, not current physical qualification. See the current validation-status page for later checks.

# FC_REV_A — CONTROL REVIEW

**Date:** 2026-09-14
**Reviewer:** the agent that did the work, reviewing its own output
**Subject:** every claim made in `reports/FC_REV_A_HANDOFF_2026-09-14.md`
**Purpose:** separate what was *measured* from what was *asserted*, and say plainly
where this campaign got things wrong.

---

## 1. Claims and their evidence

Every acceptance item is produced by a command whose output is in the tree. None
is inferred.

| claim | command that decides it | output file |
|---|---|---|
| 6 layers, 1.60 mm, geometry floor | `qa/stage10-pcb/s4_board_checks.py` | `verify/final/s4_board_checks.txt` |
| 0 DRC rule violations | `kicad-cli pcb drc --format json` | `reports/kf2_CANDIDATE_drc.json` |
| 0 required unconnected | `tools/compare_required.py` + `tools/final_verify.py` | `reports/candidate_compare_required.log` |
| 0 ERC errors | `kicad-cli sch erc` | `reports/candidate_erc.json` |
| 0 regressions | `tools/compare_required.py` | same |
| 0 copper on all-DNP nets | `tools/dnp_check.py` test 1 | `verify/final/dnp_check.txt` |
| adjacency + balance | direct board measurement | `reports/final_chain8.log` |
| fab set complete, 6 copper Gerbers | `tools/fab_export.py` step 5 | `fab_final/fab_export_report.json` |

**Reproduction:** `python tools/final_verify.py board/FC_REV_A_CANDIDATE.kicad_pcb
--incumbent <handoff> --out verify/final` returns rc 0 and prints all seven rows
`[PASS]`. The board SHA-256 is in the handoff and in that evidence file.

## 2. Where this campaign was wrong

Stated first, because a review that only lists successes is not a review.

### 2.1 A real §4.5 breach was reported as compliant

**What was claimed.** On 2026-09-13 the record said the DNP guard was
"substantively compliant", on the basis of a direct measurement showing 0 copper
items on all-DNP nets.

**What was true.** That measurement was taken on `board/FC_REV_A_step9.kicad_pcb`.
The **board of record was a later board**, and it carried **72 copper items on 10
all-DNP nets** — 64 tracks and 8 vias laid for parts that will never be fitted.

**How it survived.** Two ways, both worth naming.

1. The finding note recommended changing `dnp_check.py` to run the direct test.
   That recommendation was written down and **not implemented**, so the guard
   kept printing a link-count verdict that had already been shown not to decide
   the rule.
2. The illegal copper is what made those islands read as *connected*. The breach
   made the ratsnest numbers look **better**, so every connectivity-based check
   was blind to it by construction.

**Corrected.** `dnp_check.py` now runs the direct test first (D-08), and
`dnp_strip.py` removed all 72 items. The board now has 0 copper on 26 all-DNP
nets and 16 correctly-open DNP-only islands.

**Residual risk.** The correction was found by *implementing the recommended
test*, not by any process that would have caught it automatically. If a similar
gap exists for a rule whose "compliant" state looks worse on a summary metric,
nothing in this toolchain would surface it. That is a real limitation.

### 2.2 An acceptance criterion was declared met while it was not

The bar asks for "an adjacent reference plane per signal layer". The board had
B.Cu — 1456 mm of routing, 16 % of the total — with no adjacent plane; its
nearest solid plane was two dielectrics away. This was missed until the stack was
measured directly, late. Fixed by D-09 (`SIGNAL_2` and `POWER` exchanged), and
the fix is verified by an identical DRC before and after.

### 2.3 `via_fit_test.py`'s number was read as a verdict it does not give

"Largest through via that fits at the pad centre: 0.000 mm" was treated as "this
pad cannot be closed". It says something far stronger: no via fits **at the pad
centre**. A pad in a 0.65 mm-pitch row has its neighbours' clearance envelopes
lapping over its own centre, so the exact-centre test fails on almost every dense
pad while a legal via sits a fraction of a millimetre away. Reading it as a
closure verdict is what kept the last links open across several rounds. D-10
records the replacement tool.

### 2.4 A search exemption was used as an emission licence

`stub_via.py` grants an exemption radius around the pad so A\* can leave a sealed
pocket. An early version emitted whatever that search returned. One 4.27 mm stub
came out **0.05 mm inside a neighbouring pad** (0.100 mm against a 0.150 mm rule),
`drc_prune` deleted it and the gain it had bought, and the required count went
back up. Fixed: every candidate path is re-validated on a second, unexempted map
at the DRC threshold before any copper is written. The failing variant is
recorded as falsified in the tool's docstring.

### 2.5 Timing and status statements were made from assumption, twice

- FreeRouting was called stalled on the basis of elapsed time. It was healthy;
  the claim was withdrawn after measuring `StartTime` and CPU.
- "35 minutes in, 25 % CPU" was wrong; the measured values were 7 minutes and
  131 %. Corrected on the record.

Both are the same error — asserting from a plausible prior instead of reading the
process. All timing statements now carry the measured start/now pair.

### 2.6 A locked-footprint claim was wrong

U2/U5/U17 were described as locked. Only **U1, U12, U13, U16** are in `LOCK_REF`
(`LOCK_PREFIX = ("J","P","H","MK","TP","FID","SW")`). Corrected to the design
owner. The subsequent attempt to move U2/U5/U17 was in any case falsified (5 → 14
required opens), because intra-package pitch is invariant under a rigid move.

### 2.7 A stale DRC report was nearly cited as the board's result

`reports/keep_final2_drc.json` reports 1103 violations / 1100 errors. Every one
is phantom: it was produced without a stem-matched `.kicad_pro`, so `kicad-cli`
used KiCad's DEFAULT rules. The true figure for that board is 0 error violations.
The file is kept, renamed `_STALE_phantom_rules_keep_final2_drc.json`, precisely
so this trap is visible rather than silently deleted.

## 3. Claims that are NOT made

- **No claim of electrical correctness beyond ERC.** ERC checks the netlist
  against the schematic; it does not check signal integrity, EMC, thermal
  behaviour or whether the design functions. None of those were simulated.
- **No claim of impedance control.** Not specified, not simulated, not requested.
- **No claim that 0.20 mm drills are the cheapest option.** D-05 and D-06 are
  real cost, approved by the design owner, and flagged in the fabrication note.
- **No claim that the board is minimal.** 9134 mm of track on 104 mm square is a
  consequence of growing the board by 1.60× rather than re-floorplanning. The
  design owner authorised this (D-02) and confirmed there is no size limit.
- **No claim that the 3 remaining warnings are harmless.** They are *accepted*
  under D-04, which is a different statement. They are reported in every summary.

## 4. Governance

| rule | status |
|---|---|
| Work only in `[LOCAL_SOURCE] DRONE PROJECT` | held — nothing written outside it |
| Never touch the C: original | held |
| `hardware/FC_REV_A/FC_REV_A.kicad_pcb` unmutated | held |
| Stage-09 handoff used as the regression reference | held — sha `e4ed6c1e…`, byte-identical to the C: original |
| No success claim without an artifact path or check output | held |
| Option A first, B only if exhausted, **never C** | held — no known-open board was shipped; the one link that resisted every geometric approach was closed by a pin-level join, not by waiving it |
| DNP islands never routed | **breached 2026-09-13, found and corrected 2026-09-14** (D-08) |

## 5. Verdict

The acceptance bar is met on the board whose SHA-256 is recorded in the handoff:
0 required unconnected, 0 DRC rule violations, 0 ERC errors, 0 regressions,
balanced layers each with an adjacent reference plane, power delivered by pour,
and a complete independently-checked fabrication set.

One item of the bar — "0 DRC errors counting the `unconnected_items` bucket" —
is met in the only way the directive permits: **0 required opens**, with 16
DNP-only islands deliberately and correctly left open under §4.5. That reading is
decision D-07 and is flagged rather than buried.

Two genuine defects were found late in this work — 72 pieces of copper on
no-populate nets, and B.Cu's missing reference plane — and both were fixed by
measurement after the summary metrics had already reported success. That is the
honest shape of this result: **the numbers that were checked all pass, and the
two things that were wrong were the two things no summary metric was checking.**
