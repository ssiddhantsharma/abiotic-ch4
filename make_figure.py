import math
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

from abiotic_ch4.convert import tmol_per_yr_to_flux
from abiotic_ch4.data import earth_modern_realized, load
from abiotic_ch4.kt2018 import MODERN_EARTH, ch4_tmol_per_yr

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

GM2013_MAX = 6.8e8  # Guzmán-Marmolejo+ 2013, their stated maximum for 1 M_earth

SHORT = {
    "merdith_2020_preferred": "Merdith+ 2020",
    "emmanuel_ague_2007": "Emmanuel & Ague 2007",
    "schindler_kasting_2000": "Schindler & Kasting 2000",
    "cannat_2010": "Cannat+ 2010",
    "keir_2010": "Keir 2010",
    "catling_kasting_2017_axial": "Catling & Kasting 2017 (axial)",
    "catling_kasting_2017_offaxis": "Catling & Kasting 2017 (off-axis)",
    "guzman_marmolejo_2013_1me": "Guzmán-Marmolejo+ 2013",
    "kasting_2005_present": "Kasting 2005",
    "fiebig_2007_present": "Fiebig+ 2007",
    "fiebig_2009": "Fiebig+ 2009 (continental)",
    "portella_2019": "Portella+ 2019",
    "klein_2019": "Klein+ 2019",
}


def main():
    rows = earth_modern_realized(load()).sort_values("flux_lo").reset_index(drop=True)
    realized_earth = math.log10(tmol_per_yr_to_flux(ch4_tmol_per_yr(MODERN_EARTH)))

    fig = plt.figure(figsize=(7.6, 5.8))
    gs = GridSpec(2, 1, height_ratios=[4, 1.4], hspace=0.30)
    ax, bx = fig.add_subplot(gs[0]), fig.add_subplot(gs[1])

    for a in (ax, bx):
        a.set_xlim(2.6, 13.2)
        a.spines[["top", "right"]].set_visible(False)
    bx.axvline(math.log10(THRESHOLD), color="0.15", lw=1.4, zorder=1)

    for y, r in rows.iterrows():
        color, marker, _ = STYLE[r.kind]
        ax.plot(math.log10(r.flux_lo), y, marker, color=color, ms=7, zorder=3)
        ax.text(
            math.log10(r.flux_lo) - 0.18, y, SHORT[r.source_key],
            ha="right", va="center", fontsize=7.5, color="0.2",
        )

    gm = math.log10(GM2013_MAX)
    ax.plot(gm, len(rows), "D", mfc="white", mec="0.25", mew=1.3, ms=7, zorder=3)
    ax.text(gm - 0.18, len(rows), "Guzmán-Marmolejo+ 2013 (stated maximum)",
            ha="right", va="center", fontsize=7.5, color="0.2")

    top = len(rows) + 1.4
    ax.errorbar(
        RETRIEVED, top, xerr=[[RETRIEVED - CI_LO], [CI_HI - RETRIEVED]],
        fmt="o", color="0.15", ms=6, capsize=3, lw=1.4, zorder=3,
    )
    ax.text(CI_HI + 0.2, top, "retrieved,\n10 JWST transits",
            ha="left", va="center", fontsize=7.5, color="0.2")

    # Reference lines stop below the retrieval row so its label does not cross them.
    for x, color, ls in [(math.log10(THRESHOLD), "0.15", "-"),
                         (math.log10(BIOLOGICAL), "0.45", (0, (4, 2)))]:
        ax.plot([x, x], [-1.3, len(rows) + 0.4], color=color, lw=1.2, ls=ls, zorder=1)
    ax.text(math.log10(BIOLOGICAL) + 0.08, -1.1, "modern Earth\nbiological",
            fontsize=7.5, color="0.35", va="bottom")
    ax.text(math.log10(THRESHOLD) - 0.08, -1.1, "adopted abiotic\nceiling",
            fontsize=7.5, color="0.15", ha="right", va="bottom")

    ax.set_ylim(-1.3, top + 1.3)
    ax.set_yticks([])
    ax.set_xticklabels([])
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="x", length=0)
    handles = [
        plt.Line2D([], [], marker=m, color=c, ls="", ms=7, label=lab)
        for c, m, lab in STYLE.values()
    ]
    ax.legend(handles=handles, loc="upper left", fontsize=7.5, frameon=False,
              title="published abiotic estimate", title_fontsize=7.5)

    spans = [
        (realized_earth, math.log10(THRESHOLD), "ceiling above realised Earth, 2.90 dex", "#D55E00"),
        (math.log10(GM2013_MAX), math.log10(THRESHOLD),
         "ceiling above the other published maximum, 1.74 dex", "#E69F00"),
        (CI_LO, CI_HI, "spectroscopic CI, 1.5 dex", "0.15"),
        (RETRIEVED - BEST_CASE_CI / 2, RETRIEVED + BEST_CASE_CI / 2,
         "best case with perfect abundances, 0.1 dex", "0.45"),
    ]
    for y, (lo, hi, label, color) in enumerate(spans):
        bx.plot([lo, hi], [-y, -y], color=color, lw=3.5, solid_capstyle="butt", zorder=3)
        bx.text(hi + 0.15, -y, label, va="center", fontsize=7.5, color="0.2")

    bx.set_ylim(-3.7, 0.8)
    bx.set_yticks([])
    bx.spines["left"].set_visible(False)
    bx.set_xlabel("log$_{10}$ surface CH$_4$ flux (molecules cm$^{-2}$ s$^{-1}$)", fontsize=9)
    bx.tick_params(labelsize=8)

    out = Path(__file__).resolve().parent / "note" / "figure.png"
    fig.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")


if __name__ == "__main__":
    main()
