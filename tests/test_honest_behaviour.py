from habari_mcp import server

_fn = lambda name: (getattr(server, name).fn if hasattr(getattr(server, name), "fn") else getattr(server, name))


def test_an_unknown_gazette_notice_type_is_an_error_not_legal_notices():
    r = _fn("gazette_search")("tax assessment")
    assert "error" in r and "legal_notice" in r["valid_types"] and "description" not in r


def test_a_known_type_still_works():
    assert "description" in _fn("gazette_search")("appointment")
