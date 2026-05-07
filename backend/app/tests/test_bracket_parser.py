from app.services.bracket_parser import parse_bracket


def test_parse_bracket_with_byes():
    parsed = parse_bracket({"A": [["JAMSRAN ANUDARI", None]]})
    assert parsed["A"][0] == ("Anudari Jamsran", None)
