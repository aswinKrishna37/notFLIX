# NotFlix - Not Netflix

A personal movie library manager that automatically fetches metadata from The Movie Database (TMDB) and provides a web-based interface to browse your movie collection with posters and details.

## Features

- **Automatic Metadata Fetching**: Scans your movie folders and automatically fetches titles, posters, and metadata from TMDB
- **Smart Title Recognition**: Uses `guessit` library to extract movie titles from filenames
- **SQLite Database**: Local database to store movie information and avoid duplicate API calls
- **Web Interface**: Flask-based web application to browse your movie library with poster art
- **Manual Entry**: Option to manually add movies by TMDB ID if automatic detection fails
- **Rate Limiting Protection**: Includes built-in delays and error handling for TMDB API rate limits

## Project Structure

```
├── main.py                    # Automatic scanner and metadata fetcher
├── db-poster.py               # Flask web app for browsing the library
├── manual-data-fetcher.py     # Manual movie entry tool
└── movies.db                  # SQLite database (auto-generated)
```

## Prerequisites

- Python 3.7+
- TMDB API Key (free account at [themoviedb.org](https://www.themoviedb.org/settings/api))

## Installation

1. **Clone or download** the project
2. **Install dependencies**:
   ```bash
   pip install requests guessit flask python-dotenv
   ```

3. **Set up environment variables**:
   Create a `.env` file in the project directory:
   ```
   TMDB_TOKEN=your_tmdb_api_key_here
   ```

4. **Update movie path** (optional):
   Edit `main.py` and update the `my_movies_path` variable to point to your movie directory:
   ```python
   my_movies_path = r'path\to\your\movies'
   ```

## Usage

### 1. Scan and Fetch Metadata
Run the automatic scanner to add all movies from your folder:
```bash
python main.py
```
This will:
- Scan your movies folder recursively
- Extract titles from filenames
- Fetch metadata and posters from TMDB
- Store everything in the local SQLite database
- Skip files already in the database

### 2. Browse Your Library
Start the web interface:
```bash
python db-poster.py
```
Then open your browser to `http://localhost:5000` to view your movie library with posters.

### 3. Manually Add Movies
If a movie wasn't automatically detected, add it manually:
```bash
python manual-data-fetcher.py
```
Follow the prompts to enter the TMDB ID and file path.

## Database Schema

The `movies.db` SQLite database contains:

```sql
CREATE TABLE movies (
    id INTEGER PRIMARY KEY,
    title TEXT,
    tmdb_id INTEGER UNIQUE,
    file_path TEXT,
    poster_url TEXT
)
```

## Configuration

- **Supported formats**: `.mp4`, `.mkv`, `.avi`
- **Series folder**: Automatically excluded from scanning
- **API delay**: 1 second between requests to TMDB (configurable in `main.py`)
- **Rate limit handling**: 10-second backoff when rate limited

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "API Search returned NO results" | The filename might need manual entry via `manual-data-fetcher.py` |
| "Rate limit hit" | Script automatically waits 10 seconds and retries |
| "Connection lost" | Script skips the file and retries on next run |
| Missing TMDB token | Ensure `.env` file contains `TMDB_TOKEN` with valid API key |

## Dependencies

- **requests**: HTTP library for TMDB API calls
- **guessit**: Intelligent filename parser for movie titles
- **flask**: Lightweight web framework
- **sqlite3**: Built-in Python database (no installation needed)
- **python-dotenv**: Environment variable management

## License

Personal project - Use freely

## Notes

- The project excludes "Series" folders by default (edit `main.py` to modify)
- Posters are loaded from TMDB's image CDN
- The web interface uses Bootstrap 5 for styling
- All metadata is stored locally to minimize API calls
