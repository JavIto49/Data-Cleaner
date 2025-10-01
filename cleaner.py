from pathlib import Path
from utils import parse_args, setup_logging
from cleaning import load_clean_movies, load_clean_ratings
from reporting import generate_report
from database import write_sqlite, run_queries


def main():
    args = parse_args()
    logger = setup_logging(args.log_level)

    logger.info("Loading and cleaning datasets")
    movies = load_clean_movies(Path(args.movies), logger=logger)
    ratings = load_clean_ratings(Path(args.ratings), logger=logger)

    print("\nMovies dataset:")
    print(movies.head())
    movies.info()

    print("\nRatings dataset:")
    print(ratings.head())
    ratings.info()

    # Data quality report
    generate_report(movies, ratings, args.report, logger=logger)

    if args.dry_run:
        logger.info("Dry-run: skipping DB write and queries.")
        return

    logger.info("Writing to SQLite at %s", args.db)
    write_sqlite(movies, ratings, args.db, logger=logger)
    logger.info("Saved tables and indexes.")

    print("\nRunning queries")
    run_queries(args.db, min_votes=args.min_votes, limit=args.limit)


if __name__ == "__main__":
    main()