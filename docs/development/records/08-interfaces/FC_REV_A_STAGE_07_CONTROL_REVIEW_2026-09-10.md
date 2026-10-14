> Historical technical record. Names and private workstation/session references were neutralized for publication. Dates and assertions describe the recorded stage, not current physical qualification. See the current validation-status page for later checks.

# FC Drone FC Rev A — Stage 07 control review

Date: 2026-09-10  
Reviewed handoff: `FC_REV_A_STAGE_07_ESC_EXTERNAL_INTERFACES_2026-09-09.md`  
Dedicated task: `FC FC Rev A — Stage 07 ESC and External Interfaces`, thread `[PRIVATE_SESSION]`  
Disposition: **VERIFIED CONDITIONAL PASS at recommendation-grade schematic-capture scope**

## Control conclusion

Stage 07 completed the authorized ESC and external-interface schematic work. Project control accepts the handoff as a conditional pass for later Stage 08 entry review. This acceptance does not approve a production BOM, footprints, PCB work, fabrication, procurement, flight use, or any deferred electrical/physical claim.

Stage 08 is **not authorized automatically**. It remains locked until the user reviews the Stage 07 handoff/control review and explicitly releases the Stage 08 schematic-review, symbol, footprint, ERC, netlist and BOM-field stage.

## Independently verified results

- VERIFIED: the five authorized sheets now contain the ESC boundary, external UART/I2C ports, CAN, USB/debug and microSD/status circuits.
- VERIFIED: the complete hierarchical schematic exports 326 components and 302 nets.
- VERIFIED: `python -X utf8 qa/stage07-interfaces/verify_interfaces.py final_control` reproduced 606 expected component-pin connections with zero mismatches and preserved all earlier pin-to-pin topology.
- VERIFIED: `python -X utf8 qa/stage07-interfaces/audit_release.py final_control` passed 430 checks and audited 108 pins across the 15 new controlled local symbols.
- VERIFIED: the sensor sheet is byte-identical to the Stage 06 entry copy; original MCU records remain exact; the power sheet contains only the explicitly approved `5V_AUX` hierarchy boundary addition.
- VERIFIED: the frozen MCU resource map is preserved. PA0/PA1 remain reserved, `LIDAR_FC` is not restored, and no new camera/lidar FC interface or FC power allocation exists.
- VERIFIED: USB VBUS has no path to `3V3_MAIN`, `5V_AUX` or the FC input rail.
- VERIFIED: OpenESC J1 positions 1 and 4 do not exist in the controlled FC boundary symbol. J1 contains only positions 2 and 5–8; the optional position-3 current branch is separately represented and wholly DNP.
- VERIFIED: CAN1 is populated at schematic-recommendation scope and the complete CAN2 evaluation path is DNP.
- VERIFIED: no `.kicad_pcb`, board geometry, layer stack, placement, routing, fabrication output, Stage 08 work, order or manufacturer contact was created.
- VERIFIED: the root handoff and retained evidence copy have identical SHA-256 `38B00C4C6ACB7E78FD044FAA78A7E19B017B1711B1698688BABDC3A17B0FA5C1`.
- VERIFIED: project control visually inspected the nine full schematic pages and all 15 generated Stage 07 circuit close-ups. The sheets are readable, DNP groups are visibly crossed, connector contacts are explicit, and no unauthorized circuit was observed.

## ERC disposition

Native KiCad ERC reports 13 findings. They are controlled findings, not a clean-ERC claim:

- six one-ended retained MCU reservations: AUX_UART TX/RX, retired LIDAR_FC TX/RX, BUZZER and `VBAT_SENSE_3V3`;
- the previously accepted VCAP power-output pairing;
- two mode-dependent unused-channel-to-GND pin-type warnings in the retained Stage 06 isolation logic;
- four intentional rail/input aliases involving `3V3_MAIN`/`3V3_REF` and the parallel POWER1 input-contact naming.

No broad ERC suppression was added. Stage 08 must review every finding and may clear it only through a controlled correction or a documented retained exception.

## Accepted recommendation-grade capture

- RECOMMENDATION: TMUX1511 bidirectional motor isolation, ground-referenced TPD ESD and the sparse bench-only ESC boundary.
- RECOMMENDATION: powered-off-safe UART protection using SN74LVC2G07 outbound open-drain drivers, SN74LVC2G34 inbound buffers and remote-own-rail 2.2 kOhm pull-ups required by the cable/carrier contracts.
- RECOMMENDATION: MAX-M10S plus IST8310 GNSS/compass carrier target; final carrier design and full official IST8310 evidence remain OPEN.
- RECOMMENDATION: RFD900x telemetry with external power by default. Its FC-power branch remains wholly DNP.
- RECOMMENDATION: separately powered CM5 advisory UART with no FC power for CM5, camera or lidar.
- RECOMMENDATION: TCAN332 for populated CAN1, DNP 120-ohm end termination, and CAN2 wholly DNP.
- RECOMMENDATION: self-powered USB-C FS interface using USB4105-GF-A, ground-referenced TPD protection, CC resistors and VBUS sensing only.
- RECOMMENDATION: MEM2075 removable microSD socket and the captured four-bit SDMMC1 protection/pull-up network.
- RECOMMENDATION: LM66100-based reverse-blocked auxiliary/reference paths where populated. Final footprints and production sourcing remain Stage 08/09 work.

## Material limitations retained as OPEN

The following Stage 07 matters are not closed by schematic checks:

1. `S07-01` — flight ESC harness, physically absent contacts 1/4, keying, strain relief and continuity jig.
2. `S07-02` — actual OpenESC build/firmware, off-state injection and PWM/DShot/bidirectional-DShot waveforms and error rate.
3. `S07-03` — remote-own-rail pull-up adapters and powered-off clamp behavior for OpenRX, GNSS, RFD and CM5.
4. `S07-04` — connector/harness voltage drop and module minimum-input/thermal qualification. The realistic GH screen reaches about 4.70294 V for the 150 mm RC case, below the 4.75 V external-boundary target; the prior 25 mOhm planning allowance is therefore not proven for a finished GH harness.
5. `S07-05` — all power-state, mid-rail brownout, MAIN bleed, debug/reference and upstream reverse-current measurements.
6. `S07-06` — actual AUX cold-start and powered-insertion `I(V,t)`, module concurrency, capacitance no greater than 680 uF and active startup load no greater than 1 A.
7. `S07-07` — exact land patterns and pin-number mapping for the GCT socket, TPD1 DYA, sparse ESC termination and service contacts.
8. `S07-08` — USB signal integrity, both orientations, VBUS attach/detach, enumeration and ROM DFU.
9. `S07-09` — CAN topology/end termination, common-mode/ground-loop behavior, fault thermal response, ESD/EMI and choke decision.
10. `S07-10` — final microSD card/current, timing, detect bounce, removal and brownout data integrity.
11. `S07-11` — GNSS carrier final BOM, official IST8310 evidence, pull-ups/capacitance and optional PPS.
12. `S07-12` — high-rate UART, cable, reset/no-frame/handshake behavior, host advisory isolation and optional LED visibility.

The conservative interface off-state arithmetic screen is 222.9 uA. It is not a guaranteed current into POWER1 and does not close the system requirement for less than 100 uA backfeed into an unpowered source. The assembled-system backfeed matrix remains mandatory at its later electrical/bench gate.

All Stage 04–06 retained OPEN items also remain in force. None is silently promoted to DECISION or VERIFIED.

## Stage 08 entry gate

Before Stage 08 starts, project control must explicitly authorize it and provide a dedicated prompt limited to:

- full schematic and hierarchy review;
- final symbol audits and controlled correction of symbol metadata;
- footprint candidate selection and manufacturer land-pattern verification, while leaving PCB geometry/placement/routing to Stage 09;
- review and classification of all 13 current ERC findings;
- deterministic netlist and BOM-field completeness checks;
- production-field normalization without silently approving unresolved sourcing or physical-validation matters;
- closure or controlled deferral of `S07-07` and any other item directly owned by Stage 08.

Stage 08 may not begin PCB layout, placement, routing, Gerbers, assembly exports, fabrication, ordering or Stage 09. Physical tests assigned to Stages 11–13 may remain OPEN if Stage 08 preserves their gates and does not claim production or flight readiness.

## Next action

Review this control record and the Stage 07 handoff. If acceptable, issue a new explicit Stage 08 authorization. Do not begin Stage 08 automatically.
