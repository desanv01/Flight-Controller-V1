> Historical technical record. Names and private workstation/session references were neutralized for publication. Dates and assertions describe the recorded stage, not current physical qualification. See the current validation-status page for later checks.

# FC Drone FC Rev A — Stage 03 KiCad project foundation

Date: 2026-09-07  
Revision: A-S03-01  
Result: VERIFIED FOUNDATION — submitted for project-control acceptance. Stage 04 NOT STARTED.

## Work completed

Created canonical project `hardware/FC_REV_A/FC_REV_A.kicad_pro`, one root and eight empty functional child sheets, portable project-local symbol/footprint tables and empty libraries, revision metadata, a 79-row port/net registry, rule and semantic net-class placeholders, documentation and evidence folders. No historical ESC design was copied. Pre-creation file inventory is recorded in `qa/stage03-foundation/precreation_inventory.txt`.

Sheet plan: MCU core; power/monitoring; local sensors; ESC boundary; external UART/I2C ports; CAN; USB/debug; storage/status. Paper layout is organizational only. No components, wires, net labels, sheet pins, connector symbols, footprints or PCB file exist. Native classes and assignments are empty; descriptive net-class groups reside in JSON with null numeric constraints. The version-only rule file has no active rules. No manufacturing/default geometry is frozen.

## Confirmed decisions

All seven approved Stage 02 decisions remain frozen. Exact STM32H743VIT6 LQFP100 and pin/timer/DMA/DMAMUX assignments are unchanged. Motor PD12–PD15/TIM4, dedicated SPI1, local I2C2, SDMMC1 four-bit storage, USB sense-only/no-backfeed, and all UART reservations carry forward. CAN1 is required to be populated in its later circuit stage; Stage 03 has zero parts. CAN2 PB5/PB6, transceiver and connector remain reserved DNP and require later approval to populate. ESC J1-1/J1-4 have no contact, conductor or copper; they are represented as prohibited registry rows with no net name. CURR is optional DNP, informational, firmware-disabled and excluded from safety use. CM5 remains separately powered and outside the basic FC safety path.

POWER1 remains 5.2 V nominal, 4.9–5.5 V operating, at least 2 A continuous and 3 A for 100 ms. No UBEC, supplier or production BOM choice was made. The recovered memo cannot authorize raw-battery FC self-power. Input SHA-256 checks prove all eight controlled input files, including current control state, are unchanged.

## Recommendations, assumptions and all OPEN items

The exhaustive source-line carry-forward ledger is `hardware/FC_REV_A/docs/retained_status_ledger.md`; it retains every OPEN, ASSUMPTION, RECOMMENDATION, CANDIDATE and DNP source line from the eight controlled inputs, including ESC register IDs and owners. Nothing is closed by this foundation.

Retained recommendations include the POWER1 test shortlist (Holybro SKU 15034 and Matek BEC12S-PRO), Hobbywing and conditional mBEC12S candidates, JST-GH family, TCAN332DCNR, USBLC6-2SC6, HSE/SWO/PPS/auxiliary and detect/interrupt options. None becomes a selected library part. Retained assumptions include first-bench ESC cable <=150 mm, planning ESC 3S–8S with 6S vehicle baseline, 5V_AUX 1 A interim budget, UART/I2C <=300 mm, CAN <=1 m, and 8 MHz HSE for parser validation only.

OPEN work includes missing originals/release/BOM; ESC as-built and mechanical parity; exact connector headers/mates/keying/pin-1/contact/wire/crimp/flight cable; 2S qualification and hot-plug procedure; CURR calibration/fault data; PWM/DShot/bidirectional telemetry, reset/disarm/loss and logging; exact AM32 target/binary/bootloader/configuration and stale-telemetry applicability; propulsion parameters and measured envelope; ESC release audit/manufacturing package; external module identities; final UBEC/supplier and all power/thermal/EMI/authenticity/harness measurements; firmware build/board ID/bootloader/PX4; oscillator implementation; sensor orientation and DS-000347 v1.9 detailed review; USB/microSD/protection/regulator/load-switch parts; all geometry/mounting/layers/stackup/impedance/placement/manufacturing values. The ledger preserves individual identifiers and containment.

Foundation convention: prefixed UART/CAN/USB/SDMMC net labels disambiguate repeated logical role names. They do not alter resources or establish physical connector order. COMPANION RTS=PE9, CTS=PE10 follows the explicit matrix. POWER1 A/B stay separate logical labels until entry-circuit implementation. Literal `3V3` is retained; mapping it to internal rail names is deferred to Stage 05. No inferred rail short is created. Internal core/sensor names outside the port contract remain for the relevant circuit stages.

## Verification and unresolved errors

KiCad CLI version 10.0.6. Reproducible primary check: `python qa/stage03-foundation/verify_foundation.py` from the project root. See commands.json, verification.json, supplemental_verification.json, netlist.xml, erc.rpt and nine SVG files. Native KiCad successfully loaded all nine sheets and exported the netlist and render. Netlist: zero components, zero nets. Structural checks: nine schematics, no circuit objects, no PCB, valid JSON, balanced single-root S-expressions, existing local library URI targets, prohibited ESC positions empty, CAN2 DNP, motor pins preserved, all source hashes unchanged. PDF contains nine pages; root and ESC sheet images were visually inspected and are readable without overlapping content.

ERC: executed for empty-hierarchy load verification; 0 errors and 0 warnings. The report lists four default ignored check categories. This is not circuit ERC acceptance. DRC: NOT APPLICABLE, no PCB. Native PCB rule parsing is not exercised; placeholder syntax is structurally checked only. No fabrication/assembly exports exist.

Unresolved environment diagnostic: CLI cannot create/open HKCU\Software\kicad-cli under the sandbox. All relevant commands exit 0 and output files verify successfully; diagnostic is retained in commands.json. No registry changes were attempted. No unresolved schematic parser or structural error remains. CairoSVG was unavailable; native KiCad PDF and existing PyMuPDF supplied the inspected raster views. No electrical, signal-integrity, firmware, thermal or bench performance is claimed.

## Required human approvals and exact Stage 04 entry criteria

Project control must review this handoff, complete file inventory and verification evidence, accept Stage 03 and its carried OPEN items, then update FC_REV_A_CURRENT_CONTROL_STATE.md and explicitly authorize Stage 04. This agent has not changed control state or dispatched Stage 04. No frozen-item exception was needed.

Before Stage 04 changes: recheck controlled-input and foundation hashes; read current control state, Stage 01 circuit selection, Stage 02 freeze/matrix/port contract, ESC boundary/register, sourcing policy and this handoff; load applicable KiCad skills. Confirm the exact H743 LQFP100 datasheet and symbol pin mapping, and resolve or explicitly retain implementation blockers for clock/VBAT/support choices before affected capture. The DS-000347 Version 1.9 review remains required before any detailed IMU capture; Stage 04 is core-only under the current Stage 02–14 workflow. Older Stage 03 full-capture/Stage 04 mechanics maps are superseded.

## Exact next-stage instructions (not authorization)

Only after project-control authorization, implement Stage 04 STM32H743 core in the canonical project: verify all five VDD and five VSS pins, VDDA/VSSA/VREF+, VCAP1/2, decoupling, NRST, BOOT0, HSE, optional LSE, SWD, core USB connections and VBAT against exact datasheet and symbol. Preserve PA9/PA11/PA12 USB sense-only/no-backfeed and PA13/PA14 SWD; preserve all Stage 02 peripheral reservations. Keep USB external connector/protection work coordinated with Stage 07 and power-tree work with Stage 05. Do not implement sensor, ESC, external port or PCB circuits outside the authorized core scope. Return frozen-map conflicts to project control. Do not select final connectors, geometry, manufacturing or production UBEC. Run appropriate netlist/pin audits, render review and scoped ERC, and write a dated Stage 04 handoff without beginning Stage 05 automatically.

## Complete created/modified file inventory

All listed artifacts are newly created for Stage 03; no pre-existing controlled files were modified. `qa/stage03-foundation/file_manifest.json` records SHA-256 and size of every deliverable except itself (self-hash excluded to avoid recursion). The precreation inventory is a path snapshot taken after the evidence bootstrap directory/script existed, before any KiCad artifacts existed. Builder is an initial-creation script; do not rerun it over later-stage work. Verification script is the intended repeatable check.

- `FC_REV_A_STAGE_03_KICAD_FOUNDATION_2026-09-07.md`
- `hardware/FC_REV_A/docs/evidence/README.md`
- `hardware/FC_REV_A/docs/library_provenance.md`
- `hardware/FC_REV_A/docs/net_registry.csv`
- `hardware/FC_REV_A/docs/netclass_placeholders.json`
- `hardware/FC_REV_A/docs/README.md`
- `hardware/FC_REV_A/docs/retained_status_ledger.md`
- `hardware/FC_REV_A/FC_REV_A.kicad_dru`
- `hardware/FC_REV_A/FC_REV_A.kicad_prl`
- `hardware/FC_REV_A/FC_REV_A.kicad_pro`
- `hardware/FC_REV_A/FC_REV_A.kicad_sch`
- `hardware/FC_REV_A/fp-lib-table`
- `hardware/FC_REV_A/libraries/FC_REV_A_Local.kicad_sym`
- `hardware/FC_REV_A/libraries/FC_REV_A_Local.pretty/README.md`
- `hardware/FC_REV_A/sheets/01_mcu_core.kicad_sch`
- `hardware/FC_REV_A/sheets/02_power.kicad_sch`
- `hardware/FC_REV_A/sheets/03_sensors.kicad_sch`
- `hardware/FC_REV_A/sheets/04_esc.kicad_sch`
- `hardware/FC_REV_A/sheets/05_external_ports.kicad_sch`
- `hardware/FC_REV_A/sheets/06_can.kicad_sch`
- `hardware/FC_REV_A/sheets/07_usb_debug.kicad_sch`
- `hardware/FC_REV_A/sheets/08_storage_status.kicad_sch`
- `hardware/FC_REV_A/sym-lib-table`
- `qa/stage03-foundation/build_foundation.py`
- `qa/stage03-foundation/commands.json`
- `qa/stage03-foundation/erc.rpt`
- `qa/stage03-foundation/esc.png`
- `qa/stage03-foundation/finalize_handoff.py`
- `qa/stage03-foundation/foundation.pdf`
- `qa/stage03-foundation/input_hashes.json`
- `qa/stage03-foundation/netlist.xml`
- `qa/stage03-foundation/precreation_inventory.txt`
- `qa/stage03-foundation/root.png`
- `qa/stage03-foundation/supplemental_verification.json`
- `qa/stage03-foundation/svg/FC_REV_A-CAN interfaces.svg`
- `qa/stage03-foundation/svg/FC_REV_A-ESC signal boundary.svg`
- `qa/stage03-foundation/svg/FC_REV_A-External UART and I2C ports.svg`
- `qa/stage03-foundation/svg/FC_REV_A-Local sensors.svg`
- `qa/stage03-foundation/svg/FC_REV_A-Power and monitoring.svg`
- `qa/stage03-foundation/svg/FC_REV_A-STM32H743 core.svg`
- `qa/stage03-foundation/svg/FC_REV_A-Storage and status.svg`
- `qa/stage03-foundation/svg/FC_REV_A-USB and debug.svg`
- `qa/stage03-foundation/svg/FC_REV_A.svg`
- `qa/stage03-foundation/verification.json`
- `qa/stage03-foundation/verify_foundation.py`
- `qa/stage03-foundation/file_manifest.json`
