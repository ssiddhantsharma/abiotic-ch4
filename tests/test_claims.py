# Every number quoted in the note, regenerated from published inputs.
# A failure here means the claim is wrong.

import math
from pathlib import Path

import pandas as pd
from pytest import approx

from abiotic_ch4.convert import tmol_per_yr_to_flux
from abiotic_ch4.data import earth_modern_realized, load
from abiotic_ch4.kt2018 import (
    MAX_CORNER,
    MODERN_EARTH,
    ch4_tmol_per_yr,
    feo_tmol_per_yr,
    h2_tmol_per_yr,
)

DATA = Path(__file__).resolve().parents[1] / "data"

# Wogan et al. 2026 (arXiv:2604.21848). Sec. 2.2 for the biological flux,
# after Catling & Kasting 2017; Eq. 1 for the threshold; Sec. 3.2 for the retrieval.
BIOLOGICAL = 1.122e11
THRESHOLD = 3.7e10
THRESHOLD_TMOL = 10.0
RETRIEVED_LOG10 = 11.2

REALIZED_EARTH = tmol_per_yr_to_flux(ch4_tmol_per_yr(MODERN_EARTH))


def test_ten_tmol_per_year_is_the_quoted_threshold():
    assert tmol_per_yr_to_flux(THRESHOLD_TMOL) == approx(THRESHOLD, rel=0.02)


def test_kt2018b_feo_production_is_79_tmol():
    assert feo_tmol_per_yr(5.7e13, 0.10) == approx(79.0, rel=0.01)


def test_kt2018b_modern_earth_h2_is_point_two_tmol():
    assert h2_tmol_per_yr(MODERN_EARTH) == approx(0.2, rel=0.02)


def test_low_corner_of_kt2018b_ranges_is_realised_modern_earth():
    assert math.log10(REALIZED_EARTH) == approx(7.67, abs=0.01)


def test_high_corner_sits_above_the_adopted_threshold():
    high = tmol_per_yr_to_flux(ch4_tmol_per_yr(MAX_CORNER))
    assert math.log10(high) == approx(10.87, abs=0.01)
    assert high > THRESHOLD


def test_ceiling_ambiguity_spans_2_9_dex():
    assert math.log10(THRESHOLD / REALIZED_EARTH) == approx(2.90, abs=0.02)


def test_threshold_is_three_times_under_earths_biological_flux():
    assert BIOLOGICAL / THRESHOLD == approx(3.0, abs=0.05)


def test_no_published_realised_estimate_reaches_the_threshold():
    rows = earth_modern_realized(load())
    assert len(rows) == 11
    highest = rows.flux_hi.max()
    assert highest < THRESHOLD
    assert math.log10(highest) == approx(9.06, abs=0.02)  # Fiebig et al. 2009, continental


def test_ceiling_ambiguity_exceeds_the_spectroscopic_uncertainty():
    table = pd.read_csv(DATA / "wogan2026_tableA1_ci_widths.csv")
    as_retrieved = table.loc[table.column == 1, "ci_width_dex"].item()
    best_case = table.ci_width_dex.min()
    assert (as_retrieved, best_case) == (1.5, 0.1)

    ambiguity = math.log10(THRESHOLD / REALIZED_EARTH)
    assert ambiguity / as_retrieved == approx(1.93, abs=0.05)
    assert ambiguity / best_case == approx(29, abs=1)


def test_ceiling_choice_moves_the_detectability_floor_800_fold():
    assert BIOLOGICAL / REALIZED_EARTH == approx(2400, rel=0.05)
    assert THRESHOLD / REALIZED_EARTH == approx(800, rel=0.05)


def test_retrieved_flux_clears_both_the_threshold_and_realised_earth():
    assert RETRIEVED_LOG10 > math.log10(THRESHOLD)
    assert RETRIEVED_LOG10 - math.log10(REALIZED_EARTH) == approx(3.53, abs=0.02)
