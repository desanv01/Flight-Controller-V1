> Historical technical record. Names and private workstation/session references were neutralized for publication. Dates and assertions describe the recorded stage, not current physical qualification. See the current validation-status page for later checks.

# FC Rev A — Stage 10 Continuation Control Review

**Date:** 2026-09-11
**Subject:** `FC_REV_A_STAGE_10_CONTINUATION_HANDOFF_2026-09-11.md`
**Scope:** `[LOCAL_SOURCE] DRONE PROJECT` (sandbox copy) only
**Reviewer role:** project control (independent re-run of deterministic checks)

---

## 1. Disposition

**ACCEPTED as a VERIFIED CONDITIONAL PASS at recommendation-grade PCB-implementation scope.**

Stage 10 is **NOT complete**. Stage 11 remains **locked**. No manufacturing export, procurement, fabrication or flight approval is granted or implied.

This is the first control review Stage 10 has ever had. Stage 10 was previously the only stage in the ladder without one.

---

## 2. What was independently re-verified

| Check | Method | Result |
|---|---|---|
| Board identity | SHA-256 of `hardware/FC_REV_A/FC_REV_A.kicad_pcb` | `08727f3679195f6fcb3a48c1224ad8b00695c5643853e6af0550d412dbc348ce`, 4,255,004 B |
| Hash-chain integrity | manifest entry vs `continuation_state.pcb_sha256` vs disk | **all three agree** (previously three different boards were on record) |
| Native DRC | `kicad-cli pcb drc --format json --schematic-parity`, KiCad 10.0.6 | **0 errors**, 11 warnings, 96 unconnected, 3 parity |
| Native ERC | `kicad-cli sch erc --format json` | **13 findings**, unchanged and classified |
| Invariants | `verify_stage10.py` from project root, KiCad bundled Python 3.11.5 | **25/25 PASS, exit 0** |
| Connectivity | `connectivity_accounting.py` + `classify_remaining.py` | 96 links = 73 required + 23 DNP-only; 0 conductive-item artifacts |
| Frozen set | comparison against `entry_manifest.json` | 58 files unchanged; **8 changed = exactly the 8 the Stage 10 release authorises** |
| History | previous stage handoffs and control reviews | **unmodified** |

### 2.1 A necessary correction to the verifier itself

`verify_stage10.py` **could not run on this copy at all** before this work: `entry_manifest.json` stored 66 absolute `[LOCAL_SOURCE]` paths, so `path.relative_to(R)` raised `ValueError`. The manifest has been rewritten to absolute **D:** paths with the **sealed SHA-256 values preserved unchanged**. This is a portability repair, not a relaxation: 58 of 66 entries still match their original sealed hashes, and the 8 that differ are the authorised canonical set.

Two exemptions remain in the 25th check, both now explicitly auditable:

| Exemption | Mechanism | Authorisation |
|---|---|---|
| `FC_REV_A_CURRENT_CONTROL_STATE.md` | bound via `continuation/entry_manifest.json` | Stage 10 may update the rolling control state |
| `hardware/FC_REV_A/docs/retained_status_ledger.md` | pinned digest | Stage 10 may append the ledger |

**Both pins were updated in this change to the new, correct content, and the previous values are recorded here** — see §5. Neither was loosened, and no check was disabled.

---

## 3. Evidence integrity findings raised by this review

1. **⚠ The 2026-09-10 Stage 10 handoff never described the board.** It states 153 unconnected links, 4,880 track segments and 663 vias. The board in the sandbox was measured at **123 / 5,538 / 720**, and the figures were already stale by 19:53 on 2026-09-10. Any downstream document that quotes 153 is quoting documentation, not measurement.
2. **The manifests were stale and the chain was broken.** `final_design_manifest.json` and `continuation_state.json` recorded a 3,958,677-byte board with SHA-256 `1d395da5…`; the Stage 09 ledger recorded `871a0554…`; the file on disk was a third value. The live hash appeared in **no** manifest. Now repaired.
3. **A DRC-flagged dangling via is not necessarily dead copper.** The naive removal of all 88 flagged items raised the unconnected count 123 → 126 and was reverted. Fifteen items are load-bearing layer transitions. The 11 remaining `track_dangling` warnings must be **completed by routing, never deleted**.
4. **`kicad-erc-json.ps1` reported false failure.** It read a top-level `violations` key that the ERC schema does not contain, threw `PropertyNotFoundStrict`, and exited 1 on a successful ERC. Fixed to flatten `sheets[].violations`; ERC now correctly reports 13 findings / 1 error / exit 0.
5. **`~FC_REV_A.kicad_pro.lck` / concurrent-writer risk.** The live original was observed being written during analysis. This sandbox copy was not written by any other process, and the path-repointing of `freerouting.json` (which still targeted `[LOCAL_SOURCE]`) prevents an accidental write into the original.
6. **`verify_stage10.py` remains weakly bound.** Its 25th check compares the control state against a *continuation baseline manifest* rather than a hash recorded at acceptance time. It is honest for this change set, but it is not a strong seal. Recommended for Stage 11: bind both control documents by explicit digest recorded in the control review.

---

## 4. Accepted scope of change

Only the following were modified, all within the Stage 10 release:

- routing, vias and copper on the canonical board (435 track segments added, 15 vias removed net)
- removal of 194 non-load-bearing dangling copper items
- `FC_REV_A.kicad_prl` (editor state)
- QC tooling under `qa/stage10-pcb/`
- `FC_REV_A_CURRENT_CONTROL_STATE.md` and `hardware/FC_REV_A/docs/retained_status_ledger.md`

**Not changed:** electrical topology, component values, net names, UUIDs, the MCU resource map, the 40 schematic DNP decisions, `U5.21` (`EXTVCC_NC`), the USB no-power topology, the `J1`/`J2`/`Y2` footprintless state, the four-layer stackup, the 65 × 65 mm outline, the four Ø2.2 mm NPTH mounts, the POWER1 pads 1–4 / NPTH 5–6 construction, or the sparse five-conductor ESC boundary.

**Deliberately not routed, and verified absent from all copper:** `+BATT`, `/CURR` and every `ESC_CURR*` variant, `CAN2`, and `PA0`/`PA1`.

---

## 5. Pinned values updated in this change

| File | Previous pin | New pin |
|---|---|---|
| `hardware/FC_REV_A/docs/retained_status_ledger.md` | `ad2495b0ff01733af9e25ac1b379bd3557fe8b78aaec820c834ef7ce9c05acdf` | recorded in `verify_stage10.py` after the ledger append |
| `FC_REV_A_CURRENT_CONTROL_STATE.md` | via `continuation/entry_manifest.json` | updated to the new control-state digest |

---

## 6. Required before Stage 11 may be released

1. Close the **73 required** unconnected links (61 nets). `3V3_REF` alone is 9.
2. Keep the **23 DNP-only** island links explicitly classified — do not route them and do not remove the netlist members.
3. Re-run native DRC **with `--schematic-parity` explicitly supplied**, ERC, and `verify_stage10.py`, and regenerate `routing_metrics.json`, `final_design_manifest.json` and `continuation_state.json` against the frozen board.
4. Regenerate renders and 3D views and inspect them.
5. Resolve or explicitly carry forward every Stage 05–09 physical gate — in particular the **absent `(stackup)` block**, which leaves dielectric, copper weight and controlled impedance formally undefined.
6. Put the project under version control. Neither copy has a `.git` of its own; the canonical 4.25 MB board has no undo.

**Do not begin Stage 11 automatically.**

---

## 7. Review statement

The deterministic evidence in §2 was re-run against the frozen board after the change set was complete. The 8-file canonical delta is exactly the authorised set. The hash chain is now internally consistent. The residual 73 required links are recorded as **design work, not waived findings**, and the board is **not fabrication-ready**.

**Stage 10 continuation: ACCEPTED — VERIFIED CONDITIONAL PASS.**
