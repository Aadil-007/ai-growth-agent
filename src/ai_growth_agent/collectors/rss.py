import logging
import urllib.request
import time

import feedparser

from ..models import Item

log = logging.getLogger(__name__)
USER_AGENT = "ai-growth-agent/0.1 (+https://github.com/Aadil-007)"


def parse_feed(content: bytes, source: str, region: str) -> list[Item]:
    """Turn raw RSS/Atom bytes into Item objects. Kept separate so it is easy to test."""
    feed = feedparser.parse(content)
    items = []
    for entry in feed.entries:
        link = entry.get("link")
        title = entry.get("title", "").strip()
        if not link or not title:
            continue
        items.append(
            Item(
                source=source,
                region=region,
                title=title,
                url=link,
                summary=entry.get("summary", "")[:1000],
                published=entry.get("published", ""),
            )
        )
    return items


def fetch_feed(url: str, source: str, region: str, timeout: int = 15, retries: int = 3) -> list[Item]:
    """Download a feed with a timeout and retries. Failures are logged, not fatal."""
    for attempt in range(1, retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return parse_feed(resp.read(), source, region)
        except Exception as exc:
            log.warning("Attempt %d/%d failed for %s: %s", attempt, retries, source, exc)
            if attempt < retries:
                time.sleep(2 ** attempt)  # wait 2s, then 4s before the next try
    log.error("Giving up on %s after %d attempts", source, retries)
    return []
