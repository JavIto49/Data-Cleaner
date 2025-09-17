# Data-Cleaner

A Python project for cleaning and querying movie data using pandas and SQLite.  
The project demonstrates basic data cleaning, database handling, and SQL queries (including JOINs).

---

### Features
- Clean movies dataset (remove missing values, duplicates, and blank titles)
- Normalize genres and enforce numeric types for IDs, years, and ratings
- Clean ratings dataset (user ratings, clipped to 0–10)
- Load both datasets into SQLite with indexes for performance
- Run SQL queries to:
  - Count movies per genre
  - Calculate average ratings by genre
  - Get top movies by average user rating (with vote threshold)

---

### Tech Stack
- Python 3  
- pandas  
- SQLite  

---

### Getting Started
1. Clone the repo:
   git clone <https://github.com/JavIto49/Data-Cleaner.git>
   cd Data-Cleaner

2. Install dependencies:
   pip install pandas

3. Place your datasets in the `data/` folder:
   - movies.csv
   - ratings.csv

4. Run the script:
   python cleaner.py

### Example Output
Movies per genre:
('Sci-Fi', 3)
('Action', 2)
('Drama', 1)
('Crime', 1)

Average rating by genre (movies dataset):
('Crime', 9.2)
('Sci-Fi', 8.7)
('Action', 8.7)
('Drama', 8.5)

Top 5 movies by average user rating:
('The Dark Knight', 9.5, 2)
('The Godfather', 9.5, 2)
('The Matrix', 8.67, 3)
('Whiplash', 8.5, 2)
('Interstellar', 8.5, 2)
