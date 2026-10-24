from ai_growth_agent.collectors.rss import parse_feed
from ai_growth_agent.models import Item
from ai_growth_agent.storage import Store, normalize_url

SAMPLE = b"""<?xml version="1.0"?>
<rss version="2.0"><channel><title>Test</title>
<item><title>New open model released</title>
<link>https://example.com/post?utm_source=x</link>
<description>Short summary</description></item>
<item><title></title><link>https://example.com/bad</link></item>
</channel></rss>"""


def test_parse_feed_skips_bad_entries():
    items = parse_feed(SAMPLE, "Test", "global")
    assert len(items) == 1
    assert items[0].title == "New open model released"


def test_normalize_url_removes_tracking():
    assert normalize_url("https://Example.com/a/?utm_source=x&id=1") == "https://example.com/a?id=1"


def test_duplicates_are_ignored(tmp_path):
    store = Store(str(tmp_path / "t.db"))
    a = Item("S", "global", "T", "https://example.com/a?utm_source=x", "", "")
    b = Item("S", "global", "T", "https://example.com/a", "", "")
    assert store.add_if_new(a) is True
    assert store.add_if_new(b) is False
    assert store.count() == 1
