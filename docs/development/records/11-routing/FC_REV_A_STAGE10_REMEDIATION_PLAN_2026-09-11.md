> Historical technical record. Names and private workstation/session references were neutralized for publication. Dates and assertions describe the recorded stage, not current physical qualification. See the current validation-status page for later checks.

# FC Rev A — Stage 10 Routing Remediation Plan and Stage Records

**Date:** 2026-09-11
**Authority:** user granted full permission to make crucial design changes to close the Stage 10 routing gap, provided no change introduces new errors/violations.
**Scope:** `[LOCAL_SOURCE] DRONE PROJECT` sandbox only. `[LOCAL_SOURCE] DRONE PROJECT` was never written to.
**Baseline (entry):** `FC_REV_A.kicad_pcb` = `08727f3679195f6fcb3a48c1224ad8b00695c5643853e6af0550d412dbc348ce`, 96 unconnected links (73 required + 23 DNP-only), 0 DRC errors, ERC 13 classified, 25/25 invariants.

---

## Staged plan

| Stage | Objective | Exit criterion |
|---|---|---|
| **S0** | Tool selection | a routing engine chosen on documented capability, not availability |
| **S1** | Controlled design-rule change | signal floor relaxed, everything else unchanged, **no regression** on the existing board |
| **S2** | Routing campaign at the new floor | a candidate board that reduces required links |
| **S3** | Iterate | re-route every net the router broke; drive required links toward zero |
| **S4** | Acceptance gate | 0 DRC errors · 0 ERC errors · 0 tracks on In1.Cu · no net broken · prohibited nets absent · 25/25 invariants |
| **S5** | Seal | manifests regenerated, control review + handoff + control state + ledger updated |

---

## S0 — Tool selection: **KiCadRoutingTools accepted, OrthoRoute rejected**

| | KiCadRoutingTools v0.22.0 | OrthoRoute |
|---|---|---|
| Purpose | general-purpose grid A\* autorouter for KiCad; rip-up and reroute, plane stitching, fanout | by its own README, **"not a general-purpose PCB autorouter"** — a Manhattan-lattice PathFinder engine for very large, dense, highly regular backplanes and BGA escapes |
| Measured on ordinary boards | performed "dramatically better" | **1 % clean-pass / 30 % routability** on synthetic D2; **2 % clean-pass / 51 % routability** on 99 open-source boards (`PCBWorld`, arXiv:2607.05915, Table 3) |
| Hardware need | none beyond Python (prebuilt Rust core) | **CuPy + CUDA 12.x** (NVIDIA GPU) |
| Verdict | **ACCEPTED** — already installed, validated against our board, and it routes nets our own tools could not | **REJECTED** on its own documented evidence. The machine does have an NVIDIA GPU, so it *could* run, but the benchmarks make it the wrong engine for a 65 × 65 mm 4-layer flight controller |

OrthoRoute is retained extracted at `tools/OrthoRoute-main/` for the record only. It was **not** installed and **not** run.

## S1 — Controlled design-rule change: **applied and regression-tested**

**Change:** `min_track_width` in `hardware/FC_REV_A/FC_REV_A.kicad_pro` **0.15 mm → 0.10 mm**. One value, nothing else.

| Rule | Before | After |
|---|---|---|
| **`min_track_width`** | 0.15 | **0.10** ← the only change |
| `min_clearance` | 0.15 | 0.15 (unchanged) |
| `min_via_diameter` | 0.6 | 0.6 (unchanged) |
| `min_through_hole_diameter` | 0.3 | 0.3 (unchanged) |
| `min_hole_clearance` / `min_hole_to_hole` | 0.15 / 0.25 | unchanged |
| `min_copper_edge_clearance` | 0.3 | 0.3 (unchanged) |

**Rationale.** The router's failures are caused by our own floor, not by router weakness: at 0.15 mm it closed 2 links, at its own 0.0889 mm default it closed far more but produced illegal geometry. 0.10 mm (4 mil) is a standard, no-extra-cost JLCPCB capability (their floor is ~0.09 mm/3.5 mil), it is reversible, and it applies **only to signal necking** — vias and clearance are untouched, so power integrity, the ground plane and the design's electrical contract are unaffected.

**Regression test (the S1 exit criterion).** The board file was not touched and was re-graded under the new rules:

| | Value |
|---|---|
| Board SHA-256 | `08727f36…` — **identical to entry** |
| Native DRC under new rules | **11 warnings, 0 errors** — identical to entry |
| Unconnected links | **96** — identical to entry |
| Schematic parity | 3 (J1, J2, Y2 — intentional) — identical |
| ERC | 13 classified — identical |

**No regression.** Relaxing a minimum cannot introduce a violation, and the measurement confirms it.

**Rollback:** `qa/stage10-pcb/pre_rule_change_20260911/` holds the pre-change `FC_REV_A.kicad_pcb`, `.kicad_pro`, `.kicad_dru` and `.kicad_sch`. Restoring that directory reverts S1 completely.

**Propagation:** the router's own floor file `qa/stage10-pcb/krt/fab_overrides_fc_rev_a.txt` was updated to `track_width = 0.10` so the router may use the new floor but nothing below it (vias still pinned at 0.6/0.3, clearance at 0.15).

---

## S2 — Routing campaign (in progress)

```
route.py krt/FC_REV_A_s2.kicad_pcb --output krt/FC_REV_A_s2_out.kicad_pcb \
    --nets <50 target nets> \
    --layers F.Cu In2.Cu B.Cu \
    --fab-tier standard \
    --fab-overrides krt/fab_overrides_fc_rev_a.txt \
    --escalation off
# KICAD_NET_RESCUE=1, KICAD_TERMINAL_ESCALATION=1 (rescue may narrow, but only to 0.10 mm)
```

Differences from the earlier runs that produced illegal output:
- the floor is now **0.10 mm**, so the rescue/escalation paths that previously emitted 0.0889 mm tracks can only reach a **legal** width;
- the run is graded **with its sibling `.kicad_pro` present**, which the earlier grading omitted (that omission manufactured 499 phantom clearance and 199 phantom track-width errors).

**Mandatory output checks (learned the hard way):**
1. **`In1.Cu` must carry zero tracks.** `--layers F.Cu In2.Cu B.Cu` was honoured in the main phase but a later reconciliation phase placed **1,001 tracks on `In1.Cu`** in an earlier run. This is checked first, every time.
2. No track below 0.10 mm; no via outside 0.6/0.3 mm.
3. Native DRC **with the sibling `.kicad_pro` present** must be 0 errors.
4. Unconnected links strictly lower than 96, with no previously-connected net broken.

---

*The canonical board remains `08727f36…` at 96 links with 0 DRC errors. Stage 11, manufacturing exports, procurement, fabrication and flight remain locked.*
