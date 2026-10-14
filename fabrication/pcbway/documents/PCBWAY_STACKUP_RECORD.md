# PCBWay stack-up record

## What the design defines

**Nothing.** The board file carries `(thickness 1.6)` and a default dielectric
stack; there is no `(stackup ...)` block. No controlled-impedance stack-up is
defined in this design. That is a measured statement about the source files, not
an assumption.

## What PCBWay offers

From PCBWay's own multi-layer laminated structure page
(<http[LOCAL_SOURCE]>):

- They publish **298 standard stack-ups**, filterable by layer count (4 to 18),
  finished thickness (0.4 to 2.4 mm), inner copper (0.5 to 5 oz), outer copper
  (1 to 5 oz) and inner-layer residual copper ratio (30/50/70/90 %).
- A 6-layer, 1.6 mm, 1 oz/1 oz, 70 % residual stack-up is among their standard
  4-layer entries and the same family covers 6 layers.
- Their prepreg types and thicknesses are stated: **1080 (3.1 mil), 3313
  (4.2 mil), 2116 (5.4 mil), 7628 (7.7 mil)**, with core as the rigid
  copper-clad material between them.
- For anything outside the standard set they say: choose *Customized Services
  and Advanced Options* then *Custom stackup* or *Impedance control*, and they
  will calculate against the supplied stack-up, material and impedance data and
  confirm with the customer.

## What this means for this board

The board is a **through-hole-via, 6-layer, 1.6 mm** design with 531 through
vias and no blind or buried vias, so it fits the standard through-hole stack-up
family that PCBWay's page explicitly says its diagrams cover.

**Action required before ordering:** select the specific 6-layer / 1.6 mm /
1 oz stack-up from PCBWay's current tool and record the chosen code here. This
package cannot choose it for you, and inventing a stack-up table would be worse
than leaving it open.

## Impedance

No controlled impedance is specified by the design. Measured facts about the
board, for whoever decides:

| net pair | width | layers | vias |
|---|---|---|---|
| `/USB_DP` | 0.20 mm | F.Cu, SIGNAL_1, SIGNAL_2 | 7 |
| `/USB_DM` | 0.20 mm | F.Cu, SIGNAL_1, SIGNAL_2, B.Cu | 4 |

No diff-pair geometry is defined in any netclass, and no external USB PHY appears
in the BOM. At USB Full Speed the routing above is acceptable as-is. If USB High
Speed is intended, the pair must be re-routed as a matched pair against a
stack-up obtained from PCBWay, and the geometry recorded before ordering.

## Dielectric record

Not applicable yet: no stack-up has been selected, so there is no dielectric
data to carry. Once PCBWay confirm the stack-up, their dielectric table should be
recorded here alongside the trace geometry.
