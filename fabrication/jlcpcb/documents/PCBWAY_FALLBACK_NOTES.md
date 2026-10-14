# PCBWay fallback notes

PCBWay is a fallback only. Request a current six-layer, 1.6 mm controlled-impedance
stack-up and obtain its dielectric data before ordering. **This project defines no
controlled-impedance stack-up at all** (see `JLCPCB_IMPEDANCE_RECORD.md`), so there
is no geometry to reuse: if impedance control is required, it must be derived for
whichever supplier is selected, and the USB pair re-routed to match.

Otherwise preserve: ENIG, the single-board outline, the 0.40/0.20 mm in-pad vias,
the plane pours, and the exact connector part numbers in the BOM. JST GH, GCT and
Molex parts are named by MPN and manufacturer; no unrated substitute should be
accepted for the power connector (`J_POWER1`, Molex 43045-0600).
