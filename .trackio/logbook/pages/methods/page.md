# Methods and fixed execution contract

The paper is arXiv:2606.01292 / OpenReview `ykWN4LG9vE`. The accepted source
and active TeX hash are recorded in `sources.json` and `source/arxiv/main.tex`.
The implementation is clean-room because no author implementation was present
in the source archive.

The current publication gate reads committed `evidence/` records and does not
depend on Trackio, OpenResearch, network access, or ephemeral runtime artifacts.
The full Claim 5 feature-extraction run is represented by its pinned summary,
raw predictions, checkpoints, bootstrap intervals, and independent checker.
