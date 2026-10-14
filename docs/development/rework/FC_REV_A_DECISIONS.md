> Historical technical record. Names and private workstation/session references were neutralized for publication. Dates and assertions describe the recorded stage, not current physical qualification. See the current validation-status page for later checks.

# FC_REV_A — DESIGN DECISIONS LOG

Decisions that were made by the design owner and that everything downstream
depends on. Kept separate from the technical record so a reader can see what was
*authorised* versus what was *measured*.

---

## D-01 — Stackup: 6 layers, 1.60 mm — LOCKED

**Decided by:** design owner, 2026-09-13
**Decision:** keep the 6-layer / 1.60 mm stackup. Do not go to 8 layers; do not
return to 4.
**Basis:** the delivered 4-layer board has 3 routing layers for 302 nets, 1186
pads and 329 parts. Its inner "power" layer carries 1959 mm of signal copper —
more than either outer layer. 4 layers is where the original 79 required open
links came from.
**Route for each signal layer:** F.Cu · SIGNAL_1 · SIGNAL_2 · B.Cu, with GND and
POWER as planes.

## D-02 — Board size: 104 x 104 mm — ACCEPTED

**Decided by:** design owner, 2026-09-13
**Decision:** the board may grow, and the reworked size of **104 x 104 mm** is
accepted. The owner is the founder/designer and confirmed there is no size
limit.
**What changed:** 65.00 x 65.00 mm (4225 mm²) → 104 x 104 mm, by a rigid 1.60x
scale of the whole arrangement. Component utilisation fell **95.3 % → 37 %**.
**Why it was needed:** at 95.3 % coverage there is nowhere to run copper.
Routing channels need roughly a third of the board; there was 4.7 %.
**Consequence accepted:** the enclosure, the mounting pattern and the positions
of the connectors all change. This is a product-level change, not a layout
tweak.
**Evidence:** `board/FC_REV_A_s160_grow.json`, `renders/plane_top.png`

## D-03 — Option C is forbidden

**Decided by:** design owner, 2026-09-13
**Decision:** the board will **not** be shipped with known open connections.
**Standing:** Option A (placement/floorplan revision) is exhausted first; Option
B (changing a constraint) only if A is genuinely exhausted; Option C never.

## D-04 — Errors before warnings

**Decided by:** design owner, 2026-09-13
**Decision:** connectivity errors (`unconnected_items`) are fixed first. The
dangling-track and dangling-via warnings are addressed afterwards, and only
where they carry real risk — stub antennas on high-speed nets, and vias that
perforate the reference plane.
**Never:** trade an error away to clear a warning.
**Measured basis:** deleting all 85 dangling warnings changes the error count by
**zero** (measured on the 6-layer derivative: warnings 47 → 45, unconnected
93 → 93). They are a symptom, not the disease.

---

## D-05 — Relax the via and drill rules — APPROVED

**Decided by:** design owner, 2026-09-13
**Decision:** `min_via_diameter` **0.45 → 0.40 mm** and
`min_through_hole_diameter` **0.25 → 0.20 mm**.
**Why:** five pads on ~0.5 mm pitch inside dense ICs cannot host a 0.45 mm via.
The via-fit test shows two of them accept a 0.40 mm via and the rest accept none
at any size until a vertical channel is cleared.
**Basis for it being safe:** both values are rules this campaign authored, not
fabrication limits. JLCPCB's 6-layer process handles 0.40/0.20 comfortably.
**Consequence accepted:** the fabrication note changes and the board must be
quoted with the smaller via/drill.

## D-06 — Via-in-pad — APPROVED, with filling

**Decided by:** design owner, 2026-09-13
**Decision:** vias may be placed **in the pad** where that is the only position
available, accepting resin filling and plating-over.
**Why:** on a 0.5 mm pitch pad there is nowhere else to put one. Without filling,
solder wicks into the barrel during reflow and starves the joint.
**Consequence accepted:** a paid JLCPCB option; the fabrication note must request
via-in-pad filling on the affected nets.

## D-07 — The DNP-only island convention — APPROVED

**Decided by:** design owner, 2026-09-13
**Decision:** the connectivity bar is read as **"0 REQUIRED unconnected links"**.
A DNP-only island left unconnected is **correct by design**, not a failure.
**Why this is necessary:** the acceptance bar as written is in tension with
itself. "0 DRC errors counting the `unconnected_items` bucket" requires every
island connected; directive §4.5 forbids connecting a no-populate island. Both
cannot hold when a DNP-only island exists.
**Verified basis:** zero copper exists on any net whose pads are all DNP — the
substantive test, measured directly (`verify/DNP_FINDING_2026-09-13.md`).
**Consequence accepted:** the `unconnected_items` bucket will report a non-zero
count that is expected and documented rather than a defect. On the final board
that count is **16**, and all 16 are DNP-only islands with **0 required opens**.

**Superseded in part by D-08.** The 2026-09-13 finding measured the substantive
test on `board/FC_REV_A_step9.kicad_pcb`, which was clean. The board of record
was a later one, and it was **not** clean — see D-08.

---

## D-08 — Strip the copper illegally routed to no-populate nets — DONE

**Decided by:** design owner's standing rule (directive §4.5), executed 2026-09-14
**Finding:** the board of record carried **72 copper items on 10 nets whose pads
are all do-not-populate** — `/CAN interfaces/CAN2_EVAL_*` (5 nets),
`/ESC signal boundary/ESC_CURR_*` (3 nets), `/Storage and status/LED_A` and
`/USB and debug/BOOT_SERVICE`. That is 64 tracks and 8 vias of copper laid for
parts that will never be fitted. §4.5 forbids exactly this.
**How it got there:** it was inherited from a FreeRouting session through the
import chain. It is invisible in every connectivity number — in fact the illegal
copper is what made those islands read as *connected*, so the breach made the
board look better on a ratsnest count.
**Why it was not caught earlier:** the 2026-09-13 finding note measured the
substantive test on a different, earlier board. The note also recommended that
`dnp_check.py` report copper on all-DNP nets directly instead of inferring from a
link count; that recommendation had not been implemented.
**Action:** `tools/dnp_check.py` now runs the direct test first (it is what §4.5
asks, and a link count that necessarily falls with any routing cannot decide the
rule), and `tools/dnp_strip.py` removed all 72 items.
**Consequence accepted:** removing that copper re-opens **16 DNP-only islands**.
That is the correct state under §4.5 — they are deliberate open nets, must not be
routed, and must not be counted as defects. Required opens remained **0**
throughout; the strip did not disconnect anything that matters, because an
all-DNP net has no populated pad and therefore can never hold a required open.
**Evidence:** `reports/final_chain7.log`, `verify/final/dnp_check.txt`

---

## D-09 — Exchange POWER and SIGNAL_2 in the stack — DONE

**Decided by:** design owner's standing rule (the acceptance bar names it),
executed 2026-09-14
**Finding:** the inherited stack was

```
0 F.Cu      signal   ref GND
1 GND       PLANE
2 SIGNAL_1  signal   ref GND
3 POWER     PLANE
4 SIGNAL_2  signal   ref POWER
5 B.Cu      signal   ref SIGNAL_2   <-- NO ADJACENT REFERENCE PLANE
```

B.Cu carries **1456 mm**, 16 % of the board's 9134 mm of routing, and its nearest
solid plane was two dielectrics away. The bar asks for "an adjacent reference
plane per signal layer", so this was a real miss: return current for every B.Cu
trace has to spread laterally through SIGNAL_2 before it reaches POWER.
**Action:** `tools/stack_swap.py` exchanges the contents *and the names* of the
two inner layers. Final stack:

```
0 F.Cu      signal   2998.4 mm   ref GND
1 GND       PLANE        0.0 mm   1 zone
2 SIGNAL_1  signal   2777.7 mm   ref GND
3 SIGNAL_2  signal   1902.3 mm   ref POWER
4 POWER     PLANE        0.0 mm   1 zone
5 B.Cu      signal   1456.1 mm   ref POWER
```

**Nothing was added, deleted or rerouted.** 448 tracks, 1 zone and their layer
names changed index; all 531 vias are through F.Cu–B.Cu and were untouched (the
tool refuses to run if any blind or buried via is present, because their layer
pairs would need remapping too).
**Verification:** DRC before and after the swap are identical — 0 rule
violations, 16 unconnected (all DNP-only), 3 warnings — and required opens,
regressions and the S4 gate are unchanged.
**Consequence accepted:** the Gerber layer order changes. `SIGNAL_2` is now `.g3`
and `POWER` is now `.g4`. Any previous stack drawing is superseded.
**Evidence:** `reports/final_chain8.log`, `reports/kf2_swapped_drc.json`

---

## D-10 — The tools built to close the last links — ADOPTED

**Decided by:** design owner's instruction to finish the board, 2026-09-14
**Decision:** five small, single-purpose tools were written during the endgame
and are part of the deliverable. Each exists because a number was being read as
answering a question it did not answer.

| tool | the question it answers | what it replaced |
|---|---|---|
| `tools/stub_via.py` | where does a via both FIT and CONNECT, and can a stub legally reach it | `via_fit_test.py`'s "max via at the pad centre", which is a far stronger claim than "no via can close this pad" |
| `tools/pad_blockers.py` | which specific item of foreign copper, on which layer, is stopping it | a bare distance with no attribution |
| `tools/nudge_track.py` | move that one item the 0.12 mm needed, and prove the new path is clear before writing it | "the track is in the way" |
| `tools/place_pad_via.py` | is this exact point legal — asked of the rule engine, not of a raster | the copper map, which marks a cell `-1` whenever two different nets' *envelopes* overlap even where the copper has 0.15 mm of real slack |
| `tools/join_points.py` | connect two points of the same net with the shortest clear track on any layer | a multi-layer A\* that reported NO ROUTE for a 1.67 mm straight line |

**Also adopted:** `tools/dnp_strip.py` (D-08) and `tools/stack_swap.py` (D-09).
**Standing rule these encode:** a search aid is not an emission licence. Every
candidate path is re-validated on a second, unexempted map at the DRC threshold
before any copper is written. The one time that rule was broken — a 4.45 mm
search exemption was also treated as permission to emit — the result was a stub
0.05 mm inside a neighbouring pad, and `drc_prune` correctly deleted the whole
gain. That variant is falsified and recorded.

