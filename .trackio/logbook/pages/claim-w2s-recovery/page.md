# HISTORICAL_REJECTED_BASELINE — reduced-scale W2S recovery

---
<!-- trackio-cell
{"type": "markdown", "id": "cell_kd_i", "created_at": "2026-07-22T05:00:00+00:00", "title": "Thm 1 decomposition + Thm 4 weak-to-strong + Thm 5 recovery"}
-->
### Historical evidence — not current claim evidence

Linear-Gaussian spectral model (the paper's setting). A weak teacher (ridge on few noisy samples) is distilled into a smoother student (spectral truncation). **Thm 4**: the student beats the teacher by filtering high-frequency estimation variance. **Thm 1**: the T2S risk decomposes into non-negative components summing exactly to the risk. **Thm 5**: at the optimal filter the student recovers most of the teacher→oracle gap (PGR), and the optimal filter grows with teacher data.

---
<!-- trackio-cell
{"type": "code", "id": "cell_kd_r", "created_at": "2026-07-22T05:00:00+00:00", "title": "Executed reproduction", "command": ["python", "repro/src/verify_distill.py"], "exit_code": 0, "duration_s": 20.0}
-->
````bash
$ python repro/src/verify_distill.py
````

````output
claim: Distillation_W2S_Thm1_Thm4_Thm5
Linear-Gaussian spectral model (D=60, lambda_k=1/k, sigma^2=0.1); weak teacher ridge -> spectral-truncation student.

[Thm 5] student spectral-filter sweep at weak-teacher N=100:
    k*= 3: R_T=0.1547 R_T2S=0.0408 R_oracle=0.0332 PGR=0.9373 (W2S:True)
    k*= 5: R_T=0.1547 R_T2S=0.0259 R_oracle=0.0135 PGR=0.9125 (W2S:True)
    k*= 8: R_T=0.1547 R_T2S=0.0254 R_oracle=0.0056 PGR=0.8673 (W2S:True)
    k*=12: R_T=0.1547 R_T2S=0.0324 R_oracle=0.0025 PGR=0.8037 (W2S:True)
    k*=16: R_T=0.1547 R_T2S=0.0423 R_oracle=0.0014 PGR=0.7336 (W2S:True)
    k*=20: R_T=0.1547 R_T2S=0.0523 R_oracle=0.0009 PGR=0.6658 (W2S:True)
    k*=30: R_T=0.1547 R_T2S=0.0773 R_oracle=0.0003 PGR=0.5014 (W2S:True)
    k*=45: R_T=0.1547 R_T2S=0.1160 R_oracle=0.0001 PGR=0.2503 (W2S:True)
    k*=60: R_T=0.1547 R_T2S=0.1547 R_oracle=0.0000 PGR=0.0 (W2S:False)
[Thm 4] best filter k*=8: R_T2S=0.02541 < R_T=0.15474 -> student beats teacher: True
[Thm 1] decomposition: (I)prop=0.01978 + (II)opt=0.0 + (III)bias=0.00562 = 0.02541 == R_T2S 0.02541 (nonneg: True)
[Thm 5] PGR at best filter = 0.8673 (recovers majority: True)
        performance recovery at the OPTIMAL filter per teacher-data N:
      N=  40: opt k*= 5  R_T=0.2464 R_T2S=0.0515 -> PGR=0.8369
      N=  60: opt k*= 3  R_T=2.1454 R_T2S=0.1442 -> PGR=0.9475
      N= 100: opt k*= 8  R_T=0.1520 R_T2S=0.0252 -> PGR=0.8665
      N= 200: opt k*=12  R_T=0.0428 R_T2S=0.0111 -> PGR=0.7884
      N= 400: opt k*=12  R_T=0.0180 R_T2S=0.0063 -> PGR=0.7598
      N= 800: opt k*=16  R_T=0.0083 R_T2S=0.0037 -> PGR=0.6729
        W2S holds at all N: True; recovery >0.5 at all N: True
verdict: supports
````

---
<!-- trackio-cell
{"type": "markdown", "id": "cell_kd_c", "created_at": "2026-07-22T05:00:00+00:00", "title": "Interpretation"}
-->
This reduced-scale sweep is retained for provenance only. It does not test the
current Theorem 4 universal quantifier or Theorem 5 rate contract.
