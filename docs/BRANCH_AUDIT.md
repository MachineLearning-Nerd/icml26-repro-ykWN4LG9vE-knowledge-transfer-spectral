# Branch audit and normalization map

The original repository had one `main` branch and six experiment branches
with the `orx/` prefix. The prefix described the runner that created them, not
the scientific role of the branch. The normalized names below describe the
content directly.

## Original remote tips

These are the tips audited before normalization:

| Original branch | Tip before normalization | Scientific role |
| --- | --- | --- |
| `main` | `97639f06dbd5c07f6aafc0f95883fd1a83cb353f` | Original public release candidate |
| `orx/judged-baseline-with-locked-uv-environment` | `14f3c66f8aa15128b1b4358b72a71045e210439e` | Locked baseline and judged Claims 1–2 |
| `orx/claim-3-exact-theorem-4-quantifier-audit` | `1ac586d398fb768e118add5fce8ab2330726c72b` | Theorem 4 quantifier audit |
| `orx/claim-3-high-dimensional-exact-embedding` | `cedf9ad5b025e747dcf5dd0a2050fb51965ab843` | `D=4096` exact witness |
| `orx/claim-4-exact-pgr-and-stopping-rate-audit` | `d255238936e5d179f4e6eeaddc5cbc7d6c6ee72b` | Theorem 5 PGR/rate audit |
| `orx/claim-5-utkface-real-architecture-w2s` | `3a71e66759eb4b8f05cd17c19e07a514bff76b03` | Real-architecture W2S experiment |
| `orx/cumulative-release-candidate-and-evaluator-visib` | `e1a3b3a3248f1386118f3c3303e7412859cd72bd` | Cumulative release and visibility audit |

## Final branch contract

| Final branch | Source branch | What it contains |
| --- | --- | --- |
| `main` | `main` | Canonical README, source pin, evidence bundle, and publication gate |
| `baseline/judged-locked-uv` | `orx/judged-baseline-with-locked-uv-environment` | Reproducible judged baseline |
| `audit/claim-3-theorem4-quantifier` | `orx/claim-3-exact-theorem-4-quantifier-audit` | Exact universal-quantifier audit |
| `audit/claim-3-high-dimensional-witness` | `orx/claim-3-high-dimensional-exact-embedding` | Admissible high-dimensional counterexample |
| `audit/claim-4-pgr-stopping-rate` | `orx/claim-4-exact-pgr-and-stopping-rate-audit` | Exact PGR and stopping-rate contradictions |
| `experiment/claim-5-real-architecture-w2s` | `orx/claim-5-utkface-real-architecture-w2s` | Paper-scale real W2S experiment |
| `release/cumulative-candidate` | `orx/cumulative-release-candidate-and-evaluator-visib` | Cumulative release candidate and evaluator traversal |

The old `orx/*` names are deleted after the final refs are pushed. They remain
in this file only as historical provenance. All final branch tips are checked
with `git ls-remote --heads`, and all reachable commits are required to use:

```text
MachineLearning-Nerd <MachineLearning-Nerd@users.noreply.github.com>
```

The final remote branch names and tips are also recorded in the parent
collection tracker after GitHub verification.
