# Connector pinouts from the public netlist

Generated from the exact public schematic after neutralization. Pin numbers identify schematic/footprint pins, not cable wire colours. Check actual mating orientation against the source drawing. Mechanical/shield pads can appear as pin entries.

## J1 — ESC BENCH: positions 1/4 ABSENT

| Pin | Net |
|---|---|
| 2 | `/GND` |
| 5 | `/ESC signal boundary/ESC_M1_PORT` |
| 6 | `/ESC signal boundary/ESC_M2_PORT` |
| 7 | `/ESC signal boundary/ESC_M3_PORT` |
| 8 | `/ESC signal boundary/ESC_M4_PORT` |

## J10 — SWD probe / target powered

| Pin | Net |
|---|---|
| 1 | `/USB and debug/SWD_REF_OUT` |
| 2 | `/GND` |
| 3 | `/USB and debug/SWDIO_PORT` |
| 4 | `/USB and debug/SWCLK_PORT` |
| 5 | `/USB and debug/NRST_PORT` |
| 6 | `/USB and debug/SWO_PORT` |

## J11 — BOOT service shunt DNP

| Pin | Net |
|---|---|
| 1 | `3V3_REF` |
| 2 | `/USB and debug/BOOT_SERVICE` |

## J12 — microSD GCT MEM2075

| Pin | Net |
|---|---|
| 1 | `/Storage and status/SD_D2_PORT` |
| 2 | `/Storage and status/SD_D3_PORT` |
| 3 | `/Storage and status/SD_CMD_PORT` |
| 4 | `3V3_REF` |
| 5 | `/Storage and status/SD_CLK_PORT` |
| 6 | `/GND` |
| 7 | `/Storage and status/SD_D0_PORT` |
| 8 | `/Storage and status/SD_D1_PORT` |
| CD | `/SD_CARD_DETECT` |
| SH | `/GND` |

## J2 — CURR contact J1-3: DNP

| Pin | Net |
|---|---|
| 1 | `/ESC signal boundary/ESC_CURR_RAW` |

## J3 — RC_IN

| Pin | Net |
|---|---|
| 1 | `/External UART and I2C ports/RC_5V_OUT` |
| 2 | `/GND` |
| 3 | `/External UART and I2C ports/RC_IN_TX_PORT` |
| 4 | `/External UART and I2C ports/RC_IN_RX_PORT` |

## J4 — GPS1

| Pin | Net |
|---|---|
| 1 | `/External UART and I2C ports/GPS_5V_OUT` |
| 2 | `/GND` |
| 3 | `/External UART and I2C ports/GPS1_TX_PORT` |
| 4 | `/External UART and I2C ports/GPS1_RX_PORT` |
| 5 | `/External UART and I2C ports/GPS1_SCL_PORT` |
| 6 | `/External UART and I2C ports/GPS1_SDA_PORT` |
| 7 | `/External UART and I2C ports/GPS1_PPS_PORT` |
| 8 | `unconnected-(J4-Pad8)` |

## J5 — TELEM1

| Pin | Net |
|---|---|
| 1 | `/External UART and I2C ports/TELEM_5V_OUT` |
| 2 | `/GND` |
| 3 | `/External UART and I2C ports/TELEM1_TX_PORT` |
| 4 | `/External UART and I2C ports/TELEM1_RX_PORT` |
| 5 | `/External UART and I2C ports/TELEM1_CTS_PORT` |
| 6 | `/External UART and I2C ports/TELEM1_RTS_PORT` |

## J6 — COMPANION

| Pin | Net |
|---|---|
| 1 | `/External UART and I2C ports/COMP_REF_OUT` |
| 2 | `/GND` |
| 3 | `/External UART and I2C ports/COMPANION_TX_PORT` |
| 4 | `/External UART and I2C ports/COMPANION_RX_PORT` |
| 5 | `/External UART and I2C ports/COMPANION_CTS_PORT` |
| 6 | `/External UART and I2C ports/COMPANION_RTS_PORT` |

## J7 — CAN1

| Pin | Net |
|---|---|
| 1 | `/CAN interfaces/CAN1_5V_OUT` |
| 2 | `/GND` |
| 3 | `/CAN interfaces/CAN1_CANH` |
| 4 | `/CAN interfaces/CAN1_CANL` |

## J8 — CAN2_EVAL

| Pin | Net |
|---|---|
| 1 | `/CAN interfaces/CAN2_EVAL_5V_OUT` |
| 2 | `/GND` |
| 3 | `/CAN interfaces/CAN2_EVAL_CANH` |
| 4 | `/CAN interfaces/CAN2_EVAL_CANL` |

## J9 — USB-C GCT USB4105

| Pin | Net |
|---|---|
| A1 | `/GND` |
| A12 | `/GND` |
| A4 | `/USB and debug/USB_VBUS_PORT` |
| A5 | `/USB and debug/USB_CC1` |
| A6 | `/USB and debug/USB_DP_PORT` |
| A7 | `/USB and debug/USB_DM_PORT` |
| A8 | `unconnected-(J9-SBU1-PadA8)` |
| A9 | `/USB and debug/USB_VBUS_PORT` |
| B1 | `/GND` |
| B12 | `/GND` |
| B4 | `/USB and debug/USB_VBUS_PORT` |
| B5 | `/USB and debug/USB_CC2` |
| B6 | `/USB and debug/USB_DP_PORT` |
| B7 | `/USB and debug/USB_DM_PORT` |
| B8 | `unconnected-(J9-SBU2-PadB8)` |
| B9 | `/USB and debug/USB_VBUS_PORT` |
| S1 | `/USB and debug/USB_SHIELD` |
| S2 | `/USB and debug/USB_SHIELD` |
| S3 | `/USB and debug/USB_SHIELD` |
| S4 | `/USB and debug/USB_SHIELD` |

## J_ESC_FC — SM05B-SRSS-TB

| Pin | Net |
|---|---|
| 1 | `/GND` |
| 2 | `/ESC signal boundary/ESC_M1_PORT` |
| 3 | `/ESC signal boundary/ESC_M2_PORT` |
| 4 | `/ESC signal boundary/ESC_M3_PORT` |
| 5 | `/ESC signal boundary/ESC_M4_PORT` |

## J_POWER1 — 43045-0600

| Pin | Net |
|---|---|
| 1 | `5V_FC_IN_A` |
| 2 | `/GND` |
| 3 | `5V_FC_IN_A` |
| 4 | `/GND` |
