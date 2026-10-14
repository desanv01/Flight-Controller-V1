> Historical technical record. Names and private workstation/session references were neutralized for publication. Dates and assertions describe the recorded stage, not current physical qualification. See the current validation-status page for later checks.

# FC Rev A — KiCadRoutingTools Integration and First Results

> ## ⚠ CORRECTED VERDICT (supersedes §4–§6 below)
>
> The first edition of this document quoted "96 → 61 links" and "996 DRC errors" for the
> unconstrained pass. Both numbers were taken from **mid-run output states**, and the DRC
> grading was wrong. The corrected, fully-measured position is:
>
> | Board | Unconnected | Sub-spec tracks (<0.15 mm) | Sub-spec vias | Tracks on **In1.Cu** |
> |---|---:|---:|---:|---:|
> | **INCUMBENT** (D: canonical, `08727f36…`) | **96** | 0 | 0 | **0** |
> | pass 2 — **our floors pinned** (0.15 mm / 0.6 mm, rescue off) | **94** | 0 | 0 | **0** |
> | pass 1 — tool defaults (0.0889 mm / 0.45 mm) | 94 | 452 | 52 | **1,001** ❌ |
>
> **1. The DRC-grading artifact.** DRC on a board whose sibling `.kicad_pro` is missing falls
> back to KiCad's DEFAULT rules, which manufactured 499 phantom `clearance` and 199 phantom
> `track_width` errors in my first reading. The output board must be graded **with its own
> sibling `.kicad_pro` present** (KRT does write one). Always copy `.kicad_pro`, `.kicad_dru`
> and `fp-lib-table` alongside any renamed board before DRC.
>
> **2. `--layers F.Cu In2.Cu B.Cu` is NOT sufficient to protect the GND plane.** The flag is
> honoured during the main routing phase (`In1.Cu=-1x` in the log), but a later reconciliation
> phase re-entered with *four* routing layers and **placed 1,001 tracks on `In1.Cu`** in
> pass 1. Any KRT output **must** be checked for In1.Cu copper before it can be considered.
>
> **3. The real trade-off is our own design floor, not the router.** At our legal minimum
> geometry the router closes only **2** of the 96 links (96 → 94). Given its own much smaller
> 4-layer floor it routes far more, but produces illegal geometry *and* breaks the plane
> invariant. **The remaining links are blocked by our rules, not by router capability** — which
> independently confirms `FC_REV_A_STAGE_10_ROUTING_BLOCKER_ANALYSIS_2026-09-11.md`.
>
> **4. Conclusion:** KiCadRoutingTools **alone does not solve the Stage 10 routing gap as
> configured.** It is a genuinely capable router and it is now installed and working, but
> closing the remaining links requires a design-rule or layout decision (§8), not more router
> configuration.
>
> **5. Canonical board untouched throughout:** `08727f3679195f6fcb3a48c1224ad8b00695c5643853e6af0550d412dbc348ce`, 96 links, 0 DRC errors.

**Date:** 2026-09-11
**Tool:** KiCad Routing Tools v0.22.0 (Andy Haas, MIT) — Rust-accelerated A\* autorouter for KiCad
**Scope:** `[LOCAL_SOURCE] DRONE PROJECT` sandbox only. `[LOCAL_SOURCE] DRONE PROJECT` was never written to.
**Board under test:** `hardware/FC_REV_A/FC_REV_A.kicad_pcb` — `08727f3679195f6fcb3a48c1224ad8b00695c5643853e6af0550d412dbc348ce`, 96 unconnected links (73 required + 23 DNP-only), 0 DRC errors.

---

## 1. Installation (complete and working)

| Component | Location | Status |
|---|---|---|
| Source | `tools\KiCadRoutingTools-main\` | extracted from the supplied ZIP |
| Tool venv | `.krt-venv\` | numpy 2.4.6, scipy 1.17.1, shapely 2.1.2, Pillow 12.3.0 |
| Rust core | `tools\KiCadRoutingTools-main\rust_router\grid_router.pyd` | **798,720 bytes, v0.22.0** — downloaded prebuilt, version-matched; imports as `GridRouter`, `PoseRouter`, `GridObstacleMap`, `identify_blocking_obstacles` |
| Rust toolchain | `[LOCAL_SOURCE]` | cargo/rustc 1.95.0 present but **not needed** — the prebuilt was used |

Notes:
- `uv` needed `UV_CACHE_DIR` inside the workspace; its default cache (`[LOCAL_SOURCE]`) is outside the sandbox and was denied.
- The tools need `numpy`, `scipy`, `shapely`, `Pillow`. KiCad's bundled Python has numpy + Pillow but **not** scipy/shapely, so a dedicated venv was created from KiCad's interpreter rather than installing into `Program Files`.
- Workspace layout for KRT runs: `qa/stage10-pcb/krt/`.

## 2. Independent validation of our board

`check_connected.py` read the board and reported **5,973 segments, 705 vias, 1,244 pads, 12 zones** and a **KiCad refill cross-check of 96 link(s)** — exactly matching our own measurements. The router also auto-detected our netclasses (Default 0.2/0.6/0.3 clearance 0.15) and two BGA exclusion zones (U12, U16). **The tool parses our board faithfully.**

## 3. Confirmation of the blocker analysis

For `/STM32H743 core/I2C2_SCL` — the net my own router could not close — KRT independently reported:

> *"Static blockers: pads: 3V3_REF (U17), /External UART and I2C ports/TELEM1_RTS_OD (U30); pre-existing tracks: 3V3_REF … the start/target pads are boxed in by static obstacles (neighboring pads + clearance), not by congestion."*

That is the same conclusion reached in `FC_REV_A_STAGE_10_ROUTING_BLOCKER_ANALYSIS_2026-09-11.md`, from an independent implementation. **KRT then routed it** — see §4.

## 4. First real routing pass

Command (output to a **separate file**, canonical never touched):

```
route.py krt/FC_REV_A_krt_in.kicad_pcb --output krt/FC_REV_A_krt_pass1.kicad_pcb \
    --nets <50 target nets> --layers F.Cu In2.Cu B.Cu --fab-tier standard
```

| Metric | Input | Candidate (`FC_REV_A_krt_pass1.kicad_pcb`) |
|---|---:|---:|
| Native unconnected links | **96** | **61** |
| Tracks on F.Cu / In2.Cu / B.Cu | 2409 / 1582 / 1982 | 2888 / 1749 / 2226 |
| Tracks on **In1.Cu** | **0** | **0** ✅ |
| Vias | 705 | 813 |
| Footprints / zones | 329 / 22 | 329 / 22 |

- 39 nets routed, 11 failed; the run's own gate reported **31–38 nets connected** depending on configuration, and it broke 8–11 previously-connected nets which it then attempted to restore.
- Nets it closed that my own tools could not: **`3V3_REF`, `I2C2_SCL`, `I2C2_SDA`, `SPI1_SCK`, `5V_FC_IN_A`, `5V_FC_PROTECTED`, and most of the `AUX_*` monitoring group.**

### ⚠ The candidate is NOT acceptable as-is

Native DRC on the candidate: **1,206 violations — 996 errors**:

| Type | Count |
|---|---:|
| clearance | 499 |
| lib_footprint_issues | 199 |
| track_width | 199 |
| hole_clearance | 184 |
| drill_out_of_range | 57 |
| via_diameter | 57 |
| track_dangling / via_dangling | 10 / 1 |

Cause: **574 tracks below 0.15 mm** (553 of them at 0.0889 mm) and **57 vias below 0.6/0.3 mm** (0.45/0.20). The router's `--fab-tier standard` floors at **0.0889 mm track / 0.45 mm via on a 4+ layer board** — below this board's documented rules. Its `net rescue` and `terminal escalation` paths delivered those sub-spec features even with `--fab-tier standard`.

**`--layers F.Cu In2.Cu B.Cu` worked correctly**: `In1.Cu` was appended as a forbidden layer at cost `-1x`, so the GND plane was never routed on. This is verified independently (§4 table).

## 5. The correct configuration

A `--fab-overrides` file pinning **our** numbers, plus the rescue paths disabled:

```
# qa/stage10-pcb/krt/fab_overrides_fc_rev_a.txt
track_width   = 0.15
via_diameter  = 0.6
via_drill     = 0.3
clearance     = 0.15
hole_to_hole  = 0.25
board_edge    = 0.3
```

```
route.py <in> --output <out> --nets <targets> \
    --layers F.Cu In2.Cu B.Cu \
    --fab-tier standard \
    --fab-overrides qa/stage10-pcb/krt/fab_overrides_fc_rev_a.txt \
    --escalation off
# with KICAD_NET_RESCUE=0 and KICAD_TERMINAL_ESCALATION=0 in the environment
```

`--fab-overrides` pins the floor to one hard rung and disables the standard→advanced escalation. `KICAD_RIP_PREEXISTING=0` exists but did **not** fully prevent pre-existing nets from being ripped during the reconciliation phase — pre-existing rips must therefore be checked per run, not assumed away.

## 6. Acceptance rules for any KRT output

A candidate board may only replace the canonical board if **all** of these hold:

1. **0 native DRC errors** (`kicad-cli pcb drc --schematic-parity`). Warnings reviewed.
2. **0 non-via tracks on `In1.Cu`** — the L2 GND plane invariant.
3. **No track below 0.15 mm and no via outside 0.6/0.3 mm.**
4. **No previously-connected net newly broken** — compare KRT's own broke/connected lists *and* re-measure natively.
5. Native unconnected count strictly lower than the incumbent.
6. `verify_stage10.py` still 25/25 with exit 0.
7. `+BATT`, `/CURR`, every `ESC_CURR*`, `CAN2`, `PA0`/`PA1` still absent from all copper.
8. Full-file hash recorded; the incumbent board retained as a rollback copy.

The pass-1 candidate fails rules 1, 3 and 4 and is therefore **rejected and retained only as an experiment**.

## 7. Reproducing

```powershell
$root = "[LOCAL_SOURCE] DRONE PROJECT"
$py   = "$root\.krt-venv\Scripts\python.exe"
Set-Location "$root\tools\KiCadRoutingTools-main\py_router"

# connectivity / DRC cross-check
& $py check_connected.py "$root\qa\stage10-pcb\krt\FC_REV_A_krt_in.kicad_pcb" --quiet

# constrained routing run
$env:KICAD_NET_RESCUE = "0"; $env:KICAD_TERMINAL_ESCALATION = "0"
& $py route.py "$root\qa\stage10-pcb\krt\FC_REV_A_krt_in.kicad_pcb" `
      --output "$root\qa\stage10-pcb\krt\FC_REV_A_krt_pass2.kicad_pcb" `
      --nets (Get-Content "$root\qa\stage10-pcb\krt\target_nets.txt") `
      --layers F.Cu In2.Cu B.Cu --fab-tier standard `
      --fab-overrides "$root\qa\stage10-pcb\krt\fab_overrides_fc_rev_a.txt" --escalation off
```

## 8. What will actually close the remaining links

The router is not the constraint; **our own design floor is.** Ranked by likelihood of success:

| # | Option | What it needs | Cost / risk |
|---|---|---|---|
| **1** | **Relax the signal minimum track width from 0.15 mm to 0.10 mm** (keep 0.6/0.3 vias, keep 0.15 mm clearance) | a design-rule decision by you; update `FC_REV_A.kicad_pro`, the Stage 09/10 documented rules, and re-run KRT at the new floor | **Low.** 0.10 mm (4 mil) is a standard, no-cost JLCPCB capability (their minimum is ~0.09 mm/3.5 mil for 1 oz). Reversible. This is the single highest-leverage change |
| **2** | **Placement change** in the congested MCU / sensor region | a controlled change request; Stage 10 does not authorise placement beyond bounded refinement | Medium effort, high confidence — this is the classic fix and needs no rule change |
| **3** | **Iterative KRT campaign at legal rules** | repeated runs feeding back the nets it broke, `--rip-existing-nets` scoped per run, several hours of compute | Slow and uncertain; each pass is ~50 min and the gain at 0.15 mm is ~2 links |
| **4** | **Stop at 96 links** | record the remaining 73 required links as an owned OPEN item carried to a later stage | Honest, zero risk, but Stage 10 cannot then be called complete |

**Recommendation: option 1.** It is a one-line rule change with real DFB/DFM support, it is
reversible, and it converts the router from "marginally useful" into the tool that finishes the
job. Option 2 is the fallback if the rules must stay at 0.15 mm.

Whichever is chosen, **every KRT output must pass all eight acceptance checks in §6** — and
additionally be checked for `In1.Cu` copper, which §6 did not originally cover.

---


