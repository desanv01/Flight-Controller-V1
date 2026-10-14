# Validation status

Publication source checked on 14 October 2026 using KiCad 10.0.6.

| Check | Result |
|---|---|
| ERC errors / warnings | 0 / 12 |
| DRC rule errors / warnings | 0 / 3 |
| Raw unconnected entries | 16 |
| Schematic parity issues | 0 |
| Physical qualification | Pending |


Every endpoint in the 16 raw DRC unconnected entries is marked DNP. The intended all-DNP islands are retained open; zero required opens is a classified result, not an unqualified zero-error raw DRC. The 3 dangling-copper warnings and 12 ERC warnings remain recorded.

## Evidence

- [Fresh summary](../verification/latest/summary.json)
- [Raw ERC](../verification/latest/erc.json)
- [Raw DRC and parity](../verification/latest/drc.json)
- [Metadata correction and geometry assertion](../verification/latest/publication-corrections.json)

Ignored checker categories are preserved in the raw reports and source project configuration; a clean configured result is not a clean result under every possible check. Warning and DNP dispositions are engineering exceptions, not proof of physical reliability.

## Manufacturing and firmware

V1 manufacturer records retain missing sourcing and stack-selection work; no final firmware build for this board is claimed.

## Physical status

Personal project activity was confirmed by Desan, but no completed measured worksheet, powered sensor qualification or flight result is provided. No flight qualification is claimed. The public engineering bundle is not a certification of a fabricated article.
