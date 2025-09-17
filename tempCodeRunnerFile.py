conn = sqlite3.connect("movies.db")
df.to_sql("movies", conn, if_exists="replace", index=False)
cursor = conn.cursor()

print("\nMovies per genre:")
for row in cursor.execute("SELECT genre, COUNT(*) FROM movies GROUP BY genre"):
    print(row)