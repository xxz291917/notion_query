#!/usr/bin/env python3
"""Run a full or incremental sync from Notion to Qdrant."""

import argparse
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
)


def main():
    parser = argparse.ArgumentParser(description="Sync Notion data to Qdrant")
    parser.add_argument(
        "--mode",
        choices=["full", "incremental", "discover"],
        default="full",
        help="Sync mode (default: full)",
    )
    args = parser.parse_args()

    from src.notion.sync import SyncEngine

    engine = SyncEngine()

    if args.mode == "discover":
        dbs = engine._discover_databases()
        print(f"\nDiscovered {len(dbs)} databases:")
        for name, db_id in dbs.items():
            print(f"  {name}: {db_id}")
        return

    if args.mode == "full":
        count = engine.full_sync()
    else:
        count = engine.incremental_sync()

    print(f"\nSync complete. {count} chunks indexed.")
    print(f"Qdrant total: {engine.store.count()} points")


if __name__ == "__main__":
    main()
