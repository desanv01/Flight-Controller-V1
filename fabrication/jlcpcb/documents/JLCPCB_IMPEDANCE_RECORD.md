# Controlled-impedance record

## What the source defines

**Nothing.** The board file contains a `(thickness 1.6)` and a default dielectric
stack; there is no `(stackup ...)` block and therefore no controlled-impedance
stack-up is defined in this design. This is a measured statement, not an
assumption: `verification/` records the export of the stack exactly as the board
carries it.

## What is on the board that might want impedance control

| net pair | width | layers used | vias |
|---|---|---|---|
| `/USB_DP` | 0.20 mm | F.Cu, SIGNAL_1, SIGNAL_2 | 7 |
| `/USB_DM` | 0.20 mm | F.Cu, SIGNAL_1, SIGNAL_2, B.Cu | 4 |
| CAN pairs (`CAN1_CANH/CANL`, `CAN2_EVAL_CANH/CANL`) | as netclass | mixed | - |

The USB data pair is routed as general copper at the 0.20 mm netclass width and
changes layer through vias. There is **no diff-pair geometry defined in any
netclass** (`diff_pair_width` and `diff_pair_gap` are both at their 0.20 mm
defaults and unused). No external USB PHY appears in the BOM, so the pair runs to
the MCU's own USB pins.

## Consequence

- If this link is used at **USB Full Speed**, impedance control is not required
  and the routing above is acceptable.
- If **USB High Speed** is intended, this pair must be re-routed as a matched
  differential pair against a stack-up obtained from the chosen manufacturer, and
  the geometry recorded here before ordering.

That choice is the design owner's; it is not settled by this package.
