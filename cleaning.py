from pathlib import Path
from typing import Optional
import pandas as pd
import logging

def load_clean_movies(path: Path, logger: Optional[logging.Logger] = None) -> pd.DataFrame:
    raw = pd.read_csv(path)
    n0 = len(raw)

    # Required fields
    df = raw.dropna(subset=["id", "title", "genre", "rating"]).copy()
    n_missing_req = n0 - len(df)

    # Normalize text
    df.loc[:, "title"] = df["title"].astype(str).str.strip()
    df.loc[:, "genre"] = df["genre"].astype(str).str.strip().str.title()

    # Remove blank titles
    before_blank = len(df)
    df = df[df["title"].str.strip().astype(bool)]
    n_blank_title = before_blank - len(df)

    # Type enforcement
    df.loc[:, "id"] = pd.to_numeric(df["id"], errors="coerce")
    if "year" in df.columns:
        df.loc[:, "year"] = pd.to_numeric(df["year"], errors="coerce")
    df.loc[:, "rating"] = pd.to_numeric(df["rating"], errors="coerce")

    before_types = len(df)
    df = df.dropna(subset=["id", "rating"])
    n_bad_numeric = before_types - len(df)

    # Duplicates
    before_dups = len(df)
    df = df.drop_duplicates()
    n_dups = before_dups - len(df)

    # Final cast
    df.loc[:, "id"] = df["id"].astype(int)

    # Printing: reset index
    df = df.reset_index(drop=True)

    if logger:
        logger.info(
            "movies: read=%d kept=%d missing_required=%d blank_title=%d bad_numeric=%d duplicates=%d",
            n0, len(df), n_missing_req, n_blank_title, n_bad_numeric, n_dups
        )
    return df


def load_clean_ratings(path: Path, logger: Optional[logging.Logger] = None) -> pd.DataFrame:
    raw = pd.read_csv(path)
    n0 = len(raw)

    # Required fields
    df = raw.dropna(subset=["user_id", "movie_id", "rating"]).copy()
    n_missing_req = n0 - len(df)

    # Type coercion
    df.loc[:, "user_id"] = pd.to_numeric(df["user_id"], errors="coerce")
    df.loc[:, "movie_id"] = pd.to_numeric(df["movie_id"], errors="coerce")
    df.loc[:, "rating"]  = pd.to_numeric(df["rating"],  errors="coerce")

    before_types = len(df)
    df = df.dropna(subset=["user_id", "movie_id", "rating"])
    n_bad_numeric = before_types - len(df)

    # Count ratings that will be clipped
    n_clipped = int(((df["rating"] < 0) | (df["rating"] > 10)).sum())
    df.loc[:, "rating"] = df["rating"].clip(0, 10)

    # Duplicates
    before_dups = len(df)
    df = df.drop_duplicates()
    n_dups = before_dups - len(df)

    # Final cast
    df.loc[:, ["user_id", "movie_id"]] = df[["user_id", "movie_id"]].astype(int)
    # Verify rating is float for consistency
    df.loc[:, "rating"] = df["rating"].astype(float)
    # Printing: reset the index after filtering
    df = df.reset_index(drop=True)

    if logger:
        logger.info(
            "ratings: read=%d kept=%d missing_required=%d bad_numeric=%d clipped=%d duplicates=%d",
            n0, len(df), n_missing_req, n_bad_numeric, n_clipped, n_dups
        )
    return df