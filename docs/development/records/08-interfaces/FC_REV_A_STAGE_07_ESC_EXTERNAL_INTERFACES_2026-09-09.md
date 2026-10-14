> Historical technical record. Names and private workstation/session references were neutralized for publication. Dates and assertions describe the recorded stage, not current physical qualification. See the current validation-status page for later checks.

# FC Rev A — Stage 07 ESC and external interfaces

Date: 2026-09-09. Scope: schematic capture and verification only. **RECOMMENDATION / OPEN UNTESTED.**

Stage 07 implementation is complete. Native connectivity, frozen-resource preservation and the controlled symbol pin tables have been checked. This is **not electrical system release, flight approval, a clean-ERC claim, or Stage 08 authorization**. The voltage-drop, remote-adapter, brownout, ESD, timing and physical tests below remain OPEN. In particular, the accepted 25 mΩ external-path planning allowance does not cover a worst-case JST-GH cable loop; this report does not silently replace that frozen assumption.

## Delivered capture and boundaries

The five previously empty sheets now contain the ESC boundary, external UART/I2C ports, CAN, USB/SWD/boot service, and microSD/status circuits. There are 163 new components including DNP options, bringing the native project to **326 components and 302 nets**. The 606 new component-pin connections pass the expected-net check. The project-local library adds 15 symbols with 108 explicitly audited pins.

The MCU sheet received only appended boundaries for 40 frozen signals and the existing reference rail. All its original records are unchanged. The power sheet received exactly the explicitly approved `5V_AUX` output hierarchical label and short wire at TP10. Root changes join those boundaries and rearrange only the five formerly empty sheet boxes, with a small MCU-box top-edge/title adjustment for the added pins. All earlier component-pin connectivity is unchanged. The sensor sheet is byte-identical. The current control state, retained ledger and earlier handoffs were not edited. No PCB file, footprint geometry, stackup, routing, fabrication output, procurement or manufacturer contact was created.

Canonical files are under `hardware/FC_REV_A/`; evidence is in `hardware/FC_REV_A/docs/evidence/stage07-interfaces/`; scripts, intermediate checks and final QA are in `qa/stage07-interfaces/`. The authoritative final outputs are `verification_final/`, not the intermediate iterations.

## Frozen resources and interface decisions

| Boundary | Frozen MCU resources | Captured treatment / default |
|---|---|---|
| ESC M1–M4 | PD12–PD15, TIM4 | U20 TMUX1511 bidirectional paths, 0 Ω series, 47 kΩ low bias on both sides, U21 rail-less ESD; no unidirectional motor buffer |
| ESC current | PC1 | J2, R69–R71, U22/U23 and bypass entirely DNP; ADC disabled; informational only |
| RC_IN | PC6 TX, PC7 RX, USART6 | OpenRX Lite-UFL, full bidirectional CRSF; 5V_AUX reserve 0.5 A; no handshake |
| GPS1 | PD8 TX, PD9 RX; PB8 SCL, PB9 SDA | USART3 115200; I2C4 ≤400 kHz, ≤300 mm; MAX-M10S-00B plus IST8310 custom carrier recommendation |
| GPS PPS | PD10 | U44 and its bypass/pull-down optional DNP |
| TELEM1 | PA2 TX, PA3 RX; PD3 CTS, PD4 RTS | RFD900x, full handshake, 57600 initially; external power; entire FC power option DNP |
| COMPANION | PE8 TX, PE7 RX; PE10 CTS, PE9 RTS | UART7 full handshake; separate CM5 power; advisory data only; reference/sense contact, never a power feed |
| CAN1 | PD1 TX, PD0 RX | TCAN332DCNR U47 populated; classic CAN 1 Mbit/s, ≤1 m |
| CAN2_EVAL | PB6 TX, PB5 RX | Entire second path, including connector, bypass, resistors and power option, DNP |
| USB FS | PA11 D−, PA12 D+, PA9 VBUS sense | Self-powered device; U54 bidirectional isolation; U55 5 V tolerant sense buffer; no VBUS rail feed |
| SWD | PA13 SWDIO, PA14 SWCLK, NRST | U57 bidirectional isolation; target-powered reference sense; PB3 SWO series link DNP |
| Recovery | Existing BOOT0 | Local DNP shunt J11 plus 1 kΩ; existing core reset/boot network retained; no new reset button or supervisor |
| SDMMC1 | PC12 CLK, PD2 CMD, PC8–PC11 D0–D3 | 3.3 V, four-bit, removable microSD; PB12 active-low mechanical detect |
| Status | PE6 | Optional DNP green LED and 1 kΩ; low current |
| Inactive | PA0/PA1, PE1/PE0 | LIDAR_FC retired; AUX_UART disabled/unassigned; no new connector or circuit |

Camera, VL53L5CX-SATEL and CM5 consume **zero FC operating-power allocation**. There is no new `3V3_SENS` load. Module/carrier selection remains a recommendation, not a final BOM approval.

### ESC contact and source proof

The retained upstream netlist was exported from OpenESC commit `1da7dbd046760160639fb9c3f470702250b4b2cb` without editing that repository. Upstream J1-1 is battery-positive; J1-4 is an unconnected physical contact on the ordinary source connector. That does **not** make an ordinary populated eight-position mating harness safe.

The captured J1 is a controlled **sparse bench termination**, with only pins **2, 5, 6, 7, 8**. Positions 1 and 4 do not exist in its symbol, conductors or any assigned footprint. Optional source position 3 is a separate, wholly DNP contact J2. No standard eight-contact FC connector footprint is assigned. The controlled interposer is limited to ≤150 mm, continuity inspection before energization, and bench use. The final flight harness, keying and mechanical realization remain OPEN. This stage has no PCB, so it makes no fabricated-copper claim.

| Upstream contact | Meaning | Captured destination |
|---|---|---|
| 1 | +BATT | Physically absent from controlled mating boundary; prohibited |
| 2 | GND | J1-2, GND |
| 3 | /CURR | J2-1 optional termination, entirely DNP |
| 4 | Source NC contact | Physically absent from controlled mating boundary; prohibited |
| 5/6/7/8 | M1/M2/M3/M4 | J1-5/6/7/8 through bidirectional protection to PD12/13/14/15 |

Upstream series parts are R20/R39/R57/R87, each 220 Ω. The upstream AT32F421G8U7 motor input is PB4, QFN pin 25; its FT input rating is independent of VDD within the stated limits. Internal pulls must be disabled when the pin is above VDD+0.3 V. The source does not specify an all-condition off-state input leakage guarantee; that remains a physical and firmware gate. TMUX1511 adds at most 4.5 Ω in the specified operating range. Default FC series links are 0 Ω; 22 Ω may be evaluated only after observing both DShot directions. Start conservatively, verify the exact ESC firmware's return-drive and idle behavior, and do not arm on absent or malformed telemetry. Weak low bias provides inactive reset behavior; it is not a flight safety proof.

### UART and I2C protection contract

U24/U27/U30/U33 are TI SN74LVC2G07 open-drain, non-inverting outbound drivers. MCU-side 47 kΩ pull-ups make UART TX idle and RTS deasserted during reset. Each active outgoing line has 47 Ω series resistance. **The remote carrier must provide a 2.2 kΩ pull-up to its own switched 3.3 V rail at every RX/CTS input.** There is no FC pull-up on those exposed outputs. This allows the remote device to be off without the FC sourcing its input clamp. A floating input or an unspecified weak internal pull-up is not an accepted substitute.

U25/U28/U31/U34 are TI SN74LVC2G34 input buffers on MAIN. Inputs accept 0–5.5 V, including VCC=0 under the specified input/Ioff tests; nominal service is 3.3 V. Remote outputs must provide ≥2.0 V high and ≤0.8 V low. Connector-side 47 kΩ pull-downs and MCU-side 22 kΩ pull-downs bound idle and off-state leakage voltages. Disconnected RX goes low and must be treated as no valid frames, never a command. Disconnected CTS may read asserted; firmware must also require protocol presence and cannot rely on CTS alone.

These are **adapter contracts, not unqualified plug-and-play cables**. OpenRX needs the pull-up on its own 3.3 V node. RFD900x does not expose an ordinary 3.3 V supply contact in its main header: a qualified remote-side adapter or access to its actual switched logic rail is required. No RFD internal modification has been performed or released here. An adapter supply that remains on when the remote logic is off would defeat this protection policy.

GPS I2C uses U42 TMUX1511 with no FC pull-ups. The remote carrier owns both 2.2 kΩ pull-ups to its own 3.3 V; H743 pins remain open drain. Total capacitance, including both boards, protection, switch and cable, is limited to 100 pF for the initial 400 kHz case. The calculated 30–70% rise time is 192 ns including a +3% resistor allowance, below 300 ns. The 47 kΩ local pull-downs cost roughly 70 µA per high line. At 3.6 V, pull-up sink current is approximately 1.69 mA. Actual carrier pull-up population and cable capacitance must be measured. Do not add parallel pull-ups without recalculation.

At 100 pF, a 2.2 kΩ +3% UART pull-up reaches 70% in approximately 273 ns. CRSF at 420 kbaud has a 2381 ns bit period. At 921600 baud the period is only 1085 ns, so that rate is explicitly deferred to waveform and error-rate testing. GNSS is 115200 and RFD bring-up is 57600. The E22 option requires an adapter/change assessment; Holybro remains pending exact voltage and full-handshake evidence.

## Logical connectors and harness orientation

All TX/RX and RTS/CTS names below are **from the FC perspective**. Read contact numbers at the **FC header mating face using the manufacturer's pin-1 datum**. Do not infer numbering from wire colour or from a mirrored harness wire-entry view. A cable drawing must separately show the mating-face and wire-entry views and the remote equipment pin numbers before assembly. No mechanical placement or land pattern is released here.

| Ref / port | Contact order | Header recommendation | Mate |
|---|---|---|---|
| J3 RC_IN | 1 RC_5V_OUT; 2 GND; 3 FC TX→RX; 4 FC RX←TX | BM04B-GHS-TBT(LF)(SN) | GHR-04V-S |
| J4 GPS1 | 1 GPS_5V_OUT; 2 GND; 3 FC TX; 4 FC RX; 5 SCL; 6 SDA; 7 optional PPS; 8 NC | BM08B-GHS-TBT(LF)(SN) | GHR-08V-S |
| J5 TELEM1 | 1 DNP FC 5 V; 2 GND; 3 FC TX; 4 FC RX; 5 FC CTS; 6 FC RTS | BM06B-GHS-TBT(LF)(SN) | GHR-06V-S |
| J6 COMPANION | 1 sense-only reference; 2 GND; 3 FC TX; 4 FC RX; 5 FC CTS; 6 FC RTS | BM06B-GHS-TBT(LF)(SN) | GHR-06V-S |
| J7 CAN1 | 1 DNP 5 V; 2 GND; 3 CANH; 4 CANL | BM04B-GHS-TBT(LF)(SN) | GHR-04V-S |
| J8 CAN2 | Same order, entire assembly DNP | BM04B-GHS-TBT(LF)(SN), DNP | GHR-04V-S, DNP |
| J10 SWD | 1 reference; 2 GND; 3 SWDIO; 4 SWCLK; 5 NRST; 6 SWO DNP | BM06B-GHS-TBT(LF)(SN) | GHR-06V-S |
| J11 recovery | 1 local MAIN; 2 BOOT service through 1 kΩ | BM02B-GHS-TBT(LF)(SN), DNP service shunt | GHR-02V-S |

Contacts: **SSHL-002T-P0.2**, 26–30 AWG, insulation OD 0.76–1.0 mm, per JST GH document. Use 26 AWG for power/return; initial powered RC cable ≤150 mm; GPS total cable ≤300 mm. Smaller signal conductors may be evaluated within the specified crimp range. JST specifies 1 A with 26 AWG, 30 mΩ maximum initial contact resistance and 50 mΩ after test. Neither the 1 A family rating nor a nominal wire gauge proves voltage drop or thermal margin for an assembled cable.

RFD900x wiring from its official V1.2 table: FC J5-3 → RFD pin **7 RX**; J5-4 ← pin **9 TX**; J5-5 ← pin **11 RTS**; J5-6 → pin **3 CTS**; J5-2 → RFD GND pin 1 or 2. RFD pin 4 receives its external regulated supply; do not bridge its USB-power pins 5/6 or FC power pin 1 by default. Its 3.5 V serial absolute maximum is not a 5 V logic permission.

For the CM5 carrier, route TX→RX and RTS→CTS in both directions and use the carrier's actual 3.3 V GPIO domain. CM5 GPIO_VREF is set from **CM5's own** 3.3 V supply, never FC `3V3_REF`. The official CM5 Release 3 pin table identifies GPIO_VREF at module pin 78 and own 3.3 V at 84/86; 1.8 V GPIO configuration is incompatible with this direct 3.3 V contract. Carrier UART pin-mux and connector positions remain an explicit carrier assignment gate. Default CM5 harness contact 1 is omitted; fit the FC reference sense contact only for an off-state-tolerant ≥100 kΩ monitor. Never connect it to a supply input or an unpowered GPIO clamp.

### USB, debug and storage contact details

J9 recommends **GCT USB4105-GF-A**. All sixteen signal/power contacts and four shield tabs are explicit: A1/A12/B1/B12 to GND; A4/A9/B4/B9 to `USB_VBUS_PORT`; A6/B6 to D+; A7/B7 to D−; A5/B5 to separate CC1/CC2, each with 5.1 kΩ to GND; A8/B8 SBU unused with NC markers; S1–S4 bonded through 0 Ω to GND. Shield-to-board ground is the prototype recommendation, with chassis/EMC disposition deferred. This bond is a return path, not galvanic isolation.

TPD4E05U06 and TPD1E05U06 ground-referenced arrays supersede the leading USBLC6-2SC6 candidate to avoid its rail-steering backfeed concern. The chosen TVS has no VCC pin. VBUS passes only through 1 kΩ into U55's tolerant input with 47 kΩ pull-down; its output drives PA9 and has 22 kΩ pull-down. It never powers MAIN, AUX, the MCU or another port. USB-only connection therefore cannot boot this self-powered FC. External FC power is needed for USB/DFU. Full-speed operation, enumeration in both Type-C orientations, attach/detach timing and ROM DFU remain test gates; no external D+ pull-up is added in parallel with the MCU's controlled pull-up.

SWD reference uses LM66100 reverse blocking plus 3.3 kΩ, limiting a short to approximately 1.07 mA with the stated tolerances, below 10 mA. Use a ≥100 kΩ probe reference input; its actual threshold must accept the diode/reference drop. A probe must not inject target power. Only a probe with qualified off-state-tolerant signal/reference inputs is supported while powered off; otherwise disconnect it before switching the probe off. U57 cannot sense probe power. Existing NRST pull-up and BOOT0 pull-down remain unchanged. J11 is a local power-off-installed recovery shunt, not a general external power port. SWO stays DNP until needed.

J12 recommends **GCT MEM2075-00-140-01-A**: 1 DAT2, 2 DAT3, 3 CMD, 4 VDD, 5 CLK, 6 VSS, 7 DAT0, 8 DAT1. `CD` names the unnumbered mechanical detect termination; `SH` groups the grounded shell/ground terminations in the drawing, not an invented numeric contact. Exact land-pattern treatment remains OPEN. The mechanical switch is normally open and closes to ground with a card inserted, giving PB12 active-low detection. CMD/D0–D3 have 47 kΩ pull-ups to MAIN; CLK has 22 Ω source damping; other lines have default 0 Ω options. Local bypass is 22 µF plus 100 nF, with the accepted effective-capacitance assumption retained. Two rail-less ESD arrays cover the six bus lines and detect. No powered external card emulator is allowed by this contract.

## Power, startup and leakage analysis

The reproducible values are in `electrical_screens.json`; all are **calculations**, not measurements.

| Item | Result / disposition |
|---|---|
| AUX continuous allocation | RC 0.50 A + carrier 0.15 A = 0.65 A; 0.35 A unallocated; hard ceiling stays 1.00 A |
| Post-switch capacitance | Default planning allocation 320.6 µF: RC 220 µF, GPS 100 µF, existing/new populated local bypass with allowance; total ceiling stays 680 µF |
| Full permitted ramp case | 1 A active + 680 µF × 5.093115 V / 34 ms = 1.101862 A, below 1.139477 A minimum limiter screen; accepted ramp remains about 34–54 ms |
| Default ramp case | About 0.6980 A including the allocated capacitance; remote actual startup I(V,t) still OPEN |
| Frozen idealized drop screen | Using 64 mΩ limiter + accepted 25 mΩ path allowance + assumed 125 mΩ LM66100 envelope: RC 4.7812 V and GPS 4.82495 V at default concurrency |
| Full 1 A idealized RC floor | 4.75005 V before dynamic allowance; effectively no 4.75 V margin |
| Realistic GH loop screen | With two 50 mΩ after-test contacts, assumed 0.15 Ω/m wire at 20°C and 1.256 temperature factor: RC ≤150 mm gives about 4.70294 V; GPS ≤300 mm gives about 4.79299 V; an additional assumed 50 mV transient drop reduces each accordingly |
| Consequence | The original 25 mΩ *entire external loop* allowance is **not proved** for GH. The realistic calculation additionally reserves that allowance rather than silently redefining it. Remote input-voltage and thermal tolerance must close this before release |
| RFD power | Minimum specified input 5 V and approximately 1 A TX peak: FC AUX power is not demonstrated compatible on either voltage or concurrency grounds; default path remains entirely DNP |
| MAIN interface support | 15 mA planning allocation plus up to 60 mA CAN normal heavy load = 75 mA within the accepted 100 mA CAN/support bucket |
| MAIN bleed | R117 680 Ω: up to 5.181 mA and 17.704 mW at 3.417211 V and −3% R, below 50% of 0.1 W |
| Whole MAIN screen | Using the retained 1 A core bucket, 300 mA SD, 75 mA CAN/support and 23.529 mA sensor increment: 1.398529 A; accepted sensor startup case gives 1.508518 A transient, below 2 A |
| CAN fault | 180 mA bus-fault current is abnormal; a combined transient screen is 1.628518 A, but this does not authorize a sustained fault or prove thermal behavior |
| microSD | 300 mA startup allocation, including card/insertion behavior; actual card and charging waveform required; a capacitor alone is not an inrush limiter |

The 125 mΩ LM66100 drop envelope is based on its 3.6 V, ≤85°C table and is an engineering assumption over the actual AUX voltage. At 125°C, table maxima are higher. No interpolation or thermal assumption is promoted to a guaranteed limit. The 50 mV dynamic allowance and cable resistance also require measurement. The receiver reserve is not a measured OpenRX continuous current. The custom carrier must regulate locally for MAX-M10S/IST8310 and prove its minimum input voltage. No existing power converter was redesigned to hide these open items.

LM66100 CE is tied to its own output for reverse-current blocking. Its ≤5.5 V differential off-leakage maximum is 2.7 µA through 85°C and 8 µA through 105°C under the stated CE condition. RC/GPS power paths are populated; TELEM and both CAN power paths, associated capacitors and TVS parts are DNP. Companion and SWD reference paths are current limited and must not be loaded as rails.

At VCC=0, LVC buffers specify up to ±10 µA Ioff; their input current specification is ±5 µA. A 22 kΩ +3% MCU pull-down gives 0.2266 V for 10 µA; 47 kΩ +3% gives 0.2421 V for 5 µA. TMUX1511 specifies ±2 µA off leakage for 0–3.6 V signal and VDD=0; 47 kΩ gives 0.09682 V. The 2 µA number is not extended to an unqualified 5 V fault.

A deliberately conservative combined off-state arithmetic screen, even counting DNP power/CAN options, is 222.9 µA. R117's +3% value produces about 0.1561 V. This is **not a guaranteed summed injection-to-VCC specification**: the actual return paths, ground ordering, intermediate brownout voltages, temperatures and transient currents need a fixture test. The accepted Stage05 95.0877 µA input-blocker screen remains an engineering allocation, not a guaranteed maximum. Do not independently add that common upstream blocker once per port. Reverse current into AUX, into MAIN, and into the upstream input must be measured separately.

### Complete power-state matrix

“Both on” means valid nominal rails, shared ground and the specified remote pull-ups/voltage domain. “Off” leakage figures apply at VDD=0 and their documented test conditions. Below the minimum operating supply but above zero, logic behavior is not specified by Ioff alone.

| Interface | FC on / remote off | FC off / remote on | Both on | Both off / removal | Reset or brownout | Hot plug / clamp / shield paths |
|---|---|---|---|---|---|---|
| ESC | Default low, bidirectional switch on; AT32 FT input and disabled internal pulls required; driven-high off leakage not fully specified | TMUX blocks; 2 µA/channel screen; FC-side 47 kΩ and MAIN bleed | Bidirectional DShot through switch + 0 Ω + existing remote 220 Ω; verify actual return-drive mode | Both sides biased low; no source power contacts 1/4 | No motor commands until firmware explicitly configures/arms; mid-rail and restart waveform OPEN | Ground-first fixture; rail-less TVS; no positive power feed; missing-ground/transient qualification OPEN |
| RC | OD outputs cannot source remote logic; own remote pull-ups disappear; incoming local pull-down reports no frames | LVC input/Ioff isolation; LM66100 blocks receiver power return into AUX | CRSF 420k, required remote 2.2 kΩ pull-up; 0.5 A reserve | Pulls discharge signal nodes; receiver off; BOOT service remains remote only | MCU-side TX pull-up releases OD output; validate no spurious valid frame or partial-power startup | ESD on data and supply; powered insertion current is not the 34 ms cold ramp; power-off mating until validated |
| GPS UART/I2C/PPS | OD UART and I2C have no FC pull-up; remote-owned pulls vanish; PPS buffer DNP | UART Ioff; I2C switch off; LM reverse blocking; optional PPS requires same input policy | 115200 UART, ≤400k I2C; local carrier rails/pulls; PPS optional | No FC-driven high on removed carrier; capacitance discharges through biases/load | Open-drain pin configuration mandatory; false bus edges/lockup recovery OPEN | Data and supply TVS; ≤300 mm and ≤100 pF; measure insertion surge and remote clamp currents |
| TELEM | OD TX/RTS source no current with remote pulls off; RX/CTS pulled low; no-valid-protocol state required | Incoming LVC Ioff; FC power branch absent | Full handshake; external regulated RFD power; required switched 3.3 V pull-up adapter | Power wire contact unused; no relay of stale command; invalid frames ignored | Reset RTS high means deasserted at powered remote; brownout handshake timing OPEN | Data TVS populated; power TVS/path DNP; no USB/Vcc jumper power loop; grounds shared |
| COMPANION | Same OD protection; reference harness contact omitted by default, otherwise only an off-tolerant monitor | LVC Ioff plus reference reverse blocker; no external CM5 supply joins FC rails | Advisory UART7 only; remote own 3.3 V pull-ups; reference ≤10 mA contract, actual short screen ~1.07 mA | No power feed to CM5/camera/lidar | FC must reject stale/advisory data during host or FC restart; host power never grants motor authority | Data/reference ESD; monitor clamp behavior required if sense contact fitted; no camera/lidar FC cables |
| CAN1 / CAN2 | Remote CAN node must meet CAN powered-off bus loading; no FC bus-power output by default | TCAN power-off bus leakage specified; includes bus/common-ground path; CAN2 wholly absent | 1 Mbit/s, ≤1 m, only two end terminations; TCAN UVLO/TXD timeout present | CAN1 high impedance when unpowered; second interface DNP | TX pull-up gives recessive reset; UVLO/thermal behavior per source, repeated reset test OPEN | Integrated ±12 kV IEC contact bus protection; ±12 V common mode, ±14 V absolute rating; no battery-fault guarantee; ground loop/EMC OPEN |
| USB-C | MCU controlled pull-up must follow VBUS presence; never feed an unpowered host from firmware; no VBUS output | Host VBUS enters tolerant buffer only; DM/DP switch off; no USB powering of FC | Self-powered FS device, CC Rd on both pins; no PD negotiation | No source power; PA9 low via buffer/pull-down when VBUS absent | Attach/pull-up timing and ROM DFU must be verified across reset/brownout | Ground-referenced ESD on DM/DP/CC/VBUS; shield 0 Ω to GND; not 20 V PD or DC miswire protection |
| SWD / recovery | Requires probe off-state tolerance; otherwise disconnect probe; NRST and SWDIO pulls can feed an unqualified probe clamp | Bidirectional switch off; reference diode blocks probe-to-MAIN return; no probe power injection | Powered FC and qualified probe; reference ≥100 kΩ; SWO DNP; local boot shunt as needed | Remove probe/shunt before normal operation; preserved core defaults | Existing NRST/BOOT0 networks only; target must start safely with/without probe | Signal/reference TVS; ground-first service; no extra reset button/supervisor; unqualified probe remains excluded |
| microSD | Card shares MAIN; powered-off separate card is not a supported state | Externally powered card emulator excluded; ordinary removable card has no independent supply | Four-bit 3.3 V, pulls on CMD/data; active-low detect | No card: host stops transactions; SD pins reset safely; no new sensor-rail load | Brownout/write interruption requires filesystem and power-loss handling | Rail-less data/detect ESD; local bypass; contact bounce and 300 mA insertion/startup screen need actual card testing |
| Optional LED | No external device/power path | Not applicable | DNP; low-current status only | Off | No safety interpretation of LED state | Internal component; standard handling ESD, no external connector |

Ground-referenced TVS clamps are transient devices. The TPD family’s clamp voltage can exceed logic absolute limits during a surge; it does not prove end-to-end IEC immunity or protect a sustained battery/5 V miswire on every analog signal. Negative excursions use the TVS/ground return; open ground, cable inductance, connector sequencing and layout parasitics remain explicit physical gates. CAN's integrated ESD is the initial bus-protection recommendation. The retained PESD2CAN24LT-Q candidate is not populated because a 24 V standoff does not protect a ±14 V transceiver limit. Common-mode choke placement/value is deferred to EMI evidence; current capture has separate 0 Ω bypasses. DNP 120 Ω termination uses a 0.75 W Yageo RC2010FK-07120RL recommendation (exact manufacturer specification retained as RC2010FK-07120RL.pdf), sufficient for a ≤5 V differential analytical case at 50% derating.

## Evidence, symbol audit and verification

Official source PDFs and SHA-256 records are retained for TMUX1511, TCAN332, LVC2G07/34, LM66100, TPD1/4E05U06, JST GH, GCT USB4105, GCT MEM2075, AT32F421, MAX-M10S, RFD900x and the optional Kingbright LED. The manifest also retains rejected/unused candidates and failed retrievals rather than claiming they succeeded. The IST8310 full official datasheet remains a carrier/BOM gate; no invented pin table or FC magnetometer symbol was used. CM5 official Release 3 was read via the browser; direct PDF retention returned HTTP 403 and is recorded honestly in `supplemental_sources.json`, with a short source note retained.

Pin provenance is independent of the schematic net-map generator. The official numeric/function tables were compared against all 108 local symbol pins, electrical types and visibility. PCBParts/EasyEDA-derived pin tables corroborate the six main IC candidates; LM66100 active-low notation is normalized to the official datasheet. No pins are hidden. NC pins remain visible with explicit NC markers as a deliberate auditability exception. Same-number parts from TECH PUBLIC, UMW, JSMSEMI and DOWO were not accepted as TI/ST substitutes. Stock and prices are a dated discovery snapshot, not a sourcing approval or design gate. Use genuine selected manufacturers; Malaysia sourcing options and final BOM approval remain at their later gates.

The official KiCad library checker was run on a QA-only copy normalized for its required library version and decimal-token parser. Its remaining conventions findings are documented in `klc_disposition.md`; no “KLC clean” claim is made. Sparse/mixed connector numbering, visible NC pins and passive ESD/connector grounds are deliberate. Missing land-pattern assignments for the sparse bench termination, optional service contact, TPD1 DYA and GCT microSD are explicit Stage08/09 work; no approximate footprint was invented for them. Other footprints are recommendations, not audited geometry release.

Native KiCad 10.0.6 exported the complete hierarchical netlist, ERC JSON, nine-page PDF and nine SVG sheets. The final net map has **zero mismatches across 606 checks** and preserves all earlier pin-to-pin net groups. The independent release audit checks official symbol tables, default DNP groups, old-file scope, frozen MCU assignments, absence of new SENS loads, prohibited resource use, direct 5 V MCU connections and sparse ESC contacts. Full-sheet views and enlarged circuit regions were visually inspected over multiple iterations; top-label collisions, a temporary mux-select bus short, misplaced boundary text and invalid footprint names were corrected before final verification. Intermediate failing outputs are retained as iteration evidence and are not the handoff baseline.

Final native ERC is **13 findings**, classified rather than hidden:

| Count | Classification |
|---|---|
| 6 | Retained isolated labels: AUX_UART TX/RX, retired LIDAR_FC TX/RX, BUZZER and VBAT_SENSE_3V3 reservation |
| 3 | Previously accepted VCAP power-output pair and two AXC unused-channel-to-GND type conflicts |
| 4 | Intentional aliases: retained MAIN/REF and dual input contact aliases, plus two new MAIN/reference hierarchy aliases |

There are no final off-grid endpoint findings, dangling hierarchical pin findings, missing-footprint-link findings or new unclassified pin-type conflicts. This is a scoped schematic result, not a waiver of physical electrical limits. Nonfatal KiCad CLI registry-access messages are retained in command logs; exports completed successfully.

## OPEN register and stop boundary

| ID | Required closure / owner gate |
|---|---|
| S07-01 | Flight ESC harness, physical missing 1/4 contacts, strain relief/keying and continuity jig; mechanical/PCB review. Bench interposer remains ≤150 mm only |
| S07-02 | Actual OpenESC build/firmware, PB4 off-state injection, default levels and bidirectional DShot return waveform/error rate; firmware and bench |
| S07-03 | OpenRX, GNSS, RFD and CM5 remote pull-up adapters; prove own-rail tracking, thresholds and clamp paths; external-carrier electrical review |
| S07-04 | GH loop voltage drop versus frozen 25 mΩ allowance, receiver/carrier minimum input and thermal behavior; load/cable measurements and controlled disposition before release |
| S07-05 | All rail on/off combinations, MAIN bleed, reference monitor/probe qualification, mid-rail brownout and upstream reverse-current measurements; electrical bench |
| S07-06 | AUX cold-start and powered insertion I(V,t), actual downstream capacitance ≤680 µF and active load ≤1 A; module selection/bench |
| S07-07 | GCT socket, TPD1 DYA, sparse bench/service physical terminations, recommended footprints and pin-number mapping; Stage08/09 only |
| S07-08 | USB FS signal integrity, both orientations, VBUS attach/detach/pull-up behavior and ROM DFU; bench/firmware |
| S07-09 | CAN end termination, common-mode/ground loop, fault thermal response, ESD/EMI and optional choke decision; bench/EMC |
| S07-10 | microSD current/card selection, four-bit timing, detect bounce, removal/brownout data integrity; bench/firmware |
| S07-11 | GNSS carrier final BOM including official IST8310 evidence, actual I2C pulls/capacitance and optional PPS; BOM/carrier gate |
| S07-12 | UART 921600, cable variants, reset/no-frame/handshake behavior, host advisory isolation and optional LED visibility; firmware/system testing |

**Stop after this Stage 07 handoff.** No control-state update or Stage 08 work is authorized by these artifacts. The earlier accepted Stage04–06 OPEN items and status labels remain intact.
