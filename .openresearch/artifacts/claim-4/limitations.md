# Claim 4 limitations and deviations

This is a falsification of Theorem 5 as written, not evidence that spectral
early stopping never improves W2S. The stopping-rate contradiction holds for
fixed initial step size, which is the regime used by the paper's own cutoff
lemma; allowing the step size to scale with `N` would require a new theorem
that states that schedule.

The self-distillation witness uses identical models because Section 6
explicitly calls self-distillation the limit case. If the intended theorem
excludes identical models, requires strictly better direct-student risk, or
sets `R_S=0`, those restrictions must be stated; none appears in Theorem 5.
