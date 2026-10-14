> Historical technical record. Names and private workstation/session references were neutralized for publication. Dates and assertions describe the recorded stage, not current physical qualification. See the current validation-status page for later checks.

# FC Drone FC Rev A — Stage 06 OPEN-item disposition and Stage 07 entry authorization

Date: 2026-09-09  
Authority: user approval following the reviewed Stage 06 handoff and control review  
Disposition: **Stage 06 remains a VERIFIED CONDITIONAL PASS; Stage 07 entry is authorized but not yet dispatched.**

## Stage 06 disposition

- DECISION: do not reopen or modify the accepted Stage 06 sensor schematic for Stage 07 entry.
- DECISION: retain the captured ICM-42688-P direct `3V3_SENS` implementation and the BMP390 `BARO_3V3` slow-rail/isolation implementation as Rev A prototype recommendations.
- DECISION: resolve S06-03 by defining the 50 mA screen as the incremental Stage 06 direct-sensor branch screen. The accepted Stage 05 150 mA sensor-rail transient allocation owns total upstream startup including C41. The analytical approximately 133.518 mA one-millisecond case fits that allocation; physical startup `I(V,t)` remains a later validation item.
- ASSUMPTION: retain the 4 mA ICM allocation for conservative 1 MHz bring-up. The 25 mA figure is the normal planning screen and the accepted 100 mA sensor-rail ceiling is not permission for unrestricted additional load.
- RECOMMENDATION: retain SN74AUP3G17 for the current capture. Stage 08 shall compare the officially specified SN74AUP1T17 single-gate alternative if a guaranteed-threshold replacement is required; no substitution is approved here.
- OPEN: S06-01, S06-02 and S06-04 through S06-10 remain assigned to their electrical, PCB, BOM, firmware and physical-validation gates. They do not block Stage 07 external-interface schematic capture and must not be described as VERIFIED measurements.
- DECISION: require genuine TDK InvenSense ICM-42688-P and Bosch BMP390. The Tokmas-labelled search result is rejected as a substitute. JLCPCB stock is not a design gate; PCBWay, authorized distribution or customer-consigned sourcing may be evaluated at the BOM/manufacturing stages.

## Stage 07 entry policies

- DECISION: Stage 07 is limited to the external OpenESC and FC interface circuits on the existing Stage 03 sheets. No PCB geometry, placement, routing, fabrication, procurement or Stage 08 work is authorized.
- DECISION: OpenESC J1 positions 1 and 4 remain true no-contact/no-conductor/no-copper positions. J1-2 is GND, J1-5 through J1-8 are M1 through M4, and J1-3 `/CURR` remains an optional DNP, informational, non-safety-critical branch.
- DECISION: OpenRX Lite-UFL remains the receiver on USART6/CRSF with up to 0.5 A reserved from the aggregate 1.0 A `5V_AUX` allowance.
- RECOMMENDATION: use the MAX-M10S-00B plus IST8310 custom carrier as the GPS1 design target while retaining its final module/BOM approval for the later gate.
- RECOMMENDATION: use RFD900x as the full-handshake TELEM1 design target. Make its FC-provided 5 V path configurable and default DNP unless the Stage 07 load/concurrency analysis proves it fits the remaining `5V_AUX` allowance; external telemetry power is the preferred initial containment.
- DECISION: the CM5 remains separately powered and data-only over UART7. `3V3_REF` is reference/sense only. Camera and VL53L5CX-SATEL remain CM5-only and consume no FC rail budget.
- DECISION: `LIDAR_FC` remains retired and PA0/PA1 remain reserved. CAN1 is populated; CAN2 remains DNP. `AUX_UART` remains disabled/unassigned by default.
- DECISION: USB remains a self-powered USB 2.0 FS device interface with VBUS sense only and no power/backfeed path. MicroSD remains removable four-bit SDMMC1 on `3V3_MAIN`.
- RECOMMENDATION: JST-GH remains the low-current flight-port connector family. Exact connector MPNs, mates, orientation and mechanical placement remain controlled Stage 07 through Stage 09 work as applicable.

## Authorization boundary

Stage 07 may be dispatched only as a dedicated task using the approved model routing. It must read the Stage 06 handoff, Stage 06 control review, this entry record, current control state and retained ledger before modifying files. It must produce a reviewed Stage 07 handoff and stop. Stage 08 must not begin automatically.
