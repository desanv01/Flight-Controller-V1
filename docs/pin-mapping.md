# MCU resource mapping

| Function | MCU resource |
|---|---|
| M1–M4 | PD12–PD15 / TIM4_CH1–CH4 |
| IMU SPI1 | PA5 SCK, PA6 MISO, PA7 MOSI; PE3 CS, PE4 DRDY |
| BMP390 I2C2 | PB10 SCL, PB11 SDA; PC13 interrupt |
| microSD SDMMC1 | PC8–PC12 and PD2 |
| CAN1 | PD0 RX, PD1 TX |
| Reserved CAN2 | PB5 RX, PB6 TX; DNP transceiver/connector |
| CRSF USART6 | PC6 TX, PC7 RX |
| GNSS USART3 | PD8 TX, PD9 RX |
| Telemetry USART2 | PA2 TX, PA3 RX; PD3 CTS, PD4 RTS |
| Companion UART7 | PE8 TX, PE7 RX; PE9 RTS, PE10 CTS |
| AUX UART8 | PE1 TX, PE0 RX |
| USB | PA11 DM, PA12 DP; PA9 sensing policy |
| SWD | PA13 SWDIO, PA14 SWCLK |

The former PA0/PA1 lidar interface was retired/reserved; do not reuse it without a controlled resource-map change. Camera/lidar attach to the companion. `/CURR` and optional circuits remain DNP/informational until qualified. Full freeze/correction records are in the interface and sensor milestone pages.

[Actual connector nets](connector-pinouts.md).
