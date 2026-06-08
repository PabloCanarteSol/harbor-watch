import sys
sys.path.insert(0, "/home/harbor-watch")


def test_is_worthy_cargo_200m():
    from src.vessel_classifier import is_worthy   # noqa: E501
    assert is_worthy(typename="Cargo", length=200) is True   # noqa: E501


def test_is_worthy_tanker_true():
    from src.vessel_classifier import is_worthy   # noqa: E501
    assert is_worthy(typename="Tanker") is True   # noqa: E501


def test_is_worthy_ferry_type_skipped():
    from src.vessel_classifier import is_worthy   # noqa: E501
    assert is_worthy(typename="Ferry", length=200) is False   # noqa: E501


def test_is_worthy_small_vessel_30m_false():
    from src.vessel_classifier import is_worthy   # noqa: E501
    assert is_worthy(typename=None, length=30) is False   # noqa: E501


def test_is_worthy_military_type_skipped():
    from src.vessel_classifier import is_worthy   # noqa: E501
    assert is_worthy(typename="Military", length=None) is False   # noqa: E501


def test_is_worthy_passenger_match_true():
    from src.vessel_classifier import is_worthy   # noqa: E501
    assert is_worthy(typename="Passenger") is True   # noqa: E501


def test_is_worthy_length_only_fallback():
    from src.vessel_classifier import is_worthy   # noqa: E501
    assert is_worthy(typename=None, length=200) is True   # noqa: E501
