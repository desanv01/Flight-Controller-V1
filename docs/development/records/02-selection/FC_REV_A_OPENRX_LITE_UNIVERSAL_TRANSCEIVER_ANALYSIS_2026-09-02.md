> Historical technical record. Names and private workstation/session references were neutralized for publication. Dates and assertions describe the recorded stage, not current physical qualification. See the current validation-status page for later checks.

# OpenRX Lite Analysis: Universal Transceiver Suitability

## Short answer

**[DECISION] No—the supplied OpenRX Lite circuit is not a universal transceiver.**

**[RECOMMENDATION] It is suitable as a compact external 2.4 GHz ExpressLRS receiver with bidirectional CRSF telemetry**, provided the aircraft transmitter also uses compatible 2.4 GHz ExpressLRS.

The SX1281 chip itself is a transceiver, but the complete OpenRX Lite product is designed, documented, and firmware-configured as an **ExpressLRS receiver**, not as a general-purpose programmable radio.

---

## 1. What I audited

I reviewed:

- The attached schematic image.
- The legacy [OpenRX family repository](http[LOCAL_SOURCE]
- The current dedicated [OpenRX-Lite repository](http[LOCAL_SOURCE]
- Its README, technical instructions, schematic, PCB, firmware target, and shared KiCad library.
- The [OpenDrone OpenRX product page](http[LOCAL_SOURCE]
- The [OpenRX-Lite-UFL variant](http[LOCAL_SOURCE]
- Official documentation for the [SX1281](http[LOCAL_SOURCE] [ESP32-C3](http[LOCAL_SOURCE] [TLV75533](http[LOCAL_SOURCE] RF filter, antenna, and [ExpressLRS wiring/protocols](http[LOCAL_SOURCE]

The old `OpenRX` repository is mainly a family hub. The dedicated board repositories contain the actual current hardware sources.

---

## 2. What the schematic actually contains

The attached image matches the main architecture of OpenRX Lite:

```text
5 V input
   │
   ▼
TLV75533 3.3 V LDO
   │
   ├── ESP32-C3 MCU
   │     ├── ExpressLRS firmware
   │     ├── CRSF UART to flight controller
   │     ├── Wi-Fi configuration/flashing
   │     └── WS2812B status LED
   │
   └── SX1281 2.4 GHz radio
          │
          ├── 52 MHz TCXO
          ├── 2.4 GHz matching/filter network
          └── ceramic ELRS antenna
```

### Main circuit blocks

| Block | Implemented circuit | Purpose |
|---|---|---|
| MCU | ESP32-C3 | Runs ExpressLRS receiver firmware |
| ELRS radio | Semtech SX1281 | 2.4 GHz LoRa/FLRC radio link |
| RF filter | Johanson 2450FM07D0034T | SX1281 RF matching/filtering |
| Link antenna | Molex 47948-0001 ceramic antenna | 2.4 GHz ELRS antenna |
| Wi-Fi antenna | Johanson 2450AT18A100E | ESP32-C3 Wi-Fi configuration/flashing |
| Clock | 52 MHz TCXO | SX1281 radio reference clock |
| MCU clock | 40 MHz crystal | ESP32-C3 clock |
| Regulator | TI TLV75533PDQNR | Converts external 5 V to 3.3 V |
| Indicator | WS2812B RGB LED | Receiver status indication |
| Interface | Solder pads | 5 V, GND, UART RX, UART TX, BOOT |

The product page identifies the same functional blocks: SX1281, ESP32-C3, RF filter, ceramic antenna, Wi-Fi antenna, 52 MHz TCXO, TLV75533 LDO, and RGB LED.

The screenshot is useful for understanding the topology, but its resolution is not sufficient to verify every passive value, footprint, or MPN. Those should be taken from the machine-readable repository files rather than from the image.

---

## 3. RF section analysis

### Link-radio path

```text
SX1281 RFIO
   │
   ▼
2450FM07D0034T RF filter
   │
   ▼
Molex 47948-0001 ceramic antenna
```

The Johanson filter is an impedance-matched 2.4 GHz filter intended for SX1280/SX1281-type applications. Its published characteristics include approximately 0.75 dB typical insertion loss, 50 Ω operation, and 2.4–2.5 GHz coverage.  
[Johanson filter documentation](http[LOCAL_SOURCE]

The Molex antenna is specified for the 2.4 GHz band, with a published peak gain around 3.7 dBi and total efficiency above 70% under its specified conditions. Actual performance still depends strongly on PCB ground, enclosure, carbon-fibre proximity, and antenna keepout.  
[Molex 47948-0001](http[LOCAL_SOURCE]

### Important limitation

The OpenRX Lite RF path has:

- No power amplifier.
- No low-noise amplifier.
- No RF switch.
- No second frequency band.
- No general-purpose RF connector.

That is acceptable for a small integrated ELRS receiver, but it limits flexibility and RF performance compared with a larger diversity or higher-power transceiver.

The repository documents the Lite model’s telemetry power as **13 dBm / 20 mW**.

---

## 4. MCU and firmware analysis

The ESP32-C3 provides:

- RISC-V processing.
- 2.4 GHz Wi-Fi.
- Bluetooth Low Energy.
- SPI, UART, GPIO, and other peripherals.

However, the ESP32-C3’s Wi-Fi capability does **not** make the board a universal aircraft radio. In OpenRX Lite, Wi-Fi is primarily used for:

- Firmware flashing.
- Configuration.
- ExpressLRS management.

The actual RC link uses the separate SX1281 radio.

The documented firmware target is:

```text
Unified_ESP32C3_2400_RX
```

The target configuration maps:

```text
UART receive: GPIO20
UART transmit: GPIO21

Radio SPI:
SCK  GPIO6
MOSI GPIO4
MISO GPIO5

Radio control:
NSS  GPIO7
RESET GPIO2
BUSY GPIO3
DIO1 GPIO1

RGB LED: GPIO8
```

The current repository documents CRSF as the primary FC protocol.  
[OpenRX-Lite firmware target](http[LOCAL_SOURCE]

---

## 5. Power circuit

```text
External 5 V
    │
    ▼
TLV75533 3.3 V LDO
    │
    ├── ESP32-C3
    ├── SX1281
    ├── TCXO
    └── RGB LED
```

The TLV75533 is a 500 mA, 3.3 V low-dropout regulator with a 1.45–5.5 V input range and protections such as thermal shutdown and current limiting.  
[TI TLV75533 documentation](http[LOCAL_SOURCE]

But this does **not** mean the receiver should be supplied with raw battery voltage.

The OpenRX Lite board requires an external regulated **5 V input**. Its internal LDO only generates 3.3 V for its own circuitry. It is not a BEC for the flight controller, ESC, CM5, or other peripherals.

The actual receiver current consumption is not clearly specified in the public repository. Therefore:

**[OPEN]** The FC 5 V rail should not be sized from the LDO’s 500 mA rating alone. Measure:

- Startup current.
- Normal receive current.
- Telemetry transmit current.
- Wi-Fi configuration current.
- Thermal dissipation from 5 V to 3.3 V.

---

## 6. FC interface and wiring

The OpenRX Lite exposes solder pads rather than a connector.

| OpenRX Lite pad | Receiver function | FC connection |
|---|---|---|
| TP3 / 5V | Receiver supply | Regulated FC 5 V |
| TP4 / GND | Ground | FC ground |
| TP2 / TX | Receiver sends control data | FC UART RX |
| TP1 / RX | Receiver receives telemetry | FC UART TX |
| TP5 / BOOT | Firmware download mode | Normally unused |

The signal directions are important:

```text
OpenRX TX ─────► FC UART RX
OpenRX RX ◄───── FC UART TX
5 V       ────── FC regulated 5 V
GND       ────── FC GND
```

ExpressLRS CRSF requires a normal, uninverted, full-duplex UART pair. The product description’s phrase “one UART wire” should be interpreted as **one UART interface**, not one physical signal wire.  
[ExpressLRS receiver wiring](http[LOCAL_SOURCE]  
[ExpressLRS FC configuration](http[LOCAL_SOURCE]

The OpenRX board itself has no observed dedicated UART ESD protector or external signal-conditioning circuit. Therefore:

**[RECOMMENDATION]** Add protection on the flight-controller side:

- ESD/TVS protection suitable for the UART interface.
- Optional small series-resistor footprints.
- A proper keyed receiver connector on the FC.
- Clearly defined 5 V and GND routing.

Exact protection parts and resistor values should remain **OPEN** until the final connector, cable length, electrical environment, and signal-integrity requirements are known.

---

## 7. Is it a transceiver?

The answer depends on the meaning of “transceiver.”

| Capability | OpenRX Lite status |
|---|---|
| Receive 2.4 GHz ExpressLRS control commands | **YES** |
| Transmit ELRS telemetry back to the transmitter | **YES** |
| Bidirectional ELRS link | **YES** |
| Arbitrary SX1281 TX/RX application | **NO, as supplied** |
| Any RC transmitter brand/protocol | **NO** |
| 900 MHz operation | **NO** |
| Simultaneous 2.4 GHz and 900 MHz operation | **NO** |
| Wi-Fi aircraft-control transceiver | **NO** |
| General-purpose LoRa data modem | **NO, without custom firmware** |
| CRSF receiver interface to a flight controller | **YES** |
| GPS, CAN, USB, lidar, telemetry modem, or FC functions | **NO** |

The ExpressLRS ecosystem supports several serial output protocols, including CRSF, SBUS, SUMD, HoTT, and others. However, the exact OpenRX Lite target is documented primarily for CRSF. Other protocol modes should be treated as **OPEN** until tested on this exact hardware and firmware target.  
[ExpressLRS serial protocols](http[LOCAL_SOURCE]

So the accurate description is:

> OpenRX Lite is a 2.4 GHz ExpressLRS receiver with a bidirectional telemetry link and a CRSF FC interface.

It is not accurately described as a universal transceiver.

---

## 8. OpenRX family comparison

| Model | Radio capability | Antenna | Documented telemetry power | Size |
|---|---|---|---:|---:|
| Lite | 2.4 GHz SX1281 | On-board ceramic | 13 dBm | 10 × 11.5 mm |
| Lite-UFL | 2.4 GHz SX1281 | U.FL external antenna | 13 dBm | 10 × 11.5 mm |
| Mono | 2.4 GHz + 900 MHz | One U.FL | Up to 22 dBm | 10 × 17.3 mm |
| Gemini | Dual-band/Xrossband | Two U.FL connectors | Up to 22 dBm | 17 × 15.7 mm |

[OpenRX family specifications](http[LOCAL_SOURCE]

None of these should automatically be considered universal multi-protocol transceivers. Mono and Gemini expand the **ExpressLRS frequency/receiver options**, but they remain ExpressLRS devices.

For a larger drone installation, **[CANDIDATE] OpenRX-Lite-UFL** may be mechanically preferable because the antenna can be positioned away from:

- ESC switching nodes.
- High-current battery wiring.
- Carbon-fibre plates.
- Motors and motor wires.
- The flight-controller processor and digital interfaces.

That changes antenna installation flexibility; it does not make the receiver protocol-universal.

---

## 9. Strengths of the design

**[VERIFIED] Strengths**

- Very small 10 × 11.5 mm form factor.
- Integrated ESP32-C3 and SX1281.
- Proper dedicated 2.4 GHz RF filter and antenna path.
- Separate Wi-Fi antenna for configuration.
- Bidirectional ELRS telemetry.
- CRSF UART interface compatible with modern flight-controller firmware.
- On-board BOOT access.
- Six-layer, 1.0 mm RF PCB stackup.
- Open KiCad hardware sources.
- Shared OpenDrone library with listed component/footprint provenance.

The repository documents a rev2 fabrication set and a small batch manufacturing trail. That is encouraging, but it is not the same as an independent RF qualification or universal compatibility certification.

---

## 10. Limitations and risks

**[OPEN] Limitations to verify**

1. Exact delivered hardware revision.
2. Commercial availability—the product page still describes the SKU as coming soon.
3. Matching transmitter band and ExpressLRS firmware.
4. Actual current consumption and thermal performance.
5. Antenna performance after installation in the drone.
6. Receiver range and failsafe behavior.
7. Whether any non-CRSF output mode works correctly on this exact target.
8. UART ESD protection for the final FC cable/connector.
9. Actual ERC/DRC and production-fabrication verification for the chosen revision.

The current Lite PCB has only solder pads, with no USB connector, CAN, I²C sensor expansion, GPS interface, or general-purpose data interface. It is intentionally a specialized receiver board.

---

## 11. Recommendation for FC FC Rev A

**[RECOMMENDATION] Use OpenRX Lite only as an external receiver candidate.**

It fits the project’s modular architecture well:

```text
External OpenRX receiver
        │
        │ CRSF full-duplex UART
        ▼
STM32H743 flight controller
```

The FC should provide a receiver interface consisting logically of:

```text
5V_AUX
GND
FC_UART_RX
FC_UART_TX
```

However, the exact connector, pinout, UART instance, and firmware mapping should remain **OPEN** until the receiver and radio-system decisions are confirmed.

Do not modify OpenRX Lite into a universal transceiver for Rev A unless the project specifically wants to undertake:

- Custom SX1281 firmware.
- Custom RF protocol implementation.
- New transmitter-side compatibility.
- RF power and sensitivity redesign.
- New antenna and matching validation.
- EMC and regulatory assessment.
- Extensive range, failsafe, and telemetry testing.

That would become a separate radio-development project rather than a simple FC integration task.

## Final opinion

**[DECISION — analysis only]** OpenRX Lite is a credible, compact **2.4 GHz ExpressLRS receiver**, and its telemetry return makes the overall link bidirectional. It is not a universal transceiver.

**[RECOMMENDATION]** For the FC aircraft, keep it external and design the FC receiver port to be electrically receiver-agnostic. Select Lite if the ceramic antenna installation is suitable; select Lite-UFL if antenna placement and RF isolation matter. Keep all final receiver, connector, protocol, and firmware choices marked **OPEN** until the radio team confirms them.
