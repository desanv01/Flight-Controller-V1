# PCBWAY UPLOAD AND ORDER GUIDE — FC_REV_A EVT1

**Board:** FC_REV_A rev A · 104.0 × 104.0 mm · 6 copper layers · 1.60 mm
**Package:** `FC_FC_REV_A_PCBWAY_EVT1/`
**Board sha256:** `2abc737bc6b5e46deef906b0993eaf17877d6815d22cf7111c6b7df0c1ddb999`

This is the PCBWay release of the board. It is the same board as the JLCPCB
package; only the manufacturer-facing files differ (BOM column set, centroid
format, and the addition of ODB++ and IPC-2581, which PCBWay accepts).

---

## 0. WHICH FILES TO UPLOAD

### Bare PCB

| what | file(s) |
|---|---|
| Gerbers (14) | `fabrication/gerbers/` — all of them |
| Drill (2) | `fabrication/drill/FC_REV_A-PTH.drl` and `FC_REV_A-NPTH.drl` |
| Or everything at once | `fabrication/FC_REV_A-PCBWay-fab.zip` |

### Assembly

| what | file |
|---|---|
| **BOM** | `assembly/FC_REV_A-BOM-PCBWay.csv` |
| **Centroid / pick-and-place** | `assembly/FC_REV_A-Centroid-PCBWay.txt` |

### Formats PCBWay accepts that JLCPCB does not ask for

| file | use |
|---|---|
| `fabrication/FC_REV_A-odb` | **ODB++** database (single archive, 472 KB) |
| `fabrication/FC_REV_A.xml` | **IPC-2581** (7.9 MB) |
| `fabrication/FC_REV_A.ipc` | IPC-D-356 netlist |

Upload ODB++ **instead of** the Gerbers if you prefer — PCBWay supports it and
it carries the layer stack and netlist in one file. If you upload ODB++, do
**not** also upload the Gerbers; pick one.

> ### ⚠️ Use `FC_REV_A-BOM-PCBWay.csv`, not `FC_REV_A-BOM.csv`
> The plain `-BOM.csv` is the **engineering BOM** — 12 columns written for a
> person to read. `-BOM-PCBWay.csv` is the same data in PCBWay's ten-column
> turnkey format.

---

## 1. PCB FABRICATION ORDER

### Step 1.1 — Upload

1. Go to <http[LOCAL_SOURCE]> → **PCB Instant Quote**
2. Click **Add Gerber File** (or the ODB++ button if you're using that)
3. Upload `fabrication/FC_REV_A-PCBWay-fab.zip`, or drag in the 14 Gerbers plus
   2 drill files together
4. Wait for the online Gerber viewer to render

### Step 1.2 — VERIFY THE LAYER ORDER — the one that matters most

Check the layer stack reads exactly:

| layer | file | must show |
|---|---|---|
| L1 | `FC_REV_A-F_Cu.gtl` | F.Cu |
| L2 | `FC_REV_A-GND.g1` | **GND plane** |
| L3 | `FC_REV_A-SIGNAL_1.g2` | SIGNAL_1 |
| L4 | `FC_REV_A-SIGNAL_2.g3` | SIGNAL_2 |
| L5 | `FC_REV_A-POWER.g4` | **POWER plane** |
| L6 | `FC_REV_A-B_Cu.gbl` | B.Cu |

L2 must be the **ground plane** and L5 the **power plane**. This board has solid
pours on both and every signal layer references one of them. If PCBWay's
auto-detection swaps them, **the board is electrically ruined and no inspection
will catch it.** The `.gbrjob` file carries the stack, which normally gets this
right — check anyway and do not proceed if it's wrong.

### Step 1.3 — Settings

| option | set to |
|---|---|
| Base Material | FR-4 |
| Layers | **6** |
| Dimensions | **104 × 104 mm** |
| PCB Thickness | **1.6 mm** |
| Solder Mask | Green (your choice) |
| Silkscreen | White |
| Surface Finish | **ENIG** |
| Gold Fingers | No |
| Min Hole Size | **0.20 mm** — see 1.4 |
| Via Covering | **Epoxy Filled & Capped** — see 1.5 |
| Impedance Control | **No requirement** — see 1.6 |

### Step 1.4 — The 0.20 mm drill

The smallest plated hole is **0.200 mm** — 7 vias at 0.40/0.20. The rest are
0.250 mm (524), 0.600 mm slots (4) and 1.020 mm (4).

**Set the minimum hole size to 0.20 mm explicitly.** If PCBWay's instant quote
rejects 0.20 mm for a 6-layer board, do not silently accept a larger minimum —
**come back to me.** The seven 0.40/0.20 vias sit *inside* component pads on a
0.5 mm pitch; enlarging them shortens the clearance to their neighbours and
creates shorts. Fixing it is a board change, not an order setting.

### Step 1.5 — The seven in-pad vias

Seven vias are inside component pads. Select **Epoxy Filled & Capped**
(IPC-4761 Type VII). Without filling, solder wicks down the barrel during reflow
and starves the joint.

### Step 1.6 — Impedance: No requirement

**The design defines no controlled-impedance stack-up.** PCBWay publishes 298
standard stack-ups plus a custom/impedance option; the board fits the standard
6-layer through-hole family. Leave impedance control off unless you intend to
re-route the USB pair — see `PCBWAY_STACKUP_RECORD.md`.

**If you do select a stackup**, record the code you chose in that file so it
matches the delivered hardware.

### Step 1.7 — PCB Remark

Paste this (181 characters):

```
L1 F.Cu/L2 GND/L3 SIGNAL_1/L4 SIGNAL_2/L5 POWER/L6 B.Cu - do not reorder. Min plated hole 0.20mm, 7 in-pad vias, do not enlarge. Epoxy fill+capped. 16 DRC opens are intentional DNP.
```

---

## 2. ASSEMBLY ORDER

### Step 2.1 — Choose the service

PCBWay offers **Turnkey**, **Partial Turnkey** and **Consigned**. Choose
**Turnkey** — PCBWay sources the parts.

Their file-requirements page asks for BOM + Gerber + centroid, and states: *"Only
surface mounting parts are listed in the Centroid."*

### Step 2.2 — Upload

| field | file |
|---|---|
| BOM | `assembly/FC_REV_A-BOM-PCBWay.csv` |
| Centroid | `assembly/FC_REV_A-Centroid-PCBWay.txt` |
| Assembly drawing | `output/pdf/EVT1_Assembly_Drawings.pdf` |
| Reference pictures | `preview/` (the 3D views they ask for) |

**Set assembly side to BOTH.** The board has **146 placements on top and 126 on
the bottom**.

### Step 2.3 — The centroid, exactly as built

- Space-aligned plain text, header plus one line per placement
- Columns: `Designator Footprint Mid X Mid Y Ref X Ref Y Pad X Pad Y TB Rotation Comment`
  — PCBWay's own sample column set
- **Units: mm** (their note: *"please set the unit to be mm"*)
- **Origin: bottom-left corner of the board frame** (their KiCad guide)
- **272 rows** — SMD only. `J_POWER1` (the through-hole Molex power connector) is
  deliberately absent; see 2.5.

Verified: **0.000045 mm** and **0.000000°** maximum disagreement against KiCad's
independent position export.

### Step 2.4 — Part matching

**60 of 84 BOM lines carry a distributor (LCSC) part number. 40 parts do not.**

The lines that will need your attention, in priority order:

**a) Precision resistors — do NOT let them substitute these**

16 lines are **Yageo RT0603BRD series, 0.1% / 25 ppm thin film**, and the design
budget is ±0.5% total for those dividers. PCBWay's sourcing may offer 1% or 5%
thick-film parts of the same value because they're cheaper and in stock.
**Reject that.** The description column says *"Thin film 0.1%, 25ppm/C"* — hold
them to it.

Verified LCSC codes for three of them:

| MPN | value | LCSC |
|---|---|---|
| RT0603BRD0710KL | 10k | **C95204** |
| RT0603BRD0731K2L | 31.2k | **C861319** |
| RT0603BRD0745K3L | 45.3k | **C861415** |

For the other 13, give PCBWay the MPN from the BOM's `Part Number` column and
require 0.1%.

**b) Connectors — JST GH and GCT**

| refs | MPN | note |
|---|---|---|
| J5, J6, J10 | BM06B-GHS-TBT(LF)(SN) | JST GH 6-pin — **out of stock at JLCPCB**, check PCBWay |
| J3, J7 | BM04B-GHS-TBT(LF)(SN) | JST GH 4-pin |
| J4 | BM08B-GHS-TBT(LF)(SN) | JST GH 8-pin |
| J9 | USB4105-GF-A | GCT USB-C |
| J12 | MEM2075-00-140-01-A | GCT microSD — LCSC **C3029735** |

Do **not** accept a clone (`A1257WV-…` etc.) for any JST part. The mating
housing and latch geometry are not guaranteed to match, and these are the
TELEM1 / GPS1 / RC_IN / COMPANION / CAN harness connectors.

**c) Y1 — the 8 MHz crystal**

Pinned to **ABM3B-8.000MHZ-B2-T**, LCSC **C83312**. This matters: JLCPCB's
auto-matcher chose an **ABM8AIG** (3.2 × 2.5 mm) which does **not** fit the
board's ABM3B 5.0 × 3.2 mm land pattern. Y1 is the HSE clock — the MCU does not
run without it. The BOM now names the right part; check PCBWay doesn't
substitute.

**d) FB1 and L2**

| ref | MPN | LCSC |
|---|---|---|
| FB1 | BLM18AG601SN1D (Murata) | **C19330** |
| L2 | XAL7070-682MEC (Coilcraft) | — quote by MPN |

### Step 2.5 — `J_POWER1` is not in the centroid — this is deliberate

`J_POWER1` (Molex **43045-0600**, four through-hole power pins) is in the BOM
but **not** in the centroid, because a pick-and-place machine cannot place a
through-hole part.

**PCBWay may flag this** as a BOM/CPL mismatch — the same prompt JLCPCB raised.
Press **Continue**.

Then either:
- **Hand-solder it yourself.** A 4-pin 3 mm-pitch Micro-Fit header is trivial.
  Buy Molex 43045-0600, or LCSC **C240836**. This is what the JLCPCB order does.
- **Or** ask PCBWay to hand-solder it as a separate labour item.

Their file-requirements page notes: *"Centroid file … is obligatory for SMD
parts. If only THT parts, it is not needed"* — which confirms THT is handled
outside the placement file.

---

## 3. WHAT TO CONFIRM BEFORE PAYING

| check | expected |
|---|---|
| Layers / thickness / size | 6 / 1.6 mm / 104 × 104 mm |
| Layer order | `F.Cu / GND / SIGNAL_1 / SIGNAL_2 / POWER / B.Cu` |
| Minimum hole | **0.20 mm** in the quote |
| Surface finish | ENIG |
| Via covering | Epoxy Filled & Capped |
| Assembly side | **Both Sides** |
| Centroid rows | **272** |
| Placement count | 146 top, 126 bottom |
| Precision resistors | description says **0.1% Thin Film** |
| Y1 | **ABM3B-8.000MHZ-B2-T** / C83312 |
| J_POWER1 | excluded from placement |

---

## 4. WHAT NOT TO ACCEPT

- **Layer reordering** without your explicit confirmation
- **Larger vias** — the 0.40/0.20 vias are in-pad; enlarging them creates shorts
- **1% or 5% substitutes for the 0.1% precision resistors**
- **ABM8AIG for Y1** — wrong package, will not solder down
- **Clone connectors** for the JST parts
- **"Repair" of the 16 unconnected nets** — deliberate no-populate islands;
  directive §4.5 forbids routing them
- **Removal of the DNP pads** — the pads stay, the parts do not

---

## 5. WHERE PCBWAY DIFFERS FROM JLCPCB — the practical list

| | JLCPCB | PCBWay |
|---|---|---|
| BOM columns | `Comment, Designator, Footprint, LCSC Part #` | ten columns incl. Part Number, Manufacturer, MPN, Distributor PN |
| Centroid | CSV, `Designator,Val,Package,Mid X,Mid Y,Layer,Rotation` | space-aligned text, `…Mid X Mid Y Ref X Ref Y Pad X Pad Y TB Rotation Comment` |
| Centroid origin | left/bottom edge corner | **bottom-left corner of the board frame** |
| Extra formats | — | **ODB++**, **IPC-2581** |
| Stackups | fixed JLC codes (JLC06161H-3313 etc.) | 298 standard stackups + custom |

---

## 6. IF SOMETHING GOES WRONG

Paste me the exact error text or screenshot and I'll give you the fix. The
likeliest issues are:

1. **0.20 mm minimum hole** rejected for 6 layers
2. **Part sourcing** — 40 lines have no distributor code
3. **BOM/CPL mismatch** prompt for `J_POWER1` → press Continue
4. **A 1% substitute offered** for a 0.1% resistor → reject it
