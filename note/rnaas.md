# The abiotic methane ceiling sets a floor on detectable biospheres

## Abstract

Flux based biosignature assessment compares an inferred surface methane flux
against a ceiling on abiotic production. The ceiling in current use is a
deliberately conservative upper bound, adopted as a single number. It lies more
than an order of magnitude above the only other published maximum for the same
process, about three orders of magnitude above published estimates of what Earth
actually produces, and a factor of three below Earth's own biological methane
flux. The choice of ceiling therefore fixes the smallest biosphere an observation
can reveal, and the span of defensible choices is wider than the spectroscopic
uncertainty of the retrieval it is compared against. Reporting the biosignature
probability as a function of the assumed ceiling would make that dependence
visible at no additional computational cost.

## Note

Wogan et al. (2026) infer surface gas fluxes for an Archean-like TRAPPIST-1 e by
inverting a coupled photochemical and climate model, then ask whether the inferred
fluxes are consistent with life. The step from flux to biosignature runs through a
set definition: methane fluxes above 3.7e10 molecules cm^-2 s^-1 are taken to
exceed what ocean bottom serpentinization can supply. That value is the 99.7th
percentile of the distribution of maximum abiotic fluxes computed by
Krissansen-Totton et al. (2018), adopted, as Wogan et al. say, for simplicity.

As a set boundary the choice is sound and conservative by design. Its consequences
appear at the following step, where the complement of the biosignature region is
taken as the abiotic alternative and the resulting odds ratio is used as a proxy
for the Bayes factor between life and no life. A bound chosen to be generous then
does the work of a likelihood.

The clearest way to see the size of that choice is to compare it with the other
published maximum for the same process. Guzmán-Marmolejo et al. (2013) modelled
methane production by serpentinization from the kinetics of the reactions involved,
with carbon dioxide as the limiting reactant, and report a maximum surface flux of
6.8e8 molecules cm^-2 s^-1 for an Earth mass planet. Two maxima for the same
process therefore differ by 1.74 dex. Neither is a realised flux, so the comparison
does not turn on how conservative a bound ought to be.

Figure 1 places both against published estimates of Earth's realised abiotic
methane production, compiled from the supplementary material of Thompson et al.
(2022) and from Merdith et al. (2020). Every estimate for modern Earth lies below
the ceiling, the largest, from continental hydrothermal emissions, by 1.5 dex. Six
seafloor estimates, spanning mid-ocean ridges, off-axis vent fields, submarine
volcanism and subduction related sites, fall between log F = 7.3 and 8.1.

The lower corner of the four parameter ranges sampled by Krissansen-Totton et al.
is itself modern Earth. Taking their modern crustal production rate, 10 wt% FeO in
newly produced crust, the 0.25% conversion of FeO to hydrogen that they calibrate
against observation, and the hydrogen to methane ratio of 12 measured in
ultramafic hosted vent fluids, their Equation 6 returns 0.012 Tmol yr^-1, or
log F = 7.67. Their distribution runs from what Earth does to the most generous
case they were willing to entertain, and the adopted percentile sits 2.90 dex above
its lower end. That lower corner is itself uncertain upward: Merdith et al. (2020)
find a present-day hydrogen flux of about 0.7 Tmol yr^-1 from slow and ultraslow
ridges alone, against the 0.2 Tmol yr^-1 that Krissansen-Totton et al. calibrate to,
which would raise the realised corner by roughly 0.5 dex. The span between a
realised and a maximal ceiling is therefore between about 2.4 and 2.9 dex.

Two consequences follow, both in the units of the original analysis.

First, a ceiling implies a minimum detectable biosphere. Wogan et al. adopt
1.122e11 molecules cm^-2 s^-1 for modern Earth's biological methane flux, following
Catling & Kasting (2017). The ceiling lies a factor of three below that. A planet
whose biosphere produced methane at less than a third of Earth's rate could not be
called inhabited on this criterion at any signal to noise. Placing the ceiling at
the realised Earth value instead moves the floor to roughly one part in 2400 of
Earth's biological flux.

Second, the span of defensible ceilings is large next to the measurement. The
retrieval returns a 68% credible interval 1.5 dex wide for the logarithm of the
methane flux. Table A1 of Wogan et al. gives that width under every combination of
gas abundances fixed to their true values, and the narrowest entry is 0.1 dex,
which is the limit of what perfect abundance knowledge would buy on this target.
Both framings of the ceiling ambiguity, 1.74 dex between two maxima and 2.4 to 2.9
dex between a maximum and a realised flux, exceed the interval actually achieved.
A posterior width and a range of candidate thresholds are different objects, but
both enter the same decision in the same units, and here the geochemical term is
the larger of the two.

None of this is concealed in the original work. Wogan et al. state that they adopt
a single value for simplicity, note that the inhabited and lifeless flux regions
should more realistically overlap, and write down the generalisation in which the
sharp set is replaced by a weighting function p(life | F). What this note adds is
the magnitude of the quantity that generalisation would need, and the observation
that on this target it exceeds the spectroscopic term.

An inexpensive intermediate step is available, and it needs nothing that is not
already published. Reading the quoted credible interval endpoints as the 16th and
84th percentiles and 11.2 as the median fixes a split normal, which returns 0.76
for the posterior mass above the adopted ceiling against the 0.77 that Wogan et al.
tabulate. The same reconstruction puts more than 0.98 of the posterior above the
maximum of Guzmán-Marmolejo et al. and above any realised estimate, although below
the quoted interval that is an extrapolation and only the qualitative statement is
intended. Reporting the biosignature probability as a function of the assumed
ceiling, rather than at a single value, therefore costs a line of arithmetic on a
posterior that already exists, and would show directly how much of the inference
rests on geochemistry. The corresponding Bayes factor cannot be recovered this way,
since it also requires the prior mass implied by the retrieval at each candidate
ceiling. Treating the abiotic term as a reported dependence rather than a fixed
input seems the more useful division of labour as flux based biosignature
assessment develops.

One limit applies to what is compiled here. The estimates in Figure 1 describe
different reservoirs that are only partly additive, and several of the seafloor
values are alternative estimates of one quantity rather than separate contributions
to it, so the figure should be read as a range of published values and not as a
distribution. A ceiling for a planet other than Earth would also need its crustal
production rate scaled, as Guzmán-Marmolejo et al. (2013) do for a five Earth mass
planet.

## Figure 1

Published estimates of Earth's abiotic methane production, against the ceiling
adopted in flux based biosignature assessment. Filled markers distinguish
observational estimates, model estimates, and estimates obtained by dividing a
reservoir inventory by a residence time; the open diamond is the maximum reported
by Guzmán-Marmolejo et al. (2013). The solid line is the adopted abiotic ceiling
and the dashed line is modern Earth's biological methane flux. The point with error
bars is the flux retrieved from a synthetic ten transit JWST spectrum of an
Archean-like TRAPPIST-1 e. The lower panel compares both framings of the ceiling
ambiguity with the credible interval of that retrieval and with the narrowest
interval attainable if all gas abundances were known exactly.

## Software and data

The compiled estimates, the arithmetic reproducing every value quoted above, and
the script that draws Figure 1 are available at
https://github.com/ssiddhantsharma/abiotic-ch4 and archived at Zenodo. Values from
Krissansen-Totton et al. (2018) are recomputed from their Equation 6 and its four
published parameter ranges rather than read from their figure, and values from
Guzmán-Marmolejo et al. (2013) and Merdith et al. (2020) are taken from those
papers rather than from the compilations that cite them.
