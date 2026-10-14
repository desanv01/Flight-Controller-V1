# EVT1 mechanical release note

The board is a single integral outline of 104.000 x 104.000 mm with no tabs,
breakaway sections or panel features. The full assembly with every 3D body is
`mechanical/FC_REV_A-FullBoard.step` (69.2 MB).

Mounting features on the board:

| ref | value | note |
|---|---|---|
| H1-H4 | M2 / 2.2 mm | four mounting holes, marked PROVISIONAL in the source |

The seven preview renders in `preview/` are the visual record: top, bottom,
front, back, left, right and isometric. They were produced with
`kicad-cli pcb render` from the released board, so they show exactly the shipped
geometry including the 3D bodies referenced by the footprints.

**Caveat carried from the design record:** the three-dimensional bodies for
several ICs are vendor *envelope* models rather than exact vendor STEP
(`..._ENVELOPE.step`). They are correct in footprint and height class but are not
certified collision geometry. A fit check against a real enclosure should use
measured parts or exact vendor models.
