# Status — ykWN4LG9vE

## Current state

The repository contains a source-pinned, clean-room audit of all five paper
claim families. The current public result is
`VERIFIED_SCOPED_WITH_SOURCE_DEFECTS`; the strict paper-wide gate is
`NOT_READY`.

## Verified scope

- Claim 1: finite T2S decomposition and 9,000-system geometric identity audit.
- Claim 2: exact DER exponent certificate, independent audit, controls, and
  finite corroboration.
- Claim 3: exact high-dimensional counterexample to Theorem 4 as written.
- Claim 4: exact PGR-definition and stopping/rate contradictions in Theorem 5.
- Claim 5: paper-scale ResNet18→CLIP ViT-B/32 UTKFace W2S, early stopping, and
  shuffled-pseudolabel control.

## Explicit limits

The accepted source archive contains no author implementation. The paper does
not publish exact UTKFace split indices, so the audit pins the dataset revision,
seed, hashes, and protocol instead. The separate ViT-L/16 fine-tuning arm from
Figure 2 was not run. These limits prevent a strict paper-wide reproduction
claim; they do not erase the scoped results or the exact falsifications.

## Next action

Keep the committed evidence and canonical gate reproducible from a fresh clone,
then publish the normalized repository name and branch set. No score change is
claimed without a new live judge verdict.
