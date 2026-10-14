# Flight Controller V1 — engineering case study

## Objective and role

Custom STM32H743VIT6 controller developed through staged schematic capture, resource allocation, placement and a six-layer PCB routing rework. The repository preserves its engineering design, manufacturing data and development record.

Desan Vasu confirmed performing the project engineering activities except fabrication. 26 August–14 September 2026 is the documented evidence period. No employment title or tenure is inferred.

## Decisions and implementation

- STM32H743VIT6 with audited core, debug and clock circuitry
- ICM-42688-P on dedicated SPI and BMP390 barometer
- External regulated power with separate main, analog, sensor and reference rails
- Four motor signal outputs; external CRSF, GNSS, telemetry and companion interfaces
- microSD logging; CAN1 and explicitly reserved/DNP optional functions
- Six copper layers with documented routing, plane-order and DNP corrections
- Native KiCad sources, local libraries, Gerbers/drills and vendor assembly data

## Engineering result

The development moved from a 65 mm/four-layer placement study and 79 required open routing links to an approximately 104 mm/six-layer source with zero classified required opens, retaining 16 deliberate DNP islands. Final source contains 330 footprints, 3,989 segments and 531 vias. Counts are project-source metrics, not flight-performance results.

| Check | Result |
|---|---|
| ERC errors / warnings | 0 / 12 |
| DRC rule errors / warnings | 0 / 3 |
| Raw unconnected entries | 16 |
| Schematic parity issues | 0 |
| Physical qualification | Pending |


## Lessons

Preserve exact source/vendor pairing, report checker settings and exceptions, distinguish compilation from runtime qualification, and recover historical artifacts without inventing missing source states. Routing space, adjacent reference planes and DNP copper policies drove the custom-board rework.

## Evidence and remaining work

[Source](../../hardware/README.md) · [Timeline](../development/timeline.md) · [Manufacturing](../../fabrication/README.md) · [Verification](../validation-status.md). Physical qualification remains pending. Fabrication was external. Upstream designs/tests remain attributed to their authors.
