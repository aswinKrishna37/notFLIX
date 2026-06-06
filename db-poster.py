# local db validation

from flask import Flask, render_template_string
import sqlite3

app = Flask(__name__)

# Base URL for TMDb images
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

@app.route('/')
def index():
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    cursor.execute("SELECT title, file_path, poster_url FROM movies")
    movies = cursor.fetchall()
    conn.close()
    
    # Simple HTML template for your library
    html = """
    <html>
    <head><link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"></head>
    <body class="bg-dark text-white">
        <div class="container mt-4">
            <h1>My Movie Library</h1>
            <div class="row">
                {% for movie in movies %}
                <div class="col-md-3 mb-4">
                    <div class="card bg-secondary">
                        <img src="{{ 'https://image.tmdb.org/t/p/w500' + movie[2] if movie[2] else '' }}" class="card-img-top">
                        <div class="card-body">
                            <h5 class="card-title">{{ movie[0] }}</h5>
                            <p class="small text-truncate" 
   style="cursor: help; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" 
   title="{{ movie[1] }}">
   {{ movie[1] }}
</p>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html, movies=movies)

if __name__ == '__main__':
    app.run(debug=True)