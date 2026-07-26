# Claim 2 method

`repro/src/verify_theorem3_der_exact.py` uses exact `Fraction` arithmetic to
check the quotient exponent and strict sign on 180 admissible rational
triples, 40 exact finite-sum/integral tail sandwiches, and 28 perfect-power
horizon identities. Five deliberately corrupted or boundary cases must fire.

`repro/src/audit_theorem3_der_exact.py` imports no verifier code. It generates
240 separate rational cases, recovers log-log slopes, encloses 25 long
power-law tails, and repeats four sign/boundary controls.

The `d=100, N=2000, n=500000` 64-trial numerical run is corroboration only;
the exact certificate carries the asymptotic claim.
