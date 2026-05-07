from scripts.analyze_qazaqstan import run_analysis


def test_run_analysis_returns_14_weights():
    report = run_analysis(top=5, only_positive=False)
    assert report['num_weights'] == 14
    assert len(report['weights']) == 14
