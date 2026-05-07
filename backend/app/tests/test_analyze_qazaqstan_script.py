from scripts.analyze_qazaqstan import run_analysis


def test_run_analysis_returns_14_weights():
    report = run_analysis(top=5, only_positive=False)
    assert report['num_weights'] == 14
    assert len(report['weights']) == 14


def test_run_analysis_weight_normalization():
    report_a = run_analysis(weight='-60 kg')
    report_b = run_analysis(weight='-60')
    assert report_a['num_weights'] == 1
    assert report_b['num_weights'] == 1
