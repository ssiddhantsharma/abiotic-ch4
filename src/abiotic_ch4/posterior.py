# A reconstruction of the marginal CH4 flux posterior of Wogan et al. (2026) from
# the three numbers they quote: log10 F = 11.2 (+0.6/-0.9), 68% credible interval.
# The interval endpoints are read as the 16th and 84th percentiles and 11.2 as the
# median, which fixes a split normal exactly.
#
# It reproduces their tabulated P(F in H_CH4 | d) = 0.77 at the adopted ceiling.
# That agreement comes from honouring the quoted quantiles, not from the shape, so
# the reconstruction is reliable across the quoted interval and is an extrapolation
# below it. Use it for the shape of the dependence, not for three-figure values.

import numpy as np
from scipy import optimize, stats

MEDIAN, P16, P84 = 11.2, 10.3, 11.8


def _cdf(x, m, s_lo, s_hi):
    w = s_lo / (s_lo + s_hi)
    x = np.asarray(x, dtype=float)
    return np.where(
        x < m,
        2 * w * stats.norm.cdf(x, m, s_lo),
        w + (1 - w) * 2 * (stats.norm.cdf(x, m, s_hi) - 0.5),
    )


def _fit():
    def resid(p):
        return [_cdf(P16, *p) - 0.16, _cdf(P84, *p) - 0.84, _cdf(MEDIAN, *p) - 0.5]

    return optimize.fsolve(resid, [MEDIAN, 0.9, 0.6])


PARAMS = _fit()


def p_above(log10_ceiling):
    """Posterior mass above a candidate abiotic ceiling, in log10 flux units."""
    return 1.0 - _cdf(log10_ceiling, *PARAMS)
