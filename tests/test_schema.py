# Guards on the estimate table, so a row added later cannot quietly break the
# distinctions the note rests on.

from pathlib import Path

import pandas as pd
import pytest

from abiotic_ch4.convert import tmol_per_yr_to_flux
from abiotic_ch4.data import check_summable, earth_modern_realized, load

DATA = Path(__file__).resolve().parents[1] / "data"

KINDS = {
    "realized_observational",
    "realized_modelled",
    "inventory_derived",
    "maximal_bound",
    "not_extrapolatable",
    "not_extracted",
}


def test_every_row_carries_a_kind_and_a_locator():
    d = load()
    assert set(d.kind) <= KINDS
    assert d.source_locator.notna().all()
    assert d.source_key.is_unique


def test_rows_with_a_number_record_how_it_was_published():
    d = load()
    numeric = d[d.tmol_per_yr_lo.notna()]
    assert numeric.value_as_published.notna().all()
    assert numeric.units_as_published.notna().all()
    assert (numeric.tmol_per_yr_hi >= numeric.tmol_per_yr_lo).all()


def test_rows_without_a_number_say_why():
    d = load()
    assert set(d[d.tmol_per_yr_lo.isna()].kind) <= {"not_extrapolatable", "not_extracted"}


def test_conversion_is_consistent_with_the_stored_column():
    d = load()
    numeric = d[d.tmol_per_yr_lo.notna()]
    expected = numeric.tmol_per_yr_lo.map(tmol_per_yr_to_flux)
    assert (numeric.flux_lo - expected).abs().max() < 1e-6


def test_alternative_estimates_are_refused_as_a_sum():
    with pytest.raises(ValueError, match="alternative estimates"):
        check_summable(earth_modern_realized(load()))


def test_one_estimate_per_group_sums_without_complaint():
    rows = earth_modern_realized(load())
    one_each = rows.sort_values("tmol_per_yr_lo").groupby("estimate_group", dropna=False).head(1)
    check_summable(one_each.dropna(subset=["estimate_group"]))


def test_no_super_earth_row_reaches_the_earth_selection():
    assert "super_earth_5me" not in set(earth_modern_realized(load()).body)


def test_thompson_and_merdith_agree_on_cannat():
    # Merdith+2020 Sec. 4.3 quote Cannat+2010 as 0.4 Mt/a = 2.4e10 mol/a.
    # An independent check on the transcription chain through Thompson's supplement.
    row = load().set_index("source_key").loc["cannat_2010"]
    assert row.tmol_per_yr_lo == pytest.approx(2.4e10 / 1e12, rel=0.05)


def test_table_a1_flags_what_could_not_be_verified():
    a1 = pd.read_csv(DATA / "wogan2026_tableA1_ci_widths.csv")
    assert set(a1.configuration_verified) == {"yes", "no"}
    assert a1.loc[a1.configuration_verified == "yes", "configuration"].notna().all()


def test_figure_shows_every_published_maximum_for_earth():
    # Guards against the figure quoting one favourably chosen maximum while the
    # table holds others, which is how the note first overstated the comparison.
    import make_figure

    d = load()
    in_data = set(
        d[(d.kind == "maximal_bound") & (d.body == "earth")
          & (d.source_key != "kt2018b_threshold")].source_key
    )
    assert {k for k, _ in make_figure.MAXIMA} == in_data


def test_oxygen_branch_readmits_the_volcanic_false_positive():
    # B_O2 nests inside H_CH4 (Wogan+2026 Eq. 4, explicit in their LaTeX source) and
    # B_CH4 = H_CH4 \ V, so P(V and B_O2) = P(L) - P(H_CH4) + P(V). The union L
    # therefore restores part of the volcanic false-positive region Eq. 3 removes.
    # Table 2 is quoted to two decimals, so this is reported as a bound.
    t = pd.read_csv(DATA / "wogan2026_table2_flux_space_masses.csv").set_index("set")
    for col in ("prior", "posterior_given_d"):
        m = t[col]
        overlap_lo = (m["L"] - 0.005) - (m["H_CH4"] + 0.005) + (m["V"] - 0.005)
        fraction_lo = overlap_lo / (m["V"] + 0.005)
        assert 0.5 < fraction_lo < 0.7
