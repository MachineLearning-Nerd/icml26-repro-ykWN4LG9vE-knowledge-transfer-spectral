# Evaluator-blind pre-publication red team

The reviewer received only a fresh copy of the candidate artifact and the
release rubric. No OpenResearch run ID, branch, dashboard path, or evidence
location was supplied as a hint. The required starting points were
`README.md`, `logbook.json`, and `pages/index.md`.

## First pass — rejected

Files opened before rejection:

1. `README.md`
2. `logbook.json`
3. `pages/index.md`
4. `reports/spectral-transfer-reproduction/release-report.md`
5. `reports/spectral-transfer-reproduction/visibility-matrix.md`

The reviewer could locate the current five claim pages, but the report and
matrix linked to internal `.trackio/logbook/pages/...` paths that did not
exist in the downloaded Space candidate. Those conclusions were treated as
inaccessible, the visibility gate failed, and publication remained blocked.
The machine-readable first-pass record is
[visibility-traversal-first-pass.json](visibility-traversal-first-pass.json).

Fix: replace every internal `.trackio` target with the canonical root
`pages/...` path. No scientific result changed.

## Second pass — accepted

The fixed artifact was copied into a new empty directory before review.
`audit/verify_release.py` traversed links from the three canonical
entrypoints, opened 87 files, found zero broken links, and located every
claim's page, exact contract, source audit, code, raw output, checker,
control, environment, and limitations. The complete ordered file list is in
`visibility-traversal-second-pass.json`; this is the authoritative record of
every file opened.

| Claim | Current verifier located without hints | Reviewer evidence verdict | Unverified conclusion or remaining scope |
| --- | --- | --- | --- |
| 1 | yes | VERIFIED | Finite numerical evidence does not independently prove every theorem constant; this preserves the prior accepted scope. |
| 2 | yes | VERIFIED | Finite DER runs are corroborative; the exact certificate carries the asymptotic identity check. |
| 3 | yes | FALSIFIED | A reviewer could interpret strict positive spectral nondegeneracy as intended but it is absent from the stated assumptions. |
| 4 | yes | FALSIFIED | A reviewer could read a nonzero PGR denominator or oracle direct risk as implicit, but neither appears in the displayed statement used by the proof. |
| 5 | yes | VERIFIED | The separate ViT-L/16 fine-tuning panel was not run; the paper-scale real W2S arm and early-stopping requirement are directly tested. |

Historical safety also passed: all 23 judged paths are a subset of the
candidate. For each judged file, the exact bytes remain either at the
original path or in the revision-named archive. The old reduced-scale W2S
navigation is labeled exactly “Historical rejected baseline” and is not the
default verifier.

Second-pass result: **visibility gate passed**. This is a release-readiness
assessment, not a live judge result.

After linking the release verifier, command ledger, and traversal record, a
final fresh-copy regression opened 93 files with zero broken links and the same five
claim-level and 23-file preservation results. Its authoritative opened-file
record is `visibility-traversal-final.json`.
