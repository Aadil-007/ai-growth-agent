import hashlib
import sqlite3
from datetime import datetime, timezone
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

from .models import Item

TRACKING_PREFIXES = ("utm_", "fbclid", "gclid")


def normalize_url(url: str) -> str:
    """Strip tracking params so the same article is not stored twice."""
    parts = urlsplit(url.strip())
    query = [(k, v) for k, v in parse_qsl(parts.query) if not k.lower().startswith(TRACKING_PREFIXES)]
    return urlunsplit((parts.scheme, parts.netloc.lower(), parts.path.rstrip("/"), urlencode(query), ""))


def item_id(url: str) -> str:
    return hashlib.sha256(normalize_url(url).encode()).hexdigest()[:32]


class Store:
    def __init__(self, path: str = "data/items.db"):
        self.conn = sqlite3.connect(path)
        self.conn.execute(
            """CREATE TABLE IF NOT EXISTS items (
                id TEXT PRIMARY KEY,
                source TEXT, region TEXT, title TEXT, url TEXT,
                summary TEXT, published TEXT, fetched_at TEXT
            )"""
        )
        self.conn.commit()

    def add_if_new(self, item: Item) -> bool:
        """Return True if the item was new and saved, False if it was a duplicate."""
        cur = self.conn.execute(
            "INSERT OR IGNORE INTO items VALUES (?,?,?,?,?,?,?,?)",
            (
                item_id(item.url), item.source, item.region, item.title,
                normalize_url(item.url), item.summary, item.published,
                datetime.now(timezone.utc).isoformat(),
            ),
        )
        self.conn.commit()
        return cur.rowcount == 1

    def count(self) -> int:
        return self.conn.execute("SELECT COUNT(*) FROM items").fetchone()[0]

    def close(self):
        self.conn.close()
