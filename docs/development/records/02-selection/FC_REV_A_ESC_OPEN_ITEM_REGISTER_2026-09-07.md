> Historical technical record. Names and private workstation/session references were neutralized for publication. Dates and assertions describe the recorded stage, not current physical qualification. See the current validation-status page for later checks.

# FC Drone FC Rev A - ESC Open Item Register

Date: 2026-09-07  
Update point: Stage 02 exit

This register carries forward the detailed P0 table in `FC_REV_A_STAGE_01_CLOSEOUT_AND_ESC_OPEN_REGISTER_2026-09-07.md` and records Stage 02 changes only.

| ID | Stage 02 status | Change / containment | Closure owner and evidence |
|---|---|---|---|
| A-01 | VERIFIED | Local source and remote main match at `1da7dbd046760160639fb9c3f470702250b4b2cb`. | FC control retains hashes. |
| A-02 | OPEN | Integrated memo `ESC_Integration_Confirmation_FC_Team_v3.docx` recovered and checksum VERIFIED. The separately named original interface PDF, original raw ESC response, rev3.3 BOM, and release package remain absent. | ESC owner supplies remaining originals, release ID, and checksums. |
| A-03 | OPEN | No as-built parity evidence. | ESC owner/assembler supplies photos and ECO/substitution record. |
| B-01 | OPEN | Header `SM08B-SRSS-TB(LF)(SN)` and housing `SHR-08V-S-B` are supported by local source, recovered memo, and JST SH-family documentation; final physical view remains unverified. | Harness owner supplies photo and continuity. |
| B-02 | OPEN | Containment: controlled PDF uses connector-face numbering; actual board was not inspected. | Bench owner performs pin-1 continuity. |
| B-03 | OPEN | Containment: direct cable remains unreleased; first bench uses the interposer with positions 1 and 4 omitted. | Harness owner supplies cable drawing, contacts, wire, crimp, and 100% test. |
| C-01 | OPEN | ASSUMPTION for planning is 3S-8S; 2S is unqualified. | ESC owner supplies accepted 2S test if required. |
| C-04 | OPEN | No hot-plug procedure. | PDB/harness owner provides protected procedure and bulk-cap requirement. |
| D-02 | DNP | PC1/ADC1 is reserved; optional conditioning branch is disabled/unpopulated. | FC schematic owner preserves DNP fields. |
| D-03 / D-04 | OPEN | No calibration or fault evidence; hold all safety use. | Joint test owner supplies sweep and fault tests. |
| E-01 | OPEN | H743 candidate supports PWM/DShot, but no waveform test. | T-05/T-06/T-08 bench captures. |
| E-02 | OPEN | Hwdef provides bidirectional input-capture candidates; runtime still unverified. | Bidir300 then Bidir600 waveform/telemetry/error tests. |
| E-03 / F-04 | OPEN | Reset/disarm/loss behavior untested. | Joint bench reset and disconnect tests. |
| E-06 | OPEN | Telemetry fields/logging not frozen. | Firmware owner provides exact AM32/ArduPilot configuration. |
| F-01 | OPEN | AM32 upstream main recorded at `79af09b00c52021895cddff4080a983aa1b1279c`; selected ESC target/release remains unknown. | ESC owner supplies target, binary, checksum, bootloader, config, recovery. |
| F-03 | OPEN | Motor parameters not supplied. | Propulsion owner supplies motor/prop data and config. |
| F-05 | DNP | Thermal foldback is prohibited as an FC safety dependency. | No closure required unless architecture changes. |
| G-01 through G-05 | OPEN | No applicable measured envelope; hold flight claims. | Propulsion owner supplies instrumented results. |
| H-01 | OPEN | FC-facing source is traceable, but ESC ERC/DRC/library/as-built parity was not rerun here. | ESC owner supplies reproducible release audit. |
| H-03 | OPEN | No manufacturing/mechanical release. | ESC owner/manufacturer supplies controlled package. |

Stage 02 containment is sufficient for schematic-foundation work only. It is not sufficient for a direct cable, powered ESC test, flight harness, propulsion sizing, or ESC manufacturing release.

Control note: the recovered memo's proposal to self-power the FC from J1-1 raw battery is rejected by the approved boundary. J1-1 and J1-4 remain no-contact/no-conductor/no-copper positions.
