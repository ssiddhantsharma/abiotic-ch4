# abiotic-ch4

Published estimates of Earth's abiotic methane flux, in one machine-readable table,
with the arithmetic of an accompanying Research Note as a test suite.

The exoplanet literature compares a retrieved methane flux against a single abiotic
ceiling of 3.7e10 molecules cm^-2 s^-1 (10 Tmol/yr on Earth). That number is the
99.7th percentile of the maximum-flux distribution in Krissansen-Totton, Olson &
Catling (2018). This repository collects the published estimates of what Earth
actually produces, so the ceiling can be read against them.

## Data

`data/ch4_abiotic_estimates.csv` holds one row per published estimate, transcribed
from the supplementary text of Thompson et al. (2022, PNAS 119:e2117933119).
Values and units are stored as published; converted fluxes are derived in code.
Two columns do the work:

- `kind` separates a maximal bound from a realised flux, and separates an
  observational estimate from a model or an inventory divided by a residence time.
- `estimate_group` marks rows that are alternative estimates of the same quantity.
  Keir (2010), Cannat et al. (2010) and both Catling & Kasting (2017) numbers are
  alternatives for the mid-ocean-ridge flux, not additive components of it.
  `check_summable` refuses to sum them.

`data/wogan2026_tableA1_ci_widths.csv` holds the credible-interval widths from
Table A1 of Wogan et al. (2026, arXiv:2604.21848). The column-to-configuration
mapping could not be recovered reliably from the PDF and is flagged per row.

## Use

```python
from abiotic_ch4.data import earth_modern_realized, load

rows = earth_modern_realized(load())          # Earth, modern, realised estimates
rows[["source_key", "setting", "flux_lo"]]
```

Fluxes convert from whole-planet molar rates through `convert.tmol_per_yr_to_flux`,
which takes a radius. An Earth-normalised flux does not transfer to another planet.

## Tests

`tests/test_claims.py` regenerates every number quoted in the note from published
inputs, including the Eq. 6 chain of Krissansen-Totton et al. (2018) from its four
sampled parameters. A failure means the claim is wrong.

```
uv run pytest
```

## Figure

```
uv run python make_figure.py
```

## License

MIT
