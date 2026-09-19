import math
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

from abiotic_ch4.convert import tmol_per_yr_to_flux
from abiotic_ch4.data import earth_modern_realized, load
from abiotic_ch4.kt2018 import (
    FR_CH4,
    FR_FEO,
    FR_H2,
    MODERN_EARTH,
    P_CRUST,
    Params,
    ch4_tmol_per_yr,
)

THRESHOLD = 3.7e10  # Wogan et al. 2026, Eq. 1
BIOLOGICAL = 1.122e11  # modern Earth, Catling & Kasting 2017 via Wogan et al. 2026
RETRIEVED, CI_LO, CI_HI = 11.2, 10.3, 11.8  # Wogan et al. 2026, Sec. 3.2
BEST_CASE_CI = 0.1  # narrowest width in their Table A1

# Okabe-Ito; shape carries the same distinction for print and CVD readers.
STYLE = {
    "realized_observational": ("#0072B2", "o", "observational"),
    "realized_modelled": ("#D55E00", "s", "model"),
    "inventory_derived": ("#009E73", "^", "inventory / residence time"),
}

# Every other published maximum for this process, so the ceiling is not compared
# against a single favourably chosen one.
MAXIMA = [
    ("guzman_marmolejo_2013_1me", "Guzmán-Marmolejo+ 2013"),
    ("merdith_2020_max", "Merdith+ 2020 (maximum)"),
    ("fiebig_2007_archean", "Fiebig+ 2007 (Archean)"),
]

SHORT = {
    "merdith_2020_preferred": "Merdith+ 2020",
    "emmanuel_ague_2007": "Emmanuel & Ague 2007",
    "schindler_kasting_2000": "Schindler & Kasting 2000",
    "cannat_2010": "Cannat+ 2010",
    "keir_2010": "Keir 2010",
    "catling_kasting_2017_axial": "Catling & Kasting 2017 (axial)",
    "catling_kasting_2017_offaxis": "Catling & Kasting 2017 (off-axis)",
    "kasting_2005_present": "Kasting 2005",
    "fiebig_2007_present": "Fiebig+ 2007",
    "fiebig_2009": "Fiebig+ 2009 (continental)",
    "portella_2019": "Portella+ 2019",
    "klein_2019": "Klein+ 2019",
}


def main():
    d = load()
    rows = earth_modern_realized(d).sort_values("flux_lo").reset_index(drop=True)
    by_key = d.set_index("source_key")

    earth_cal = math.log10(tmol_per_yr_to_flux(ch4_tmol_per_yr(MODERN_EARTH)))
    earth_crust_max = math.log10(
        tmol_per_yr_to_flux(
            ch4_tmol_per_yr(Params(P_CRUST[0], FR_FEO[1], FR_H2[1], FR_CH4[1]))
        )
    )

    fig = plt.figure(figsize=(7.6, 6.0))
    gs = GridSpec(2, 1, height_ratios=[4.2, 1.3], hspace=0.26)
    ax, bx = fig.add_subplot(gs[0]), fig.add_subplot(gs[1])
    for a in (ax, bx):
        a.set_xlim(2.6, 13.4)
        a.spines[["top", "right"]].set_visible(False)

    for y, r in rows.iterrows():
        color, marker, _ = STYLE[r.kind]
        x = math.log10(r.flux_lo)
        ax.plot(x, y, marker, color=color, ms=6.5, zorder=3)
        ax.text(x - 0.16, y, SHORT[r.source_key], ha="right", va="center",
                fontsize=7, color="0.2")

    for i, (key, label) in enumerate(MAXIMA):
        x = math.log10(tmol_per_yr_to_flux(by_key.loc[key].tmol_per_yr_lo))
        y = len(rows) + i * 0.85
        ax.plot(x, y, "D", mfc="white", mec="0.25", mew=1.2, ms=6.5, zorder=3)
        ax.text(x - 0.16, y, label, ha="right", va="center", fontsize=7, color="0.25")

    top = len(rows) + 3.1
    ax.errorbar(RETRIEVED, top, xerr=[[RETRIEVED - CI_LO], [CI_HI - RETRIEVED]],
                fmt="o", color="0.15", ms=5.5, capsize=3, lw=1.3, zorder=3)
    ax.text(CI_HI + 0.18, top, "retrieved,\n10 JWST transits", ha="left", va="center",
            fontsize=7, color="0.2")

    lines = [
        (math.log10(THRESHOLD), "0.15", "-", 1.3, "adopted abiotic ceiling", "right", -1.3),
        (math.log10(BIOLOGICAL), "0.45", (0, (4, 2)), 1.1, "modern Earth biological", "left", -1.3),
        (earth_crust_max, "0.45", (0, (1, 1.6)), 1.1, "Eq. 6 at modern crustal production",
         "right", -2.5),
    ]
    for x, color, ls, lw, label, side, ly in lines:
        ax.plot([x, x], [ly - 0.15, len(rows) + 2.3], color=color, lw=lw, ls=ls, zorder=1)
        ax.text(x + (0.08 if side == "left" else -0.08), ly, label, fontsize=7,
                color=color, ha=side, va="center")

    ax.set_ylim(-3.1, top + 1.1)
    ax.set_yticks([])
    ax.set_xticklabels([])
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="x", length=0)
    handles = [plt.Line2D([], [], marker=m, color=c, ls="", ms=6.5, label=lab)
               for c, m, lab in STYLE.values()]
    handles.append(plt.Line2D([], [], marker="D", mfc="white", mec="0.25", mew=1.2,
                              color="none", ls="", ms=6.5, label="stated maximum"))
    ax.legend(handles=handles, loc="upper left", fontsize=7, frameon=False,
              handletextpad=0.4, labelspacing=0.35)

    spans = [
        (earth_cal, math.log10(THRESHOLD),
         "ceiling above Eq. 6 at Earth calibrated values, 2.90 dex", "#D55E00"),
        (earth_crust_max, math.log10(THRESHOLD),
         "ceiling above Eq. 6 at modern crustal production, 0.70 dex", "#E69F00"),
        (CI_LO, CI_HI, "spectroscopic credible interval, 1.5 dex", "0.15"),
        (RETRIEVED - BEST_CASE_CI / 2, RETRIEVED + BEST_CASE_CI / 2,
         "with all abundances known exactly, 0.1 dex", "0.45"),
    ]
    for y, (lo, hi, label, color) in enumerate(spans):
        bx.plot([lo, hi], [-y, -y], color=color, lw=3.2, solid_capstyle="butt", zorder=3)
        bx.text(hi + 0.14, -y, label, va="center", fontsize=7, color="0.2")
    bx.axvline(math.log10(THRESHOLD), color="0.15", lw=1.3, zorder=1)

    bx.set_ylim(-3.7, 0.8)
    bx.set_yticks([])
    bx.spines["left"].set_visible(False)
    bx.set_xlabel("log$_{10}$ surface CH$_4$ flux (molecules cm$^{-2}$ s$^{-1}$)", fontsize=8.5)
    bx.tick_params(labelsize=8)

    out = Path(__file__).resolve().parent / "note" / "figure.png"
    fig.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")


if __name__ == "__main__":
    main()
