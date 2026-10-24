import argparse
import logging
from pathlib import Path

import yaml

from .collectors.rss import fetch_feed
from .storage import Store

log = logging.getLogger("ai_growth_agent")


def load_sources(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return [s for s in yaml.safe_load(f)["sources"] if s.get("enabled")]


def run(config: str, db: str, show: int) -> None:
    Path(db).parent.mkdir(parents=True, exist_ok=True)
    store = Store(db)
    new_items = []
    for src in load_sources(config):
        items = fetch_feed(src["url"], src["name"], src.get("region", "global"))
        items = items[: src.get("max_items", 30)]
        fresh = [i for i in items if store.add_if_new(i)]
        log.info("%s: %d fetched, %d new", src["name"], len(items), len(fresh))
        new_items.extend(fresh)
    log.info("Total in database: %d", store.count())
    for item in new_items[:show]:
        print(f"[{item.source}] {item.title}\n  {item.url}\n")
    store.close()


def cli() -> None:
    parser = argparse.ArgumentParser(description="Collect AI news into a local database.")
    parser.add_argument("--config", default="config/sources.yaml")
    parser.add_argument("--db", default="data/items.db")
    parser.add_argument("--show", type=int, default=10, help="how many new items to print")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    run(args.config, args.db, args.show)


if __name__ == "__main__":
    cli()
