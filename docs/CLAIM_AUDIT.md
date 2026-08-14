# Claim audit and evidence production map

This document separates a paper claim, the executable producer that creates
the evidence, the independent check that tests it, and the scope that the
result actually supports. `VERIFIED` means the declared contract passed;
`FALSIFIED_AS_WRITTEN` means an assumption-satisfying counterexample or exact
internal contradiction passed; it does not mean that every nearby theorem or
experiment is false.

## Claim 1 — teacher-to-student decomposition

**Verdict:** `VERIFIED_SCOPED`

**Contract:** the static alignment-bias identity and the finite
teacher-to-student decomposition have non-negative components whose sum equals
the measured risk in the checked linear-Gaussian setting.

**Production path:**

1. [`repro/src/verify_transfer.py`](../repro/src/verify_transfer.py) generates
   9,000 noncommuting teacher/student subspace systems and checks the identity.
2. [`repro/src/verify_distill.py`](../repro/src/verify_distill.py) reproduces
   the finite `D=60` decomposition.
3. [`repro/tests/test_transfer.py`](../repro/tests/test_transfer.py) provides
   the independent regression test.
4. The resulting committed records are
   [`distill_results.json`](../evidence/claim-1/distill_results.json) and
   [`independent_verification.json`](../evidence/claim-1/independent_verification.json).

**Evidence:** the maximum static identity error is
`9.769962616701378e-15`; the displayed finite decomposition is
`0.01978 + 0 + 0.00562 = 0.02541`.

**Boundary:** this is finite numerical evidence for the checked identity and
components, not a formal proof of every constant in the paper's upper bound.
The exact assumptions and limitations are in the
[contract](../evidence/claim-1/claim_contract.json),
[source audit](../evidence/claim-1/source_audit.md), and
[limitations](../evidence/claim-1/limitations.md).

## Claim 2 — DER horizon rate

**Verdict:** `VERIFIED_SCOPED`

**Contract:** under `alpha_T > 1 + beta` and `alpha_S > alpha_T`, the DER
quotient exponent is
`kappa=(alpha_T-1-beta)(1/alpha_T-1/alpha_S)>0`.

**Production path:**

1. [`repro/src/verify_theorem3_der_exact.py`](../repro/src/verify_theorem3_der_exact.py)
   evaluates exact rational parameter cases, tail sandwiches, horizon cases,
   and negative controls.
2. [`repro/src/audit_theorem3_der_exact.py`](../repro/src/audit_theorem3_der_exact.py)
   independently generates cases and checks the slope relation.
3. The exact certificate and independent output are committed under
   [`evidence/claim-2/exact_der_certificate.json`](../evidence/claim-2/exact_der_certificate.json)
   and its neighboring evidence files.

**Evidence:** 180 exact rational exponent cases, 40 exact tail sandwiches, 28
perfect-power horizon cases, 240 independent cases, and maximum independent
log-log slope error `1.110e-16`. The finite paper-scale corroboration has
minimum DER `1.215879`.

**Boundary:** the certificate establishes the declared algebraic contract and
finite corroboration; it is not a replacement for every asymptotic argument in
the source paper.

## Claim 3 — Theorem 4 eventual W2S guarantee

**Verdict:** `FALSIFIED_AS_WRITTEN`

**Contract:** under the paper's cited assumptions, there should be an `n_0`
such that every finite `n > n_0` has student risk strictly below teacher risk.

**Production path:**

1. [`repro/claims/claim3_theorem4_quantifier/verify.py`](../repro/claims/claim3_theorem4_quantifier/verify.py)
   constructs the exact witness and checks all assumptions and controls.
2. [`repro/claims/claim3_theorem4_quantifier/audit.py`](../repro/claims/claim3_theorem4_quantifier/audit.py)
   independently evaluates the risk gap at 80-digit precision over horizons
   through `1,048,576`.
3. The witness, horizon sweep, and independent record are committed under
   [`evidence/claim-3/exact_counterexample.json`](../evidence/claim-3/exact_counterexample.json)
   and its neighboring evidence files.

**Evidence:** in ambient dimension `D=4096`, with a one-dimensional Rademacher
feature distribution and all recorded assumptions satisfied, the student risk
is strictly above the teacher risk for every finite positive `n`. The uniform
gap bracket has positive minimum `0.11428578335051473`; the independent final
sampled gap is `9.6337134808993e-25`, still positive.

**Boundary:** this falsifies the universal theorem statement as written. It
does not identify which strengthened hypothesis would make a corrected theorem
true.

## Claim 4 — Theorem 5 PGR and stopping rate

**Verdict:** `FALSIFIED_AS_WRITTEN`

**Contract:** the displayed optimal stopping scale, risk rate, and PGR rate
must be compatible with the paper's own PGR definition for every admissible
instance.

**Production path:**

1. [`repro/claims/claim4_theorem5_rate/verify.py`](../repro/claims/claim4_theorem5_rate/verify.py)
   checks an exact assumption witness, the PGR definition, the exponent
   relations, and four negative controls.
2. [`repro/claims/claim4_theorem5_rate/audit.py`](../repro/claims/claim4_theorem5_rate/audit.py)
   independently sweeps the competing exponents over six decades of `N`.
3. Exact and independent records are committed under
   [`evidence/claim-4/exact_rate_audit.json`](../evidence/claim-4/exact_rate_audit.json)
   and its neighboring evidence files.

**Evidence:** self-distillation gives a zero PGR denominator; the proof's
substitution of `1-PGR` with `R_T2S/R_T` is invalid unless
`R_S*(R_T-R_T2S)=0`; and at `alpha_T=alpha_S=2`, the theorem route and the
reconstructed cutoff/risk/PGR exponents disagree. The independent sweep
approaches slopes `0.05` and `0.10` for the two routes.

**Boundary:** this is an exact audit of the theorem's displayed definitions
and rates, not a claim that all weak-to-strong experiments fail.

## Claim 5 — real architectures and early stopping

**Verdict:** `VERIFIED_SCOPED_WITH_PROTOCOL_LIMITS`

**Contract:** the declared paper-scale real W2S arm must beat its teacher with
a positive paired confidence interval; an intermediate checkpoint must beat
epoch 20; a shuffled-pseudolabel control must be worse; and provenance must be
complete.

**Production path:**

1. [`repro/claims/claim5_real_architecture/experiment.py`](../repro/claims/claim5_real_architecture/experiment.py)
   extracts frozen ResNet18 and official CLIP ViT-B/32 features, trains the
   linear heads, records all checkpoints, and writes raw predictions.
2. [`repro/claims/claim5_real_architecture/verify.py`](../repro/claims/claim5_real_architecture/verify.py)
   independently recomputes the displayed metrics from the committed 2,000-row
   prediction file and rejects a corrupted summary.
3. The summary, checkpoints, predictions, bootstrap intervals, checker, and
   protocol metadata are committed under
   [`evidence/claim-5/experiment_summary.json`](../evidence/claim-5/experiment_summary.json)
   and its neighboring evidence files.

**Evidence:** teacher MSE `327.44318`; best W2S MSE `90.92108` at epoch 2;
epoch-20 MSE `104.00529`; shuffled control `356.13712`. The paired 95% CIs
for teacher-minus-best, final-minus-best, and control-minus-best are all
strictly positive.

**Boundary:** exact UTKFace split indices are not published, so the run pins a
dataset revision, seeded split, model checkpoints, and all protocol metadata.
The 20-epoch stopping audit extends the paper's five-epoch protocol, and the
separate ViT-L/16 fine-tuning arm in Figure 2 was not run. The result therefore
does not support a strict paper-wide empirical reproduction claim.

## Gate relationship

[`repro/src/cumulative_science_gate.py`](../repro/src/cumulative_science_gate.py)
checks the committed evidence records and writes
[`outputs/CUMULATIVE_SCIENCE_GATE.json`](../outputs/CUMULATIVE_SCIENCE_GATE.json).
[`repro/src/publication_gate.py`](../repro/src/publication_gate.py) runs the
lightweight executable checks, verifies the source and evidence contracts, and
writes the canonical publication gate described in
[docs/PUBLICATION_GATE.md](PUBLICATION_GATE.md).
