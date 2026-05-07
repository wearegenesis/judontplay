from app.services.normalization import normalize_name, normalize_weight


def test_normalize_name_basic():
    assert normalize_name("  ánuDáRi   jAmsrÁn  ") == "Anudari Jamsran"


def test_normalize_weight_formats():
    assert normalize_weight("-60") == "-60 kg"
    assert normalize_weight("60 kg") == "-60 kg"
