> Historical technical record. Names and private workstation/session references were neutralized for publication. Dates and assertions describe the recorded stage, not current physical qualification. See the current validation-status page for later checks.

# FC Drone FC Rev A
# Stage 02 STM32H743VIT6 Pin, Timer, DMA, and DMAMUX Matrix

Date: 2026-09-07  
MCU: STM32H743VIT6, LQFP100  
Firmware target: ArduPilot first; PX4 alternative  
Freeze status: DECISION  
Parser feasibility: VERIFIED  
Runtime/bench behavior: OPEN

## 1. Authoritative sources and revisions

| Source | Revision recorded | Use |
|---|---|---|
| ST STM32H742xI/G and STM32H743xI/G datasheet, DS12110 | Rev 11, 357 pages, accessed 2026-09-07 | LQFP100 package pins, alternate functions, reset state |
| ST RM0433 reference manual | Rev 8, accessed 2026-09-07 | DMAMUX/DMA, timers, SDMMC, FDCAN behavior |
| ArduPilot repository | commit `12f1c264f2536c4c9565eec910fa028579845d36` | `STM32H743xx.py`, H743 hwdefs, DMA resolver, parser |
| ArduPilot `FlywooH743Pro/hwdef.dat` | same commit | TIM4_UP non-sharing/priority and SDMMC1 pattern |
| ArduPilot `MatekH743/hwdef.dat` and `HWH7` records | same commit / current master | PD12-PD15 TIM4 motor grouping and bidirectional-DShot precedent |
| TDK ICM-42688-P official product record | DS-000347 Version 1.9 listed, accessed 2026-09-07 | Production status, 0.91 x 2.50 x 3.00 mm package size, and up-to-24 MHz SPI support. Full Version 1.9 PDF pin/register review remains OPEN for Stage 04. |
| Bosch BMP390 datasheet BST-BMP390-DS002 | rev 06 | I2C interface and CSB-at-power-on rule |

Source URLs:

- http[LOCAL_SOURCE]
- http[LOCAL_SOURCE]
- http[LOCAL_SOURCE]
- http[LOCAL_SOURCE]
- http[LOCAL_SOURCE]

## 2. Mandatory core/package pins

| Function | Package pin(s) | Freeze status | Rule |
|---|---:|---|---|
| VDD | 11, 27, 50, 75, 100 | DECISION | Package pins VERIFIED; connect and locally decouple all five in Stage 04. |
| VSS | 10, 26, 49, 74, 99 | DECISION | Package pins VERIFIED; connect all five to ground. |
| VCAP1 / VCAP2 | 48 / 73 | DECISION | Package pins VERIFIED; direct local capacitors only, with no load, signal, or test-point branch. |
| VDDA / VSSA / VREF+ | 21 / 19 / 20 | DECISION | Package pins VERIFIED; implement the filtered analog domain in Stage 04/05. |
| VBAT | 6 | DECISION | Package pin VERIFIED; policy implementation deferred and must never use OpenESC J1-1. |
| NRST | 14 | DECISION | Package pin VERIFIED; preserve SWD and recovery access. |
| BOOT0 | 94 | DECISION | Package pin VERIFIED; default low with recovery access. |
| HSE | PH0 pin 12 / PH1 pin 13 | RECOMMENDATION | Package pins VERIFIED; reserve for an 8 MHz candidate crystal. Exact clock parts remain OPEN. |
| LSE | PC14 pin 8 / PC15 pin 9 | CANDIDATE | Package pins VERIFIED; population remains DNP unless timekeeping requires it. |
| SWDIO / SWCLK | PA13 pin 72 / PA14 pin 76 | DECISION | Package pins VERIFIED; never repurpose. |
| SWO | PB3 pin 89 | RECOMMENDATION | Debug-only candidate; may be a pad rather than a connector position. |
| USB FS VBUS / DM / DP | PA9 pin 68 / PA11 pin 70 / PA12 pin 71 | DECISION | Package pins and alternate functions VERIFIED; VBUS sense only, with no FC power path. |

## 3. Frozen peripheral candidate allocation

| Function | MCU pin(s) and package pin(s) | AF/peripheral | Firmware logical role | Status |
|---|---|---|---|---|
| ESC M1 | PD12 pin 59 | AF2 TIM4_CH1 | PWM(1), `BIDIR` | DECISION |
| ESC M2 | PD13 pin 60 | AF2 TIM4_CH2 | PWM(2), `BIDIR` | DECISION |
| ESC M3 | PD14 pin 61 | AF2 TIM4_CH3 | PWM(3), `BIDIR` | DECISION |
| ESC M4 | PD15 pin 62 | AF2 TIM4_CH4 | PWM(4), `BIDIR` | DECISION |
| IMU SPI SCK/MISO/MOSI | PA5 pin 29 / PA6 pin 30 / PA7 pin 31 | AF5 SPI1 | dedicated `SPI1` | DECISION |
| ICM-42688-P CS | PE3 pin 2 | GPIO CS | `IMU1_CS` | DECISION |
| ICM-42688-P INT1 | PE4 pin 3 | EXTI-capable GPIO | `IMU1_DRDY` | DECISION |
| ICM-42688-P INT2 | PE2 pin 1 | EXTI-capable GPIO | optional second interrupt | RECOMMENDATION |
| BMP390 I2C | PB10 pin 46 / PB11 pin 47 | AF4 I2C2 SCL/SDA | internal I2C bus 0 | DECISION |
| BMP390 INT | PC13 pin 7 | EXTI-capable GPIO | `BARO_INT` | RECOMMENDATION |
| microSD D0-D3 | PC8 pin 65 / PC9 pin 66 / PC10 pin 78 / PC11 pin 79 | AF12 SDMMC1 | 4-bit data | DECISION |
| microSD CK/CMD | PC12 pin 80 / PD2 pin 83 | AF12 SDMMC1 | clock/command | DECISION |
| microSD detect | PB12 pin 51 | GPIO input | `SD_CARD_DETECT` | RECOMMENDATION |
| CAN1 RX/TX | PD0 pin 81 / PD1 pin 82 | AF9 FDCAN1 (`CAN1` in hwdef) | required CAN | DECISION |
| CAN2 RX/TX | PB5 pin 91 / PB6 pin 92 | AF9 FDCAN2 (`CAN2`) | second CAN evaluation; transceiver DNP | CANDIDATE |
| Receiver CRSF TX/RX | PC6 pin 63 / PC7 pin 64 | AF7 USART6 | SERIAL1 | DECISION |
| GNSS TX/RX | PD8 pin 55 / PD9 pin 56 | AF7 USART3 | SERIAL2 | DECISION |
| GNSS PPS | PD10 pin 57 | GPIO/EXTI | capture input candidate | RECOMMENDATION |
| External compass SCL/SDA | PB8 pin 95 / PB9 pin 96 | AF6 I2C4 | external I2C | DECISION |
| Telemetry TX/RX/CTS/RTS | PA2 pin 24 / PA3 pin 25 / PD3 pin 84 / PD4 pin 85 | AF7 USART2 | SERIAL3 with flow control | DECISION |
| CM5 TX/RX/RTS/CTS | PE8 pin 38 / PE7 pin 37 / PE9 pin 39 / PE10 pin 40 | AF7 UART7 | SERIAL4 with flow control | DECISION |
| Scalar lidar TX/RX | PA0 pin 22 / PA1 pin 23 | AF8 UART4 | SERIAL5 | DECISION |
| AUX UART TX/RX | PE1 pin 98 / PE0 pin 97 | AF8 UART8 | SERIAL6 | RECOMMENDATION |
| External VBAT sense | PC0 pin 15 | ADC1_INP10 | battery monitor; external source remains OPEN | DECISION |
| Optional ESC `/CURR` | PC1 pin 16 | ADC1_INP11 | current monitor candidate | DNP |
| FC power-good | PB2 pin 36 | GPIO input | power status | RECOMMENDATION |
| Buzzer | PE5 pin 4 | TIM15_CH1/GPIO | alarm | RECOMMENDATION |
| Status LED | PE6 pin 5 | GPIO output | status | RECOMMENDATION |

## 4. Motor timer/DMA/DMAMUX result

All four motors are one timer group. This is deliberate: the four outputs cannot be configured for mixed rates/protocols, which matches the required M1-M4 ESC bundle.

| Output | Timer request | Parser-selected DMA | DMAMUX request | Bidir input-capture request | Result |
|---|---|---|---|---|---|
| M1 / PD12 | TIM4_UP | DMA1 Stream 2 | `STM32_DMAMUX1_TIM4_UP` | `TIM4_CH1` / `STM32_DMAMUX1_TIM4_CH1` | VERIFIED |
| M2 / PD13 | TIM4_UP | DMA1 Stream 2 | `STM32_DMAMUX1_TIM4_UP` | `TIM4_CH2` / `STM32_DMAMUX1_TIM4_CH2` | VERIFIED |
| M3 / PD14 | TIM4_UP | DMA1 Stream 2 | `STM32_DMAMUX1_TIM4_UP` | `TIM4_CH3` / `STM32_DMAMUX1_TIM4_CH3` | VERIFIED |
| M4 / PD15 | TIM4_UP | DMA1 Stream 2 | `STM32_DMAMUX1_TIM4_UP` | `TIM4_CH4` / `STM32_DMAMUX1_TIM4_CH4` | VERIFIED |

ArduPilot policy lines used in the validation input:

```text
DMA_NOSHARE SPI1* TIM4_UP
DMA_PRIORITY SPI1* TIM4_UP SDMMC*
```

The generated definition sets `HAL_TIM4_UP_SHARED false`, provides `HAL_PWM4_DMA_CONFIG`, and emits input-capture DMA configurations for channels 1-4. This proves that the current ArduPilot H743 generator accepts the candidate without an AF, pin, or DMA allocation conflict. It does not prove signal integrity or actual bidirectional-DShot operation.

## 5. Other generated DMA/IDMA results

| Peripheral | Generated result | Status |
|---|---|---|
| SPI1 IMU RX | DMA1 Stream 0, `STM32_DMAMUX1_SPI1_RX` | VERIFIED |
| SPI1 IMU TX | DMA1 Stream 1, `STM32_DMAMUX1_SPI1_TX` | VERIFIED |
| ADC1 | DMA2 Stream 1, `STM32_DMAMUX1_ADC1` | VERIFIED |
| USART6 RC RX/TX | DMA1 Stream 3 / DMA2 Stream 7 | VERIFIED |
| USART3 GNSS RX/TX | DMA1 Stream 4 / DMA2 Stream 6 | VERIFIED |
| USART2 telemetry RX/TX | DMA1 Stream 5 / DMA2 Stream 5 | VERIFIED |
| UART7 CM5 RX/TX | DMA1 Stream 6 / DMA2 Stream 4 | VERIFIED |
| UART4 lidar RX/TX | DMA1 Stream 7 / DMA2 Stream 3 | VERIFIED |
| UART8 AUX RX/TX | DMA2 Stream 0 / DMA2 Stream 2 | VERIFIED |
| SDMMC1 | H743 SDMMC internal DMA; ArduPilot requires SDMMC-capable memory and reports an 80 MHz expected clock. Card/board test remains OPEN. | VERIFIED |

## 6. ArduPilot hwdef validation

Validation input: `qa/stage02-hwdef-validation/hwdef.dat`  
Generated output: `qa/stage02-hwdef-validation/generated/hwdef.h`  
Tool: official `chibios_hwdef.py` and `dma_resolver.py` from ArduPilot commit `12f1c264...`

Result: command exited 0 and generated `hwdef.h` plus linker/configuration artifacts. The parser accepted every assigned AF, both FDCAN instances, SDMMC1, the dedicated IMU SPI, all UARTs, and the TIM4 motor group.

Limitations:

- The validation uses temporary board ID `9999`, an empty parameter file, and no bootloader embedding. It is not a releasable board definition.
- `BARO BMP388` is intentionally used because ArduPilot's BMP388 backend probes and identifies BMP390; `BARO BMP390` is not a valid backend class name in the checked revision.
- No complete ArduPilot firmware build, bootloader build, hardware test, or PX4 target build was run in Stage 02.
- Sensor orientation remains OPEN until placement.
- TDK's current official product record lists DS-000347 Version 1.9 and verifies the package and SPI capability used at this stage. The full Version 1.9 PDF was not independently extracted in this review, so detailed sensor pin, register, timing, and reference-circuit capture remains OPEN for Stage 04 and must not rely on the retired v1.5 link.

## 7. Abandoned/conflicting candidates

| Candidate | Reason not used |
|---|---|
| USART1 on PA9/PA10 | PA9 is frozen for USB VBUS sense. |
| SPI microSD | Would share a general SPI/DMA resource and reduce logging margin; SDMMC1 is conflict-free. |
| Motor outputs split across TIM1/TIM3/TIM4 | Adds output-group configuration and DMA complexity without benefit for a four-in-one ESC. |
| CAN1 on PB8/PB9 | Conflicts with external-compass I2C4; FDCAN1 uses PD0/PD1 instead. |
| CAN2 omitted silently | Rejected by policy; PB5/PB6 are visibly reserved and the transceiver/connector are DNP candidates. |
| ESC M1-M4 on CM5-generated signals | Prohibited; motor generation remains on the H743. |

## 8. Resource margin

Unassigned usable candidates remain, including PA4, PC4, PC5, PB0, PB1, PE11-PE15, PB13-PB15, PD5-PD7, PB4, and PA15. They are not silently allocated. The TIM1 PE9/PE11/PE13/PE14 group is partly consumed by UART7 flow control (PE9/PE10) and therefore is not treated as a free four-channel motor group.

Matrix conclusion: no incompatible duplicate pin assignment exists. The four motor outputs have accepted timer, DMA, DMAMUX, and ArduPilot `BIDIR` candidates. Runtime DShot/BDShot verification remains OPEN for Stage 13 bench work.
