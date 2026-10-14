> Historical technical record. Names and private workstation/session references were neutralized for publication. Dates and assertions describe the recorded stage, not current physical qualification. See the current validation-status page for later checks.

# FC_REV_A — FABRICATION NOTE

**Issued:** 2026-09-14
**Board of record:** `board/FC_REV_A_CANDIDATE.kicad_pcb`
**SHA-256:** `50301399488e99ae72202c91105d79e60bdc7b1b7e4e202ccfce7f7bcd04df93`
**Fabrication data:** `fab_final/`
**Supersedes:** every earlier fabrication note for this board.

---

## 1. What to order

| item | value |
|---|---|
| Layers | **6** |
| Finished thickness | **1.60 mm** |
| Size | **104.05 × 104.05 mm** |
| Copper weight | 1 oz outer / 1 oz inner (recommended) |
| Surface finish | ENIG |
| Solder mask | both sides |
| Silkscreen | both sides |
| Min track width | **0.10 mm** (203 of 3974 tracks) |
| Min via | **0.40 mm pad / 0.20 mm drill** |
| Min pad hole | **0.20 mm** |
| Via count | 531 through vias, 7 of them 0.40/0.20, 524 of them 0.45/0.25 |
| Drill program | 9 tools, 550 holes |
| Components | 329 footprints, 1204 pads, 303 nets, 310 placements |

## 2. Stackup — order matters

| # | Layer | Gerber | Role |
|---|---|---|---|
| 1 | F.Cu | `.gtl` | signal — references GND |
| 2 | GND | `.g1` | **solid plane** |
| 3 | SIGNAL_1 | `.g2` | signal — references GND |
| 4 | SIGNAL_2 | `.g3` | signal — references POWER |
| 5 | POWER | `.g4` | **solid plane** |
| 6 | B.Cu | `.gbl` | signal — references POWER |

Every signal layer has an adjacent solid plane. Both plane layers carry **zero
signal tracks** — power is delivered entirely by pour. See decision **D-09**:
`SIGNAL_2` and `POWER` were exchanged relative to the earlier drawings, so
`SIGNAL_2` is now `.g3` and `POWER` is now `.g4`. **Any earlier stack drawing is
superseded.**

## 3. Options that MUST be quoted

### 3.1 0.20 mm laser-drilled vias — decision D-05

Seven vias are **0.40 mm pad with a 0.20 mm drill**, placed inside dense IC pad
rows where nothing larger fits. The board's own rule floor was relaxed to match
(`min_via_diameter` 0.45 → 0.40, `min_through_hole_diameter` 0.25 → 0.20); this
is a rule this campaign authored, not a fabrication limit. JLCPCB's 6-layer
process handles 0.40/0.20 as standard capability.

### 3.2 Via-in-pad filling and plating over — decision D-06

The 0.40/0.20 vias are **in-pad**: on a 0.5 mm-pitch row there is nowhere else to
put one. Without filling, solder wicks down the barrel during reflow and starves
the joint. **Request resin filling and plating over (IPC-4761 Type VII) on these
vias.** This is a paid option.

Affected pads: `U12.5`, `U12.8`, `U17.7`, `U47.3`, `U50.3`, `U54.10`, and the
`/Power and monitoring/5V_FC_PROTECTED` join at `(23.350, 24.150)`.

### 3.3 Impedance — not requested

No controlled-impedance requirement is placed. The board carries USB 2.0
full-speed, CAN and SPI at their normal rates and the stackup above gives every
layer a solid reference, but no impedance target was simulated or specified by
the design owner. If the fab house offers a free impedance check, the two USB
pairs are the ones worth checking.

## 4. What is already verified

| check | result |
|---|---|
| Copper layers / thickness | 6 / 1.6000 mm |
| DRC rule violations | **0** |
| DRC required unconnected | **0** |
| DRC unconnected, total | 16 — **all DNP-only islands, deliberate** (§4.5, D-07/D-08) |
| DRC warnings | 3 (2 dangling track, 1 dangling via) — accepted under D-04 |
| ERC errors | **0** |
| ERC warnings | 12 (6 isolated pin label, 4 multiple net names, 2 pin-to-pin) |
| Regressions vs Stage-09 handoff | **0**; required opens 79 → 0, 55 nets improved |
| S4 structural gate | **12 / 12 PASS** |
| Copper on all-DNP nets | **0 items** on 26 all-DNP nets (§4.5) |
| Gerbers | 13 files, 6 copper, none empty |
| NC drill | 9 tools, 550 holes, includes the 0.200 mm tool |
| Fabrication drawing | `FC_REV_A_fabrication_drawing.pdf`, 5.18 MB, 13 pages |
| Placement | `FC_REV_A_positions.csv`, 310 placements, both sides |

Evidence: `verify/final/final_verification.json`, `reports/kf2_CANDIDATE_drc.json`,
`reports/candidate_erc.json`, `fab_final/fab_export_report.json`.

## 5. Read this before releasing the order

1. **The 16 unconnected items are not defects.** They are no-populate islands.
   Directive §4.5: "It is NOT a required link. Never route it. Never count it as
   a defect." An earlier board had them connected by 72 pieces of illegal copper;
   that copper has been removed (D-08) and they are correctly open again.
2. **A Gerber export is not a DRC.** The exported data was checked against the
   board's own rule set, and the board itself was DRC'd at 0 rule violations
   after the final zone refill. Re-run `kicad-cli pcb drc` on the exact file you
   send if anything downstream edits it.
3. **The board is 104.05 mm square**, up from the Stage-09 65 mm. Enclosure,
   mounting pattern and connector positions all differ. This is decision D-02 and
   is a product-level change, not a layout tweak.
4. **Do not re-run the router on this board.** Both plane layers are solid pours;
   a rip-up pass that touches them will destroy the power delivery that
   D-09 and the S4 gate verify.
