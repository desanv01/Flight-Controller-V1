# Architecture

The STM32H743 controller owns real-time stabilization, motor-waveform generation, arming and failsafe. Receiver input, sensor data and external navigation interfaces terminate at the controller. Companion perception/navigation is advisory and separately powered; its failure must not defeat stabilization or safe shutdown.

External battery/power distribution supplies the ESC; the FC/ESC boundary is motor signals and common ground. Controller supply is externally regulated. USB is data/debug and is not a controller power supply.

The custom board contains an ICM42688P, BMP390 and microSD. Main/reference/analog/sensor rails and protection/monitoring were captured in the staged design.

Read [source pinouts](connector-pinouts.md), [power/interface boundaries](power-and-interfaces.md) and the staged development records. Requirements/calculations are not a substitute for physical qualification.
