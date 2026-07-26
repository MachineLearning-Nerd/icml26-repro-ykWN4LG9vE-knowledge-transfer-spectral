# Claim 1 source audit

Source: `https://ar5iv.labs.arxiv.org/html/2606.01292`, retrieved with an
explicit browser User-Agent on 2026-07-26, SHA-256
`4d29b2ae21c4611695532f6fd304b22f678139a19311e21e9b65d8a6d0b00089`.
The matching source archive is `source/arxiv/main.tex`.

Theorem 1 is `thm:generalt2s` at source lines 490–506. It quantifies over any
`0<delta<1/2` and gives an upper bound after a teacher trained on `N` samples
and a student trained on `n` teacher-labeled samples. Its three displayed
terms are propagated teacher error, student optimization error, and
irreducible alignment bias. Lines 515–518 interpret the learned-head
coefficient as one-to-one inheritance and the unlearned-tail coefficient as
`2 delta^2`.

The static geometric identity tested separately is Lemma
`lem:geometric_consistency`, lines 457–473.
