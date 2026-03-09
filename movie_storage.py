import json

STORAGE_FILE = "data_dictionary.json"

def get_movies():
    """
    Returns a dictionary of dictionaries that
    contains the movies information in the database.

    The function loads the information from the JSON
    file and returns the data.

    For example, the function may return:
    {
      "Titanic": {
        "rating": 9,
        "year": 1999
      },
      "..." {
        ...
      },
    }
    """
    try:
        with open(STORAGE_FILE, "r") as file:
            movies = json.load(file)
            return movies
    except FileNotFoundError:
        print("We didnt find a File to load from. Starting with empty Database.")
        return {}
    except json.JSONDecodeError:
        print("Error while reading Data. Starting with empty Database.")
        return {}

def save_movies(movies):
    """
    Gets all your movies as an argument and saves them to the JSON file.
    """
    saving_worked = False
    try:
        with open(STORAGE_FILE, "w") as file:
            json.dump(movies, file, indent=2)
            saving_worked = True
            return saving_worked
    except PermissionError:
        print("This file is read-only.")
        saving_worked = False
        return saving_worked
    except OSError:
        print("You dont have enough space in your memory.")
        saving_worked = False
        return saving_worked

def add_movie(title, rating, year):
    """
    Adds a movie to the movies database.
    Loads the information from the JSON file, add the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movies()
    movies[title] = {"rating" : rating, "year" : year}

    saving_worked = save_movies(movies)
    if saving_worked:
        return True
    else:
        return False

def delete_movie(title):
    """
    Deletes a movie from the movies database.
    Loads the information from the JSON file, deletes the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movies()
    title_lower = title.lower()
    movie_to_delete = None

    #find movie
    for movie in movies.keys():
        if movie.lower() == title_lower:
            movie_to_delete = movie
            break

    if movie_to_delete:
        del movies[movie_to_delete]
        success = save_movies(movies)
        return success
    else:
        return False


def update_movie(title, rating):
    """
    Updates a movie from the movies database.
    Loads the information from the JSON file, updates the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movies()
    title_lower = title.lower()
    movie_to_update = None

    for movie in movies.keys():
        if movie.lower() == title_lower:
            movie_to_update = movie
            break
    if movie_to_update:
        movies[movie_to_update]["rating"] = rating
        success = save_movies(movies)
        return success
    else:
        return False
