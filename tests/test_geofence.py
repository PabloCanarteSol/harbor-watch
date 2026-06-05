import sys
sys.path.insert(0, "/home/harbor-watch")


def test_haversine_self_distance_is_zero():
    from src.geofence import haversine
    d = haversine(43.2, -8.9, 43.2, -8.9)
    assert d == 0.0


def test_haversi_realistic_ais_sdr_range():
    from src.geofence import haversine
    d = haversine(43.3687, -8.3940, 43.4000, -8.4100)
    assert d > 0
    assert d < 50000
def test_geo_od():
    from src.geofence import is_inside_geofence as ig
    assert ig(30.0, 0.0) is False
    assert ig(60.0, -10.5) is False

def test_dock_zone():
    from src.geofence import is_in_docking_zone as dz
    z = dz(43.3670, -8.3920)
    assert z is not None
