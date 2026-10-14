> Historical technical record. Names and private workstation/session references were neutralized for publication. Dates and assertions describe the recorded stage, not current physical qualification. See the current validation-status page for later checks.

# FC_REV_A — STAGE-09 REVIEW AND REWORK RECORD

**Date:** 2026-09-13
**Subject:** the Stage-09 → Stage-10 handoff board, why it cannot be routed, and what was done about it
**Status:** rework in progress — routing pass running
**Working folder:** `[LOCAL_SOURCE] DRONE PROJECT\FC_REV_A_REWORK_2026-09-13\`

---

## 1. What was reviewed

The uploaded project archive (`FC_REV_A.zip`, 445 files, 522 MB) extracted to
`[LOCAL_SOURCE] DRONE PROJECT\stage09_4layer_source\`.

Its board, `FC_REV_A.kicad_pcb`, has sha256 `e4ed6c1e…` — **byte-identical to the untouched C:
original**, so this is the genuine Stage-09 handoff and not a derivative.

| property | value |
|---|---|
| copper layers | **4** — F.Cu / In1.Cu (`GND`) / In2.Cu (`POWER_SLOW`) / B.Cu |
| footprints | 329 |
| nets with pads | 302 |
| pads | 1186 |
| tracks / vias | 5969 / 745 |
| total copper length | 5671 mm |
| zones / rule areas | 12 / 10 |
| board | 65.00 × 65.00 mm = 4225 mm² |

---

## 2. The DRC report, decoded

The report supplied (`USER_DRC_4layer_2026-09-13.rpt`) states **85 violations + 102 unconnected
pads**. Both numbers were independently reproduced from the board and reconcile exactly.

| bucket | count | severity | meaning |
|---|---|---|---|
| unconnected_items | **102** | **error** | the netlist requires a connection the board does not make |
| via_dangling | 54 | warning | via touches copper on only one layer |
| track_dangling | 31 | warning | track end touches nothing |
| footprint errors | 0 | — | — |

**The number that matters: 102 = 79 REQUIRED + 23 DNP-only islands.** DNP-only islands are
deliberate no-populate regions and must never be routed; routing one is a defect in its own
right. So the board has **79 genuine broken connections on 55 nets**, worst being
`3V3_REF` (10), `/5V_AUX` (5), `GPS_5V_OUT` (4), `CAN1_5V_OUT` (4), `USB_VBUS_PORT` (3).

### 2.1 Do the warnings matter?

Not as the blocker, and not as something to fix first.

* A dangling track or via does **not** break a connection that otherwise exists. Measured on the
  6-layer derivative: stripping the dangling stubs took warnings 47 → 45 and left the
  unconnected count at **93, unchanged**.
* They are the **fingerprint** of the real failure — 85 half-finished routes are the other
  halves of the 79 missing links. The report contains tracks of length **0.0250 mm** and
  **0.0024 mm**; the board carries **235 tracks under 0.05 mm** and 48 under 0.01 mm, the
  shortest 0.0001 mm. These are orphan fragments of interrupted routes.
* Where they do carry real risk on this board: dangling stubs exist on `/STM32H743 core/SPI1_MISO`,
  `/USB_DM`, `/USB_DP`, `/SDMMC1_D0` and `/GPS1_PPS` (stub antennas on high-speed nets), and
  every stray via perforates `In1.Cu`, the only solid reference plane.
* **Order of work: connectivity first, warnings last.** Nothing here should be traded for a
  warning.

---

## 3. Root cause

Two measurements, both fatal, neither previously taken.

### 3.1 The board is 95.2 % covered by components

| | |
|---|---|
| board area | 4225 mm² |
| sum of footprint courtyards | **4028 mm²** |
| **component utilisation** | **95.3 %** |

Routing channels need roughly a third of the board. There was **4.7 %**. This single number
explains the whole symptom set — placement legalisation cannot find room, the router reports
"no path" for corridors a human would expect, and the connected count would not fall below 70
under any routing strategy tried.

### 3.2 The "power plane" is the busiest routing layer

| layer | copper length | nets |
|---|---|---|
| F.Cu | 1849 mm | 161 |
| B.Cu | 1863 mm | 136 |
| **In2.Cu (`POWER_SLOW`)** | **1959 mm** | **87** |
| In1.Cu (`GND`) | **0 mm** | 0 — a clean plane |

`In2.Cu` carries **more copper than either outer layer**, including `SPI1_MISO` (116 mm),
`SDMMC1_D0` (51 mm) and **`USB_DM`/`USB_DP` (41 mm each)**.

Consequence, measured: **10 zones compete for that one inner layer**, and the `3V3_REF` pour
there — at the lowest priority — **shatters into 44 separate polygons**, with a duplicate
`3V3_REF` zone at priority 3 alongside it. Every fragment that owns a pad becomes its own
connectivity island. 3V3_REF alone has 11 groups.

**Conclusion: the defect is at Stage 09 — floorplan and stackup — not at Stage 10 routing.**
The schematic is sound: ERC reports 0 errors, 302 nets, correct connectivity intent. The
netlist does not need to be redone.

---

## 4. Rework performed

New working folder: `FC_REV_A_REWORK_2026-09-13\` with `project/`, `board/`, `tools/`,
`reports/`, `work/`, `fr1/`.

### 4.1 ERC repaired

`fix_erc_vcap.py` — ERC reported one ERROR: STM32H743 pins 48 and 73 (both VCAP, both declared
`power_out`) tied together. Pin 73 set to `passive` in **both** the symbol library and the
schematic's cached `lib_symbols` copy (patching only the library does nothing).

**Result: ERC 0 errors.** 12 warnings remain, parked deliberately.

### 4.2 Routability checker built (the tool the plan called for first)

`tools/routability.py` **trial-routes the entire board from scratch** to score a placement,
rather than guessing at difficulty. Baseline:

| placement | index | unroutable nets | plane pads w/ via | sealed pads |
|---|---|---|---|---|
| original 65 × 65 mm | **0.8933** | 28 | 161 / 211 | 0 |
| HPWL-optimised 80 × 80 mm | **0.8483** ❌ | 43 | 145 / 211 | 31 |
| rigid 1.40× → 91 × 91 mm | 0.9236 | 21 | 178 / 211 | 0 |
| **rigid 1.60× → 104 × 104 mm** | **0.9663** | **13** | **514 / 525** | 1 |

**Recorded failures, not hidden:**

* **HPWL re-placement made it worse.** Minimising wirelength pulls parts together; legalisation
  only stops courtyards overlapping, not the pads inside them. It packed parts tightly and
  walled in 31 pads. Lesson: the original hand placement is *good* — its only defect was density.
* **Local net repair made it slightly worse** (0.9259 → 0.9181). Moving a part to fix one net
  breaks another.

### 4.3 The density defect fixed

`tools/scale_place.py` scales the entire arrangement rigidly about the board centre. Every
relative position is preserved, so design intent survives; every clearance scales up, so gaps
that were 0.20 mm become 0.32 mm at 1.6×. All existing tracks and vias removed — they cannot
survive a rigid scale and the board is being routed once, properly, from scratch.

**Result: 65 × 65 → 104 × 104 mm, utilisation 95.3 % → 37 %, 0 courtyard overlaps.**

### 4.4 Three measurement bugs found and fixed in my own tooling

1. **`/GND` was being trial-routed as a signal net.** The board names ground `/GND`; the checker
   hardcoded `GND`. 313 of 679 trial edges — **46 % of every run** — were spent routing a plane
   that already exists. Plane nets are now derived from the board.
2. **The plane-reach test was wrong.** It required a via *exactly at* the pad, which rejects every
   pad in a dense row. A legal 0.5 mm stub to a nearby via closes the net. Fixed with a real
   shortest-path search: plane reachability **478 → 514 of 525**.
3. **A work board whose filename does not match its `.kicad_pro`** makes kicad-cli fall back to
   default rules, producing **199 phantom `track_width`/`via_diameter`/`drill_out_of_range`
   errors** on legal 0.10 mm tracks. Same trap that earlier produced 900 phantom errors.

### 4.5 Routing attempted

| attempt | DRC errors | items pruned | final unconnected |
|---|---|---|---|
| greedy single pass | 767 | 1216 | **499** |
| greedy + 0.06 mm grid-quantisation margin | 402 | 357 | **384** |
| *inherited Stage-09 board, for reference* | 0 | — | *93* |

The margin halved the errors — confirming that grid-snapped routes eat clearance at a 0.10 mm
grid — but **a hand-built greedy router is not competitive** and that line of work was stopped.
FreeRouting 2.4.1 (already in the project) is now routing the new placement.

FreeRouting's first launch failed **silently on all 879 nets** with *"some of their layers are
disabled"*: scaling had left 22 zone outlines as invalid conduction areas. Zones stripped and
the DSN re-exported — correct independently, since the planes must be rebuilt anyway.

---

## 5. Standing

| item | state | evidence |
|---|---|---|
| ERC errors | **0** | `reports/baseline_erc.json` |
| root cause (density) | identified and fixed | `board/FC_REV_A_s160_grow.json` |
| placement quality | **0.9663** | `reports/s160_v2.json` |
| board | 104 × 104 mm candidate, 6 layers | `board/FC_REV_A_s160.kicad_pcb` |
| routing | **in progress** | `fr1/run.log` |
| DRC errors on delivered board | 0 (unchanged) | `reports/baseline_drc.json` |
| **required unconnected links** | **93 — UNCHANGED, bar not met** | `reports/baseline_drc.json` |
| fab export | not started — no legal routed board exists | — |

### 5.1 Not yet done

* Power-plane rebuild (plan step 3): contiguous region per rail, no duplicate zones, **zero
  signal tracks on any plane layer**.
* Final routing on the new placement.
* The 11 stuck plane pads and 13 unroutable nets listed in `reports/s160_v2.json`
  (hotspot: the U12/U13/U14/U16/U17 sensor cluster).
* Fab export and independent DRC re-check.
* The 12 ERC warnings and the dangling-stub warnings — deferred by instruction until the errors
  are closed.

---

## 6. Governance

* Work confined to `[LOCAL_SOURCE] DRONE PROJECT`. The C: original was never written to.
* `[LOCAL_SOURCE] DRONE PROJECT\hardware\FC_REV_A\FC_REV_A.kicad_pcb` (sha256 `bf55996d…`) unmutated.
* The uploaded 4-layer board (sha256 `e4ed6c1e…`) preserved unmodified in
  `stage09_4layer_source/`.
* Every claim in this document is backed by a file path under
  `FC_REV_A_REWORK_2026-09-13/reports/` or `work/`.
* DNP rule enforced: DNP-only islands are never routed.

---

## 7. Addendum — findings since the review was first written

### 7.1 Step 7 is proven before the routed board exists

**Fabrication export** (`tools/fab_export.py`, exercised on the reworked plane board):

| artefact | result |
|---|---|
| Gerbers | **13 layer files, none empty** (independently checked by the tool itself) |
| copper Gerbers | 6 — `F_Cu.gtl`, `GND.g1`, `SIGNAL_1.g2`, `POWER.g3`, `SIGNAL_2.g4`, `B_Cu.gbl` |
| NC drill | `FC_REV_A_plane.drl`, **7 tools** (0.60 … 3.00 mm) |
| fabrication drawing | multipage PDF, 4.5 MB |
| component positions | CSV, **310 placements** |

*Caveat recorded deliberately:* the four inner-layer Gerbers are small (1768 B) because
this export ran **before a zone refill**, so the pours are outlines rather than filled
copper. The pipeline is proven; the Gerbers become representative on the final board.

**Verification chain** (`tools/dnp_check.py`, `compare_required.py`, `final_verify.py`):

* DNP guard on the reworked board: **COMPLIANT — no no-populate island was routed**
  (`verify/dnp_check_plane.txt`). This matters because a DNP breach is invisible to every
  connectivity number; one was missed earlier in this campaign.
* `compare_required.py` has a **precondition that must not be misread**: it compares two
  *routed* boards. Run against the bare plane board (zero copper by construction) it reports
  **+703 "regressions"** — an artefact, not a finding. The correct invocation is
  `final_verify.py --incumbent <Stage-09 handoff> <routed board>`.

### 7.2 Visual evidence

`renders/plane_top.png` (3D, top) and `renders/plane_cu.svg` (all six copper layers plus
outline). What the render supports: components now have clear routing channels between
them, consistent with utilisation falling 95.3 % → 37 %. What it does **not** support:
routing quality, inner-layer plane integrity, or anything electrical. A render is evidence
of geometry, not of correctness.

### 7.3 Two automation defects found and fixed before they could fire

1. **Wrong import target and wrong order.** The armed finish line imported FreeRouting's
   session file onto the *plane* board, while the DSN had been exported from the *zone-free*
   board. Worse, it added planes before the route landed. The correct order — import onto
   the DSN's own board, **then** rebuild planes so the pours refill around the routed copper
   — is now fixed and written into `tools/finish_line.py`'s docstring so it cannot be
   re-broken. Doing it the other way is precisely the defect that shattered the 3V3_REF pour
   into 44 polygons in the delivered board.
2. **A silent twenty-hour hang.** The first finish line polled for the session file with a
   20-hour timeout and **no liveness check**, so a crashed router would have been
   indistinguishable from a slow one for most of a day. It now watches the java process and
   reports explicitly when the router exits without writing a session file.

### 7.4 An error in my own reporting, corrected

In an interim report I stated FreeRouting was "35 minutes in" and running at "25 % CPU
efficiency", and proposed restarting it. Both figures were wrong: elapsed time had been
inferred from how many work rounds had passed rather than read from the process, and the
measured values were **7 minutes** and **131 % of one core**. The process was healthy
throughout and no restart was warranted. All timing claims now carry the measured
start/now pair. This is recorded because the proposed action — interrupting a healthy
routing pass — would have destroyed real work.

### 7.5 Timing constraint on this session

Each work round advances roughly **20 seconds of wall time**. FreeRouting needs on the order
of **30 minutes per pass** and several passes. It therefore **cannot complete within this
session**, and the routed board cannot be imported, verified or exported here. The finish
line runs unattended and liveness-checked, so the result is measured and logged correctly
whenever the router does complete.

**The board described in §7 still carried its original 93 unconnected links and was not
fab-ready.**

---

## 8. ADDENDUM — 2026-09-14. The board is finished

§7 above was written while the re-route was still running and describes an intermediate
state. It is kept unedited because the reasoning in it was sound at the time. This section
records what happened after it.

### 8.1 Outcome against §7's open items

| §7 open item | status now |
|---|---|
| 93 unconnected links | **0 required opens** on the final board (79 on the Stage-09 handoff) |
| Board not fab-ready | **fab-ready**; Gerbers, NC drill, fab drawing and placement CSV exported and independently DRC-checked |
| FreeRouting re-route in flight | completed; three separate runs plateaued at 23, 13 and 14 unrouted. **None of them was the answer** — see 8.2 |
| Finish line unattended | ran; the final board was then closed by five purpose-built tools rather than by the router |

### 8.2 The router was not what finished the board

The third re-route (`fr4b`) plateaued at 14 unrouted after eight passes and was retired. The
board was carried from required 5 to **0** by targeted tools, each written because a number
was being read as answering a question it did not answer (decision **D-10**):

- `stub_via.py` — where a via both **fits** and **connects**, and whether a stub can legally reach it
- `pad_blockers.py` — which specific item of foreign copper, on which layer, is in the way
- `nudge_track.py` — move that one item the 0.12 mm needed, proving the new path first
- `place_pad_via.py` — ask the **rule engine** whether a point is legal, not a rasterised map
- `join_points.py` — connect two points of the same net, any layer

The single most expensive misreading of this campaign is recorded in 8.3.

### 8.3 `via_fit_test.py`'s number is not a closure verdict — the central lesson

`via_fit_test.py` reports "largest through via that fits at the pad centre". That was read as
"this pad cannot be closed", and it is a far stronger claim. A pad in a 0.65 mm-pitch row has
its neighbours' clearance envelopes lapping over its own centre, so the exact-centre test
fails on almost every dense pad **while a perfectly legal via sits a fraction of a millimetre
away**. U54.10 was reported as accepting a via of at most 0.160 mm and was in fact closable
the whole time: once a single 15 mm `PWR_STATUS` track on SIGNAL_2 was moved 0.27 mm (§8.4),
raw geometry showed 0.600 mm of headroom at that same pad centre.

Two further measurement errors are worth naming because they cost rounds each:

- The rasterised copper map marks a cell `-1` whenever two **different** nets' clearance
  *envelopes* overlap, whether or not their copper does. A dense pad row therefore has its
  own centre permanently `-1` on its own layer, so a search over that map can never place a
  legal via there however much room exists. That is why `place_pad_via.py` asks the DRC
  engine instead.
- A search exemption granted so A\* could leave a sealed pad pocket was also treated as
  permission to **emit**. One 4.27 mm stub came out 0.05 mm inside a neighbouring pad;
  `drc_prune` deleted it and the gain it had bought. Every candidate is now re-validated on
  an unexempted map at the DRC threshold before any copper is written.

### 8.4 A §4.5 breach that the earlier finding did not catch

§4.5 of the directive forbids routing no-populate islands. The 2026-09-13 finding note
(`verify/DNP_FINDING_2026-09-13.md`) verified compliance by direct measurement and found
0 copper items on all-DNP nets — **on `FC_REV_A_step9.kicad_pcb`**. The board of record was a
later board, and it carried **72 copper items on 10 all-DNP nets**: 64 tracks and 8 vias laid
for parts that will never be fitted. It was inherited from a FreeRouting import.

It survived every connectivity check because the illegal copper is what made those islands
read as *connected* — the breach made the ratsnest numbers look **better**. The finding note
had also recommended that `dnp_check.py` run the direct test instead of inferring from a link
count; that recommendation was written down and not implemented, so the guard kept printing a
verdict already shown not to decide the rule.

Corrected: `dnp_check.py` now runs the direct test first, `dnp_strip.py` removed all 72 items,
and the board reports **0 copper on 26 all-DNP nets** with 16 DNP-only islands correctly open.
Required opens stayed 0 throughout, because an all-DNP net has no populated pad and so can
never hold a required open.

### 8.5 Two stack changes

**D-05** (0.45/0.25 → 0.40/0.20 via and drill) was decided on 2026-09-13 and **had not
actually been written to the delivered `.kicad_pro`**. It has been applied; without it the
seven 0.40 mm vias produce four DRC errors (`via_diameter`, `drill_out_of_range`).

**D-09**: B.Cu carried 1456 mm — 16 % of the board's routing — with **no adjacent reference
plane**; its nearest solid plane was two dielectrics away. `POWER` and `SIGNAL_2` were
exchanged so all four signal layers sit next to a solid plane. Nothing was added, deleted or
rerouted: 448 tracks and 1 zone changed layer index, and their names changed with them. DRC
before and after the swap is identical.

Final stack:

```
0  F.Cu      signal   2998.4 mm   ref GND
1  GND       PLANE       0.0 mm   1 zone
2  SIGNAL_1  signal   2777.7 mm   ref GND
3  SIGNAL_2  signal   1902.3 mm   ref POWER
4  POWER     PLANE       0.0 mm   1 zone
5  B.Cu      signal   1456.1 mm   ref POWER
```

### 8.6 §7's falsified strategies — additions

Keep the §7 list; four more belong on it.

| strategy | measured result |
|---|---|
| Rigid move of U2/U5/U17 by 0.6 mm | required 5 → 14, errors 0 → 89, regressions 3 → 9. Intra-package pitch is invariant under a rigid move, so the crowding moves with the part |
| Orthogonal-only A\* movement (to stop diagonal corner-cutting) | clearance errors **7 → 22**. Reverted; recorded as a code comment in `tools/astar_paths.py` |
| A bold stub search (`--exempt-mm 0.70 --tries 2500`) | closed 3 links and created 6 errors — a `shorting_items`, a `solder_mask_bridge` pair and 3 clearance violations. `drc_prune` removed the copper and the whole gain with it |
| Relying on the copper map as the oracle for a single point | see 8.3 — the map's `-1` marking made a legal via site unreachable to the search |

### 8.7 Final state

| | |
|---|---|
| Board of record | `board/FC_REV_A_CANDIDATE.kicad_pcb` |
| SHA-256 | `50301399488e99ae72202c91105d79e60bdc7b1b7e4e202ccfce7f7bcd04df93` |
| Required unconnected | **0** |
| DRC rule violations | **0** |
| ERC errors | **0** |
| Regressions | **0** (79 required links closed, 55 nets improved) |
| S4 structural gate | **12 / 12 PASS** |
| Copper on all-DNP nets | **0** |
| Fabrication | 13 Gerbers (6 copper), 9-tool drill, 13-page drawing, 310 placements |

Handoff: `reports/FC_REV_A_HANDOFF_2026-09-14.md`.
Control review, including where this campaign was wrong: `reports/FC_REV_A_CONTROL_REVIEW_2026-09-14.md`.
Fabrication note: `reports/FC_REV_A_FABRICATION_NOTE_2026-09-14.md`.

