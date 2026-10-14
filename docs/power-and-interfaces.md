# Power and interface boundaries

Controller input uses an externally regulated supply. The design basis is 5.2 V nominal and 4.9–5.5 V at the input pads under load, with 3 A continuous and 4 A/100 ms transient design targets. These are requirements, not passed physical measurements.

USB is data/debug only. External power is required before USB operation. Battery voltage must never be applied to the regulated FC input. ESC and companion loads are not powered through the FC input budget.

Use the V1 POWER1 source contract and its exact connector/pad definitions. The root custom design contains separate protected power, reference, analog and sensor rails. Optional current telemetry is DNP and cannot be used as a safety input before qualification.

Common signal ground does not authorize back-powering. Use [actual connector nets](connector-pinouts.md), vendor harness data and the [physical checklist](bring-up.md). Hardware/shield references differ between V1 and V2.
