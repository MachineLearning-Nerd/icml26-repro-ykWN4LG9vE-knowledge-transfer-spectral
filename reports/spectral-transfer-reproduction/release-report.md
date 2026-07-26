Previous live judged score: `6/10`

Conservative projected score range after the proposed change: **8–10/10**

Best-supported possible new score: **10/10 forecast, not a judge result**

# Claim-by-claim release report

The live score remains 6/10 at HF Head and Judge Head
`39d8a32354134ce1777ce9adefe8f26e86ebc11b`. Only the live evaluator can
change it.

| Claim | Current points | Possible points | Confidence | Evidence status | Basis and remaining risk |
| --- | ---: | ---: | --- | --- | --- |
| 1 | 2 | 2 | HIGH | VERIFIED | The accepted 9,000-system identity and three-part decomposition both pass in the cumulative regression. |
| 2 | 2 | 2 | HIGH | VERIFIED | Exact rational DER certificate, independent reconstruction, finite paired run, and all controls pass. |
| 3 | 1 | 2 | HIGH | FALSIFIED | Exact `D=4096` assumption witness contradicts the universal eventual strict W2S quantifier for every finite horizon. Risk: evaluator interpretation of the theorem's omitted nondegeneracy intent. |
| 4 | 1 | 2 | HIGH | FALSIFIED | Undefined admissible PGR denominator, invalid proof substitution, and factor-two stopping mismatch are exact. Risk: evaluator may treat a missing regularity condition as implicit. |
| 5 | 0 | 2 | MEDIUM | VERIFIED | Paper-scale ResNet18→CLIP UTKFace W2S, paired stopping CI, shuffled-label control, and raw independent recomputation directly answer the prior missing-real-model criticism. Risk: the separate CPU-prohibitive ViT-L/16 Figure 2 panel was not run. |

Current total score: **6/10**. Conservative projected total score range:
**8–10/10**. Best-supported possible total score: **10/10 forecast**.
Claims 3, 4, and 5 changed materially since the previous judge result. No
claim remains BLOCKED; Claim 5's omitted ViT-L/16 panel is an explicit scope
limitation rather than evidence used to support its verdict.

## Publication action

After every release gate passes, upload only the exact text allowlist to the
existing Space `DineshAI/ykWN4LG9vE` through the Hugging Face API. Do not
create another Space. Then download that exact revision, recheck every hash
and canonical-entry traversal, mark the release awaiting judge, and mirror
the published text paths to GitHub `main`.

## Final cumulative experiment

- Experiment branch:
  `orx/cumulative-release-candidate-and-evaluator-visib`
- Git SHA: `e1a3b3a3248f1386118f3c3303e7412859cd72bd`
- OpenResearch run: `de09d92b-ea82-4644-9341-d390cc9785b0`
- Fixed command:
  `uv sync --frozen && uv run python repro/src/run_all.py`
- Backend: Hugging Face `cpu-upgrade`; no GPU
- Estimated useful cores: 24 (16 Torch plus 8 image loaders)
- Actual allocation: 64 logical CPUs
- Fixed-command runtime: 1,912.079 s
- Remote elapsed time: 32m34s
- Cost: not exposed by the local `orx` evidence interface

Accepted evidence runs consumed 1h04m44s of HF remote elapsed time. Counting
failed and intentionally cancelled diagnostic submissions, total recorded HF
job time was 2h01m37s. Local work was restricted to short, single-core
interactive retrieval, hashing, parsing, and validation tasks; each finished
within five minutes. Neither HF billing cost nor a per-job price is exposed
by `orx`, so no monetary amount is guessed.

Every subcommand exited zero: Claim 1 verifier 94.237 s; preserved
decomposition regression 6.240 s; Claim 2 exact certificate 0.088 s and
independent audit 0.959 s; tests 2.349 s; Claim 3 0.401 s; Claim 4 0.178 s;
Claim 5 1,807.543 s; cumulative gate 0.041 s.

## Experiment tree

The stacked lineage is baseline → exact Theorem 4 falsification → exact
Theorem 5 falsification → paper-scale real-architecture experiment →
cumulative release candidate. Each descendant inherited the identical
command and reran all accepted checks. Successful experiment branches were
not merged or rebased.

## Evidence entrypoints

- [Canonical logbook index](../../pages/index.md)
- [Illustrated report](report.md)
- [Visibility matrix](visibility-matrix.md)
- [Evaluator-blind red-team record](../../audit/red-team-review.md)
- [Exact second-pass traversal](../../audit/visibility-traversal-second-pass.json)
- [Final fresh-copy traversal](../../audit/visibility-traversal-final.json)
- [Fail-closed release verifier](../../audit/verify_release.py)
- [Command ledger](../../audit/commands-executed.txt)
- [Cumulative science gate](../../evidence/cumulative_science_gate.json)
- [Claim 1 evidence](../../evidence/claim-1/EVAL.md)
- [Claim 2 evidence](../../evidence/claim-2/EVAL.md)
- [Claim 3 evidence](../../evidence/claim-3/EVAL.md)
- [Claim 4 evidence](../../evidence/claim-4/EVAL.md)
- [Claim 5 evidence](../../evidence/claim-5/EVAL.md)

## Formal command ledger

```text
orx projects --json
orx runs a80644ad-aba9-48d6-8f74-551d23777104
orx project view a80644ad-aba9-48d6-8f74-551d23777104
orx create-experiment a80644ad-aba9-48d6-8f74-551d23777104 --title "Judged baseline with locked uv environment"
orx project edit a80644ad-aba9-48d6-8f74-551d23777104 --run-command "uv sync --frozen && uv run python repro/src/run_all.py"
orx exp run bba14047-a440-478b-8cc7-3f42ec551ccb --backend hf --flavor cpu-upgrade --image ghcr.io/astral-sh/uv:python3.12-bookworm-slim
orx exp run 8e6b9eaf-d5eb-4cc1-97eb-be3c1d8c7293 --backend hf --flavor cpu-upgrade --image ghcr.io/astral-sh/uv:python3.12-bookworm-slim
orx exp run 546d4ac8-176d-45f9-9b60-d67c65bd3c40 --backend hf --flavor cpu-upgrade --image ghcr.io/astral-sh/uv:python3.12-bookworm-slim
orx exp run 163f9e1e-7e80-4ba5-9ecc-589f52ca07b1 --backend hf --flavor cpu-upgrade --image ghcr.io/astral-sh/uv:python3.12-bookworm-slim
orx exp run 7b9934d6-a0fb-4cbd-9fc1-1746073f34fe --backend hf --flavor cpu-upgrade --image ghcr.io/astral-sh/uv:python3.12-bookworm-slim --timeout 2h
orx exp wait 7b9934d6-a0fb-4cbd-9fc1-1746073f34fe --timeout 480
orx logs de09d92b-ea82-4644-9341-d390cc9785b0
```

The full source-retrieval, Git, manifest, validation, and publication
commands are recorded in `audit/commands-executed.txt` in the Space release.

## Historical safety and release checks

The exact judged revision is archived under
[`historical/judged-39d8a32354134ce1777ce9adefe8f26e86ebc11b/PROTECTED_MANIFEST.sha256`](../../historical/judged-39d8a32354134ce1777ce9adefe8f26e86ebc11b/PROTECTED_MANIFEST.sha256).
The candidate retains every judged path, keeps all prior full-credit evidence
reachable, and labels the old reduced-scale W2S page exactly
“Historical rejected baseline.” The final subset result, blind-review record,
text allowlist, and SHA-256 manifest are published under `audit/`.

The old/new subset check passed for all 23 judged paths. The exact upload is
122 text files. Allowlist SHA-256:
`aac1dc0949ca49836afc2bb5e1827289a406f6d0a65cbe33bfa4e544a4c22d00`;
the exact manifest is `audit/upload-manifest.sha256`. The manifest hashes
all payload files except itself and includes the allowlist.
