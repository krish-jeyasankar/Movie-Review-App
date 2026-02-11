import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

# Enable foreign keys
c.execute("PRAGMA foreign_keys = ON;")

# ---------------------------
# USERS TABLE
# ---------------------------
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);
""")

# ---------------------------
# MOVIES TABLE
# ---------------------------
c.execute("""
CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    year INTEGER,
    description TEXT
);
""")

# ---------------------------
# REVIEWS TABLE
# ---------------------------
c.execute("""
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    movie_id INTEGER NOT NULL,
    rating INTEGER NOT NULL,
    text TEXT NOT NULL,
    date TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE
);
""")

# ---------------------------
# SAMPLE MOVIES (optional)
# ---------------------------
sample_movies = [
    ("Inception", 2010,
     "https://image.tmdb.org/t/p/w500/qmDpIHrmpJINaRKAfWQfftjCdyi.jpg",
     "A skilled thief enters dreams to steal secrets, but a final mission forces him to plant an idea instead."
    ),
    ("Interstellar", 2014,
     "https://image.tmdb.org/t/p/w500/rAiYTfKGqDCRIIqo664sY9XZIvQ.jpg",
     "A team of explorers travel through a wormhole in space to ensure humanity's survival."
    ),
    ("The Dark Knight", 2008,
     "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
     "Batman faces the Joker, a criminal mastermind who plunges Gotham into chaos."
    )
]

# Insert sample movies only if table is empty
c.execute("SELECT COUNT(*) FROM movies")
if c.fetchone()[0] == 0:
    c.executemany("""
        INSERT INTO movies (title, year, poster_url, description)
        VALUES (?, ?, ?, ?)
    """, sample_movies)
    print("Sample movies added.")
else:
    print("Movies table already has data. Skipping sample insert.")

conn.commit()
conn.close()

print("Database setup complete!")
