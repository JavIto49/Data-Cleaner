from typing import Optional
import sqlite3
import pandas as pd
import logging

def write_sqlite(movies: pd.DataFrame, ratings: pd.DataFrame, db_path: str, logger: Optional[logging.Logger] = None) -> None:
    with sqlite3.connect(db_path) as conn:
        movies.to_sql("movies", conn, if_exists="replace", index=False)
        ratings.to_sql("ratings", conn, if_exists="replace", index=False)
        cur = conn.cursor()
        # Indexes for lookups and joins
        cur.execute("CREATE INDEX IF NOT EXISTS ix_movies_id ON movies(id)")
        cur.execute("CREATE INDEX IF NOT EXISTS ix_ratings_movie_id ON ratings(movie_id)")
        conn.commit()
    if logger:
        logger.info("SQLite write complete: tables [movies, ratings] replaced and indexed.")


def run_queries(db_path: str, min_votes: int = 2, limit: int = 5) -> None:
    """Run SQL queries to summarize and join the data."""
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()

        print("\nMovies per genre:")
        for row in cur.execute("""
            SELECT genre, COUNT(*) AS n
            FROM movies
            GROUP BY genre
            ORDER BY n DESC;
        """):
            print(row)

        print("\nAverage rating by genre (movies dataset):")
        for row in cur.execute("""
            SELECT genre, ROUND(AVG(rating), 2) AS avg_rating
            FROM movies
            GROUP BY genre
            ORDER BY avg_rating DESC;
        """):
            print(row)

        print("\nTop movies by average user rating:")
        for row in cur.execute(f"""
            SELECT m.title, ROUND(AVG(r.rating), 2) AS avg_user_rating, COUNT(*) AS votes
            FROM movies m
            JOIN ratings r ON r.movie_id = m.id
            GROUP BY m.id, m.title
            HAVING votes >= {int(min_votes)}
            ORDER BY avg_user_rating DESC, votes DESC
            LIMIT {int(limit)};
        """):
            print(row)