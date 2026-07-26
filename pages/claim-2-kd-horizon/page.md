# Claim 2 — exact Theorem 3 DER rate

## Current verdict: VERIFIED

For `alpha_T>1+beta` and the strictly weaker student
`alpha_S>alpha_T`, Theorem 3 states

`DER_N = Omega~(N^kappa)`,

`kappa=(alpha_T-1-beta)(1/alpha_T-1/alpha_S)>0`.

The primary verifier checks the quotient identity and strict positivity with
exact rational arithmetic on 180 admissible triples, 40 exact power-law-tail
sandwiches, and 28 perfect-power horizon cases. Five controls—equal spectra,
reversed capacity order, the learnability boundary, a sign-flipped formula,
and a corrupted student rate—must fire.

An independent implementation checks 240 separately generated cases, 25 long
tail enclosures, and four boundary/sign controls. Its maximum log-log slope
error is `1.110e-16`. As finite corroboration, 64 paper-scale paired runs at
`d=100, N=2000, n=500000` have minimum DER `1.215879` and median `1.345044`.

Current code: `repro/src/verify_theorem3_der_exact.py` and
`repro/src/audit_theorem3_der_exact.py`. Fixed command:

```bash
uv sync --frozen && uv run python repro/src/run_all.py
```

The source is the 2026-07-26 ar5iv retrieval with SHA-256
`4d29b2ae21c4611695532f6fd304b22f678139a19311e21e9b65d8a6d0b00089`.

## Evaluator bundle

- Exact claim and assumptions: [contract](../../evidence/claim-2/claim_contract.json)
  and [source audit](../../evidence/claim-2/source_audit.md)
- Raw proof certificate: [exact Fraction output](../../evidence/claim-2/exact_der_certificate.json)
  and [independent checker output](../../evidence/claim-2/independent_checker.json)
- Executable current checks:
  [exact verifier](../../repro/src/verify_theorem3_der_exact.py),
  [independent auditor](../../repro/src/audit_theorem3_der_exact.py), and
  [cumulative gate](../../repro/src/cumulative_science_gate.py)
- [Method](../../evidence/claim-2/method.md),
  [fixed command/environment](../../evidence/claim-2/exact_command_and_environment.md),
  [limitations](../../evidence/claim-2/limitations.md), and
  [evaluation record](../../evidence/claim-2/EVAL.md)

Final cumulative run `de09d92b-ea82-4644-9341-d390cc9785b0`, Git
`e1a3b3a3248f1386118f3c3303e7412859cd72bd`, reran both exact routes,
all controls, and the fail-closed gate.
