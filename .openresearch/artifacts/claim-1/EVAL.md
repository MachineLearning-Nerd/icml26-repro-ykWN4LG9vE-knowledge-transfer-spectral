# Claim 1 evaluation

## Verdict: VERIFIED

The successful baseline run reproduced the 9,000 noncommuting-subspace audit
with maximum absolute identity error `9.769962616701378e-15`. The preserved
`D=60` linear-Gaussian decomposition gives propagated teacher error `0.01978`
plus student optimization error `0.0` plus alignment bias `0.00562`, equal to
T2S risk `0.02541`.

The final cumulative descendant must rerun both checks from the unchanged
fixed command. Current code fails closed if the geometric error exceeds
`1e-10`, if any component is negative, or if the sum does not match.
