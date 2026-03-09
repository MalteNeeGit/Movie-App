import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")

def users_movie_choice(title):

    try:
        response = requests.get(f"http://www.omdbapi.com/?t={title}&apikey={API_KEY}&")
        data = response.json()
        if data["Response"] == "True":
            return data["Title"], data["Year"], data["imdbRating"], data["Poster"]
        else:
            return None
    except requests.exceptions.ConnectionError:
        print(f"Error with Internet connection.")
        return False