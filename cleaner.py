import pandas as pd
import sqlite3

# Cleaning dataset
df = pd.read_csv("data/movies.csv")
print("Data before cleaning: ")
print(df)

# Dropping rows with missing title or rating from dataset
df = df.dropna(subset=["title","rating"])

# Removing white-space/blank titles
df = df[df["title"].str.strip().astype(bool)]

# Standardizing genres (capitalizing first letter)
df["genre"] = df["genre"].str.capitalize()

# Removing duplicates
df = df.drop_duplicates()

print("\nData after cleaning:")
print(df)

# SQL Queries
conn = sqlite3.connect("movies.db")
df.to_sql("movies", conn, if_exists="replace", index=False)
cursor = conn.cursor()

# Counting movies per genre
print("\nMovies per genre:")
for row in cursor.execute("SELECT genre, COUNT(*) FROM movies GROUP BY genre"):
    print(row)

# Average rating by genre  
print("\nAverage rating by genre:")
for row in cursor.execute("SELECT genre, ROUND(AVG(rating), 2) FROM movies GROUP BY genre"):
    print(row)

# Listing the top 5 highest rated movies
print("\nTop 5 highest-rated movies:")
for row in cursor.execute("SELECT title, rating FROM movies ORDER BY rating DESC LIMIT 5"):
    print(row)

conn.close()