> Historical technical record. Names and private workstation/session references were neutralized for publication. Dates and assertions describe the recorded stage, not current physical qualification. See the current validation-status page for later checks.

# FC Drone FC Rev A — Stage 04 Control Review

Date: 2026-09-08  
Reviewer: main project-control chat  
Outcome: **VERIFIED — Stage 04 accepted; Stage 05 not authorized**

## Review scope

- Re-ran the 100-pin symbol audit, crystal calculation, core verification, deterministic netlist checks and scoped ERC.
- Inspected the root, full MCU, local symbol, digital supply, analog supply, VCAP, clock, recovery/debug and USB renders.
- Confirmed that the only canonical KiCad implementation changes are the Stage 04 MCU-core sheet and project-local MCU symbol.
- Confirmed that no PCB file, board geometry, layer stack, placement, routing, Stage 05 power circuit or later-stage circuit was created.
- Refreshed the 446-entry Stage 04 evidence manifest after the independent verifier regenerated export artifacts; the post-refresh mismatch count is zero.

## Verified hashes

| Artifact | SHA-256 |
|---|---|
| `FC_REV_A_CURRENT_CONTROL_STATE.md` (R5) | `ebf4d5a7bcb12b6271df31e083215d7159c1375eb8c1fea90055cab9ede34cda` |
| `FC_REV_A_STAGE_04_H743_CORE_2026-09-07.md` | `5703ee6ed38940f3b71e9b32951baf08826b7790ca3d4d074c5fed42af1309b4` |
| `hardware/FC_REV_A/sheets/01_mcu_core.kicad_sch` | `cfdd2c628ca1d6b111e19a8772a032bbe0811b52bbfcdc354f82fee7820e5f6c` |
| `hardware/FC_REV_A/libraries/FC_REV_A_Local.kicad_sym` | `82e8b5ce81502874731fb0b7c38cb35c4660e3c5f491771a88a742fabf7df5e2` |
| `qa/stage04-core/verification_stage3/verification.json` | `5314559eeabc198ebdd83e0adb73b3716809acd0b9ff999c4e518d6018087fbd` |
| `qa/stage04-core/verification_stage3/visual_review.json` | `bf5a87e38556b1291b3635f5233476c19a6e6c03830f9607a5891d6dd16d2473` |
| `qa/stage04-core/file_manifest.json` | `b743489ca9355ebdc6a6286d968aeff5d7ce81ae4439d338ba5e28bbc0b371b` |

## Controlled exceptions and OPEN items

- Native ERC exits non-zero with 54 fully enumerated, retained items: 51 one-ended MCU resource-reservation labels, one unpowered `3V3_ANA` child boundary deferred to Stage 05, one official VCAP power-output pairing, and one intentional `3V3_REF`/`3V3_MAIN` sense alias. These are controlled findings, not a zero-ERC claim.
- The 8 MHz HSE candidate, load-capacitor calculation, assumed 6 pF stray capacitance, startup margin, drive level, footprint and availability remain **RECOMMENDATION/ASSUMPTION/OPEN** as recorded in the handoff.
- LSE remains DNP/reserved and the PC13/barometer-interrupt interaction remains controlled for later review.
- Stage 04 acceptance is a schematic-core gate only; it is not a fabrication, assembly or flight-readiness approval.

## Next gate

Project control must review the Stage 05 power-tree, regulator, protection and monitoring entry policies and receive explicit human authorization before dispatching Stage 05. Stage 05 was not created or started during this review.
