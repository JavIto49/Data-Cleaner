import argparse
import logging
from pathlib import Path

MOVIES_CSV = Path("data/movies.csv")
RATINGS_CSV = Path("data/ratings.csv")
DB_PATH = "movies.db"

def setup_logging(level: str = "INFO") -> logging.Logger:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(message)s",
    )
    return logging.getLogger("data-cleaner")

def parse_args():
    p = argparse.ArgumentParser(description="Clean CSVs and load into SQLite.")
    p.add_argument("--movies", type=str, default=str(MOVIES_CSV), help="Path to movies CSV")
    p.add_argument("--ratings", type=str, default=str(RATINGS_CSV), help="Path to ratings CSV")
    p.add_argument("--db", type=str, default=DB_PATH, help="SQLite DB path to write")
    p.add_argument("--log-level", type=str, default="INFO", help="DEBUG, INFO, WARNING, ERROR")
    p.add_argument("--min-votes", type=int, default=2, help="Min #ratings to include a movie in top list")
    p.add_argument("--limit", type=int, default=5, help="Top list size")
    p.add_argument("--report", type=str, default=None, help="Write data-quality report JSON to this path")
    p.add_argument("--dry-run", action="store_true", help="Run cleaning + report, skip DB write & queries")
    return p.parse_args()