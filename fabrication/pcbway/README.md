# Flight Controller V1 — PCBWAY engineering package

Status: engineering data available; physical qualification pending. Final sourcing and stack selection remain outstanding; do not treat this as a completed turnkey order.

## Source and fabrication

Exact source: `source/hardware/`. [Source manifest](source/source-manifest.json). [Fresh source checks](verification/summary.json). Regenerated neutral Gerbers/drills are in `fabrication/`; upload the Gerber/drill-only ZIP rather than a documentation archive. Technical source and electrical/placement geometry are preserved; visible naming and descriptive metadata were updated for publication.

## Assembly files

- [FC_REV_A-BOM-PCBWay.csv](assembly/reference/FC_REV_A-BOM-PCBWay.csv)
- [FC_REV_A-Centroid-PCBWay.txt](assembly/FC_REV_A-Centroid-PCBWay.txt)
- [FC_REV_A-pos-KiCad.csv](assembly/reference/FC_REV_A-pos-KiCad.csv)



Use this vendor's exact BOM and centroid. Confirm rotation and sourcing with the manufacturer. J12 in V1 is microSD; J12 in V2 is POWER1, so designators must not be transferred between versions. [Current connector nets](../../docs/connector-pinouts.md).

## Documentation

Readable neutral exports are in `exports/`. Historical manufacturer notes in `documents/` retain original technical intent but some file references predate publication restructuring; use this README and exact source manifest as the upload map. [Physical checklist](../../docs/bring-up.md).

## Definitive upload map

| Supplier field | Public file |
|---|---|
| PCB fabrication | [Gerber/drill-only ZIP](fabrication/Gerber-Drill-Upload.zip) |
| Assembly BOM | [FC_REV_A-BOM-PCBWay.csv](assembly/reference/FC_REV_A-BOM-PCBWay.csv) |
| SMT placement | [FC_REV_A-Centroid-PCBWay.txt](assembly/FC_REV_A-Centroid-PCBWay.txt) |
| Assembly drawing | [Assembly PDF](exports/assembly.pdf) |
| Fabrication drawing | [Fabrication PDF](exports/fabrication.pdf) |
| Schematic | [Schematic PDF](exports/schematic.pdf) |

Fresh reconciliation: 77 BOM rows, 273 BOM references and 272 placement references. Placement-only references: zero. BOM-only references: `J_POWER1`; these require the separate THT/manual instructions. [Pair report](verification/final-upload-pair.json).

Raw export files under `assembly/reference/` are retained for traceability and are not the supplier upload pair. Part sourcing/rotation/vendor CAM and physical qualification are still required.
