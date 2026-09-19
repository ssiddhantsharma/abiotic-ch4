# Global production rate <-> per-area surface flux.
# Radius is a parameter, not a constant: an Earth-normalised flux does not
# transfer to a planet of another size.

import math

AVOGADRO = 6.02214076e23
SECONDS_PER_YEAR = 3.1557e7
EARTH_RADIUS_CM = 6.371e8


def surface_area_cm2(radius_cm=EARTH_RADIUS_CM):
    return 4 * math.pi * radius_cm**2


def tmol_per_yr_to_flux(tmol_per_yr, radius_cm=EARTH_RADIUS_CM):
    return tmol_per_yr * 1e12 * AVOGADRO / SECONDS_PER_YEAR / surface_area_cm2(radius_cm)


def flux_to_tmol_per_yr(flux, radius_cm=EARTH_RADIUS_CM):
    return flux * surface_area_cm2(radius_cm) * SECONDS_PER_YEAR / AVOGADRO / 1e12
