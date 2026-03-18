from storage import movie_storage_sql as storage
import os

def read_html_template():
    """Reads the HTML template file and returns its content as a string."""
    try:
        with open("static/templates/index_template.html", "r") as fileobj:
            return fileobj.read()
    except FileNotFoundError:
        print("Error: Template file 'index_template.html' not found.")
        return None
    except PermissionError:
        print("Error: No permission to read 'index_template.html'.")
        return None

def replace_title_information(html_text, title):
    """Replaces the title placeholder in the HTML template."""
    updated_html = html_text.replace("__TEMPLATE_TITLE__", title)
    return updated_html

def write_new_html(new_text):
    """Writes the generated HTML to index.html."""
    try:
        with open("index.html", "w") as fileobj:  # ← "index.html" und "w" !
            fileobj.write(new_text)
    except PermissionError:
        print("Error: No permission to write 'index.html'.")
        return False
    return True

def generate_movie_grid(movies):
    """Generates the HTML movie grid from the movies dictionary."""
    output = ""
    for title, info in movies.items():
        output += f"""
        <li>
            <div class="movie">
                <img class="movie-poster" src="{info['poster']}"/>
                <div class="movie-title">{title}</div>
                <div class="movie-year">{info['year']}</div>
            </div>
        </li>
        """
    return output

def generate_website():
    """Orchestrates the website generation process."""
    html_text = read_html_template()
    if html_text is None:
        return
    html_text = replace_title_information(html_text, "Movie-App | The Watchlist Manager")
    movies = storage.list_movies()
    movie_grid = generate_movie_grid(movies)
    html_text = html_text.replace("__TEMPLATE_MOVIE_GRID__", movie_grid)
    success = write_new_html(html_text)
    if success:
        print(f"Website generated at: {os.path.abspath('index.html')}")

