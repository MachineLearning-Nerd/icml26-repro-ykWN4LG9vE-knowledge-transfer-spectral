import hashlib, json, subprocess, sys
from pathlib import Path
root=Path(__file__).resolve().parents[2]
r=json.loads((root/'outputs/independent_verification.json').read_text())
assert r['protocol']['n']==500000 and r['protocol']['trials']==64
assert r['claim_1_geometric_decomposition']['max_static_gap_identity_error'] < 1e-10
assert r['claim_2_kd_horizon']['minimum_der'] > 1
assert r['claim_3_w2s_denoising']['mean_best_student_risk'] < r['claim_3_w2s_denoising']['mean_teacher_risk']
assert 'FULL_GATE_READY: ykWN4LG9vE' in (root/'.trackio/logbook/pages/conclusion/page.md').read_text()
subprocess.run([sys.executable,'-m','pytest','-q','repro/tests'],cwd=root,check=True)
records=[]
for f in ['sources.json','source/arxiv/main.tex','repro/src/verify_transfer.py','repro/tests/test_transfer.py','outputs/independent_verification.json','.trackio/metadata.json','.trackio/logbook/pages/conclusion/page.md']:
    b=(root/f).read_bytes(); records.append({'path':f,'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)})
(root/'outputs/evidence_bundle.json').write_text(json.dumps({'paper':'ykWN4LG9vE','records':records},indent=2)+'\n')
gate={'paper':'ykWN4LG9vE','status':'passed','tests_passed':True,'publication_gate_passed':True,'claim_outcomes':{'claim_1':'verified','claim_2':'verified','claim_3':'verified'}}
(root/'outputs/PUBLICATION_GATE_PASSED.json').write_text(json.dumps(gate,indent=2)+'\n')
print(json.dumps(gate,indent=2))
