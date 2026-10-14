# JLCPCB UPLOAD AND ORDER GUIDE — FC_REV_A EVT1

**Board:** FC_REV_A rev A · 104.0 × 104.0 mm · 6 copper layers · 1.60 mm
**Package:** `FC_FC_REV_A_ENGINEERING_VALIDATION_EVT1/`
**Board sha256:** `2abc737bc6b5e46deef906b0993eaf17877d6815d22cf7111c6b7df0c1ddb999`

---

## 0. WHICH FILES TO UPLOAD

### For the bare PCB (fabrication)

| what | file(s) |
|---|---|
| Gerbers (14 files) | `fabrication/gerbers/` — all of them |
| Drill (2 files) | `fabrication/drill/FC_REV_A-PTH.drl` and `FC_REV_A-NPTH.drl` |
| Or everything in one go | `fabrication/FC_REV_A-single-board-fab.zip` |

The ZIP is the easy path: it contains the 14 Gerbers, the 2 drill files, the drill
maps and the IPC-D-356 netlist. Either works.

### For assembly (SMT)

| what | file |
|---|---|
| **BOM** | `assembly/FC_REV_A-BOM-JLCPCB.csv` |
| **CPL / pick-and-place** | `assembly/FC_REV_A-CPL-JLCPCB.csv` |

> ### ⚠️ DO NOT UPLOAD `FC_REV_A-BOM.csv`
> That is the **engineering BOM** — 12 columns (`Refs, Value, Footprint, MPN,
> Manufacturer, LCSC, Description, Status, Specification, Datasheet, Qty, DNP`).
> It is written for a person to read and it is **not** JLCPCB's template.
> Uploading it produces a wall of unmatched lines.
>
> `FC_REV_A-BOM-JLCPCB.csv` is the same data in JLCPCB's four-column format:
> `Comment, Designator, Footprint, LCSC Part #` — 76 lines covering 273 placed
> parts. Use that one.

---

## 1. PCB FABRICATION ORDER

### Step 1.1 — Upload the Gerbers

1. Go to <http[LOCAL_SOURCE]> → **Order Now** → **PCB Instant Quote**.
2. Click **Add Gerber file**.
3. Upload `FC_REV_A-single-board-fab.zip`, or drag in all 14 Gerbers plus the 2
   `.drl` files together.
4. Wait for the Gerber viewer to finish parsing.

### Step 1.2 — VERIFY THE LAYER ORDER — this is the one that matters

The viewer shows a layer stack on the right. **Check it reads exactly:**

| layer | file | must show |
|---|---|---|
| L1 (top) | `FC_REV_A-F_Cu.gtl` | F.Cu |
| L2 | `FC_REV_A-GND.g1` | **GND plane** |
| L3 | `FC_REV_A-SIGNAL_1.g2` | SIGNAL_1 |
| L4 | `FC_REV_A-SIGNAL_2.g3` | SIGNAL_2 |
| L5 | `FC_REV_A-POWER.g4` | **POWER plane** |
| L6 (bottom) | `FC_REV_A-B_Cu.gbl` | B.Cu |
| — | `F_Mask.gts` / `B_Mask.gbs` | solder mask |
| — | `F_Silkscreen.gto` / `B_Silkscreen.gbo` | silkscreen |
| — | `F_Paste.gtp` / `B_Paste.gbp` | paste |
| — | `Edge_Cuts.gm1` | board outline |

**Why this matters more than anything else here:** this board has a solid ground
plane on L2 and a solid power plane on L5, and every signal layer is referenced
to one of them. If JLCPCB's auto-detection puts GND on L3 and SIGNAL_1 on L2,
the board is electrically ruined and no inspection will catch it. The `.gbrjob`
file is included and carries the stack, which normally gets this right — but
check it anyway.

**If the order is wrong:** use the layer-assignment dropdowns in the viewer to
fix it and tell them in the order comments that the stack is
`F.Cu / GND / SIGNAL_1 / SIGNAL_2 / POWER / B.Cu`. Do **not** proceed with a
wrong mapping.

### Step 1.3 — Configure the options

| option | set to |
|---|---|
| Base Material | FR-4 |
| Layers | **6** |
| Dimensions | **104 × 104 mm** (should auto-detect) |
| PCB Thickness | **1.6 mm** |
| PCB Color | your choice (green is default/cheapest) |
| Silkscreen | White |
| Surface Finish | **ENIG** (recommended) |
| Gold Fingers | No |
| Material Type | FR-4 |
| Min Hole Size | may auto-select — see 1.4 |
| Via Covering | **Tented** is acceptable; see 1.5 |
| Impedance Control | **leave OFF** — see 1.6 |
| Panel by JLCPCB | **No** (see 2.7 if you want a panel) |

### Step 1.4 — The 0.20 mm drill

The board's smallest plated hole is **0.200 mm** — seven vias use 0.40 mm pad /
0.20 mm drill. There are also 524 vias at 0.45/0.25.

Common 0.20 mm drill tools: 4 plated tools (0.200, 0.250, 0.600 slot, 1.020) and
5 unplated tools.

**If JLCPCB says the hole size is outside their capability for 6 layers:**
- Check whether they offer 0.20 mm as an option you need to select explicitly.
- If they genuinely cannot do 0.20 mm, **do not let them enlarge the vias** —
  the seven 0.40/0.20 vias sit *inside* component pads on a 0.5 mm pitch. Making
  them bigger shortens the clearance to their neighbours and creates shorts.
  Come back to me instead; the alternative is to re-route those seven
  connections, which is a board change, not an order setting.

Confirm in the quote that the drill program shows a **0.200 mm** tool.

### Step 1.5 — The seven in-pad vias

Seven vias sit inside component pads. Without filling, solder wicks down the
barrel during reflow and starves the joint.

- If JLCPCB's DFM flags anything about via-in-pad, request **resin filling and
  plating over (IPC-4761 Type VII)**.
- If "Via Covering" choices are offered, pick the one that fills/plugs rather
  than merely tents, if the price difference is acceptable.

### Step 1.6 — Impedance control: leave it OFF

**The design defines no controlled-impedance stack-up.** There is no `(stackup)`
block in the board file, and the USB pair is routed as ordinary 0.20 mm copper
across three layers with vias.

- Leaving impedance control OFF is correct and matches the design.
- USB Full Speed does not need it.
- If you *do* want impedance control, you must first pick one of JLCPCB's
  standard 6-layer stack-ups and have the USB pair re-routed to match. That is a
  board change and both packages would need rebuilding.

### Step 1.7 — Before you save to cart

- **Do not** accept any offer to "fix" unconnected nets. The 16 unconnected
  items in the DRC report are deliberate no-populate islands — directive §4.5
  forbids routing them.
- **Do not** accept a re-panel with mouse bites inside the outline.
- Note the price and lead time, then **Save to Cart** (do not pay yet — do the
  assembly step first so both go on one order).

---

## 2. SMT ASSEMBLY ORDER

### Step 2.1 — Start assembly

From the cart, click **PCB Assembly** next to the board. Or go to
**PCB Assembly → Quote Now** after the PCB is in the cart.

### Step 2.2 — Choose the service level

- **Standard PCBA** — wider part library, handles more package types, higher
  setup cost. Safer for this board.
- **Economic PCBA** — cheaper, but rejects "standard-only" components. You will
  get a **"Standard Only"** error listing them, with the option to switch to
  Standard or mark those parts "do not place".

This board has 0603/0402 passives, LQFP-100, QFN/WQFN, TSSOP, SOT-23 and several
connectors, including a USB-C receptacle and a microSD socket. **Standard PCBA is
the realistic choice.**

### Step 2.3 — Upload the BOM and CPL

1. **BOM:** `assembly/FC_REV_A-BOM-JLCPCB.csv`
2. **CPL:** `assembly/FC_REV_A-CPL-JLCPCB.csv`
3. Set **Build Quantity** to however many boards you want assembled.
4. If the CPL or BOM fails with *"The Uploaded File Format Is Incorrect"* or
   *"File Processing Failed"*, see §3.

### Step 2.4 — Confirm the BOM/CPL consistency prompt

You will likely see **"Inconsistent Reference Designators Between BOM and CPL"**.

**This is expected and correct.** The CPL has 272 placements; the BOM has 273
parts across 76 lines. The difference is one part, and 18 further references are
deliberately absent from both:

| excluded | count | why |
|---|---|---|
| DNP (do not populate) | 39 refs | not fitted by design |
| Test points / mounting holes | 18 refs | not assembly items |

If the dialog says the unmatched designators are intended to be not placed,
click **Continue**. **Do not** "fix" it by adding them back.

### Step 2.5 — Part matching — this is where the work is

**62 of the 76 BOM lines have no LCSC part number.** Only 14 do. JLCPCB will
show those lines as unmatched with **"No Part Selected"**.

For each unmatched line you have three options:

1. **Search for the part** using the MPN. The engineering BOM
   (`assembly/FC_REV_A-BOM.csv`) has the manufacturer and MPN for 297 of 325
   parts — look the line up there by designator, then paste the MPN into
   JLCPCB's search.
2. **Consign the parts** — buy them yourself and ship them to JLCPCB.
3. **"Do not place this part"** — leave it for hand soldering. Reasonable for
   the connectors if you would rather fit them yourself.

**Watch for the yellow exclamation marks.** These appear when:
- the matched part's model does not exactly match the BOM (case-insensitive,
  spaces ignored)
- the matched package differs from the BOM's package
- the same component is used across several BOM rows
- one row contains multiple component types (mixed prefixes)
- the part needs special handling

**Hover over each one and tick it.** Only ticked components count as selected —
an unticked one silently will not be placed.

### Step 2.6 — Package strings

The `Package` column in the CPL and the `Footprint` column in the BOM are
identical strings by construction (`Capacitor_SMD__C_0603_1608Metric` etc.),
because they are both generated from the same board. If JLCPCB warns that a
package is inconsistent, check it against the engineering BOM's `Specification`
column before accepting a substitute.

### Step 2.7 — Panelisation

If you asked JLCPCB to panelise, you will get:
**"Single Piece, please help me repeat the data"** vs
**"Complete File, just proceed with my own files"**.

Our BOM and CPL are **for a single PCB**. Choose **"Single Piece, please help me
repeat the data"** so the component quantities scale with the panel count.

### Step 2.8 — Checkout review

Before paying, verify:
- Placement count matches the CPL: **272**
- Part quantity per line is sensible (e.g. 49 × 100 nF)
- The 7 in-pad vias and the 0.200 mm drill survived into the final quote
- No part has been silently substituted without your confirmation

---

## 3. ERRORS YOU MAY HIT, AND THE FIX

| message | cause | fix |
|---|---|---|
| **"Parameter Error"** on upload | browser or system locale, not the file | Try another browser, use incognito, or set browser/system language to **English** |
| **"The Uploaded File Format Is Incorrect"** / **"File Processing Failed"** | malformed file, or special characters in the filename | Our files are plain ASCII with no spaces. If it persists, re-download from the ZIP and try again |
| **"No Part Selected"** | no LCSC number on that line | Match manually by MPN or C-code — see §2.5 |
| **"Shortfall"** | JLCPCB stock too low, or the minimum placement quantity/loss allowance exceeds stock | Pick an alternative, or use **Pre-order**, **Global Sourcing** or **Consigned Parts** |
| **"Standard Only"** | you chose Economic PCBA but a part is Standard-only | Switch to **Standard PCBA**, or mark that part "do not place" |
| **"Repeated Designator"** | a designator appears twice, or two designators are closer than 0.2 mm | Should not happen — the CPL is generated from the board and checked. If it does, tell me |
| **"Inconsistent Reference Designators Between BOM and CPL"** | expected here | Click **Continue** — see §2.4 |
| Yellow **!** warnings | matched part needs your confirmation | Hover, read, tick each one — see §2.5 |
| DFM flags **"unconnected nets"** | the 16 DNP-only islands | **Decline any repair.** §4.5 forbids routing them |
| DFM flags **via-in-pad** | the 7 reserved vias | Request resin filling / plating over, or tell me |
| DFM flags **min drill 0.20 mm** | outside a default tier | Check the 0.20 mm option; **do not let them enlarge the vias** |

---

## 4. THINGS TO CONFIRM ON THE FINAL REVIEW SCREEN

1. **6 layers**, **1.6 mm**, **104 × 104 mm**
2. Layer order `F.Cu / GND / SIGNAL_1 / SIGNAL_2 / POWER / B.Cu`
3. Drill program contains a **0.200 mm** tool
4. Surface finish **ENIG**
5. Assembly placement count **272**
6. Every unmatched BOM line resolved or deliberately set to "do not place"
7. No unconnected-net "repair" has been applied
8. The gerber you are ordering is the one from this package
   (sha256 `2abc737bc6b5e46deef906b0993eaf17877d6815d22cf7111c6b7df0c1ddb999`)

---

## 5. WHAT NOT TO ACCEPT

- **Layer reordering** without your explicit confirmation
- **Larger vias** to suit their process — the 0.40/0.20 vias are in-pad and
  enlarging them creates shorts
- **Repair of the 16 unconnected nets** — deliberate, §4.5
- **Silent part substitutions** — the BOM names exact manufacturers and MPNs
- **Removal of the 37 DNP references' pads** — the pads stay, the parts do not

---

## 6. IF SOMETHING GOES WRONG

Paste me the exact error text (and a screenshot if it helps) and I will give you
the fix. The most likely ones are the 0.20 mm drill and the 62 unmatched BOM
lines, and both have real answers rather than "just accept it".

Sources for the error messages above:
[JLCPCB — Common BOM / CPL Matching Issues](http[LOCAL_SOURCE] ·
[JLCPCB — PCBA file requirements](http[LOCAL_SOURCE] ·
[JLCPCB — BOM format](http[LOCAL_SOURCE] ·
[JLCPCB — CPL format](http[LOCAL_SOURCE] ·
[JLCPCB — via filling guide](http[LOCAL_SOURCE]
