from repro.src.verify_transfer import projectors_identity, rate_audits, schedule


def test_step_decay_is_nonincreasing():
    values = schedule(2048, .01)
    assert values[0] == .01
    assert (values[1:] <= values[:-1]).all()


def test_geometric_consistency_identity():
    result = projectors_identity(250, 4)
    assert result["max_static_gap_identity_error"] < 1e-11


def test_kd_and_w2s_exponents_have_expected_signs():
    result = rate_audits()
    assert result["kd_admissible_cells"] > 100_000
    assert result["kd_positive_exponent_violations"] == 0
    assert result["w2s_positive_rate_violations"] == 0
