import pandas as pd
import sqlite3
from pathlib import Path

MOVIES_CSV = Path("data/movies.csv")
RATINGS_CSV = Path("data/ratings.csv")
DB_PATH = "movies.db"

def load_clean_movies(path: Path) -> pd.DataFrame:
    """Load movies, standardize columns, and enforce types."""
    df = pd.read_csv(path)

    # Required fields
    df = df.dropna(subset=["id", "title", "genre", "rating"])
    
    # Normalize text
    df["title"] = df["title"].str.strip()
    df["genre"] = df["genre"].astype(str).str.strip().str.title()
    
    # Remove blank titles
    df = df[df["title"].str.strip().astype(bool)]
    
    # Type check
    df["id"] = pd.to_numeric(df["id"], errors="coerce")
    if "year" in df:df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")

    # Valid id and rating check
    df = df.dropna(subset=["id", "rating"]).drop_duplicates()
    df["id"] = df["id"].astype(int)
    return df

def load_clean_ratings(path: Path) -> pd.DataFrame:
    """Load ratings, enforce numeric types, clip to 0–10, and remove bad rows."""
    df = pd.read_csv(path)
    df = df.dropna(subset=["user_id", "movie_id", "rating"])

    df["user_id"] = pd.to_numeric(df["user_id"], errors="coerce")
    df["movie_id"] = pd.to_numeric(df["movie_id"], errors="coerce")
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce").clip(0, 10)

    df = df.dropna(subset=["user_id", "movie_id", "rating"]).drop_duplicates()
    df[["user_id", "movie_id"]] = df[["user_id", "movie_id"]].astype(int)
    return df

def write_sqlite(movies: pd.DataFrame, ratings: pd.DataFrame, db_path: str) -> None:
    with sqlite3.connect(db_path) as conn:
        movies.to_sql("movies", conn, if_exists="replace", index=False)
        ratings.to_sql("ratings", conn, if_exists="replace", index=False)
        cur = conn.cursor()
        # Add indexes for faster lookups and joins
        cur.execute("CREATE INDEX IF NOT EXISTS ix_movies_id ON movies(id)")
        cur.execute("CREATE INDEX IF NOT EXISTS ix_ratings_movie_id ON ratings(movie_id)")
        conn.commit()

def run_queries(db_path: str) -> None:
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

        print("\nTop 5 movies by average user rating:")
        for row in cur.execute("""
            SELECT m.title, ROUND(AVG(r.rating), 2) AS avg_user_rating, COUNT(*) AS votes
            FROM movies m
            JOIN ratings r ON r.movie_id = m.id
            GROUP BY m.id, m.title
            HAVING votes >= 2
            ORDER BY avg_user_rating DESC, votes DESC
            LIMIT 5;
        """):
            print(row)

def main():
    print("Loading and cleaning datasets")
    movies = load_clean_movies(MOVIES_CSV)
    ratings = load_clean_ratings(RATINGS_CSV)

    print("\nMovies dataset:")
    print(movies.head())
    movies.info()

    print("\nRatings dataset:")
    print(ratings.head())
    ratings.info()

    print("\nWriting to SQLite")
    write_sqlite(movies, ratings, DB_PATH)
    print(f"Saved tables to {DB_PATH}")

    print("\nRunning queries")
    run_queries(DB_PATH)

if __name__ == "__main__":
    main()