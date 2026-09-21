# abiotic-ch4

Published estimates of Earth's abiotic methane production, in one machine-readable
table. Flux-based biosignature work compares a retrieved methane flux against a single
abiotic ceiling of 3.7e10 molecules cm^-2 s^-1.

## Data

`data/ch4_abiotic_estimates.csv` — one row per published estimate. Values and units
appear as published; fluxes are derived in code, never typed. Three columns carry
the distinctions the argument rests on:

- `kind` — a maximal bound is not a realised flux, and an observational estimate is
  not a model or an inventory over a residence time.
- `estimate_group` — rows estimating the same quantity are alternatives, not
  additive components. `check_summable` refuses to sum them.
- `body` — keeps the five Earth-mass estimate out of any Earth selection.

`data/wogan2026_tableA1_ci_widths.csv` — credible-interval widths from Wogan et al.
(2026), each row flagged for whether its configuration could be verified.

