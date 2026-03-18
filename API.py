import requests
from dotenv import load_dotenv
import os

RED = "\033[31m"
RESET = "\033[0m"

load_dotenv()
API_KEY = os.getenv("API_KEY")

def users_movie_choice(title):
    """Fetches movie data from OMDb API.
    Returns (title, year, rating, poster) if found, None if not found, False on error."""
    try:
        response = requests.get(f"http://www.omdbapi.com/?t={title}&apikey={API_KEY}&", timeout=5)
        if not response.ok:
            print(f"{RED}API error: Status code {response.status_code}{RESET}")
            return False
        data = response.json()
        if data["Response"] == "True":
            return data["Title"], data["Year"], data["imdbRating"], data["Poster"]
        else:
            return None
    except requests.exceptions.ConnectionError:
        print(f"{RED}Error with Internet connection.{RESET}")
        return False
    except requests.exceptions.Timeout:
        print(f"{RED}Error: Request timed out.{RESET}")
        return False
    except requests.exceptions.JSONDecodeError:
        print(f"{RED}Error: Invalid response from API.{RESET}")
        return False