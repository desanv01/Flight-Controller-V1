# PCBWay assembly notes

## Files and why each one exists

| file | PCBWay's requirement |
|---|---|
| `assembly/FC_REV_A-BOM-PCBWay.csv` | "BOM in CSV or Excel format" |
| `assembly/FC_REV_A-Centroid-PCBWay.txt` | "Pick and place file or XYRS data file" |
| `fabrication/gerbers/*` | "Copper, silkscreen, and solder paste layer gerbers in RS274X format" |
| `output/pdf/EVT1_Assembly_Drawings.pdf` | "assembly drawings, special assembly instructions" |
| `output/pdf/EVT1_Harness_Drawing.pdf` | connector pinouts for harness and test |

Sources: <http[LOCAL_SOURCE]>, <http[LOCAL_SOURCE]>, <http[LOCAL_SOURCE]>.

## The centroid, exactly as built

- Format: space-aligned plain text, one header line plus one line per placement.
- Columns: `Designator Footprint Mid X Mid Y Ref X Ref Y Pad X Pad Y TB Rotation Comment`
  which is the column set of PCBWay's own sample centroid file.
- **Units: mm.** PCBWay's note is explicit: "please set the unit to be mm".
- **Origin: bottom-left corner of the board frame**, which is where PCBWay's
  KiCad guide says to place the drill/position offset.
- **SMD only.** PCBWay: "Only surface mounting parts are listed in the Centroid."
  One part on this board has no surface-mount pad at all - `J_POWER1`, the Molex
  43045-0600 power header - and it is therefore absent. Every other part,
  including the USB-C receptacle (which has SMD signal pads plus through-hole
  shield tabs, a hybrid part) is listed, because a hybrid part is still placed
  and reflowed by the machine.
- `Mid X/Y` is the component origin. `Ref X/Y` is the reference-text origin.
  `Pad X/Y` is the centre of pad 1. The last two are derived, and the header of
  the file says so.
- Rotation is KiCad's fabrication rotation normalised to [0, 360). Package
  specific offsets that PCBWay's engineering may ask for are an order-entry
  confirmation, not a design gate.

## Provenance of the centroid

The centroid is not a translation of another file. It is computed from the board
and then checked against KiCad's independent position export:
`verification/pcbway-centroid-review.json` records a maximum disagreement of
**0.000045 mm** in position and **0.000000 degrees** in rotation across
272 placements, with no side mismatches and every derived coordinate inside
the board outline.

## Polarity and orientation

PCBWay asks for polarity to be clear for diodes, LEDs, ICs and tantalum
capacitors. The assembly drawings in `output/pdf/` are plotted from the board and
carry the silkscreen reference designators and the courtyard outlines, so pin 1
and cathode markings visible in the copper and silkscreen layers are the
authority. The preview renders in `preview/` are the 3D cross-check.

## Through-hole parts

PCBWay hand-solders or separately places through-hole parts. On this board:

- `J_POWER1` (Molex 43045-0600, 4 electrical pins + 2 NPTH) - power input
- Mounting holes `H1`-`H4` (M2) are not parts
- Test points `TP1`-`TP15` are exposed pads, not fitted parts

## Before you upload

1. Fill the `Distributors Part Number` column: 281 BOM parts have none.
2. Confirm the centroid row count against the assembly drawing (272 rows).
3. Confirm the stack-up selection (see PCBWAY_STACKUP_RECORD.md).
4. Tell their engineering that the 16 unconnected nets in the DRC report are
   deliberate no-populate islands and must not be "repaired".
