# ESC INTERFACE CABLE — FC to ESC

**Board:** FC_REV_A rev A · board sha256 `2abc737bc6b5e46deef906b0993eaf17877d6815d22cf7111c6b7df0c1ddb999`

## The two ends are different, and that is expected

| end | connector | positions | pitch |
|---|---|---|---|
| **FC** (this board) | JST **SH**, `SM05B-SRSS-TB` | **5** | **1.0 mm** |
| **ESC** | JST **SH**, `SM08B-SRSS-TB` | **8** | **1.0 mm** |

Both ends are the JST **SH** family at **1.0 mm**. Only the position count differs,
because the FC dropped the three cavities it does not use (VBAT, current sense, NC).

> ⚠️ **Every other connector on this FC is JST GH at 1.25 mm** (RC_IN, GPS1,
> TELEM1, COMPANION, CAN1, CAN2, SWD). The ESC connector is the *only* 1.0 mm SH
> on the board. A GH housing will look almost right and will not fit.

## Wiring — five conductors

| wire | FC pin | signal | ESC pin |
|---|---|---|---|
| 1 | **1** | **GND** | **2** |
| 2 | **2** | **M1** | **5** |
| 3 | **3** | **M2** | **6** |
| 4 | **4** | **M3** | **7** |
| 5 | **5** | **M4** | **8** |

ESC cavities **1, 3 and 4 stay empty** — they are VBAT, current sense and NC.
No VBAT, no current sense, no 5 V conductor is fitted.

### This is "straight-through" if you count populated cavities

The wiring is the Nth wire into the Nth *used* cavity on both ends. It is **not**
straight-through by absolute pin number — `FC1 → ESC2` is a two-position offset.
Any harness drawing that says "straight-through by pin number" applies to an
**8-to-8** cable only; written on a 5-to-8 adapter it would put **GND onto M3**.

## Parts to order

| part | MPN | where |
|---|---|---|
| FC-end housing (5-position) | **SHR-05V-S-B** | JST SH series |
| ESC-end housing (8-position) | **SHR-08V-S-B** | JST SH series |
| Crimp terminal | **SSH-003T-P0.2-H** | AWG **32–28** |

**Wire gauge is limited to AWG 32–28** by the terminal. 26 AWG will not crimp.

## How to build it — easiest practical route

**Buy one off-the-shelf 8-position SH cable and re-terminate one end.** This uses
a standard part for the awkward side and only requires re-doing the other.

1. Buy an **8-position JST SH 1.0 mm cable**, 150 mm, all 8 wires.
2. **Before cutting, note the wire colours** against ESC positions 2, 5, 6, 7, 8.
   If the cable is all-black, buzz it out with a meter first and label the five.
3. Cut off the **8-position housing at one end**.
4. Remove the wires that were in ESC cavities **1, 3 and 4** — leave five.
5. Crimp (or solder) those five into an **SHR-05V-S-B**, keeping their order.
6. Result: 8-position at the ESC, 5-position at the FC, five conductors.

**Alternatives**

- **No tools:** buy a 5-position SH cable *and* an 8-position SH cable, cut both,
  splice the five conductors, heat-shrink. Fine for bench; not for flight.
- **Custom harness seller:** hand them the table above and the parts list. Best
  quality, a few ringgit each. Recommended for the flight harness.

## Verify before you plug anything in

1. **Continuity-check all five conductors** against the table with a multimeter.
2. **Check no conductor lands in ESC cavities 1, 3 or 4.**
3. **Check the pitch.** A 5-position SH 1.0 mm housing measures about **6.6 mm**
   across its mounting pegs; that figure is taken from this board's own copper.
   Anything wider is GH (1.25 mm) or ZH (1.5 mm) and is the wrong part.
4. **Confirm pin 1 from the mating face** against the
   [official JST SH drawing](http[LOCAL_SOURCE] and
   then electrically on the actual ESC. This is the classic mirrored-cable
   failure and it costs an ESC.

## Electrical notes for the harness owner

- **Cable length ≤150 mm** for first bench work.
- Run the **GND conductor adjacent to the motor-signal bundle**.
- **Do not use the connector shell as the only return.**
- Motor signals are 3.3 V CMOS, bidirectional DShot capable. Series elements, if
  any, belong at the ESC end — the FC side is 0R by default.
- The optional current-sense branch is **DNP on the FC**, including contact,
  divider, switch, bypass and protection. PC1 ADC is disabled. Do not fit a
  current-sense conductor on the assumption it will work.

## Board-side history

The FC was built with a 5-position `SM05B-SRSS-TB`. Changing it to the
8-position `SM08B-SRSS-TB` was attempted and abandoned: the taller connector
displaces a **0.80 mm `5V_FC_PROTECTED` power feed** that runs through that
corner, and no connector placement lets the feed pass. The board of record is
unchanged and remains the 5-position part. A rev B could move the connector or
the 5 V feed and adopt the 8-position part.
