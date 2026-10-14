> Historical technical record. Names and private workstation/session references were neutralized for publication. Dates and assertions describe the recorded stage, not current physical qualification. See the current validation-status page for later checks.

# FC Drone FC Rev A - Stage 02 Entry Brief

Date: 2026-09-07  
Entry check: VERIFIED

Objective: freeze bounded FC electrical interfaces, the external power/USB policy, and a conflict-free STM32H743VIT6 resource map suitable for an ArduPilot-first board definition.

Entry decisions: bare H743VIT6; dedicated SPI ICM-42688-P; onboard BMP390; external regulated FC power; separately powered CM5; OpenESC interposer with J1-1 and J1-4 electrically NC; M1-M4 in J1 pins 5-8 order; optional `/CURR` DNP; one required CAN plus a visible second-CAN evaluation; USB-C VBUS sense/no-backfeed; fixed microSD; ArduPilot first and PX4 alternative.

Controlled exceptions: original ESC interface PDF, response document, and BOM are missing; final board outline, layer count, mounting, connector placement, cable release, and external module MPNs remain OPEN.

Required outputs: interface/resource freeze, H743 pin/timer/DMA matrix, port contract, controlled interposer drawing, updated ESC register, and Stage 03 entry brief.

Exit rule: no unresolved pin conflict; four firmware-compatible motor candidates; bounded electrical contract for every required port; explicit NC treatment for J1-1/J1-4; explicit power/USB no-backfeed policies; all remaining OPEN items visible. No KiCad project or circuit capture is authorized in Stage 02.
