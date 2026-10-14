> Historical technical record. Names and private workstation/session references were neutralized for publication. Dates and assertions describe the recorded stage, not current physical qualification. See the current validation-status page for later checks.

# SCHEMATIC PARITY — FINDING AND RESOLUTION

**Opened:** 2026-09-14, by running a check the packages had not run.
**Closed:** 2026-09-14, by Option B for Y2 and `on_board no` for J1/J2.
**Board:** `source/Hardware/FC_REV_A.kicad_pcb`

---

## 1. What was wrong with the checking

`kicad-cli pcb drc` only runs schematic parity when passed `--schematic-parity`.
Earlier runs did not, so the reports showed `schematic_parity: 0` — which reads
as "clean" but meant **"never asked"**. The check was also impossible from the
packages as built, because `source/Hardware/` was missing the root schematic
file entirely. Both were fixed before the check could run at all.

Running it found **3 `missing_footprint` issues**. Both are now **resolved: 0**.

## 2. The three, and how each was closed

| ref | finding | resolution |
|---|---|---|
| **Y2** | 32.768 kHz LSE crystal — schematic said `dnp yes` **and `on_board yes`**, annotated "RESERVED", but the board had no footprint | **Option B** — a real, unpopulated footprint was added (this document, §3) |
| J1 | ESC bench interposer, "positions 1/4 ABSENT" | `on_board no` — it is a bench harness, not a board component |
| J2 | current-sense contact, "CURR contact J1-3: DNP" | `on_board no` — a contact on that harness |

J1 and J2 are described in `04_esc.kicad_sch` as *"J1 has ONLY 2,5,6,7,8. No 1/4
pins, pads, wires or nets. Controlled interposer <=150mm"*. Adding copper for
either would have been wrong; `on_board no` is the KiCad mechanism for "this
symbol is not placed".

## 3. Option B — the Y2 LSE crystal

### 3.1 Why a footprint was worth adding

The board already carried `U1.8`→`C17.1` on `LSE_IN` and `U1.9`→`C18.1` on
`LSE_OUT`: the MCU's LSE pins and **both load capacitors' pads**, with C17 and
C18 marked DNP and their values "TBD". So the capacitors were reserved and the
crystal was not. Without a footprint the LSE could never be fitted, despite the
schematic saying RESERVED. The footprint closes that gap.

### 3.2 What was added

| | |
|---|---|
| Reference | `Y2` |
| Footprint | `FC_REV_A_Local:Crystal_SMD_1610-2Pin_1.6x1.0mm` (new, written into the project library) |
| Size | 1.6 × 1.0 mm, 2-pad SMD — the modern standard 32.768 kHz package (Abracon ABS07, ECS-.327, Micro Crystal CC7V, Seiko SSP-T7 class) |
| Position | (51.00, 53.20) mm, on F.Cu |
| Pads | 0.80 × 1.00 mm, 1.20 mm span → 0.40 mm mask web |
| State | **DNP** — excluded from the BOM placement data and from both CPL/centroid files |
| Routing | Y2.1 → `LSE_IN` in 2.32 mm; Y2.2 → `LSE_OUT` in 0.85 mm, both 0.20 mm track, joined onto the existing net copper |

### 3.3 Why this package and this site

- A **3215** (3.2 × 1.5 mm) crystal fits nowhere in the LSE cluster without
  moving parts; a **2012** had only sites 10 mm away. A **1610** had 745 legal
  sites, the best 1.7 mm from the MCU's LSE pins.
- The site search tests three things per candidate: courtyard clearance on the
  **same side only**, no foreign copper within 0.18 mm of either pad rectangle,
  and a real route to each net. Getting that right took three attempts, each
  caught by DRC rather than by argument:
  1. **Courtyards only** → the crystal landed on top of the two LSE traces
     (LSE_IN at y≈53.5, LSE_OUT at y≈54.0) → `shorting_items` + 2
     `solder_mask_bridge`.
  2. **Disc proxy for the pad** → too coarse: the pad's *corner* approaches a
     diagonal track, so the search passed a site the geometry did not.
  3. **Bottom-side parts counted as occupancy** → C17 and C18 are on **B.Cu**,
     so they cannot physically block an F.Cu part, but `GetBoundingBox()` is
     side-agnostic. Including them made the cluster look full and the search
     reported zero legal sites. Excluding them found 745.

### 3.4 The errata condition — this is not a free upgrade

The footprint is a **reservation, not a licence to populate**. The design record
is explicit:

> ES0392 — PC13 toggling can disturb LSE on LQFP packages. PC13 BARO_INT
> assignment is preserved and LSE is DNP; **any later LSE population requires
> explicit errata review.**

So the board now carries that condition where it cannot be missed:

- **F.Fab text**: *"Y2 LSE DNP - DO NOT FIT WITHOUT STM32H743 ES0392 ERRATA
  REVIEW (PC13 toggling can disturb the LSE on LQFP packages)"* — prints on the
  fabrication drawing.
- Footprint field `Status`: *"DNP - MPN/load capacitance OPEN; PC14/PC15
  reserved"* — matched to the schematic symbol's own value.
- Footprint field `Footprint_Status`: *"RESERVED - footprint defined (1610);
  population requires ES0392 errata review"*.

**Still open before anyone fits it:** the crystal MPN, and the load capacitor
values for C17/C18 (both "TBD"), plus the errata review itself.

## 4. Verification of the resolved state

| check | before Option B | after Option B |
|---|---|---|
| schematic parity | 3 `missing_footprint` | **0** |
| DRC rule violations | 0 errors / 3 warnings | **0 errors / 3 warnings** |
| DRC warnings | 3 (2 `track_dangling`, 1 `via_dangling`) | **same 3, unchanged** |
| required unconnected | 0 | **0** |
| unconnected total | 16 (all DNP-only) | **16, unchanged** |
| copper on all-DNP nets | 0 | **0** |
| S4 structural gate | 12/12 | **12/12** |
| ERC | 0 errors | **0 errors** |
| regressions vs handoff | 0 | **0** |

The board of record is now
`source/Hardware/FC_REV_A.kicad_pcb`, sha256
`2abc737bc6b5e46deef906b0993eaf17877d6815d22cf7111c6b7df0c1ddb999`.

**Fabrication data changed.** Adding a footprint adds pads, mask and paste
openings, so the Gerbers, drill files, STEP, previews, CPL/centroid and both
packages were all rebuilt and re-verified from the new board. Any earlier
archive is superseded.

## 5. What did NOT change

- No existing copper was moved, deleted or re-routed. The two stubs join the
  existing LSE traces; nothing else on those nets was touched.
- No part was relocated.
- The 16 DNP-only islands are untouched and still deliberate.
- The stackup, the plane pours and the layer assignment are unchanged.
