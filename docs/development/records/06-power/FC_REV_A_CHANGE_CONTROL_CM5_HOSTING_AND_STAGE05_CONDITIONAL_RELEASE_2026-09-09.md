> Historical technical record. Names and private workstation/session references were neutralized for publication. Dates and assertions describe the recorded stage, not current physical qualification. See the current validation-status page for later checks.

# FC Drone FC Rev A - CM5 hosting and Stage 05 conditional-release change control

Date: 2026-09-09, Asia/Kuala_Lumpur

## Approved architecture corrections

- DECISION: the camera and ST `VL53L5CX-SATEL` lidar are peripherals of the separately powered CM5, not FC peripherals.
- DECISION: the camera and lidar draw no power from `5V_AUX`, `3V3_MAIN`, `3V3_SENS` or any other FC rail. Their power domains must not backfeed the FC.
- DECISION: the former `LIDAR_FC` UART4 interface is retired. PA0/PA1 remain reserved and unavailable for reuse until a later resource-map change explicitly reassigns them.
- OPEN: the exact camera MPN, camera interface/cable/voltage and CM5-side power budget.
- DECISION: navigation, obstacle and perception information derived by the CM5 may be sent to the FC only through the controlled CM5 data interface. The exact protocol, rate, validation and failure behavior remain OPEN for the interface and firmware stages.
- DECISION: CM5-derived navigation information is advisory. Loss, corruption, reset or power failure of the CM5 must not prevent FC stabilization, arming policy, failsafe, safe motor shutdown or direct motor-waveform generation.
- DECISION: `OpenRX Lite-UFL` is the FC receiver. `5V_AUX` connects to OpenRX 5 V, GND to GND, PC6/`RC_IN_TX` to OpenRX RX, and OpenRX TX to PC7/`RC_IN_RX`. CTS/RTS are not used. BOOT is an optional receiver-service pad only.
- ASSUMPTION: reserve up to 0.5 A of the aggregate 1.0 A `5V_AUX` allowance for OpenRX until measured startup and peak current are available.
- OPEN: powered-state mismatch and UART-line backfeed verification for OpenRX.
- RECOMMENDATION: a custom GNSS/compass carrier using u-blox `MAX-M10S-00B` and iSentek `IST8310`, powered from `5V_AUX` with a local regulated 3.3 V rail, USART3 on PD8/PD9 and I2C4 on PB8/PB9.
- CANDIDATE: `MAX-M10S-00B` plus `MMC5983MA` as an alternate compass implementation.
- RECOMMENDATION: `RFD900x` for the existing full TELEM1 TX/RX/CTS/RTS contract.
- CANDIDATE: `Ebyte E22-900T22S` only if TELEM1 is explicitly changed to TX/RX-only or an approved adapter is added.
- CANDIDATE: Holybro SiK Telemetry Radio V3 pending official CTS/RTS confirmation.
- OPEN: exact GNSS/compass and telemetry selections, measured currents, startup profiles and concurrency. No recommendation or candidate above is promoted to a final module DECISION.

## Stage 05 load-budget correction

- DECISION: camera and lidar loads are excluded from every FC rail and from the Stage 05 `5V_AUX` load budget.
- DECISION: `5V_AUX` remains 1.0 A aggregate continuous with the approved 1.10-1.50 A settled current-limit interval.
- ASSUMPTION: reserve up to 0.5 A for OpenRX. Remaining GNSS/compass, telemetry and any populated CAN/external accessory loads must fit within the other 0.5 A unless Stage 07 returns an approved concurrency or budget change.
- OPEN: exact external-module startup `I(V,t)`, capacitance and simultaneous-use policy. Stage 07 owns module-specific qualification.

## Stage 05 conditional engineering-release policy

- DECISION: Stage 05 may complete and capture a conservative datasheet-backed power design without claiming that simulation or documentary evidence proves every board-dependent physical result.
- DECISION: the hard steady-state electrical requirements remain: valid POWER1 range at the FC pads, `5V_AUX` at least 4.75 V at the approved steady 1 A load, and settled AUX current limiting between 1.10 A and 1.50 A.
- DECISION: official simulations and the TI workbook are supporting evidence where available, not mandatory pre-capture proof.
- DECISION: switched-network stability, startup SOA, 55/70 degC physical thermal behavior, EMI and transient performance may remain OPEN for a dedicated power coupon and Stages 11-13. They must pass before flight or production release.
- DECISION: split the below-100 uA POWER1 backfeed verification. Stage 05 calculates the implemented internal power-chain contribution; Stage 07 evaluates the selected external-interface paths; Stages 11-13 verify the assembled-system total.
- DECISION: `PWR_STATUS` remains informational and non-safety-critical. It must fail low for defined implemented power faults, but is not a precision 4.75 V compliance detector and may not control NRST, arming, failsafe or motor waveforms.
- DECISION: exact ICs, magnetics, passives and footprints captured in Stage 05 remain RECOMMENDATION pending handoff, sourcing, layout and prototype review. `VBAT_SENSE_3V3` remains DNP.
- DECISION: Stage 05 must still stop rather than capture if its analytical design violates an absolute maximum, recommended operating condition, the steady-state rail requirements, or the guaranteed current-limit interval.
- DECISION: Stage 06 is not authorized automatically. Project control must review and accept the Stage 05 conditional-pass handoff first.

## Tool evidence supplied by the user

- VERIFIED: PSpice for TI is installed under `[LOCAL_SOURCE]`; Capture, PSpice and simulation-server processes were observed running on 2026-09-09.
- VERIFIED: the official encrypted TPS552892 model package remains retained and integrity-checked from R16.
- OPEN: the user reported downloading the TPS552892 calculation workbook, but no `.xlsx`, `.xlsm` or `.xls` file was found in the specified R16 evidence folder or standard Downloads/Documents locations during this control update. Stage 05 may proceed under the conditional-release policy without silently inventing workbook evidence.
