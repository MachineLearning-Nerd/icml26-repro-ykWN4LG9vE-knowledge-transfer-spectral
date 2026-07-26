# Claim 3 limitations and deviations

This is a mathematical falsification of a universally quantified theorem, not
an empirical claim about typical dense high-dimensional behavior. Its ambient
dimension is 4096, but its data covariance has rank one, matching the theorem's
low-intrinsic-dimension premise. The theorem states no positive-definiteness
requirement and explicitly includes the self-distillation limit. The target
and noise are both nonzero, all source assumptions are audited, and the
paper's exact SGD algorithm is used.

The result does not deny that early stopping can produce W2S in noisy
high-dimensional instances. It shows only that Assumptions 1, 4, and 5 are
insufficient for the theorem's stated “there exists `n_0`; for all `n>n_0`”
guarantee. A corrected theorem would need a quantified variance-over-bias
condition and an early-stopping interval rather than an eventual-horizon
quantifier.
