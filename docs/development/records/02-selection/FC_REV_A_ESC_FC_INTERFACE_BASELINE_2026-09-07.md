> Historical technical record. Names and private workstation/session references were neutralized for publication. Dates and assertions describe the recorded stage, not current physical qualification. See the current validation-status page for later checks.

# FC Drone FC Rev A
# ESC-FC Interface Baseline

Date: 2026-09-07  
Controlled interface: OpenESC-30x30 J1 to FC/interposer  
Electrical-boundary status: DECISION  
Physical-cable status: OPEN

## 1. Boundary rule

```text
Battery/PDB/ESC domain                         FC logic domain
raw battery, motor current, phases             externally regulated FC power
              |                                             |
OpenESC J1 -> passive bench interposer -> GND + M1..M4 only by default
              X pin 1 +BATT
              X pin 4 NC
              o pin 3 /CURR only as capped DNP option
```

DECISION: the FC-to-ESC boundary is signal and ground only. J1 pin 1 and pin 4 have no FC copper. The interposer must omit conductors for both positions.

## 2. Controlled pin contract

| OpenESC J1 | ESC net | Direction at FC | FC/interposer treatment | Status |
|---:|---|---|---|---|
| 1 | `+BATT` | prohibited | No contact/conductor on first-bench cable; no interposer trace; no FC pad connection, ADC, TVS, divider, test point, or copper | DECISION |
| 2 | `GND` | reference | One dedicated signal-return conductor to FC GND; continuity required before power | DECISION |
| 3 | `/CURR` | analog input candidate | Conductor may terminate at a capped, labelled `CURR_DNP` point only; optional FC conditioning is DNP and informational | DNP |
| 4 | NC | none | No contact/conductor; no trace or FC copper | DECISION |
| 5 | `/M1` | FC output / Bidir return | Logical `ESC_M1`, STM32 TIM4_CH1 candidate | DECISION |
| 6 | `/M2` | FC output / Bidir return | Logical `ESC_M2`, STM32 TIM4_CH2 candidate | DECISION |
| 7 | `/M3` | FC output / Bidir return | Logical `ESC_M3`, STM32 TIM4_CH3 candidate | DECISION |
| 8 | `/M4` | FC output / Bidir return | Logical `ESC_M4`, STM32 TIM4_CH4 candidate | DECISION |

## 3. Electrical contract

- Motor lines: 3.3 V CMOS waveform from the FC; ESC-side approximately 220 ohm series elements are present in the local source. No populated FC/interposer pull-up, pull-down, capacitor, level shifter, or additional series element by default.
- Reset: H743 motor pins are configured as reset-safe pulldown/low in the firmware hardware definition; no arming claim is made until bench reset/disarm tests pass.
- Ground: J1 pin 2 is the only accepted numbered return. Cable length target is at most 150 mm for first bench work; keep the ground conductor adjacent to the motor-signal bundle and do not use the connector shell as the only return.
- `/CURR`: nominal 0-3.3 V reported range, nominal 10 mV/A, approximately 1 kOhm source path. These values are not calibration evidence. PC1/ADC1 is the reserved candidate. Optional input network must be DNP, high-impedance, protected, and non-safety-critical.
- Power: no ESC conductor powers the FC. FC and CM5 use separate regulated branches.

## 4. Physical implementation rule

- ESC header in local source: JST `SM08B-SRSS-TB(LF)(SN)`, side-entry SH family, 1.0 mm pitch.
- Candidate cable housing: JST `SHR-08V-S-B`; exact contacts, wire gauge, crimp process, and finished cable remain OPEN until controlled by the harness owner.
- Pin numbering must be checked from the connector mating face against the official JST SH drawing and then confirmed electrically on the actual ESC.
- First bench interposer has no copper/conductor for J1-1 or J1-4. Their isolation is tested to FC GND, `5V_FC`, `3V3_MAIN`, and every motor lead before any battery connection.
- The interposer is bench-only and is not a flight harness.

## 5. Qualification sequence

1. Unpowered continuity, including explicit J1-1 and J1-4 isolation.
2. PWM, one channel then all channels, props removed.
3. DShot300.
4. Bidirectional DShot300.
5. DShot600.
6. Bidirectional DShot600.
7. FC reset with ESC powered, ESC reset with FC powered, signal disconnect, and ground-disconnect containment.
8. `/CURR` calibration/fault tests only after motor control is stable; results remain informational until accepted.

## 6. Source basis

- Local OpenESC commit `1da7dbd046760160639fb9c3f470702250b4b2cb`.
- Official JST SH connector drawing: https://www.jst-mfg.com/product/pdf/eng/eSH.pdf
- Official AM32 repository README: https://github.com/am32-firmware/AM32/blob/main/README.md
- Recovered integrated memo: `[LOCAL_SOURCE] FILES\ESC_Integration_Confirmation_FC_Team_v3.docx`, SHA-256 `EBA75496BA2D96328D0B650CDC12E1478F503C959608C68E616846C42D58C7D4`.
- The separately named original project interface PDF, original raw ESC response, rev3.3 BOM, and controlled release package are still missing and remain OPEN.
- Any raw-battery self-power instruction in the recovered memo is superseded by this controlled baseline; J1-1 and J1-4 remain no-contact/no-conductor/no-copper.
