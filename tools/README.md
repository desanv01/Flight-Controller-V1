# Publication tools

Run `python tools/check_repository.py` to check current-tree identity, primary local links and manufacturer-source completeness. Fresh KiCad raw checks and geometry assertions are in verification/latest. Historical scripts in the development archive are experiments; their private paths were neutralized and they are not advertised as turnkey tools.

For native rechecking use KiCad CLI `sch erc --format json` and `pcb drc --format json --schematic-parity` with matching project/PCB stems. Preserve configured exceptions; do not suppress warnings merely to claim a pass.
