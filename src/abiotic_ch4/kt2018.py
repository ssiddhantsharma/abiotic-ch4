# Krissansen-Totton, Olson & Catling 2018, Sci. Adv. 4:eaao5747, Eq. 6:
#
#     F_CH4 = (P_crust / M_FeO) * fr_FeO * fr_H2 * fr_CH4
#
# All four factors are sampled uniformly over ranges chosen to be generous, so
# the published distribution is of the *maximum* abiotic flux under parameter
# uncertainty, not the flux a planet realises. Its low corner is modern Earth.

from typing import NamedTuple

M_FEO = 0.056 + 0.016  # kg/mol

P_CRUST = (5.7e13, 5.7e14)  # kg/yr, modern Earth to 10x modern
FR_FEO = (0.10, 0.25)  # wt% FeO in newly produced crust
FR_H2 = (0.0025, 0.04)  # fraction of FeO oxidised to H2
FR_CH4 = (1 / 16, 0.25)  # fraction of H2 converted to CH4 by FTT


class Params(NamedTuple):
    p_crust: float
    fr_feo: float
    fr_h2: float
    fr_ch4: float


MODERN_EARTH = Params(P_CRUST[0], FR_FEO[0], FR_H2[0], FR_CH4[0])
MAX_CORNER = Params(P_CRUST[1], FR_FEO[1], FR_H2[1], FR_CH4[1])


def feo_tmol_per_yr(p_crust, fr_feo):
    return p_crust * fr_feo / M_FEO / 1e12


def h2_tmol_per_yr(p):
    return feo_tmol_per_yr(p.p_crust, p.fr_feo) * p.fr_h2


def ch4_tmol_per_yr(p):
    return h2_tmol_per_yr(p) * p.fr_ch4
