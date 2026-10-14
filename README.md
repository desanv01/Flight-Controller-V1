<p align="center">
  <img src="media/hero-top.png" alt="Flight Controller V1 top CAD render" width="49%" />
  <img src="media/hero-bottom.png" alt="Flight Controller V1 bottom CAD render" width="49%" />
</p>

<h1 align="center">Flight Controller V1</h1>

<p align="center">Custom STM32H743 controller design and six-layer PCB implementation</p>

<p align="center">
  <img src="https://img.shields.io/badge/MCU-STM32H743VIT6-03234B?style=flat-square" alt="STM32H743VIT6" />
  <img src="https://img.shields.io/badge/KiCad-10.0-314CB0?style=flat-square" alt="KiCad 10" />
  <img src="https://img.shields.io/badge/PCB-6_layers-426B50?style=flat-square" alt="Six layers" />
  <img src="https://img.shields.io/badge/Status-Engineering_prototype-E6A23C?style=flat-square" alt="Engineering prototype" />
</p>

---

Custom STM32H743VIT6 controller developed through staged schematic capture, resource allocation, placement and a six-layer PCB routing rework. The repository preserves its engineering design, manufacturing data and development record.

**Project contributor:** [Desan Vasu](https://github.com/desanv01). Project engineering activities were performed by Desan; physical fabrication was external. Documented development: 26 August–14 September 2026. These are evidence dates, not employment dates.

> **Current status:** Engineering prototype. Fabrication data is available; assembly sourcing, stack selection and physical validation remain outstanding. No final V1 firmware build is claimed.

**Quick links:** [KiCad project](hardware/FC_REV_A.kicad_pro) · [Schematic PDF](docs/exports/schematic.pdf) · [Manufacturing](fabrication/README.md) · [Development history](docs/development/timeline.md) · [Verification](docs/validation-status.md) · [Releases](https://github.com/desanv01/Flight-Controller-V1/releases)



---

## Table of contents

- [Features](#features)
- [Hardware specifications](#hardware-specifications)
- [Architecture](#architecture)
- [Pin mapping](#pin-mapping)
- [Board layout and wiring](#board-layout-and-wiring)
- [Development history](#development-history)
- [Design and manufacturing files](#design-and-manufacturing-files)
- [Getting started](#getting-started)
- [Firmware](#firmware)
- [Verification](#verification)
- [Repository structure](#repository-structure)
- [License and credits](#license-and-credits)

---

## Features

- STM32H743VIT6 with audited core, debug and clock circuitry
- ICM-42688-P on dedicated SPI and BMP390 barometer
- External regulated power with separate main, analog, sensor and reference rails
- Four motor signal outputs; external CRSF, GNSS, telemetry and companion interfaces
- microSD logging; CAN1 and explicitly reserved/DNP optional functions
- Six copper layers with documented routing, plane-order and DNP corrections
- Native KiCad sources, local libraries, Gerbers/drills and vendor assembly data

---

## Hardware specifications

<details>
<summary>Full specifications and engineering status</summary>

| Parameter | Value |
|---|---|
| MCU | STM32H743VIT6, LQFP100 |
| PCB | 6 copper layers, 1.60 mm nominal |
| Design tool | KiCad 10.0.6 |
| Primary IMU | ICM-42688-P |
| Barometer | BMP390 |
| Power | External regulated input; exact boundary in power-and-interfaces documentation |
| USB | Data/debug; external controller power required |
| Motor signals | 4 controlled outputs |
| CAN | CAN1; optional CAN2 reserved/DNP |
| Storage | microSD |
| Board body | Approximately 104 mm square |
| Mounting | See exact source outline and holes; enlarged floorplan differs from initial 20 mm study |
| Clock | 8 MHz passive HSE crystal |
| Fabrication status | Engineering data available; final part sourcing/stack selection outstanding |

</details>

Specifications describe the design intent and source. Runtime capabilities require physical qualification; see [validation status](docs/validation-status.md).

---

## Architecture

```mermaid
flowchart LR
    POWER[External regulated supply] --> FC[STM32H743 flight controller]
    IMU[ICM42688P and BMP390] --> FC
    RC[CRSF receiver] --> FC
    GPS[External GNSS and compass] --> FC
    FC -->|Motor signals and ground| ESC[OpenESC]
    BAT[Battery and power distribution] --> ESC
    COMP[Separately powered companion] <-->|Advisory data interface| FC
    USB[USB data and debug] <--> FC
```

The controller owns stabilization, motor waveforms, arming and failsafe. Companion perception/navigation is advisory and separately powered. [Architecture and boundaries](docs/architecture.md).

---

## Pin mapping

Four motor signals use PD12–PD15 / TIM4_CH1–CH4. ICM42688P uses SPI1 and BMP390 uses I2C2. microSD is on SDMMC1. [Resource matrix](docs/pin-mapping.md).

The [connector pin tables](docs/connector-pinouts.md) are generated from the exact public netlist. Do not infer connector numbering from another version or from an unlabelled photograph.

---

## Board layout and wiring

<p align="center"><img src="media/layout-top.svg" alt="Flight Controller V1 top PCB layer layout" width="90%" /></p>

<p align="center"><img src="media/wiring/boundaries.svg" alt="Power and signal boundary diagram" width="95%" /></p>

<p align="center"><img src="media/wiring/boundaries.svg" alt="Power and signal boundary diagram" width="95%" /></p>

CAD renders above represent the published source, not photographs of tested hardware. [PCB layer and assembly exports](docs/exports/README.md) · [Power and interfaces](docs/power-and-interfaces.md) · [Bring-up procedure](docs/bring-up.md).

---

## Development history

The [timeline](docs/development/timeline.md) follows requirements, resource freeze, schematic capture, correction, placement, routing and manufacturing stages. Each milestone links its evidence and tag. Publication commits use their actual import date; historical dates remain in the records.

The [development archive](archive/README.md) preserves unique CAD experiments and engineering scripts, including failed approaches. Source fragments are labelled as fragments; no missing historical source state is fabricated.

---

## Design and manufacturing files

| Material | Location |
|---|---|
| Editable current KiCad source | [hardware/](hardware/README.md) |
| Browser-readable schematic and PCB drawings | [docs/exports/](docs/exports/README.md) |
| JLCPCB engineering source and assembly data | [fabrication/jlcpcb/](fabrication/jlcpcb/README.md) |
| PCBWay engineering source and assembly data | [fabrication/pcbway/](fabrication/pcbway/README.md) |
| Downloadable source-associated bundles | [Engineering releases](https://github.com/desanv01/Flight-Controller-V1/releases) |
| Historical sources and experiments | [Archive index](archive/README.md) |

Choose one version and vendor package as a complete set. Do not mix source, Gerbers, BOM or placement files across packages. New public manifests replace original private-package hashes after neutral naming and metadata changes.

---

## Getting started

1. Download or clone this repository.
2. Install KiCad 10 with its standard symbol, footprint and 3D libraries.
3. Open [FC_REV_A.kicad_pro](hardware/FC_REV_A.kicad_pro), then the root schematic and PCB.
4. Review [hardware instructions](hardware/README.md), [verification](docs/validation-status.md) and the correct [vendor package](fabrication/README.md).
5. Review the props-off [bring-up checklist](docs/bring-up.md) before any powered hardware work.

This hardware release has no demonstrated final V1 firmware binary. Resource planning is preserved; a board-specific firmware implementation remains necessary.

---

## Firmware

See [firmware status](firmware/README.md) for resource planning and the missing final-board build.

---

## Verification

Fresh source checks: **14 October 2026**, KiCad **10.0.6**.

| Check | Result |
|---|---|
| ERC errors / warnings | 0 / 12 |
| DRC rule errors / warnings | 0 / 3 |
| Raw unconnected entries | 16 |
| Schematic parity issues | 0 |
| Physical qualification | Pending |


The 16 raw unconnected entries are intentionally isolated DNP-only endpoints; the footprint-attribute checks are included. They remain visible in raw DRC rather than being hidden as a zero-error result.

Ignored checker categories and warning dispositions are recorded in [validation status](docs/validation-status.md). EDA checks and a firmware build do not establish physical reliability or flight qualification.

---

## Repository structure

```text
hardware/       Current coherent KiCad source and libraries
firmware/       Target availability, configuration and build provenance
fabrication/    Vendor-specific source, assembly data and export instructions
docs/           Architecture, pinouts, development history and portfolio case study
media/          Exact-source CAD renders and layer views
verification/   Fresh native reports, corrections and exception evidence
tools/          Portable checking/export utilities
archive/        Recovered source states and indexed development experiments
```

---

## License and credits

Original V1 project material has no blanket redistribution license assigned in this publication; see [licensing scope](LICENSE.md). KiCad-derived libraries, ArduPilot and other third-party content retain their own notices. [Third-party notices](THIRD_PARTY_NOTICES.md).

Desan Vasu performed the project engineering activities; fabrication was external. [Contribution statement](CONTRIBUTIONS.md) · [Portfolio case study](docs/portfolio/case-study.md).

Reference projects: [ArduPilot](https://github.com/ArduPilot/ardupilot), [KiCad](https://www.kicad.org/), and the OpenESC/OpenRX ecosystem identified in the source records.

Related project: [Flight Controller V2](https://github.com/desanv01/Flight-Controller-V2).
