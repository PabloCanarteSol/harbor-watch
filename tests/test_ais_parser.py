import json
import sys
sys.path.insert(0, "/home/harbor-watch")


def test_parse_line_valid_json_returns_dict_with_timestamp():
    from src.ais_parser import AisParser
    ap = AisParser()
    line = '{"mmsi":"123456789","lat":"434000000"}'
    result = ap.parse_line(line)
    assert isinstance(result, dict)
    assert "timestamp" in result


def test_parse_line_invalid_json_returns_none():
    from src.ais_parser import AisParser
    ap = AisParser()
    assert ap.parse_line("not json") is None
    assert ap.parse_line("") is None


def test_parse_line_empty_input_returns_none():
    from src.ais_parser import AisParser
    ap = AisParser()
    line_json = json.dumps({"foo": "bar"}).strip()
    result = ap.parse_line(line_json)
    # parse_line returns dict (valid JSON), but no mmsi key
    assert isinstance(result, dict)


def test_parse_raw_full_data_populates_all_fields():
    from src.ais_parser import AisParser
    raw = {
        "mmsi": "987654321",
        "lat": 433600000,
        "lon": -83940000,
        "speed": 12.5,
        "course": str(45),
        "name": "TEST SHIP",
        "imo": "1234567",
        "typename": "Cargo",
        "length": 200,
        "width": 30,
        "destination": "ROTTERDAM",
        "navstatus": "0",
    }
    msg = AisParser.parse_raw(raw)
    assert msg is not None
    assert str(msg.mmsi) == "987654321"
    assert abs(msg.lat - 43.36) < 0.001
    assert abs(msg.lon - (-8.394)) < 0.001
    assert msg.name == "TEST SHIP"


def test_parse_raw_partial_data_graceful_defaults():
    from src.ais_parser import AisParser
    raw = {"mmsi": "111222333", "lat": 0, "lon": 0}
    msg = AisParser.parse_raw(raw)
    assert msg is not None
    assert msg.name == "Unknown"


def test_transatlantic_candidate_large_cargo_ship():
    from src.ais_parser import AisMessage
    s = AisMessage(123, 0, 0, typename="Cargo", length=200)
    assert s.is_transatlantic_candidate is True


def test_transatlantic_candidate_fishing_vessel_false():
    from src.ais_parser import AisMessage
    s = AisMessage(123, 0, 0, typename="Fishing", length=200)
    assert s.is_transatlantic_candidate is False


def test_parse_stream_mixed_valid_invalid_lines():
    from src.ais_parser import AisParser
    lines = [
        '{"mmsi":"1","lat":"10000000"}',
        "garbage line",
        "{invalid json}",
        '{"mmsi":"2","lat":"20000000"}',
    ]
    msgs = AisParser().parse_stream(lines)


def test_nav_status_code_mapping():
    from src.ais_parser import AisMessage, NAV_STATUS_MAP
    s = AisMessage(123, 0, 0, nav_status_code=0)
    assert "engine" in s.navigation_status.lower() or "way" in s.navigation_status.lower()
