# Flight Controller V1 physical-validation checklist

No completed measured-result worksheet is established in the inspected evidence. Propellers must be removed for every motor test. Use current-limited regulated power and confirm the exact version/connector contract.

1. Visual inspection, component orientation and DNP/deleted-reference check.
2. Harness polarity, continuity and strain relief.
3. Unpowered rail-to-rail resistance check.
4. Current-limited regulated first power-up; record quiescent current.
5. Measure logic/analog/sensor rails under intended load.
6. Continuous and transient input-load tests; connector/copper temperature.
7. USB-only isolation and externally powered USB backfeed.
8. USB enumeration, reconnect, brownout and recovery.
9. Clock stability; sensor identification, orientation and plausible data.
10. Logging/storage and required external interfaces.
11. CRSF receiver-loss failsafe.
12. ESC signal integrity and motor order/direction with propellers removed.
13. Bidirectional DShot only after baseline waveform qualification.
14. Mechanical fit and supplier CAM/DFM confirmation.
15. Thermal and relevant EMC checks.
16. Record measured values, operator/date and deviations before release decision.

Record results in [worksheet PDF](exports/physical-validation.pdf). A build or EDA pass does not complete these tests.
