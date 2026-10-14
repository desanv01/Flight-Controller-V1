> Historical technical record. Names and private workstation/session references were neutralized for publication. Dates and assertions describe the recorded stage, not current physical qualification. See the current validation-status page for later checks.

# FC Drone FC Rev A
# Stage 02 Port Contract

Date: 2026-09-07  
Electrical/logical contract status: DECISION  
Connector/mechanical status: OPEN

## 1. Global external-interface rules

- Signal I/O is 3.3 V logic unless stated. Normal range is 0-3.3 V. The protected MCU-side exposure must stay within -0.3 to 3.6 V; no external 5 V logic is accepted directly.
- External 5 V accessory outputs come only from current-limited `5V_AUX`; total auxiliary budget is 1.0 A continuous until a measured load budget raises or lowers it.
- `3V3_REF` is a sense/reference output only, maximum 10 mA, and must never power a CM5 or external module.
- Low-current flight ports should use positive-polarization/retention features appropriate to their chosen family. JST-GH 1.25 mm is the RECOMMENDATION for non-ESC low-current flight ports. OpenESC J1 is separately constrained to JST SH 1.0 mm by the ESC. Exact board header, mate, retention interpretation, orientation, pin-1 view, and placement remain OPEN until the mechanical stage.
- Cable-length bounds below are Stage 02 design limits, not verified signal-integrity results.
- Every externally exposed port requires ESD review in Stage 07. Exact protection MPNs and footprints are OPEN unless listed as a CANDIDATE.

## 2. POWER1 and source contract

DECISION: the FC accepts one externally regulated source at `POWER1`; USB and OpenESC cannot power or backfeed it.

| Parameter | Frozen contract |
|---|---|
| Nominal input | 5.2 V DC |
| Normal operating range at FC connector | 4.9-5.5 V |
| Absolute connector exposure | 0-6.0 V; design must protect downstream rails and not claim operation above 5.5 V |
| Required source capability | at least 2.0 A continuous; 3.0 A transient for 100 ms at the FC connector |
| FC connector current | two parallel 5 V contacts and two parallel GND contacts; 1 A/contact maximum design basis |
| Inrush | FC input stage target at most 1 A for the first 5 ms; exact capacitor/load-switch solution is Stage 05 |
| Backfeed | less than 100 uA steady-state into an unpowered external source from USB, SWD, CM5, ESC, or auxiliary ports; verify in bring-up |
| Raw battery | prohibited on all POWER1 pins |

POWER1 module status remains OPEN. The controlled test shortlist is:

- RECOMMENDATION: Matek `BEC12S-PRO` configured to 5.2 V for electrical headroom; upstream reverse-polarity protection is required.
- RECOMMENDATION: Holybro `UBEC 5A (3-14S)`, SKU `15034`, configured to 5.2 V, as reference/fallback test candidate only and not the final production module or BOM choice.
- CANDIDATE: Hobbywing UBEC 5A V2 Air `30607000` configured to 5.0 V for fixed-6S bench evaluation; 5.0 V is inside the accepted operating window but is not the nominal target.
- CANDIDATE: Matek `mBEC12S` only for conditional low-current evaluation; it does not presently close the full POWER1 current contract.

Follow `FC_REV_A_MALAYSIA_SOURCING_POLICY_2026-09-07.md`. Procurement availability/authenticity, output tolerance/ripple, harness connector, backfeed, conducted/radiated noise, thermal rise, and actual battery-transient behavior remain OPEN and must be measured before final approval.

Proposed logical POWER1 pins, independent of placement:

| Pin | Net | Direction | Treatment |
|---:|---|---|---|
| 1 | `5V_FC_IN_A` | in | parallel with pin 2 at protected entry |
| 2 | `5V_FC_IN_B` | in | parallel with pin 1 at protected entry |
| 3 | GND | return | parallel with pin 4 |
| 4 | GND | return | parallel with pin 3 |
| 5 | `VBAT_SENSE_3V3` | in | 0-3.3 V scaled analog from an external monitor; source OPEN; never raw battery |
| 6 | `PWR_STATUS` | in | 3.3 V logic; default low; DNP if unsupported |

## 3. Port-by-port contract

| Port | Logical pins | MCU resource | Electrical/protocol contract | Cable and reset behavior | Status |
|---|---|---|---|---|---|
| `ESC_INTERPOSER` | J1 exact 1-8 order | TIM4 PD12-PD15; PC1 optional ADC | J1-1 NC no copper; J1-2 GND; J1-3 `/CURR` DNP 0-3.3 V; J1-4 NC no copper; J1-5..8 M1..M4 3.3 V | <=150 mm first bench; no motor command until armed; PWM then DShot300, Bidir300, DShot600, Bidir600; physical cable remains OPEN | DECISION |
| `RC_IN` | `5V_AUX`, GND, FC_TX, FC_RX | USART6 PC6/PC7 | OpenRX Lite-UFL, CRSF full-duplex, uninverted 3.3 V; default 420000 baud; 5 V supply limited to 0.5 A | <=300 mm; receiver loss invokes FC-owned failsafe; CM5 irrelevant | DECISION |
| `GPS1` | `5V_AUX`, GND, FC_TX, FC_RX, SCL, SDA | USART3 PD8/PD9; I2C4 PB8/PB9 | 3.3 V UART default 115200; I2C open-drain at 3.3 V, 400 kHz maximum; 5 V limited 0.5 A | <=300 mm; PPS is separate PD10 test/pad candidate; module/compass MPN remains OPEN | DECISION |
| `TELEM1` | `5V_AUX`, GND, TX, RX, CTS, RTS | USART2 PA2/PA3/PD3/PD4 | 3.3 V full-duplex UART, default 57600, up to 921600 after test; 5 V limited 0.75 A | <=300 mm; exact module remains OPEN and its absence must not block arm/disarm/failsafe | DECISION |
| `CAN1` | `5V_AUX`, CANH, CANL, GND | FDCAN1 PD0/PD1 plus transceiver | ISO 11898-2 high-speed CAN, default 1 Mbit/s, classic CAN first; 5 V limited 0.5 A | twisted pair, <=1 m vehicle harness target; 120 ohm termination DNP/selectable and populated only at a bus end | DECISION |
| `CAN2_EVAL` | same logical pins if populated | FDCAN2 PB5/PB6 | Same as CAN1; second transceiver and connector DNP in initial Rev A unless approved | Reservation is explicit; it does not consume SDMMC, SPI1, USB, SWD, or motor resources | CANDIDATE |
| `COMPANION` | `3V3_REF`, GND, FC_TX, FC_RX, CTS, RTS | UART7 PE8/PE7/PE9/PE10 | 3.3 V UART; default 115200, qualification target 921600; MAVLink; `3V3_REF` <=10 mA | <=300 mm; CM5 carrier separately powered; absence, crash, or stale data cannot affect basic FC safety path | DECISION |
| `LIDAR_FC` | `5V_AUX`, GND, FC_TX, FC_RX | UART4 PA0/PA1 | 3.3 V UART, default 115200; 5 V limited 0.5 A | <=300 mm; scalar range only; exact sensor MPN and final baud remain OPEN | DECISION |
| `AUX_UART` | `5V_AUX`, GND, FC_TX, FC_RX | UART8 PE1/PE0 | 3.3 V UART, default 115200; 5 V limited 0.25 A | <=300 mm; disabled/unassigned by default | RECOMMENDATION |
| `SWD/DEBUG` | SWDIO, SWCLK, NRST, 3V3_REF, GND, optional SWO | PA13/PA14/NRST/PB3 | 3.3 V debug only; no target power injection through `3V3_REF` | short bench lead <=200 mm; BOOT0 has separate labelled recovery pad | DECISION |
| `USB-C` | VBUS, D-, D+, CC1, CC2, shield/GND | PA9/PA11/PA12 | USB 2.0 FS device, self-powered; CC1/CC2 each Rd 5.1 kOhm to GND; VBUS sense only; D+/D- ESD candidate `USBLC6-2SC6` | standard USB cable; no diode, switch, or copper path from VBUS to `5V_FC`, `5V_AUX`, or `3V3`; shield treatment OPEN for EMC review | DECISION |
| `microSD` | CLK, CMD, D0-D3, detect, 3V3, GND | SDMMC1 PC12/PD2/PC8-PC11; PB12 detect | removable microSD, 4-bit SDMMC; 3.3 V only; card-detect recommended | local board interface, not an external harness; exact socket/placement OPEN | DECISION |

## 4. CAN implementation candidates

CAN1 is required and populated. CAN2 is visibly reserved but DNP. RECOMMENDATION for each populated bus is TI `TCAN332DCNR`, a 3.3 V, 1 Mbit/s ISO 11898-2 transceiver in SOT-23-8; exact ESD/common-mode choke parts and termination switch are Stage 07 work. TI source: http[LOCAL_SOURCE] and datasheet Rev F: http[LOCAL_SOURCE]

The second bus consumes PB5/PB6 and one optional transceiver footprint only. These pins do not collide with the motor group, USB, SWD, SDMMC1, SPI1 IMU, or required UARTs. Human approval is required before populating CAN2 or assigning its connector placement.

## 5. Optional `/CURR` DNP circuit contract

The Stage 07 schematic shall provide a visibly DNP branch from interposer/J1-3 to PC1/ADC1:

```text
J1-3 /CURR -> DNP series/protection footprint -> DNP RC/filter footprint -> PC1 ADC1
                                                        |
                                                   labelled test point
```

Requirements: input 0-3.3 V nominal, high impedance relative to the reported approximately 1 kOhm ESC source path, no default pull, no effect on motor control if open/short, and firmware disabled by default. Exact resistor/capacitor/clamp values and MPNs remain OPEN pending calibration data. The signal must never be used for arming, failsafe, motor shutdown, battery sizing, or a safety alarm until D-03/D-04 close.

## 6. Acceptance tests attached to every port

Every port requires unpowered pin-order/short testing, supply-current limit confirmation, powered logic-level measurement, protocol loop/identity test, hot/unplug behavior, reset behavior, and absence behavior. USB additionally requires all-source backfeed measurements. CAN requires termination and dominant/recessive waveform checks. Motor outputs follow the fixed five-step protocol sequence.

Port-contract result: every required port has a bounded electrical and protocol contract. Exact external module models, final connector MPNs/orientation, connector placement, and EMC protection values remain OPEN and must not be converted into final schematic/BOM choices without the stated evidence.
