> Historical technical record. Names and private workstation/session references were neutralized for publication. Dates and assertions describe the recorded stage, not current physical qualification. See the current validation-status page for later checks.

# FC Drone FC Rev A - Stage 03 Entry Brief

Date: 2026-09-07  
Entry status: APPROVED  
Gate condition: SATISFIED on 2026-09-07 by explicit project-control acceptance of all seven Stage 02 exit decisions

## Objective

Create only the controlled KiCad project foundation: project identity, hierarchical sheet skeleton, library tables, initial rules/net classes, revision metadata, net-name registry, and documentation folders. Do not capture detailed circuits and do not create PCB geometry.

## Frozen inputs

- STM32H743VIT6 LQFP100.
- TIM4 PD12-PD15 for M1-M4; SPI1 PA5-PA7 for ICM-42688-P; I2C2 PB10/PB11 for BMP390.
- Before detailed ICM-42688-P circuit capture in Stage 04, obtain and review the current TDK DS-000347 Version 1.9 PDF; the obsolete v1.5 link is not authoritative.
- SDMMC1 PC8-PC12/PD2 for removable microSD.
- FDCAN1 PD0/PD1 required; FDCAN2 PB5/PB6 reserved with transceiver/connector DNP.
- USB FS PA9/PA11/PA12, self-powered/VBUS-sense/no-backfeed.
- USART6 receiver, USART3 GNSS, I2C4 compass, USART2 telemetry, UART7 CM5, UART4 lidar, UART8 AUX.
- External 5.2 V nominal POWER1; OpenESC and USB cannot power FC; CM5 power is separate.
- OpenESC J1-1 and J1-4 are true no-copper NC; first integration uses the controlled interposer.
- `/CURR` is optional DNP/informational on PC1 ADC1.
- The recovered ESC memo's raw-battery self-power instruction is superseded and prohibited. It cannot change the FC power boundary.
- Holybro UBEC 5A SKU 15034 is a RECOMMENDATION/test-shortlist item only; no final production UBEC or supplier is selected.

## OPEN inputs that must remain visible

Final board outline, layer count, mounting, connector placement/MPNs, cable release, exact USB-C and microSD sockets, protection MPNs, external module MPNs, oscillator choice, sensor orientation, and all runtime/bench evidence.

Final POWER1 module/supplier, exact ESC pin-1/keying view, contact suffix, wire/crimp process, and flight-harness release also remain OPEN. Follow `FC_REV_A_MALAYSIA_SOURCING_POLICY_2026-09-07.md` for later procurement work.

## Required Stage 03 deliverables

Create the KiCad project skeleton and hierarchy, project/local library tables, revision metadata, controlled net-label dictionary matching the Stage 02 port contract, initial rule placeholders, documentation/evidence structure, and a Stage 03 handoff. Record the KiCad version and every created file.

## Stop conditions

Stop and return to project control if any proposed foundation change requires reassigning a frozen H743 pin, connecting OpenESC J1-1/J1-4, powering the CM5 from FC, allowing USB backfeed, replacing SDMMC with SPI, removing CAN1, populating CAN2 without approval, or selecting final board geometry/connector placement.
