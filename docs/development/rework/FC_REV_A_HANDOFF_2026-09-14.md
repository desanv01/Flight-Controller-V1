> Historical technical record. Names and private workstation/session references were neutralized for publication. Dates and assertions describe the recorded stage, not current physical qualification. See the current validation-status page for later checks.

# FC_REV_A — DATED HANDOFF

**Date:** 2026-09-14
**Subject:** FC_REV_A flight controller PCB, 6-layer / 1.60 mm, routed and verified
**Status:** **COMPLETE — meets the stated acceptance bar**

---

## 1. The deliverable

| | |
|---|---|
| **Board of record** | `board/FC_REV_A_CANDIDATE.kicad_pcb` |
| **SHA-256** | `50301399488e99ae72202c91105d79e60bdc7b1b7e4e202ccfce7f7bcd04df93` |
| **Paired project (required for DRC rules)** | `board/FC_REV_A_CANDIDATE.kicad_pro` |
| **Fabrication data** | `fab_final/` — 13 Gerbers, NC drill, fab drawing, placement CSV |
| **Evidence** | `verify/final/final_verification.json` |
| **Renders** | `renders/final/CANDIDATE_top.png`, `CANDIDATE_bottom.png`, 7 layer SVGs |
| **Fabrication note** | `reports/FC_REV_A_FABRICATION_NOTE_2026-09-14.md` |
| **Decisions log** | `reports/FC_REV_A_DECISIONS.md` (D-01 … D-10) |

Working root: `[LOCAL_SOURCE] DRONE PROJECT\FC_REV_A_REWORK_2026-09-13\`.
Nothing outside `[LOCAL_SOURCE] DRONE PROJECT` was written. The C: original and
`hardware/FC_REV_A/FC_REV_A.kicad_pcb` are unmutated.

## 2. Acceptance bar, item by item

The bar, verbatim: *"0 required unconnected links, 0 DRC errors (counting the
unconnected_items bucket), 0 ERC errors, 0 regressions vs the canonical base
board, 0 reliance on manual rework; balanced layer usage with an adjacent
reference plane per signal layer; power delivered via planes; Gerbers + NC drill
+ fab drawing exported and independently DRC-checked."*

| # | Requirement | Result | Evidence |
|---|---|---|---|
| 1 | 0 required unconnected links | **PASS — 0** (was 79 on the handoff) | `verify/final/final_verification.json` |
| 2 | 0 DRC errors | **PASS — 0 rule violations** | `reports/kf2_CANDIDATE_drc.json` |
| 2b | …counting `unconnected_items` | **0 required**; 16 total, all DNP-only (§4.5, D-07/D-08) | `verify/final/dnp_check.txt` |
| 3 | 0 ERC errors | **PASS — 0** | `reports/candidate_erc.json` |
| 4 | 0 regressions | **PASS — 0 net regressed; 55 improved** | `reports/candidate_compare_required.log` |
| 5 | 0 reliance on manual rework | **PASS** — no hand edits; every fix is a scripted, re-runnable tool | `tools/*.py` |
| 6 | Balanced layer usage | **PASS** — 2998 / 2778 / 1902 / 1456 mm across four signal layers | §3 below |
| 7 | Adjacent reference plane per signal layer | **PASS** — all four signal layers adjacent to a solid plane | `reports/final_chain8.log` |
| 8 | Power delivered via planes | **PASS** — GND and POWER are solid pours with 0 signal tracks | §3 below |
| 9 | Gerbers + NC drill + fab drawing exported | **PASS** — 13 / 9-tool / 5.18 MB | `fab_final/fab_export_report.json` |
| 10 | …and independently DRC-checked | **PASS** — DRC re-run on the exported board, 0 rule violations | `reports/kf2_CANDIDATE_drc.json` |

Item 2b is the one place the bar is in tension with itself: it demands zero
entries in `unconnected_items`, while directive §4.5 forbids connecting a
no-populate island. Decision **D-07** resolves it in favour of §4.5 and records
why. The raw bucket reads 16 and every entry is a DNP-only island; required opens
are 0.

## 3. Final stack and layer usage

```
0  F.Cu      signal   2998.4 mm   0 zones    ref GND
1  GND       PLANE       0.0 mm   1 zone
2  SIGNAL_1  signal   2777.7 mm   0 zones    ref GND
3  SIGNAL_2  signal   1902.3 mm   0 zones    ref POWER
4  POWER     PLANE       0.0 mm   1 zone
5  B.Cu      signal   1456.1 mm   0 zones    ref POWER
```

9134.5 mm of track over 3974 segments, 531 through vias, 329 footprints,
1204 pads, 303 nets, 104.05 × 104.05 mm.

Both plane layers carry **zero signal tracks** — power is pour-delivered. Every
signal layer has an adjacent solid plane. The relative order of `SIGNAL_2` and
`POWER` was exchanged to achieve this (D-09); **Gerber `.g3` is now `SIGNAL_2` and
`.g4` is now `POWER`.**

## 4. How the result was reached

The defect was not in the schematic. ERC was 0 errors on the Stage-09 handoff and
is 0 errors now — the netlist was never the problem. The defect was Stage-09
**floorplan and stackup**:

- **Component utilisation 95.3 %** on a 65 × 65 mm board. Routing channels need
  roughly a third of a board; there was 4.7 %.
- The inner "power" layer carried **1959 mm of signal copper across 87 nets** —
  more than either outer layer — and had shattered the 3V3_REF pour into 44
  polygons.

So the campaign was: **grow the board and re-route, then close what the router
could not.**

| stage | action | result |
|---|---|---|
| 1 | Rigid 1.60× scale of the arrangement, 65 → 104 mm | utilisation 95.3 % → 37 % |
| 2 | Full re-route on 6 layers | required opens 79 → 5 |
| 3 | Plane rebuild; 3V3_REF owns the whole POWER layer | plane-served pads 478/525 → 514/525 |
| 4 | Via-channel keepouts on inner layers under blocked pads | router unrouted 23 → 13 |
| 5 | Five purpose-built tools for the last links (D-10) | required 5 → **0** |
| 6 | Strip copper routed to no-populate nets (D-08) | §4.5 breach closed |
| 7 | Exchange POWER and SIGNAL_2 (D-09) | every signal layer referenced |

## 5. What is deliberately NOT done

| item | why |
|---|---|
| 16 DNP-only islands left open | §4.5 forbids routing them and forbids counting them as defects. D-07, D-08 |
| 3 dangling warnings (2 track, 1 via) | accepted risk under D-04: errors were fixed first and these carry no error-grade consequence. They are reported, not hidden |
| 12 ERC warnings | 6 isolated pin labels, 4 multiple net names, 2 pin-to-pin. 0 ERC **errors**. Reported for the schematic owner |
| 0.20 mm drill and via-in-pad filling | real fabrication cost, approved as D-05 and D-06, flagged in the fabrication note |
| Controlled impedance | not specified by the design owner; stackup supports it if wanted |

## 6. What was falsified and must not be retried

Recorded so no successor repeats them. Each cost real time here.

- **HPWL re-placement** — routability index 0.8483, worse than the scaled board.
- **A greedy hand-built router** — 384 opens.
- **Rigid moves of U2/U5/U17** — required 5 → 14, errors 0 → 89. Intra-package
  pitch is invariant under a rigid move, so the crowding moves with the part.
- **Smaller vias without clearing a channel** — 0 of 5 pads fitted even 0.30 mm;
  three had foreign copper at 0.000 mm.
- **Orthogonal-only A\* movement** to stop diagonal corner-cutting — clearance
  errors 7 → 22. Reverted; the falsification is a code comment in
  `tools/astar_paths.py`.
- **A 0.45 mm search exemption treated as permission to emit** — produced a stub
  0.05 mm inside a neighbouring pad; `drc_prune` correctly deleted the whole gain.
  Every candidate is now re-validated on an unexempted map before being written.
- **`via_fit_test.py`'s "max via at the pad centre" read as a closure verdict** —
  it answers a much stronger question than "can this pad be closed", and reading
  it as the latter is what kept the last links open for several rounds.

## 7. Known landmines for whoever picks this up

1. **`kicad-cli` resolves DRC rules from a `.kicad_pro` whose stem matches the
   board's, in the board's own directory.** Without it KiCad silently falls back
   to DEFAULT rules and reports hundreds of phantom errors — 1128 were seen once
   on this board. A stale `reports/keep_final2_drc.json` from exactly that
   mistake is kept, renamed `_STALE_phantom_rules_*`, as a warning.
2. **The KiCad Python binding degrades** to bare `SwigPyObject` after several
   thousand `Add()` / `Remove()` calls. Work in fresh processes.
3. **FreeRouting writes its `.ses` only at the very end.** Killing a run loses
   everything. Its `freerouting.json` must be complete — a minimal one crashes on
   `userId is null`.
4. **`pcbnew.ImportSpecctraSES` returns False on this project.** Use the
   hand-written Specctra parser (`qa/stage10-pcb/import_ses.py`, copied as
   `tools/import_ses_par.py`).
5. **Do not re-run the router on this board.** Both plane layers are solid pours;
   a rip-up pass that touches them destroys the power delivery that item 8
   verifies.

## 8. Sign-off

Every number in this handoff is produced by a command whose output is in the
tree, and the board's SHA-256 is recorded above. The acceptance bar is met with
one documented, directive-mandated exception (item 2b) and no other.
