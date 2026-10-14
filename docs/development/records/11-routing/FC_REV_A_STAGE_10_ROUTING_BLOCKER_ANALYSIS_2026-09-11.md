> Historical technical record. Names and private workstation/session references were neutralized for publication. Dates and assertions describe the recorded stage, not current physical qualification. See the current validation-status page for later checks.

# FC Rev A — Stage 10 Routing Blocker Analysis

**Date:** 2026-09-11
**Subject:** why the remaining Stage 10 links cannot be closed by additive routing
**Scope:** `[LOCAL_SOURCE] DRONE PROJECT` sandbox copy. `C:` original untouched.
**Board under analysis:** `08727f3679195f6fcb3a48c1224ad8b00695c5643853e6af0550d412dbc348ce` (4,255,004 B), 96 native unconnected links = **73 required + 23 DNP-only**, 0 DRC errors.

---

## 1. Summary

The remaining 73 required links are **not closable by any additive routing method** available within Stage 10's frozen constraints. They are blocked by other signals' already-routed copper, not by a weak router.

Measured over the direct corridor between each unrouted net's nearest island pair, at the required 0.225 mm half-width (0.15 mm clearance + 0.15 mm track):

| Measure | Value |
|---|---|
| Unrouted nets analysed | 50 |
| Median foreign copper items inside a corridor | **21** |
| Worst corridor (`/Local sensors/SPI1_SCK`, 33.4 mm) | **104 blockers** — 13 pads, **80 tracks**, 11 vias |
| Second worst (`/TELEM1_TX`, 34.1 mm) | 91 blockers |
| Third worst (`/GPS1_TX`, 25.1 mm) | 80 blockers |
| Share of blockers that are `/GND` | **2.7 % – 19.6 %** (median ≈ 10 %) |

The blockers are predominantly **other signal nets' tracks** — `SPI1_MOSI`, `3V3_REF`, `IMU1_DRDY`, `BARO_3V3`, `COMPANION_TX_OD`, `VCAP`, `AUX_HEALTH` and their neighbours. Ground copper is a minority contributor, and removing it would not help.

---

## 2. What was tried, and what each attempt proved

### 2.1 A corrected per-net A\* router (`qa/stage10-pcb/route_fresh.py`)

Three defects in the project's original raster router (`grid_world.py` + `multilayer_grid.py`) were identified and fixed:

| # | Defect | Consequence | Fix |
|---|---|---|---|
| 1 | `raster()` writes `mask[pos] = -1` when two foreign items' clearances overlap a cell | that cell becomes blocked for **every** net, permanently and order-dependently, including the net that owns it | rebuild a fresh occupancy mask per target net; foreign copper only |
| 2 | A diagonal track is rasterised by its **bounding box** | blocks several times the real area | rasterise a **capsule** (segment + half width) |
| 3 | `endpoint_nodes` returns only the single nearest free cell | a pad with several pockets gets one chance | return the whole local free set |

Result: the previously reported failures changed from `disconnected raster` (a mask artefact) to `unreachable explored=178 of ~500,000 free cells` — i.e. the start really is in a sealed pocket, about 1.3 mm across.

### 2.2 Using an island's existing copper as anchors

The first corrected version still only used **pad positions** as routing anchors. An island usually already has tracks and vias reaching out of the congested pad field, and those are valid anchors. Adding them did not change the outcome for the sampled nets — the islands that remain are single pads with no copper.

### 2.3 Connectivity-guarded rip-up

`guarded_open()` removes foreign copper bordering the sealed pocket, but **only** where removal does not increase the board-wide native unconnected count — so a redundant parallel path is free to take, and a load-bearing one is refused. Hard exclusions: never a pad, never `/GND` (unless the diagnostic flag is set), never a power net, never a track ≥ 0.5 mm.

Result on `/STM32H743 core/I2C2_SCL`: **15 redundant foreign items removed successfully** (from `/COMPANION_TX`, `/COMPANION_TX_OD`, `/COMPANION_CTS_PORT`, `/TELEM1_RTS`), and the pocket **stayed sealed at `explored=178`**. The items that seal it are not removable candidates.

### 2.4 Ground rip-up diagnostic

Re-run with `/GND` tracks eligible for guarded removal: **zero** GND items were removable inside the pocket, and the result was unchanged (`explored=178`). This rules out "just rip the ground stitching" as a solution.

### 2.5 Direct island stitching (`stitch_islands.py`)

A purpose-built nearest-copper straight/L-path stitcher with exact collision validation closed **0** links, independently confirming that the blockers are congestion rather than a missing short connection.

### 2.6 Freerouting 2.4.1

Run with Java 25 against an exported Specctra DSN. It spent ~55 minutes in the **fanout** stage and never reached the autoroute pass — fanout passes routed 85 / 47 / 46 / 45 SMD pins against a constant **135 unroutable**, at escalating rip-up costs (100 → 400). There is no CLI switch to skip or bound the fanout stage. A long run was relaunched in the background; see §4.

---

## 3. Conclusion

**Stage 10's remaining 73 required links need rip-up-and-reroute of load-bearing signal tracks.** That is a negotiated-congestion routing problem: existing routes must be relocated, not just avoided. No additive method can solve it, and the project's own bounded raster router, a direct stitcher, guarded rip-up and a GND-rip diagnostic have each now been eliminated as sufficient.

This is a **design-level** finding, not an implementation shortfall. It is also consistent with the project's own history: the unrouted count fell from 201 to 96 through incremental additive batches and then stopped falling.

## 4. The three ways to close them

| Option | What it involves | Notes |
|---|---|---|
| **A. Full negotiated-congestion reroute** | let Freerouting (or an equivalent router with rip-up) run to completion and import the `.ses` | Already launched in the background. The import path (`import_session.py`) **rips up every unlocked track** and re-adds the router's result, so it must be trialled and DRC-checked before acceptance — and there is a real risk it produces a *worse* board than the current verified 96-link state. Canonical changes only on acceptance |
| **B. Placement / topology change** | move the blocking components or re-plan the congested region | Outside the Stage 10 release as written. Needs a controlled change request. This is the option most likely to succeed cleanly |
| **C. Accept and record** | carry the 73 links forward as an owned open item at a later gate | Honest, but Stage 10 cannot then be called complete |

**Recommendation:** let the background Freerouting run finish and evaluate its result against the current board **on the trial path only**. If it does not beat 96 links with zero DRC errors, keep the current verified board and take option **B** — a controlled placement change in the congested MCU/sensor region — because additive routing and GND rip-up are now both disproven.

---

## 5. Reproducing this analysis

```powershell
$kpy = "[LOCAL_SOURCE] Files\KiCad\10.0\bin\python.exe"   # pcbnew lives here, not in the venv
Set-Location "[LOCAL_SOURCE] DRONE PROJECT"

# corridor congestion measurement -> qa/stage10-pcb/congestion.json
& $kpy -X utf8 "qa\stage10-pcb\diagnose_congestion.py" 20

# corrected router, dry-run, with guarded rip-up
& $kpy -X utf8 "qa\stage10-pcb\route_fresh.py" `
      --nets "I2C2_SCL" --widths "0.2,0.15" --budget 150 --ripup 12

# add --allow-gnd-rip for the ground-rip diagnostic, and --apply to write the board
```

`route_fresh.py` writes nothing without `--apply`, and even then only saves when the unconnected count actually falls. Every produced path is re-validated with exact shape collision before a single track or via is added, so it cannot introduce a DRC clearance violation.

---

*No project design file was modified in producing this analysis. The board remains at `08727f36…`, 96 unconnected links, 0 DRC errors, 25/25 invariant checks passing.*
