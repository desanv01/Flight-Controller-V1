> Historical technical record. Names and private workstation/session references were neutralized for publication. Dates and assertions describe the recorded stage, not current physical qualification. See the current validation-status page for later checks.

# FC Drone FC Rev A — Stage 04 STM32H743 core

Execution: 2026-09-08, Asia/Kuala_Lumpur. Revision A-S04-01. Filename date retained as requested.

**COMPLETE for Stage 04 capture and scoped review. OPEN — UNTESTED, NOT FOR FABRICATION.** Stage 05 has not been started or dispatched. Project control must review this handoff; this report does not grant later-stage authorization.

## Scope and entry evidence

The assigned sole writer modified only `hardware/FC_REV_A/sheets/01_mcu_core.kicad_sch` and `hardware/FC_REV_A/libraries/FC_REV_A_Local.kicad_sym`. Root/project, other seven circuit sheets, current control state, Stage 02 contracts/map, 79-row net registry and retained-status ledger remain byte-identical to entry. No PCB exists. Evidence and scripts are under `qa/stage04-core/` and `hardware/FC_REV_A/docs/evidence/stm32h743/`.

Read the R4 control state, EDA policy, Stage 01 selection, Stage 02 freeze/matrix/port contract, Stage 03 entry/handoff, registry, retained ledger and applicable ESC/sourcing records. The preflight confirmed nine empty sheets, no components/nets/PCB and matching canonical Stage 03 foundation hashes. The expected R4 control-state hash change was accepted at entry; historical Stage 03 exports reflect the parent's independent rerun and were not rewritten. `prechange_manifest.json` records 48 pre-existing files; all except the two authorized targets remain unchanged.

Initial direct downloads failed; parent project-control recovered all six official ST originals through the browser and explicitly resumed this task. Local PDF headers, lengths and hashes were verified before capture. The prior blocked draft is superseded; `failed_direct_attempts.json` and stopped-state evidence are historical only. No automatic approval rejection occurred.

## Official sources retained

All six retrieved 2026-09-08. Exact official URLs, dates, revisions, byte sizes and SHA-256 are in `hardware/FC_REV_A/docs/evidence/stm32h743/source_manifest.json`; original PDFs and extracted text are retained beside it.

| Document | Rev | Date | Pages | Bytes | SHA-256 |
|---|---|---|---|---|---|
| DS12110 | 11 | January 2026 | 357 | 7075281 | `f6e620179006c8c4d497b477ba065edc89c6dd9ac24d9debb3362910651f42ee` |
| RM0433 | 8 | January 2023 | 3353 | 40711860 | `9ba54135736a47a302cdc28fdc7ca8f23c6eed5a646fa0a639af6ed2ad71336e` |
| AN4938 | 7 | October 2024 | 46 | 1126615 | `217b5dcbfdd27cec4f6013cf1f51930bf81c338ccbaf7bf8dce3fa69592bb8b3` |
| AN2867 | 24 | February 2026 | 60 | 3207867 | `1c92e22e215ca66a159c790589d568830c619d14f31193429787902664eae04e` |
| AN2606 | 70 | February 2026 | 553 | 7560428 | `25b466e39ecc61671dcb988d8ca538462d6452d85f68140cb981ed728f57e654` |
| ES0392 | 15 | September 2025 | 73 | 3278533 | `effe23b2b79ec4ee33a8ab42b1b934cdd34100775cd6ca6b8dc8f3f2f01a1f9e` |

Abracon official ABM3B datasheet, Rev U 2024-08-27, 6 pages, 735461 bytes, SHA-256 `17b7417ea2fa9bdde04c2dd11db78dea61bf362fbbf2009aa94b340d74ecc210`, retained as `abm3b.pdf`; URL `https://abracon.com/Resonators/abm3b.pdf`. Crystal calculation records its provenance separately.

## Symbol audit and provenance

KiCad 10.0.6 installed `MCU_ST_STM32H7.kicad_sym` source SHA-256 `a8a079fa0e3d514e3ce4de014374e61cf7c9b869bbd866c98bab52269361f229` (16221813 bytes). Extracted STM32H743VITx SHA-256 `46d884c1229cb7178aa8de39b86fa703e1102f660e56c5d5f155a7d6cc6f94ac`. The exact local part is STM32H743VIT6, single unit, 100 pins, LQFP100.

`symbol_100_pin_audit.csv` audits every pin against DS12110 Figure 5 and Table 9, including electrical-type interpretation; `verification_stage3/100_pin_net_audit.csv` audits all 100 actual native netlist assignments. Original number/name/type tuples are preserved. The source's hidden legacy VSS stack (10/26/49/74/99) was exposed and geometrically separated; VSSA is also separate. All 100 local pin endpoints are unique.

Inherited modeling exceptions are explicit: NRST is KiCad input although ST describes I/O (internal reset drive); VREF+ is KiCad input although ST lists supply, valid only with external reference mode; PC2_C/PC3_C are analog-only despite inherited bidirectional types and are explicitly NC; four formerly stacked VSS pins remain passive types. VCAP pins remain power outputs, making their required common-regulator connection visible to ERC. Independent net checks compensate for these modeling limits. No full KLC-compliance claim is made. Official KLC checkout `qa/stage04-core/tools/klc`, commit `a8e6066b2498c86ad6333e5425992a12a5c10ed0`, was consulted; no automated KLC checker was run. No EasyEDA import was used.

## Captured circuit and electrical review

| Block | Implemented and checked |
|---|---|
| Digital supply | VDD 11/27/50/75/100 to 3V3_MAIN; VSS 10/26/49/74/99 to common GND. C1–C5 100 nF, one per pair; C6 4.7 uF minimum effective bulk. Placement and effective capacitance remain Stage 08/09 requirements. |
| Internal LDO | Pins 48 and 73 share isolated VCAP, exactly U1.48/U1.73/C7.1/C8.1. C7/C8 each 2.2 uF, ESR <100 mΩ. AN4938 Rev 7 §2.2 explicitly requires VCAP1/2 connection. No other load or test point. Normal LDO firmware configuration and startup sequencing remain bench/firmware obligations. |
| Analog | VDDA21 and VREF+20 to 3V3_ANA, each 100 nF +1 uF (C9/C10, C11/C12); VSSA19 to common GND. VREFBUF external mode ENVR=0, HIZ=1. No ground island. Stage 05 owns analog rail generation/sequencing and parent hierarchy entry. |
| Backup domain | VBAT6 on 3V3_MAIN, C13 100 nF to GND; no separate battery source. |
| HSE | PH0/12 and PH1/13, populated 8 MHz Y1, C15/C16 24 pF. Y1 pins 1/3 are oscillator terminals and 2/4 GND, verified against official package drawing and native netlist. No oscillator test points. |
| LSE | PC14/8 and PC15/9 reserved to Y2/C17/C18, all DNP. Capacitor values and part selection TBD, not frozen. |
| Reset/recovery | NRST14 with C14 100 nF and TP1, internal pull-up; BOOT0/94 with R1 10 kΩ to GND and TP2. No new button or supervisor. Recovery stimulus must be 3.3 V referenced to common GND. |
| Debug | PA13/72 SWDIO TP3, PA14/76 SWCLK TP4, PB3/89 SWO TP5 DNP, GND TP6. TP7 3V3_REF is a direct sense alias of 3V3_MAIN, <=10 mA, no target power injection. Physical access/geometry remain OPEN. |
| USB | PA9/68 USB_VBUS sense reservation only; PA11/70 USB_DM and PA12/71 USB_DP. Each has only its MCU node. No connector, CC, ESD, VBUS-to-FC rail path or power circuit captured. Stage 07 must condition/protect VBUS across all power states and preserve ROM bootloader behavior. |
| Frozen interfaces | Native registry-to-pin comparison passes for every MCU registry row. Other approved peripheral reservations retained; unused pins explicit NC. CAN2 remains DNP/reserved; ESC_CURR_DNP remains informational only. No pin reassignment. |

PWR_FLAG symbols on main, analog and GND declare required driven boundaries; they are not real power sources and do not qualify the future power design. No new ERC exclusions or project settings were introduced.

## HSE recommendation and assumptions

**RECOMMENDATION:** ABM3B-8.000MHZ-B2-T, official ordering-table candidate, CL=18 pF, C0 max 7 pF, ESR max 200 Ω, drive max 100 µW, temperature -20 to +70 °C, tolerance 20 ppm/default stability 50 ppm. Availability, temperature suitability, exact MPN and footprint remain Stage 08 review items.

**ASSUMPTION:** total stray capacitance Cs=6 pF, bounded 5–7 pF pending PCB validation. Symmetric C1=C2=2(CL-Cs)=24 pF, C0G/NP0 1%. Effective CL range 16.88–19.12 pF. AN2867 gmcrit calculation gives 1.2633 mA/V nominal and 1.3791 mA/V upper bound, below the DS12110 HSE maximum critical gm of 1.5 mA/V. This is a conditional analytical check, not measured startup margin. Do not divide the already specified maximum critical gm by five again.

`crystal_calculation.py/json` retains formula, assumptions and results. Startup over voltage/temperature, real parasitics, crystal drive <=100 µW and possible series damping remain OPEN. No drive measurement or production crystal approval is claimed. Frozen firmware OSCILLATOR_HZ 8000000 remains unchanged; future firmware must use crystal mode, not bypass.

## Reference-manual, boot and errata obligations

RM0433 normal LDO startup requires correct LDOEN/BYPASS and ACTVOSRDY handling before RAM/VOS transitions. External VREF mode must remain as captured. AN2606 H74/75 boot pattern and BOOT_ADD option-byte settings must be checked against actual silicon/ROM version during recovery/DFU validation; no firmware/bootloader build was performed. PA9 behavior can depend on ROM version, so later VBUS conditioning must support ROM recovery as well as application firmware.

ES0392 PC13 toggling can disturb LSE on LQFP packages. PC13 BARO_INT assignment is preserved and LSE is DNP; any later LSE population requires explicit errata review. USB pin drive limits, silicon revision and applicable firmware workarounds require Stage 13 validation. No erratum is declared closed by schematic capture.

## Verification and retained ERC

Native KiCad 10.0.6 exports load all nine sheets. Final result: 29 real components (plus 3 PWR_FLAG symbols), 100 MCU pins, 88 exported nets including explicit unconnected pins, zero PCB files. DNP components: C17, C18, Y2 and TP5. All source/type/number checks, exact core net membership, frozen registry mapping and scope hashes pass.

**Native ERC is not clean:** exit 5 with 54 retained items, all individually recorded with justification in `verification_stage3/retained_erc.json`: 51 isolated MCU reservations awaiting downstream circuits; one 3V3_ANA unmatched parent hierarchy entry owned by Stage 05; one required VCAP power-output pair; one intentional 3V3_REF/3V3_MAIN sense alias. Unexpected violations stop verification. Existing project ignored categories are unchanged; no category was newly suppressed. Future interface integration must clear its corresponding retained items.

Native XML netlist, component CSV, nine SVG sheets, nine-page PDF and local-symbol SVG are in `verification_stage3/`; exact CLI commands/stdout/stderr/exit codes are in `commands.json`. Manual review covered root, full core, supply/VCAP/clocks/reset/debug/USB close-ups and native local symbol. Label overlaps found during review were corrected and re-exported. `visual_review.json` binds acceptance to final capture hashes; `verification.json` deliberately defers visual status to that separate record. Root title and library-table description still contain Stage 03 foundation text because those files are outside write scope.

Recheck with `python -X utf8 qa/stage04-core/audit_symbol.py`, `python -X utf8 qa/stage04-core/crystal_calculation.py`, `python -X utf8 qa/stage04-core/verify_core.py` and `python -X utf8 qa/stage04-core/render_views.py`. Review changed renders before refreshing closure. `preflight.py` and `verify_stopped_state.py` are historical pre-capture checkpoints, not final rerun commands. Do not invoke the build script to start any later stage.

## Retained status and handoff boundary

**DECISION:** all nine authorized entry policies are implemented at schematic level. Exact STM32H743VIT6, supply/LDO/analog/VBAT, populated 8 MHz HSE, DNP LSE, reset/boot/debug and MCU-only USB boundaries remain fixed.

**RECOMMENDATION:** MCU `Package_QFP:LQFP-100_14x14mm_P0.5mm` association is retained pending Stage 08 verification; all other footprints are blank and production passive MPNs OPEN. Crystal recommendation is conditional as above.

**DNP:** LSE, optional SWO access, CAN2 external hardware, optional ESC current path and all carried DNP statuses remain preserved. **OPEN:** all original ledger items remain OPEN, including ESC originals/as-built/harness/AM32/bench, UBEC/power qualification, external modules/connectors/sensors, firmware builds/board ID/bootloader, thermal/EMC, exact parts, stackup/layout/routing/manufacturing and physical hardware testing. No authority or status outside Stage 04 was changed.

Next-stage owners must consume the retained boundaries and evidence, particularly 3V3_ANA parent wiring, power-source qualification, USB no-backfeed/ROM behavior, crystal/decoupler placement, and silicon/firmware validation. This task stops here and does not authorize or dispatch Stage 05.

## Exhaustive artifact inventory

`qa/stage04-core/file_manifest.json` enumerates every file under Stage 04 QA (including tool checkout and historical evidence), every retained source-evidence file, this handoff, and the two modified canonical files with sizes/SHA-256. It excludes only its own recursive hash. Generated cache/tool files are identified by their paths and are not circuit deliverables. `final_scope.json` lists the two modifications and confirms all other entry files unchanged. No unrelated circuit file was modified.

## Continuation entry reconciliation — 2026-09-08 12:19 +08:00

**STOP for this continuation: checkpoint description conflicts with existing completed capture.** The new assignment described a source-retention/100-pin-audit checkpoint with no schematic mutation. On entry, the canonical core sheet and local library were already populated, three transaction records and final verification/render evidence existed, and this completed handoff was already present. No capture mutation or verification-script rerun was performed by this continuation, to preserve the existing controlled result.

Fresh SHA-256 read-back compared all 443 entries in the existing `qa/stage04-core/file_manifest.json`: all matched, including the six ST PDFs, extracted texts, source manifest/README, source symbol, 100-pin audit, final capture and this handoff before this addendum. Canonical project is `hardware/FC_REV_A/FC_REV_A.kicad_pro`; zero PCB files exist beneath it. Evidence: `qa/stage04-core/continuation_entry_check.json`. This establishes artifact integrity against the retained manifest, not an independent electrical or visual approval.

The prior completion claims above remain attributed to the existing capture and its evidence. Exact blocker: project control must reconcile the stale dispatch with that completed result and review the existing Stage 04 handoff before any further capture or Stage 05 authorization. Existing native ERC remains reported as 54 retained items; this continuation does not close them. All recommendations, assumptions, OPEN items and human-review requirements above remain in force. Stage 05 was not started. The current control state, canonical KiCad files and prior verification artifacts were not changed. Only this addendum and the new continuation entry evidence were written; the historical entry check retains the pre-addendum handoff hash; the current file manifest is refreshed by the subsequent documentation correction below.

## Project Stage 04 / capture transaction schema correction

Project control subsequently authorized this documentation-only correction and verification rerun. The directories `verification_stage1`, `verification_stage2`, and `verification_stage3` mean bounded capture transactions 1, 2, and 3 within **project Stage 04**, not project Stages 01–03. `verify_core.py` now emits explicit `project_stage: 4` and `capture_transaction: 3` in final `verification.json`. The legacy `stage` key in `expected_capture.json` is read only as the capture-transaction selector.

Both `verify_core.py` and `render_views.py` reran successfully: 29 real components, 100 MCU pins, 88 nets, the same 54 explicitly retained ERC items, and nine rendered views. Existing visual acceptance remains separately bound to unchanged canonical capture hashes; this correction makes no new electrical or physical approval claim. Core schematic SHA-256 remains `cfdd2c628ca1d6b111e19a8772a032bbe0811b52bbfcdc354f82fee7820e5f6c`; local symbol SHA-256 remains `82e8b5ce81502874731fb0b7c38cb35c4660e3c5f491771a88a742fabf7df5e2`. Current control state remains SHA-256 `6f92b3fb74c24da8d87b07a21913f025a9385627dce705d01eeb66cbd17107c0`; no PCB exists. No KiCad file was changed and Stage 05 was not begun.

The file manifest was refreshed after this final handoff text to cover current QA/source evidence, this handoff and both canonical capture files, excluding only the manifest itself. Historical transaction/entry snapshots retain their original meaning and hashes.
