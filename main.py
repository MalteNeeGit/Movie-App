
import statistics
import random
import matplotlib.pyplot as plt
from storage import movie_storage_sql as storage
import API
import html_generator

#ANSI COLOR CODES:
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"

def menu_display():
    """
    shows the user the menu.
    """
    print()
    print(BLUE)
    print("Menu:\n"
        "0. Exit\n"
        "1. List movies\n"
        "2. Add movie\n"
        "3. Delete movie\n"
        "4. Update movie\n"
        "5. Stats\n"
        "6. Random movie\n"
        "7. Search movie\n"
        "8. Movies sorted by rating\n"
        "9. Create ratings histogram\n"
        "10. Show movies based on year\n"
        "11. Filter movies\n"
        "12. Generate Website")
    print()
    print(RESET)

def get_user_choice():
    """
    gets the user choice
    :return: user input
    """
    choice = int(input(CYAN + "Enter choice (0-12): " + RESET))
    return choice

def press_enter_to_continue():
    """Pauses the program until the user presses enter."""
    input(YELLOW + "Press enter to continue..." + RESET)

#VALID RATING:
def is_valid_rating(rating):
    """
    validates the input of rating in a certain range
    """
    return 0 <= float(rating) <= 10


#VALID YEAR:
def is_valid_year(year):
    """
    validates the input of year in a certain range
    """
    return 1888 <= int(year[:4]) <= 2027

#VALID MOVIE TITLE:
def is_valid_title(title):
    """
    validates the input of title as its not empty
    """
    return title != ""

def get_valid_title(prompt):
    """Asks for a title until a non-empty one is given."""
    while True:
        title = input(prompt).strip()
        if is_valid_title(title):
            return title
        print(f"{RED}Title cannot be empty!{RESET}")

#FILME AUFLISTEN
def list_of_all_movies():
    """
    shows every movie in the database
    """
    movies = storage.list_movies()
    print(GREEN + f"------{len(movies)} Movies in total------" + RESET)

    for title, info in movies.items():
        print(f"{title} {BLUE} ({info['year']}) {RESET}: {info['rating']}")

#FILM HINZUFÜGEN
def add_movie_and_rating_and_year():
    """
    adds the movie with information from OMDb API
    """
    #Validating the user input
    title_to_search = get_valid_title(CYAN + "Enter movie to add: " + RESET)

    #Asking the api for the Movie
    result = API.users_movie_choice(title_to_search)
    if result is None:
        print(f"{RED}Movie not found in OMDb!{RESET}")
        return
    elif result is False:
        print(f"{RED}No internet connection!{RESET}")
        return

    title, year, rating, poster = result

    #Save Movie in Database
    movies = storage.list_movies()
    if title in movies.keys():
        print(f"{RED}We already got this movie!{RESET}")
    else:
        success = storage.add_movie(title, year, rating, poster)
        if success:
            print(f"{GREEN}{title} ({year}) added with rating: {rating}{RESET}")
        else:
            print(f"{RED}Error saving movie!{RESET}")

#FILM LÖSCHEN
def delete_movie():
    """Deletes a movie from the database."""
    movie_to_delete = get_valid_title(CYAN + "Enter movie to delete: " + RESET)
    success = storage.delete_movie(movie_to_delete.lower())
    if success:
        print(GREEN + f"{movie_to_delete} was deleted" + RESET)
    else:
        print(RED + "Movie not found :-(" + RESET)


#FILME AKTUALISIEREN
def update_movie():
    """
    updates existing movie with new information (rating)
    """
    movie_to_update = get_valid_title(CYAN + "Enter movie to update: " + RESET)

    while True:
        try:
            new_rating = float(input(CYAN + "Enter new rating: " + RESET))
            if is_valid_rating(new_rating):
                break
            print(f"{RED}Enter any rating from 0 to 10{RESET}")
        except ValueError:
            print(f"{RED}We need a number for the rating{RESET}")

    success = storage.update_movie(movie_to_update.lower(), new_rating)

    if success:
        print(GREEN + f"{movie_to_update} updated with {new_rating}" + RESET)
    else:
        print(RED + "Movie not in Database :-(" + RESET)

def get_ratings_and_extremes(movies):
    """Collects ratings, best and worst movies in a single loop."""
    ratings = []
    best_rating = 0
    worst_rating = 10
    best_movies = []
    worst_movies = []

    for title, info in movies.items():
        rating = float(info["rating"])
        ratings.append(rating)
        if rating > best_rating:
            best_rating = rating
            best_movies = [title]        # Restart list
        elif rating == best_rating:
            best_movies.append(title)    # if even, take both
        if rating < worst_rating:
            worst_rating = rating
            worst_movies = [title]
        elif rating == worst_rating:
            worst_movies.append(title)

    return ratings, best_movies, best_rating, worst_movies, worst_rating

def calculate_average(ratings):
    """Returns the average rating."""
    return round(sum(ratings) / len(ratings), 2)

def calculate_median(ratings):
    """Returns the median rating."""
    return statistics.median(ratings)

#HELPER FUNKTION FOR PRINTING STATS_OF_MOVIES
def print_best_or_worst_movies(movies_list, rating, label):
    """Prints best or worst movies with their rating."""
    if len(movies_list) == 1:
        print(f"{label} Movie: {movies_list[0]} with a rating of: {rating}")
    else:
        print(f"{label} Movies (with a rating of: {rating})")
        for movie in movies_list:
            print(f"-- \t {movie}")


#STATISTIKEN
def stats_of_movies():
    """
    shows stats of the movies in database.Orchestrates the helper functions.
    1. Average      2. Median       3. Best movie(s)        4. Worst Movies(s)
    """
    print(GREEN + "------Stats of Movie-Database:------" + RESET)
    movies = storage.list_movies()

    if len(movies) == 0:
        print(f"{RED}No movies in database!{RESET}")
        return

    ratings, best_movies, best_rating, worst_movies, worst_rating = get_ratings_and_extremes(movies)

    print(f"Average rating: {calculate_average(ratings)}")
    print(f"Median rating: {calculate_median(ratings)}")
    print_best_or_worst_movies(best_movies, best_rating, "Best")
    print_best_or_worst_movies(worst_movies, worst_rating, "Worst")


#ZUFALLSFILM
def random_movie():
    """
    shows random movie with its information (rating and year)
    """
    try:
        movies = storage.list_movies()
        movie, info = random.choice(list(movies.items()))
        print( GREEN + "------Our random suggestion for you:------" + RESET)
        print(f"Your movie for tonight: {movie}, its rated {info['rating']}")
    except IndexError:
        print(f"{RED}Database is empty. Please add some movies before.{RESET}")

#FILM SUCHEN
def search_movie():
    """Case insensitive search for movies in the database."""
    word_to_search = get_valid_title(CYAN + "Enter part of the movie name: " + RESET).lower()
    movies = storage.list_movies()
    movies_found = 0

    for movie, title in movies.items():
        if word_to_search in movie.lower():
            movies_found += 1
            print(f"{movie} \t {BLUE} with a rating of: {movies[movie]['rating']}, "
                  f"{RESET} {CYAN} from the year: {movies[movie]['year']}{RESET}")
    if movies_found == 0:
        print(RED + "No movies found :-(" + RESET)

#FILME SORTIEREN UND NACH BEWERTUNG AUSGEBEN
def movies_based_on_rating():
    """
    shows the movies based on rating
    """
    print(GREEN + "------Ranking of all Movies:------" + RESET)
    movies = storage.list_movies()
    movies_as_list = []
    for movie in movies:
        rating = float(movies[movie]["rating"])
        movies_as_list.append((rating, movie))
    movies_as_list.sort(reverse=True)
    for rating, movie in movies_as_list:
        print(f"{movie} : {rating}")

#FILME SORTIEREN UND NACH JAHR AUSGEBEN
def movies_based_on_year():
    """
    shows the movies listed by year. either newest or oldest
    """
    movies = storage.list_movies()
    order_of_sorting = input(f"{CYAN}Do you want to see the Movies ordered by newest or oldest?{RESET}")
    print()
    movies_as_list_for_year = []
    for movie in movies:
        year = int(str(movies[movie]["year"])[:4])
        movies_as_list_for_year.append((year, movie))

    if order_of_sorting.lower() == "oldest":
        movies_as_list_for_year.sort()

    elif order_of_sorting.lower() == "newest":
        movies_as_list_for_year.sort(reverse=True)

    else:
        print(f"{RED}You need to write either 'oldest' or 'newest'{RESET}")
        return

    for year, movie in movies_as_list_for_year:
        print(f"{movie} : {CYAN}from the year: {RESET}{year}")

def get_validated_float(prompt, allow_empty=True):
    """Helper funktion, asks or a number, returns none if empty"""
    while True:
        user_input = input(prompt)
        if allow_empty and user_input == "":
            return None
        try:
            return float(user_input)
        except ValueError:
            print(f"{RED}Please enter a number!{RESET}")

def filter_movies():
    """Filters the movies and validates the input.
    If movies found it returns movies within the 3 criteria"""
    movies = storage.list_movies()

    # Rating
    min_rating_input = get_validated_float(
        f"{CYAN}Enter min rating (empty = no min rating): {RESET}"
    )
    if min_rating_input is not None and not is_valid_rating(min_rating_input):
        print(f"{RED}Rating needs to be between 0 and 10!{RESET}")
        return
    min_rating = min_rating_input if min_rating_input is not None else 0.0

    # Startyear
    start_year_input = get_validated_float(
        f"{CYAN}Enter a year from which your selection starts (empty = no min year): {RESET}"
    )
    if start_year_input is not None and not is_valid_year(str(int(start_year_input))):
        print(f"{RED}Year must be between 1888 and 2027!{RESET}")
        return
    start_year = int(start_year_input) if start_year_input is not None else 1895

    # Endyear
    end_year_input = get_validated_float(
        f"{CYAN}Enter a year for your selection to end (empty = no max year): {RESET}"
    )
    if end_year_input is not None and not is_valid_year(str(int(end_year_input))):
        print(f"{RED}Year must be between 1888 and 2027!{RESET}")
        return
    end_year = int(end_year_input) if end_year_input is not None else 2027

    # using the Filters
    print(f"{GREEN}Filtered Movies:{RESET}")
    found = False
    for title, info in movies.items():
        rating = info["rating"]
        year = int(str(info["year"])[:4])
        if rating >= min_rating and start_year <= year <= end_year:
            print(f"{title} ({year}): {rating}")
            found = True

    if not found:
        print(f"{RED}No Movies found.{RESET}")


#HISTOGRAM
def ratings_histogram():
    """
    shows a histogram of movies in databbase
    """
    movies = storage.list_movies()
    ratings = []
    for info in movies.values():
        ratings.append(info["rating"])
    filename = input(CYAN + "Enter filename for histogram to save:"
                            "(e.g. ratings.png or ratings.jpg): " + RESET)
    plt.hist(ratings, bins = 10)
    plt.title("MOVIE RATINGS HISTOGRAM")
    plt.xlabel("Rating")
    plt.ylabel("Number of Movies")
    plt.savefig(filename)
    plt.show()
    plt.clf()
    print(f"Histogram saved as {filename}")


def main():
    """
    runs the whole thing and handels the user choice
    """
    print("********** My Movies Database **********")

    while True:
        menu_display()
        try:
            action_number = get_user_choice()
            print()
        except ValueError:
            print()
            print(f"{RED}Please enter any number from the shown menu{RESET} {GREEN}:-){RESET}")
            continue
        if action_number == 0:
            print("Bye!")
            break

        elif action_number == 1:
            list_of_all_movies()

        elif action_number == 2:
            add_movie_and_rating_and_year()

        elif action_number == 3:
            delete_movie()

        elif action_number == 4:
            update_movie()

        elif action_number == 5:
            stats_of_movies()

        elif action_number == 6:
            random_movie()

        elif action_number == 7:
            search_movie()

        elif action_number == 8:
            movies_based_on_rating()

        elif action_number == 9:
            ratings_histogram()

        elif action_number == 10:
            movies_based_on_year()

        elif action_number == 11:
            filter_movies()

        elif action_number == 12:
            html_generator.generate_website()

        print()
        press_enter_to_continue()

if __name__ == "__main__":
    main()
