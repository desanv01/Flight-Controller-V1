> Historical technical record. Names and private workstation/session references were neutralized for publication. Dates and assertions describe the recorded stage, not current physical qualification. See the current validation-status page for later checks.

# FC Rev A Stage 10 Continuation — PCB routing, copper and connectors

**Date:** 2026-09-11
**Scope of this continuation:** `[LOCAL_SOURCE] DRONE PROJECT` (sandbox copy) only. The live original at `[LOCAL_SOURCE] DRONE PROJECT` was **never written to** by this work.
**Disposition: VERIFIED CONDITIONAL PASS — residual required routing remains OPEN. STAGE 10 NOT COMPLETE. HOLD STAGE 11.**

This handoff supersedes the *disposition* of `FC_REV_A_STAGE_10_PCB_ROUTING_COPPER_CONNECTORS_2026-09-10.md`. That document declared `VERIFIED STOPPED / CONTINUATION` at **153 unconnected links, 4,880 track segments, 663 vias**. Those figures were **documentation, not measurement**: the board was already at **123 links / 5,538 segments / 720 vias** when the sandbox copy was frozen. The 2026-09-10 handoff is retained unedited as history.

---

## 1. Result

| Metric | Entry (2026-09-11 05:45) | Now | Change |
|---|---:|---:|---:|
| Native unconnected links | **123** | **96** | **−27** |
| — of which required (populated) | 99 | **73** | −26 |
| — of which DNP-only islands | 24 | **23** | −1 |
| Native DRC errors | 0 | **0** | — |
| DRC warnings | 88 (33 track + 55 via dangling) | **11** (all `track_dangling`) | **−77** |
| Track segments | 5,538 | **5,973** | +435 |
| Vias | 720 | **705** | −15 |
| Copper zones / rule areas | 12 / 10 | 12 / 10 | — |
| Schematic components / nets | 328 / 302 | 328 / 302 | frozen |
| Electrical footprints | 325 | 325 | frozen |
| Board DNP | 38 | 38 | frozen |
| ERC findings | 13 | **13** | unchanged, all classified |
| Schematic parity findings | 3 (J1, J2, Y2 — intentional) | **3** | unchanged |
| Invariant checks | 25/25 pass | **25/25 pass** | — |

**Canonical board:** `hardware/FC_REV_A/FC_REV_A.kicad_pcb`
**4,255,004 bytes · SHA-256 `08727f3679195f6fcb3a48c1224ad8b00695c5643853e6af0550d412dbc348ce`**

Cross-reference: the live original reached control revision R34 with **102** unconnected links (79 required + 23 DNP-only). This sandbox is therefore now **6 links ahead**, on 73 required links.

---

## 2. What was done

### 2.1 Entry seal
`qa/stage10-pcb/entry_r33_20260911/` — 436-file SHA-256 manifest of `hardware/FC_REV_A` (521.8 MB), an immutable board rollback copy, and preserved copies of 13 R33-sealed QA artifacts (including the original `entry_manifest.json`, `final_design_manifest.json`, `continuation_state.json` and `freerouting.json`).

### 2.2 Dangling-copper cleanup (batch 013)
A naive pass removing all 88 DRC-flagged dangling items **raised** the unconnected count 123 → 126 and was reverted. Some items KiCad reports as `via_dangling` are still load-bearing: a through via joining F.Cu and B.Cu tracks without touching an inner-layer track can be reported as "not connected on all layers" while remaining a functional layer transition. **DRC warning text is not sufficient authority to delete copper.**

Replaced with `prune_dangling_safe.py`, which removes an item only if the native unconnected count does not increase. Iterated to convergence: 88 → 64 → 25 → 20 → 15 → **11** warnings, with **123 links held constant throughout**. 194 copper items removed; 15 rejected as load-bearing.

### 2.3 Routing (batches 014–020)
Accepted progression: **123 → 113 → 111 → 107 → 103 → 98 → 97 → 96**.

The decisive finding was in `grid_world.py`: the raster blocks a cell for every net when two foreign clearances overlap, and the mask inflates foreign copper by `0.15 + width/2`. In `power` mode (0.8 mm) that is a **0.55 mm inflation**, which seals dense pads into ~130-node pockets — the cause of the repeated `disconnected raster` failures. `3V3_REF` is a **≤10 mA sense reference**, so routing it 0.8 mm wide was both electrically unnecessary and the direct cause of the blockage. Added an `any:<substr>` mode that routes a supply-classified net at signal width; the first such run closed 4 islands immediately.

### 2.4 Tooling changes (all on D:)
| File | Change | Why |
|---|---|---|
| `multilayer_grid.py` | endpoint escape search widened from ±0.23 mm to ±0.62 mm | pad-in-pocket failures |
| `route_required_batch.py` | added `all` and `any:<substr>` modes; PowerShell-safe (no empty-string argument) | empty mode string was silently dropped by PowerShell, so the mode became `"0.1"` and matched no net |
| `prune_dangling_safe.py` | new | connectivity-guarded copper removal |
| `prune_dead_copper.py` | new | proved there is no pad-free island copper |
| `stitch_islands.py` | new | direct island stitching; closed 0 — confirmed the blocker is congestion, not missing direct paths |
| `seal_manifests.py` | new | regenerates both stale manifests |
| `sweep_route.ps1` | new | route → cheap check → DRC → accept driver |
| `kicad-erc-json.ps1` | **fixed**: reads `sheets[].violations` | the ERC schema has no top-level `violations` key; the old wrapper threw `PropertyNotFoundStrict` and exited 1 even on success |
| `entry_manifest.json` | rewritten with absolute **D:** paths | it stored absolute **C:** paths, so `verify_stage10.py` could not run on this copy at all |
| `tools/freerouting-241/freerouting.json` | log path repointed D:; telemetry disabled | **it still pointed at `[LOCAL_SOURCE]` — Freerouting would have written into the original project** |

### 2.5 Freerouting — attempted, not adopted
Run with Java 25 (Temurin 25.0.4.1) against an exported Specctra DSN. It spent ~55 minutes in the **fanout** stage and never reached the autoroute pass: passes routed 85 / 47 / 46 / 45 SMD pins with a constant **135 unreachable**, at escalating rip-up costs (100→400). Terminated; **no `.ses` was produced and the canonical board was never touched by it.** The DSN seed, the exact command and the resume procedure are retained in `freerouting_run01_NOTE.txt`.

---

## 3. Verification evidence

- **Native DRC** `kicad-cli pcb drc --format json --schematic-parity` (KiCad 10.0.6, 2026-09-11): **0 errors**, 11 warnings (`track_dangling`), **96 unconnected**, 3 parity findings (J1, J2, Y2 — intentional footprintless).
- **Native ERC**: **13 findings** — 6 `isolated_pin_label`, 3 `pin_to_pin` (1 error: the ST-required VCAP pin 48/73 pair; 2 warning: SN74AXC4T774 B4→GND), 4 `multiple_net_names`. No suppression added.
- **`verify_stage10.py`: 25/25 checks PASS, exit code 0.** Run from the project root with KiCad's bundled Python 3.11.5 (`pcbnew`). The 8 files differing from the entry seal are exactly the 8 the Stage 10 release authorises.
- **Independent accounting** (`connectivity_accounting.py` + `classify_remaining.py`): 123 → **96 native links**, 73 required + 23 DNP-only, `native_equals_pad_island_links: true`, **0** conductive-item artifacts.
- **Routing metrics**: 163 routed nets.
- **Visual evidence**: `qa/stage10-pcb/board_views_final/` — front, back, L1, L2 (GND), L3 (POWER_SLOW), L4 layer plots plus `3d_top.png` / `3d_bottom.png`, all regenerated 2026-09-11.
- **Hash chain repaired**: `final_design_manifest.json` (166 files, 12,380,954 bytes) and `continuation_state.json` now both record `08727f36…` / 4,255,004 bytes, matching the board on disk. Both previously recorded a board of 3,958,677 bytes / `1d395da5…` that no longer existed; the live board's hash appeared in **no** manifest.

---

## 4. What remains — 73 required links across 61 nets

| # | Net | Required links | Islands |
|---|---|---:|---:|
| 1 | `3V3_REF` | **9** | 4 |
| 2 | `/USB and debug/USB_VBUS_PORT` | 3 | 4 |
| 3 | `/3V3_SENS` | 3 | 4 |
| 4 | `/Local sensors/IMU_INT2_LOCAL` | 2 | 3 |
| 5 | `/Local sensors/IMU_MISO` | 2 | 3 |
| 6 | `/Local sensors/BARO_INT_LOCAL` | 2 | 3 |
| 7 | `/Local sensors/BARO_SDA` | 2 | 3 |
| 8 | `/Local sensors/IMU_MOSI` | 2 | 3 |
| 9 | `/Power and monitoring/IN_UV` | 2 | 3 |
| 10 | `/USB and debug/SWO_PORT` | 2 | 3 |
| 11 | `/Local sensors/IMU_SCK` | 2 | 3 |
| 12 | `5V_FC_IN_A` | 2 | 3 |
| — | 49 further nets | 1 each | 2 |

**23 DNP-only island links must remain classified as DNP and must not be routed.** They sit on `/BOOT0`, `CAN1_5V_OUT`, `CAN2_EVAL_RX`, `ESC_CURR_FILTER`, `ESC_CURR_ISO`, `ESC_CURR_RAW`, `/ESC_CURR_DNP`, `GPS1_PPS_PORT`, `TELEM_5V_OUT`, `3V3_ANA` and `/SWO`.

**The 11 remaining `track_dangling` warnings are load-bearing** — removing them increases the unconnected count. They must be completed by routing, not deleted.

---

## 5. What was NOT done, and what remains prohibited

**No manufacturing output of any kind was produced.** No Gerbers, drill files, CPL, jobset, production BOM, purchase order or fabrication package. No Stage 11 work.

Stage 11 remains locked pending a separate explicit authorization. That release must preserve the 73 required residual links as an owned routing-completion gate, retain the 23 DNP-only islands without false closure, and require final native DRC/connectivity, rendering and mechanical review before any manufacturing export.

All Stage 05–09 physical-validation items remain **OPEN** and unchanged, including: converter stability and startup SOA; 55 °C continuous / 70 °C screening thermal; EMI; assembled-system backfeed < 100 µA; POWER1 crimp/wire/derating/vibration; the JST-GH harness voltage drop; the SSH-003T-P0.2 vs `-H` contact suffix; **no `(stackup)` block — dielectric, copper weight and controlled impedance are formally undefined**; and L3 USB impedance.

## 6. Files changed in this continuation

Canonical:
- `hardware/FC_REV_A/FC_REV_A.kicad_pcb`
- `hardware/FC_REV_A/FC_REV_A.kicad_prl`
- `hardware/FC_REV_A/FC_REV_A.kicad_pro` *(text variables only, via the router's zone refill)*

QC and evidence (`qa/stage10-pcb/`):
- new: `entry_r33_20260911/`, `board_views_final/`, `rejected_trials/`, `accepted_batches/013`–`020/`
- new tooling: `prune_dangling_safe.py`, `prune_dead_copper.py`, `stitch_islands.py`, `seal_manifests.py`, `sweep_route.ps1`
- regenerated: `connectivity_accounting.{json,md}`, `remaining_classification.json`, `routing_metrics.json`, `verification_summary.json`, `final_design_manifest.json`, `continuation_state.json`, `drc-final-stage10.json`, `erc-final-stage10.json`
- repaired: `entry_manifest.json`, `tools/freerouting-241/freerouting.json`

Root: `FC_REV_A_CURRENT_CONTROL_STATE.md`, `hardware/FC_REV_A/docs/retained_status_ledger.md` (see the control review).

**No previous stage handoff or control review was edited.**
