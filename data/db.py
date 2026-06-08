import sqlite3, os
DB_PATH = os.environ.get("DW_DB", os.path.join(os.getcwd(), "data.db"))
CONN: dict[str, sqlite3.Connection] = {}


def _conn() -> sqlite3.Connection:
    if DB_PATH not in CONN or not CONN[DB_PATH]:
        cnx = sqlite3.connect(DB_PATH)
        cnx.execute("PRAGMA journal_mode=WAL")
        CONN[DB_PATH] = cnx
        return CONN[DB_PATH]


def init():
    c = _conn().cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS ships (
            msi TEXT PRIMARY KEY,
            name TEXT DEFAULT '?',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS tracks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            msi TEXT NOT NULL,
            name TEXT,
            lat REAL,
            lon REAL,
            ts INTEGER,
            msg_type INTEGER DEFAULT 0,
            source TEXT DEFAULT 'raw',
            inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
        CREATE INDEX IF NOT EXISTS idx_trk ON tracks(msi);
      """)


def insert(msi: str, name=None, lat=0.0, lon=0.0, ts=0):
    c = _conn().cursor()
    nm = name or "?"
    c.execute("INSERT OR IGNORE INTO ships(msi,name) VALUES(?,?)", (msi, nm))
    c.execute(
        "INSERT INTO tracks(msi,name,lat,lon,msg_type,source) VALUES(?,?,?,?,?,?)",
        [msi, nm, lat, lon, ts, "raw"])


def get_recent(hours: int = 24, msi=None):
    c = _conn().cursor()
    sql = "SELECT * FROM tracks WHERE inserted_at >= datetime('now', ?)"
    params = [f"-{hours} hours"]
    if msi:
        sql += " AND msi=?"
        params.append(msi)
    sql += " ORDER BY inserted_at DESC LIMIT 500"
    rows = c.execute(sql, params).fetchall()
    cols = [d[0] for d in c.description]
    return [dict(zip(cols, r)) for r in rows]


def get_last(msi: str):
    c = _conn().cursor()
    row = c.execute(
        "SELECT * FROM tracks WHERE msi=? ORDER BY inserted_at DESC LIMIT 1",
        [msi]).fetchone()
    cols = [d[0] for d in c.description]
    return dict(zip(cols, row)) if row else None


def last_lat(msi: str):
    r = get_last(msi)
    return r["lat"] if r else None


# Compatibility so main.py import works
init_db = init


class AISDB:
    """DB wrapper for main.py compatibility."""

    @staticmethod
    def init():
        init()

    @staticmethod
    def insert(msi, name=None, lat=0.0, lon=0.0, ts=0):
        insert(msi=msi, name=name, lat=lat, lon=lon, ts=ts)

    @staticmethod
    def get_recent(hours=24, msi=None):
        return get_recent(hours=hours, msi=msi)

    @staticmethod
    def get_last(msi: str):
        return get_last(msi)

    @staticmethod
    def last_lat(msi: str):
        return last_lat(msi)
