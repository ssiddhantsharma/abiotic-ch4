from pathlib import Path

import pandas as pd

from .convert import EARTH_RADIUS_CM, tmol_per_yr_to_flux

DATA = Path(__file__).resolve().parents[2] / "data"

REALIZED = ("realized_observational", "realized_modelled", "inventory_derived")


def load(radius_cm=EARTH_RADIUS_CM):
    df = pd.read_csv(DATA / "ch4_abiotic_estimates.csv")
    for end in ("lo", "hi"):
        df[f"flux_{end}"] = tmol_per_yr_to_flux(df[f"tmol_per_yr_{end}"], radius_cm)
    return df


def earth_modern_realized(df):
    return df[(df.body == "earth") & (df.epoch == "modern") & df.kind.isin(REALIZED)].copy()


def check_summable(df):
    # Keir 2010, Cannat 2010 and both Catling & Kasting 2017 numbers estimate the
    # same mid-ocean-ridge flux. Alternatives, not additive components; summing
    # them double-counts that reservoir several-fold.
    clashes = df.estimate_group.dropna().value_counts()
    clashes = clashes[clashes > 1]
    if len(clashes):
        raise ValueError(f"alternative estimates of one quantity: {list(clashes.index)}")


def reservoir_total(df, column="tmol_per_yr_lo"):
    check_summable(df)
    return df[column].dropna().sum()
