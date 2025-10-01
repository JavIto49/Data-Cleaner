from typing import Optional
import json
import pandas as pd
import logging

def dq_summary(df: pd.DataFrame, name: str) -> dict:
    return {
        "table": name,
        "rows": int(len(df)),
        "columns": {col: str(df[col].dtype) for col in df.columns},
        "nulls_per_column": {col: int(df[col].isna().sum()) for col in df.columns},
        "null_pct_per_column": {col: float(df[col].isna().mean()) for col in df.columns},
    }

def referential_issues(movies: pd.DataFrame, ratings: pd.DataFrame) -> dict:
    if movies.empty or ratings.empty or "id" not in movies or "movie_id" not in ratings:
        return {"orphan_ratings_count": 0}
    movie_ids = set(movies["id"].astype(int).tolist())
    orphan_mask = ~ratings["movie_id"].isin(movie_ids)
    return {"orphan_ratings_count": int(orphan_mask.sum())}

def generate_report(movies: pd.DataFrame, ratings: pd.DataFrame, out_path: Optional[str], logger: Optional[logging.Logger] = None) -> dict:
    report = {
        "movies": dq_summary(movies, "movies"),
        "ratings": dq_summary(ratings, "ratings"),
        "integrity": referential_issues(movies, ratings),
    }

    # Log for short preview
    if logger:
        js = json.dumps(report, indent=2)
        logger.info("DQ report summary:\n%s", js if len(js) < 1200 else js[:1200] + "\n... [truncated]")

    if out_path:
        with open(out_path, "w") as f:
            json.dump(report, f, indent=2)
        if logger:
            logger.info("Wrote data-quality report to %s", out_path)

    return report