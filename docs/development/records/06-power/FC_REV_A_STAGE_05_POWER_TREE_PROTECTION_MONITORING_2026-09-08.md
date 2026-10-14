> Historical technical record. Names and private workstation/session references were neutralized for publication. Dates and assertions describe the recorded stage, not current physical qualification. See the current validation-status page for later checks.

# Stage 05 — R18 CONDITIONAL PASS

Date: 2026-09-09. Disposition: CONDITIONAL PASS at engineering recommendation and schematic-capture scope. This is not a production part freeze, fabrication release, flight approval, or Stage 06 authorization.

The six power blocks are captured in `hardware/FC_REV_A/sheets/02_power.kicad_sch` and integrated with the accepted MCU core. Exact selected parts and passives remain RECOMMENDATION. Physical validation and the four source/load/ambient envelopes remain OPEN for approval and measurement; values below are explicit screening assumptions. The R18 conditional-release policy supersedes the historical R16 requirement to prove every physical item before capture. Historical stopped records are retained, including `qa/stage05-power/history/FC_REV_A_STAGE_05_STOPPED_R16_2026-09-09.md` (SHA-256 67bd50cb800e131aaa5546e072e603700868fedccd31f2c877891d757ef02990).

## Authority and human approvals

Authority is `FC_REV_A_CHANGE_CONTROL_CM5_HOSTING_AND_STAGE05_CONDITIONAL_RELEASE_2026-09-09.md` and the R18 control snapshot in `qa/stage05-power/correction_r18/control_R18.md`. Project control explicitly instructed completion of conservative capture, verification and a conditional-pass handoff, with physical proof deferred to assigned gates. The current dispatch explicitly instructed finishing this handoff without redesign or reopening settled policy.

Project control separately approved the minimum MAIN/GND/PWR_STATUS core hierarchy boundary and matching root connections. Final visual cleanup adds three short boundary wire extensions to separate those hierarchy labels from existing local labels. All original core records and original library symbols are preserved. Pending human actions are project-control acceptance of this conditional handoff, approval of unresolved envelopes and later part/footprint freeze, and separate authorization before Stage 06, ordering, fabrication or flight. No manufacturer message was sent.

## Captured implementation

| Function | Exact recommendation | Selection and capture |
|---|---|---|
| POWER1 protection U2 | TPS259470LRPWR | Latching input eFuse; UV/OV, 732 ohm current setting, 100 nF C0G controlled rise, reverse-blocking architecture |
| Startup U3/U11 | TPS3808G01DBVR | Both raw and protected source valid, CT open, wired-AND POWER_RUN; 12–28 ms delay; never connected to NRST |
| MAIN U4 | TPS62130ARGTR | 3 A buck, 1.5 A continuous allocation/2 A transient screen; 31.2k/10k feedback, 100 nF SS |
| AUX converter U5 | TPS552892RYQR | Local feedback before switch; 31.6k/10k feedback; 49.9k frequency resistor; internal VCC LDO; EXTVCC pin21 open |
| AUX limiter U6 | TPS25940LRVCR | Latching protection, 71.5k current setting; 100 nF controlled rise; post-switch health sensing |
| SENS U7 | TPS73633DBVR | 400 mA fixed 3.3 V low-noise LDO, EN controlled by hardware input health AND MAIN PG |
| Health U9/U10 | TPS3700DDCR | Input-health translation and post-switch AUX health; main-powered open-drain outputs |
| Logic U8 | SN74HCS11DR | Main-powered Schmitt AND logic; fail-low informational PB2 status; unused gate inputs grounded |
| MAIN L1 | XAL4020-222MEC | 2.2 uH, ±20%, maximum DCR 38.7 mOhm; 5.6 A saturation/4 A reference RMS rating |
| AUX L2 | XAL7070-682MEC | 6.8 uH, ±20%, maximum DCR 19.62 mOhm; 12.8 A saturation/6.8 A reference RMS rating |
| ANA FB1 | BLM18AG601SN1D | 600 ohm at100 MHz, maximum DCR0.38 ohm; common contiguous GND; R27 zero-ohm bypass DNP |

U2 RPW0010A and U5 RYQ0021A exact recommended packages are recorded, but their footprint fields are intentionally blank pending Stage 08 manufacturer land-pattern creation/audit. Other footprint fields are recommendations, not an approved placement library. TPS552892 pin21 is EXTVCC, not an exposed ground pad. TPS25940 pin21 represents the grounded exposed pad. Duplicate physical supply contacts are all connected; one logical power driver per common output avoids false ERC conflicts.

Critical passives use ±0.5% total resistance error as a design allocation: initial 0.1%, temperature and aging are not silently omitted. The exact 0603 thin-film Yageo RT MPN for every resistor is listed below. Bulk capacitors are GRM32ER71E226KE15L, 22 uF/25 V/X7R/1210; assumed effective range10–28 uF per part requires bias/temperature/lot qualification. C19/C20/C27/C38/C42 are C1206C104J5GACTU 100 nF/50 V/C0G/1206, ±6% total screen. C36 is GRM31CR71H225KA88L 2.2 uF/50 V/X7R/1206 with1.5–2.7 uF assumed effective. C37 is C0603C472J5GACTU 4.7 nF/50 V/C0G/0603. Other100 nF bypasses use GRM188R71H104KA93D. Availability evidence is dated metadata, not stock reservation; exact passive procurement qualification remains OPEN.

## Electrical screening and limits

POWER1 remains5.2 V nominal,4.9–5.5 V at the FC connector,3 A continuous/4 A for100 ms, and input current≤1 A for the first5 ms. AUX remains1 A aggregate, settled limit1.10–1.50 A, and≥4.75 V at the external boundary. OpenRX consumes a reserved0.5 A AUX bucket; all other AUX modules share0.5 A. GNSS/telemetry selection is not frozen. Camera and VL53L5CX-SATEL are separately powered CM5 devices with zero FC load. This is a deliberate hosting decision, not an assumption that unknown FC loads are zero.

| Screen | Result | Meaning |
|---|---|---|
| AUX local regulation | 4.901550–5.093115 V | Reference, divider and FB leakage bounds included |
| AUX external steady floor at1 A | 4.812550 V | Includes64 mOhm switch maximum and25 mOhm allocated external path |
| Floor after illustrative50 mV droop | 4.762550 V | Arithmetic headroom only; no dynamic guarantee |
| Settled AUX limit | 1.139477–1.351091 A | Published±8% accuracy plus total resistor error |
| MAIN rail bound | 3.192792–3.417211 V | PSM reference bounds and100 nA maximum FB leakage |
| Input eFuse current limit | 4.078786–5.035286 A | Accepts4 A pulse; upstream fault coordination remains physical validation |
| First5 ms | 0.311660 A |106 nF pre-eFuse,2 us edge,250 uF protected allocation,10 mA bias reserve; converters delayed≥12 ms |
| AUX startup peak current | 1.100246 A |680 uF total post-switch plus1 A simultaneous load; below settled limit minimum |
| AUX ramp |34.55–54.52 ms | Sensitivity screen; module startup compatibility OPEN |
| Internal POWER1 backfeed allocation | 95.087667 uA | Engineering budget only; assembled all-state measurement OPEN |

The 24 load/efficiency cases and18 AUX startup cases are retained in `calculations.json`. Efficiency80/85/90% is an engineering assumption. At80%, the1.5 A MAIN/25 mA sensor continuous case is below3 A and the2 A MAIN/50 mA sensor transient case is below4 A. The2 A MAIN case is not authorized as continuous: some sensitivity cases exceed3 A. All15 declared screening gates pass. Source impedance, edge/rise behavior, aggregate capacitance/startup concurrency and maximum board ambient remain OPEN envelopes;2 us,680 uF and55/70 C are analysis cases, not a final freeze.

The AUX converter feedback remains local, with compensation680 ohm/2.2 uF/4.7 nF. Historical reduced-order candidate D had approximately71.96 mV additional droop in one screen; that result is not erased or promoted to a50 mV guarantee. R18 permits capture while complete switched-network loop stability, nonlinear startup and transient proof remain OPEN. Effective local AUX capacitance30–84 uF plus680 uF gives≤764 uF, within the published scalar10–1000 uF range; scalar compliance does not prove loop stability.

Thermal calculations use assumed IC losses and reference board thermal resistances. At70 C, estimated main/AUX converter junction temperatures are110.5/117.74 C; these are not guaranteed FC-board results. Copper, hot loss, magnetics loss/saturation, enclosure/airflow and source-contact heating require physical verification. The retained thermal cases cover55 and70 C.

The backfeed budget allocates24.3 uA to the input blocker (five times a4.86 uA typical value, not a guaranteed maximum), about68.69 uA to two100k main-powered status paths,0.1 uA to sequencer sense and2 uA to other internal paths. Downstream reverse currents share the input blocker and are not counted again as separate POWER1 branches. Future external signal paths must be added at Stage07; the strictly-below100 uA assembled requirement remains OPEN.

## Fault states and monitoring

| State | Intended hardware response | Remaining proof |
|---|---|---|
| Cold input insertion | U2 controls protected charging; U3/U11 hold POWER_RUN low until both supplies valid plus delay | Source edge/impedance and first5 ms waveform |
| AUX overload/short | U6 current regulation; persistent thermal fault latches; AUX_HEALTH pulls status low | Startup SOA, short energy, temperature and reset/retry behavior |
| POWER1 invalid/removal | Input health deasserts; SENS_EN and PWR_STATUS go low; sequencers stop converters | Finite delays and very short source interruptions |
| MAIN invalid | MAIN_PG inhibits SENS_EN and PWR_STATUS | Brownout and power-off logic behavior |
| AUX absent/low | U10 open-drain health input deasserts status | Threshold/timing across temperature and prebias |
| Prebiased rails | Input blocking and disabled sensor LDO intended to prevent feed-through | Abrupt short, external prebias and complete reverse-current test |

PWR_STATUS = MAIN_PG AND INPUT_HEALTH AND AUX_HEALTH. It is informational only, with finite delay, and is not an exact4.75 V detector. AUX health rises around4.31–4.49 V. PB2 must remain an input without a pull-up and has no arming, NRST or motor-safety authority. Schmitt thresholds between tabulated supplies use explicit0.8VCC high/0.15VCC low screening allocations. Main-powered inputs avoid direct5 V logic injection. R35 provides220k fail-low bias.

TPS736 reverse-blocking guarantee requires EN≤0.5 V before its input disappears. The protected minimum80 uF bank gives about39 us of calculated hold at3 A to3.3 V. The comparator18 us is typical, not a guaranteed maximum; abrupt source shorts and reverse stress are still OPEN. TPS73630 uVrms noise is typical with100 nF NR; high-frequency PSRR is not claimed without measurement. Sensor allocation25 mA continuous/50 mA screen and100 mA reserve requires Stage06 reconciliation.

VBAT_SENSE remains DNP with no conditioning or external conductor. No new ADC source is captured; any later divider requires source-impedance/acquisition analysis before enabling it. No USB-to-FC power path, ESCJ1-1/J1-4 conductor, CM5 power path, VCAP test load, oscillator test point or raw-battery test point was added. CAN2 and ESC_CURR_DNP remain reserved. Historical LIDAR_FC labels at PA0/PA1 are preserved core reservation records only; the interface is retired and unconsumed. RC CRSF remains PC6/PC7.

TP8–TP15 expose raw input, protected input, AUX, MAIN, SENS, ANA, PWR_STATUS and GND respectively. ANA uses FB1 or the mutually exclusive DNP R27 bypass; no split ground island is introduced.

## Verification and exact scope delta

KiCad10.0.6 native XML, ERC JSON, nine SVG pages and nine-page PDF were regenerated. Final result:118 real components (29 retained core plus89 Stage05),138 nets,262 real Stage05 pin-net checks plus one power-flag declaration, zero mismatches, and100 manufacturer-to-symbol IC pin checks. Native export excludes power flags from real-component counts. Eight new IC symbol definitions retain exact physical pin numbering; the original MCU library symbol remains byte-identical.

ERC retains53 findings:50 unconsumed MCU labels, one official-required VCAP power-output pair, and two intentional aliases (MAIN/REF and POWER1 A/B). The prior ANA hierarchy and PWR_STATUS isolated-label findings are consumed. There are no remaining off-grid or undriven-power findings and no new ERC suppression. `retained_erc.json` enumerates every finding. ERC is controlled, not zero-error circuit acceptance.

The101-file entry audit permits only the root, local symbol library, core boundary, power sheet and this handoff to differ. Existing core records are preserved exactly; only3 hierarchical labels and3 short boundary wire extensions are appended. Root changes connect MAIN/GND/ANA/PWR_STATUS between the two existing sheets and align their boxes. Other six child sheets, MCU resources, project settings and controlled net registry are unchanged. Root title, revision A-S05-R18 and date 2026-09-09 identify Stage05 capture. Its visible note states that the MCU core and Stage05 power are captured and remaining sheets are unpopulated; the title block states RECOMMENDATION / OPEN / UNTESTED - NOT FOR FABRICATION. This control-requested metadata correction changes no sheet geometry, pins, wires, circuits or child sheets.

Full power/core/root and all six power close-ups were visually inspected. Overlapping power and core boundary labels were corrected and rendered again. Source pin diagrams for the new LDO, sequencer and Schmitt logic were inspected. R18 output hashes bind the final review. No Stage06 or PCB work occurred; zero PCB files exist. `FC_REV_A_CURRENT_CONTROL_STATE.md` is unchanged.

Reproduce with the available Python environment: run `calculations.py`, `verify_capture.py`, `render_extra.py`, then `final_verify.py` in `qa/stage05-power/correction_r18`. Do not rerun one-time entry or boundary-capture scripts. `final_audit.json`, `source_to_symbol_pin_audit.csv`, `recommendation_bom.csv`, `verification_6/commands.json` and `file_manifest.json` form the handoff evidence.

PSpice for TI is installed; the user reported a successful vendor-project run. No FC-specific R18 PSpice result or inaccessible workbook formula is claimed. The retained official SLVME05 ZIP has SHA-256 b6e087f603ce774de0a6b2ec197d733b8e2723e0a3160ee7509142f5a658c525. Historical aborted runs remain historical. Simulation is supporting work under R18, not a substitute for physical qualification.

## Deferred OPEN items, owners and gates

| OPEN item | Owner | Required gate |
|---|---|---|
| Source rise/impedance, startup concurrency/capacitance, ambient envelopes | Project control with power engineer | Approve final contract before part/production freeze; reassess calculations on any change |
| Actual sensor loads, sequence and noise susceptibility | Stage06 sensor owner | Reconcile25/50 mA and100 mA reserve before sensor capture acceptance |
| AUX module1 A aggregate, OpenRX0.5 A, external leakage, connector≤25 mOhm allocation | Stage07 interfaces owner | Qualify selected modules/connectors, startup compatibility and all power-state paths |
| U2/U5 land patterns, all package/pad/assembly validation | Stage08 footprint owner | Manufacturer drawing and pin-pad audit before placement/fabrication |
| Power loop layout, return paths and thermal copper | PCB owner | Placement/routing review; no schematic thermal estimate substitutes for board review |
| Startup SOA, loop stability, load transients, prebias/removal/restart, short/latch behavior | Power coupon and Stages11–13 validation owner | Measure approved corners; demonstrate4.75 V requirement and first5 ms≤1 A before flight/production |
|55/70 C thermal performance, EMI/PSRR and actual magnetic loss | Stages11–13 validation owner | Enclosure/airflow/hot-load measurements and applicable EMC tests |
| Strictly<100 uA assembled POWER1 backfeed and timed sensor reverse blocking | Stage07 path accounting plus Stages11–13 test owner | All assembled power states measured before flight/production |
| Exact passive availability, effective capacitance, resistor drift, production sourcing | BOM/Stage08 owner | Qualify exact MPNs and approve production freeze |

All earlier OPEN items survive unless explicitly superseded above; none is silently closed by this conditional pass.

## Exact Stage06 entry criteria

1. Project control explicitly accepts this R18 conditional handoff and its complete deferred OPEN ledger.
2. Project control explicitly authorizes Stage06 and assigns the sensor owner; this report does not dispatch it.
3. Stage06 uses the accepted MCU resources and captured3V3_SENS/MAIN/GND boundaries, reconciles actual sensor load and startup/noise requirements within the allocations, and submits any change through control.
4. Camera/VL53L5CX remain on separately powered CM5; retired LIDAR_FC/PA0/PA1 remain reserved. No new FC rail or MCU resource is inferred.
5. Production freeze, PCB, fabrication and flight remain gated separately; the physical OPEN validations stay assigned and visible.

## Exact captured recommendation BOM

This is the native-netlist-derived Stage05 BOM, including DNP recommendation R27 and test access. No order or production approval is implied.

| Reference | Value | Exact MPN | Recommended footprint |
|---|---|---|---|
| C19 | 100n | C1206C104J5GACTU | Capacitor_SMD:C_1206_3216Metric |
| C20 | 100n | C1206C104J5GACTU | Capacitor_SMD:C_1206_3216Metric |
| C21 | 22u | GRM32ER71E226KE15L | Capacitor_SMD:C_1210_3225Metric |
| C22 | 100n | GRM188R71H104KA93D | Capacitor_SMD:C_0603_1608Metric |
| C23 | 22u | GRM32ER71E226KE15L | Capacitor_SMD:C_1210_3225Metric |
| C24 | 22u | GRM32ER71E226KE15L | Capacitor_SMD:C_1210_3225Metric |
| C25 | 22u | GRM32ER71E226KE15L | Capacitor_SMD:C_1210_3225Metric |
| C26 | 100n | GRM188R71H104KA93D | Capacitor_SMD:C_0603_1608Metric |
| C27 | 100n | C1206C104J5GACTU | Capacitor_SMD:C_1206_3216Metric |
| C28 | 100n | C1206C104J5GACTU | Capacitor_SMD:C_1206_3216Metric |
| C29 | 100n | C1206C104J5GACTU | Capacitor_SMD:C_1206_3216Metric |
| C30 | 22u | GRM32ER71E226KE15L | Capacitor_SMD:C_1210_3225Metric |
| C31 | 22u | GRM32ER71E226KE15L | Capacitor_SMD:C_1210_3225Metric |
| C32 | 22u | GRM32ER71E226KE15L | Capacitor_SMD:C_1210_3225Metric |
| C33 | 22u | GRM32ER71E226KE15L | Capacitor_SMD:C_1210_3225Metric |
| C34 | 22u | GRM32ER71E226KE15L | Capacitor_SMD:C_1210_3225Metric |
| C35 | 100n | GRM188R71H104KA93D | Capacitor_SMD:C_0603_1608Metric |
| C36 | 2.2u | GRM31CR71H225KA88L | Capacitor_SMD:C_1206_3216Metric |
| C37 | 4.7n | C0603C472J5GACTU | Capacitor_SMD:C_0603_1608Metric |
| C38 | 100n | C1206C104J5GACTU | Capacitor_SMD:C_1206_3216Metric |
| C39 | 100n | GRM188R71H104KA93D | Capacitor_SMD:C_0603_1608Metric |
| C40 | 22u | GRM32ER71E226KE15L | Capacitor_SMD:C_1210_3225Metric |
| C41 | 22u | GRM32ER71E226KE15L | Capacitor_SMD:C_1210_3225Metric |
| C42 | 100n | C1206C104J5GACTU | Capacitor_SMD:C_1206_3216Metric |
| C43 | 100n | GRM188R71H104KA93D | Capacitor_SMD:C_0603_1608Metric |
| C44 | 100n | GRM188R71H104KA93D | Capacitor_SMD:C_0603_1608Metric |
| C45 | 100n | GRM188R71H104KA93D | Capacitor_SMD:C_0603_1608Metric |
| C46 | 100n | GRM188R71H104KA93D | Capacitor_SMD:C_0603_1608Metric |
| C47 | 22u | GRM32ER71E226KE15L | Capacitor_SMD:C_1210_3225Metric |
| C48 | 22u | GRM32ER71E226KE15L | Capacitor_SMD:C_1210_3225Metric |
| C49 | 22u | GRM32ER71E226KE15L | Capacitor_SMD:C_1210_3225Metric |
| C50 | 22u | GRM32ER71E226KE15L | Capacitor_SMD:C_1210_3225Metric |
| FB1 | 600R@100MHz | BLM18AG601SN1D | Inductor_SMD:L_0603_1608Metric |
| L1 | 2.2u | XAL4020-222MEC | Inductor_SMD:L_Coilcraft_XAL4020-XXX |
| L2 | 6.8u | XAL7070-682MEC | Inductor_SMD:L_Coilcraft_XAL7070-XXX |
| R2 | 28.7k | RT0603BRD0728K7L | Resistor_SMD:R_0603_1608Metric |
| R3 | 10k | RT0603BRD0710KL | Resistor_SMD:R_0603_1608Metric |
| R4 | 37.4k | RT0603BRD0737K4L | Resistor_SMD:R_0603_1608Metric |
| R5 | 10k | RT0603BRD0710KL | Resistor_SMD:R_0603_1608Metric |
| R6 | 732 | RT0603BRD07732RL | Resistor_SMD:R_0603_1608Metric |
| R7 | 100 | RT0603BRD07100RL | Resistor_SMD:R_0603_1608Metric |
| R8 | 100k | RT0603BRD07100KL | Resistor_SMD:R_0603_1608Metric |
| R9 | 10k | RT0603BRD0710KL | Resistor_SMD:R_0603_1608Metric |
| R10 | 100k | RT0603BRD07100KL | Resistor_SMD:R_0603_1608Metric |
| R11 | 31.2k | RT0603BRD0731K2L | Resistor_SMD:R_0603_1608Metric |
| R12 | 10k | RT0603BRD0710KL | Resistor_SMD:R_0603_1608Metric |
| R13 | 10k | RT0603BRD0710KL | Resistor_SMD:R_0603_1608Metric |
| R14 | 31.6k | RT0603BRD0731K6L | Resistor_SMD:R_0603_1608Metric |
| R15 | 10k | RT0603BRD0710KL | Resistor_SMD:R_0603_1608Metric |
| R16 | 49.9k | RT0603BRD0749K9L | Resistor_SMD:R_0603_1608Metric |
| R17 | 680 | RT0603BRD07680RL | Resistor_SMD:R_0603_1608Metric |
| R18 | 71.5k | RT0603BRD0771K5L | Resistor_SMD:R_0603_1608Metric |
| R19 | 34.8k | RT0603BRD0734K8L | Resistor_SMD:R_0603_1608Metric |
| R20 | 10k | RT0603BRD0710KL | Resistor_SMD:R_0603_1608Metric |
| R21 | 45.3k | RT0603BRD0745K3L | Resistor_SMD:R_0603_1608Metric |
| R22 | 10k | RT0603BRD0710KL | Resistor_SMD:R_0603_1608Metric |
| R23 | 1k | RT0603BRD071KL | Resistor_SMD:R_0603_1608Metric |
| R24 | 34.8k | RT0603BRD0734K8L | Resistor_SMD:R_0603_1608Metric |
| R25 | 10k | RT0603BRD0710KL | Resistor_SMD:R_0603_1608Metric |
| R26 | 220k | RT0603BRD07220KL | Resistor_SMD:R_0603_1608Metric |
| R27 | 0 | RC0603JR-070RL | Resistor_SMD:R_0603_1608Metric |
| R28 | 100k | RT0603BRD07100KL | Resistor_SMD:R_0603_1608Metric |
| R29 | 137k | RT0603BRD07137KL | Resistor_SMD:R_0603_1608Metric |
| R30 | 49.9k | RT0603BRD0749K9L | Resistor_SMD:R_0603_1608Metric |
| R31 | 100k | RT0603BRD07100KL | Resistor_SMD:R_0603_1608Metric |
| R32 | 10k | RT0603BRD0710KL | Resistor_SMD:R_0603_1608Metric |
| R33 | 100k | RT0603BRD07100KL | Resistor_SMD:R_0603_1608Metric |
| R34 | 10k | RT0603BRD0710KL | Resistor_SMD:R_0603_1608Metric |
| R35 | 220k | RT0603BRD07220KL | Resistor_SMD:R_0603_1608Metric |
| R36 | 100k | RT0603BRD07100KL | Resistor_SMD:R_0603_1608Metric |
| R37 | 10k | RT0603BRD0710KL | Resistor_SMD:R_0603_1608Metric |
| TP8 | 5V_FC_IN | PCB_TEST_PAD | TestPoint:TestPoint_Pad_D1.0mm |
| TP9 | 5V_FC_PROTECTED | PCB_TEST_PAD | TestPoint:TestPoint_Pad_D1.0mm |
| TP10 | 5V_AUX | PCB_TEST_PAD | TestPoint:TestPoint_Pad_D1.0mm |
| TP11 | 3V3_MAIN | PCB_TEST_PAD | TestPoint:TestPoint_Pad_D1.0mm |
| TP12 | 3V3_SENS | PCB_TEST_PAD | TestPoint:TestPoint_Pad_D1.0mm |
| TP13 | 3V3_ANA | PCB_TEST_PAD | TestPoint:TestPoint_Pad_D1.0mm |
| TP14 | PWR_STATUS | PCB_TEST_PAD | TestPoint:TestPoint_Pad_D1.0mm |
| TP15 | GND | PCB_TEST_PAD | TestPoint:TestPoint_Pad_D1.0mm |
| U2 | TPS259470LRPWR | TPS259470LRPWR | OPEN — exact package recorded |
| U3 | TPS3808G01DBVR | TPS3808G01DBVR | Package_TO_SOT_SMD:SOT-23-6 |
| U4 | TPS62130ARGTR | TPS62130ARGTR | Package_DFN_QFN:VQFN-16-1EP_3x3mm_P0.5mm_EP1.68x1.68mm |
| U5 | TPS552892RYQR | TPS552892RYQR | OPEN — exact package recorded |
| U6 | TPS25940LRVCR | TPS25940LRVCR | Package_DFN_QFN:Texas_RVC0020A_WQFN-20-1EP_3x4mm_P0.5mm_EP1.6x2.6mm |
| U7 | TPS73633DBVR | TPS73633DBVR | Package_TO_SOT_SMD:SOT-23-5 |
| U8 | SN74HCS11DR | SN74HCS11DR | Package_SO:SOIC-14_3.9x8.7mm_P1.27mm |
| U9 | TPS3700DDCR | TPS3700DDCR | Package_TO_SOT_SMD:SOT-23-6 |
| U10 | TPS3700DDCR | TPS3700DDCR | Package_TO_SOT_SMD:SOT-23-6 |
| U11 | TPS3808G01DBVR | TPS3808G01DBVR | Package_TO_SOT_SMD:SOT-23-6 |

## Retained manufacturer sources and SHA-256

Official URLs are recorded in captured Datasheet fields and the source manifests. The following archived PDFs are the electrical/pin references; catalog metadata is not electrical authority.

- `hardware/FC_REV_A/docs/evidence/stage05-power/correction_r18/tps736.pdf` — 2682751 bytes; SHA-256 `f2da4943d86f038b91ae01bd0557005ed3668cd19deb5f9cf2643605a0a3c09a`.
- `hardware/FC_REV_A/docs/evidence/stage05-power/correction_r18/tps3808.pdf` — 2046179 bytes; SHA-256 `74d889c0f68af88032f1633c26381817cc03e10d9fd3b4c177a044ad3ed86eed`.
- `hardware/FC_REV_A/docs/evidence/stage05-power/correction_r18/sn74hcs11.pdf` — 866132 bytes; SHA-256 `6ffa1a25896aa1ccd3710cf4de2dbe53df0a0ce2c55c264cf4d6056c7a1f43bc`.
- `hardware/FC_REV_A/docs/evidence/stage05-power/correction_r18/xal7070.pdf` — 340033 bytes; SHA-256 `9bb7b523fa75218340ed3f1fa1dd34674de3d991fa90295d25b8bb2dbfe1e0c7`.
- `hardware/FC_REV_A/docs/evidence/stage05-power/correction_r14/tps552892.pdf` — 4029366 bytes; SHA-256 `e6c43e81cf061644829df94d5a31c01b3ed27999af6bbe71f8ea0837e32e2d92`.
- `hardware/FC_REV_A/docs/evidence/stage05-power/correction_r14/tps25940.pdf` — 2415019 bytes; SHA-256 `9db4dc76b1040251f56d994041d2e6f02f1307d687aecbc5218f137a5c830adc`.
- `hardware/FC_REV_A/docs/evidence/stage05-power/correction_r14/tps25947.pdf` — 5316794 bytes; SHA-256 `8f96de389903091650d4f462dcfad3210071c3ae7093623a7978f34baf8a65b4`.
- `hardware/FC_REV_A/docs/evidence/stage05-power/correction_r12/tps62130a.pdf` — 2536822 bytes; SHA-256 `f9b1af285622c0cf1a5991f9641a6e64c5e6d899e52cc0b1632808742019579f`.
- `hardware/FC_REV_A/docs/evidence/stage05-power/correction_r16/tps3700.pdf` — 682865 bytes; SHA-256 `8475322a39f31bdfedcaf114c748d133e2572ff1b63d12c1c304778909431eab`.
- `hardware/FC_REV_A/docs/evidence/stage05-power/correction_r10/xal40xx.pdf` — 210340 bytes; SHA-256 `b26cf975bd56a807173b05665bddd49ed49323400330eb8f6fa63e24ff6d7d15`.
