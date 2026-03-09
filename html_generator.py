import movie_storage_sql as storage

def read_html_template():
    with open("index_template.html", "r") as fileobj:
        html_text = fileobj.read()
        return html_text

def replace_title_information(html_text, title):
    updated_html = html_text.replace("__TEMPLATE_TITLE__", title)
    return updated_html

def write_new_html(new_text):
    with open("index.html", "w") as fileobj:
        fileobj.write(new_text)

def generate_movie_grid(movies):
    output = ""
    for title, info in movies.items():
        output += f"""
        <li>
            <div class="movie">
                <img class="movie-poster" src="{info["poster"]}"/>
                <div class="movie-title">{title}</div>
                <div class="movie-year">{info["year"]}</div>
            </div>
        </li>
        """
    return output

def generate_website():
    html_text = read_html_template()
    html_text = replace_title_information(html_text, "My Movies")
    movies = storage.list_movies()
    movie_grid = generate_movie_grid(movies)
    html_text = html_text.replace("__TEMPLATE_MOVIE_GRID__", movie_grid)
    write_new_html(html_text)

