from dataclasses import dataclass


@dataclass(frozen=True)
class Item:
    """One news item collected from a source."""
    source: str
    region: str
    title: str
    url: str
    summary: str
    published: str
