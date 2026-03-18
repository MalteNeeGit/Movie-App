from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError, OperationalError


# Define the database URL
DB_URL = "sqlite:///data/movies.db"

# Create the engine
engine = create_engine(DB_URL, echo=False)

# Create the movies table if it does not exist
with engine.connect() as connection:
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL,
            poster TEXT
        )
    """))
    connection.commit()

def list_movies():
    """Retrieve all movies from the database."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT title, year, rating, poster FROM movies"))
        movies = result.fetchall()

    return {row[0]: {"year": row[1], "rating": row[2], "poster": row[3]} for row in movies}

def add_movie(title, year, rating, poster):
    """Add a new movie to the database."""
    with engine.connect() as connection:
        try:
            connection.execute(text("INSERT INTO movies (title, year, rating, poster) VALUES (:title, :year, :rating, :poster)"),
                               {"title": title, "year": year, "rating": rating, "poster": poster})
            connection.commit()
            print(f"Movie '{title}' added successfully.")
            return True
        except IntegrityError:
            connection.rollback()
            print(f"Error: Movie '{title}' already exists (unique constraint).")
            return False
        except OperationalError as e:
            connection.rollback()
            print(f"Error: Database connection issue: {e}")
            return False

def delete_movie(title):
    """Delete a movie from the database."""
    with engine.connect() as connection:
        try:
            result = connection.execute(text("DELETE FROM movies WHERE LOWER(title) = (:title)"),
                                    {"title" : title})
            connection.commit()
            if result.rowcount == 0:
                return False  # Film wurde nicht gefunden

            print(f"Movie '{title}' deleted successfully.")
            return True
        except OperationalError as e:
            connection.rollback()
            print(f"Error: Database connection issue: {e}")
            return False


def update_movie(title, rating):
    """Update a movie's rating in the database."""
    with engine.connect() as connection:
        try:
            result = connection.execute(text("UPDATE movies SET rating = (:rating) WHERE LOWER(title) = (:title)"),
                                    {"title" : title, "rating" : rating})
            connection.commit()
            if result.rowcount == 0:
                return False  # Film wurde nicht gefunden
            print(f"Movie '{title}' updated successfully with rating of {rating}.")
            return True
        except OperationalError as e:
            connection.rollback()
            print(f"Error: Database connection issue: {e}")
            return False

