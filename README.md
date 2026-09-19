# abiotic-ch4

Published estimates of Earth's abiotic methane production, in one machine-readable
table, with the arithmetic of an accompanying note held in place by tests.

Flux-based biosignature work compares a retrieved methane flux against a single
abiotic ceiling of 3.7e10 molecules cm^-2 s^-1, or 10 Tmol/yr on Earth. That number
is the 99.7th percentile of the maximum-flux distribution of Krissansen-Totton,
Olson & Catling (2018), and it now carries more weight than a bound was meant to:
it sits 1.74 dex above the only other published maximum for the same process, 0.70
dex above anything its own generating equation yields at modern Earth crustal
production rates, and a factor of three below Earth's own biological methane flux.
This repository collects what has actually been published, so the ceiling can be
read against it.

## Data

`data/ch4_abiotic_estimates.csv`, one row per published estimate. Values and units
appear exactly as published; converted fluxes are derived in code, never typed.
Most rows come from the supplementary text of Thompson et al. (2022); the
Guzmán-Marmolejo et al. (2013) and Merdith et al. (2020) rows were read from those
papers directly, which is how the first was found to be a stated *maximum* rather
than a realised flux.

Three columns carry the distinctions the argument rests on:

- `kind` separates a maximal bound from a realised flux, and separates an
  observational estimate from a model or from an inventory divided by a residence
  time. Rows that cannot be extrapolated to a global flux say so instead of
  carrying a number.
- `estimate_group` marks rows that are alternative estimates of the same quantity.
  Keir (2010), Cannat et al. (2010) and both Catling & Kasting (2017) numbers all
  estimate the mid-ocean-ridge flux; they are alternatives, not additive
  components. `check_summable` refuses to sum them.
- `body` keeps the five Earth-mass estimate out of any Earth selection.

`data/wogan2026_tableA1_ci_widths.csv` holds the credible-interval widths from Table
A1 of Wogan et al. (2026). The column-to-configuration mapping could not be
recovered reliably from the PDF, so each row records whether it was verified.

## Use

```python
from abiotic_ch4.data import earth_modern_realized, load

rows = earth_modern_realized(load())          # Earth, modern, realised estimates
rows[["source_key", "setting", "flux_lo"]]
```

`convert.tmol_per_yr_to_flux` takes a radius rather than assuming Earth's, because
an Earth-normalised flux does not transfer to a planet of another size.

`posterior.p_above(log10_ceiling)` rebuilds the marginal methane flux posterior of
Wogan et al. (2026) from the three quantiles they quote and returns the mass above a
candidate ceiling. It reproduces their tabulated 0.77 at the ceiling they adopt. The
agreement follows from honouring the quoted quantiles rather than from the shape
assumed, so it is dependable across the quoted interval and an extrapolation below
it.

## Tests

```
uv run pytest
```

`test_claims.py` regenerates every number quoted in the note from published inputs,
including the Equation 6 chain of Krissansen-Totton et al. (2018) from its four
sampled parameters. A failure there means a claim is wrong, not that a test is
stale. `test_schema.py` guards the table itself, so a row added later cannot quietly
blur the distinctions above.

## Note and figure

```
uv run python make_figure.py        # writes note/figure.png
cd note && latexmk -pdf rnaas.tex
```

Every reference in `note/refs.bib` was transcribed from the reference list of a
paper read in full, or from the cited paper itself. Entries whose DOI could not be
verified simply have no DOI field. AASTeX v7.0.1 dropped the RNAAS class option, so
the file uses the standard manuscript style; confirm the current Research Notes
template with AAS before submitting.

## License

MIT
