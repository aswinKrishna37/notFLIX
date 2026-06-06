# Automatic metadata fetcher, storing in local db

import os
import sqlite3
import requests
import time
from dotenv import load_dotenv
from guessit import guessit

# 1. Setup
load_dotenv()
BEARER_TOKEN = os.getenv("TMDB_TOKEN")
HEADERS = {
    "accept": "application/json",
    "Authorization": f"Bearer {BEARER_TOKEN}",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# 2. Database Helper
def init_db():
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS movies 
                      (id INTEGER PRIMARY KEY, title TEXT, tmdb_id INTEGER UNIQUE, file_path TEXT, poster_url TEXT)''')
    conn.commit()
    conn.close()

def run_scanner(root_path):
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()

    for root, dirs, files in os.walk(root_path):
        dirs[:] = [d for d in dirs if d not in {'Series'}]
        
        for filename in files:
            if filename.lower().endswith((".mp4", ".mkv", ".avi")):
                file_path = os.path.join(root, filename)
                
                # 1. CHECK DATABASE FIRST
                cursor.execute("SELECT id FROM movies WHERE file_path = ?", (file_path,))
                if cursor.fetchone():
                    print(f"Already in database: {filename}")
                    continue # Skip to the next file
                
                # 2. IF NOT IN DB, FETCH FROM TMDB
                print(f"New file found, fetching from API: {filename}")
                match = guessit(filename)
                clean_title = match.get('title')
                year = match.get('year') # Optional: use the year to make the search more accurate

                if not clean_title:
                    print(f"Could not identify title for {filename}, skipping.")
                    continue
                

                
                params = {
                    "query": clean_title,
                }
                if year:
                    params["year"] = year
                
                try:
                    response = requests.get("https://api.themoviedb.org/3/search/movie", params=params, headers=HEADERS)
                    
                    if response.status_code == 200:
                        results = response.json().get('results')
                        if results:
                            movie = results[0]
                            cursor.execute("INSERT OR IGNORE INTO movies (title, tmdb_id, file_path, poster_url) VALUES (?,?,?,?)",
                                           (movie['title'], movie['id'], file_path, movie.get('poster_path')))
                            conn.commit()
                            print(f"Added: {movie['title']}")
                        else:
                            print(f"API Search returned NO results for query: {clean_title} (Year: {year})")
                    elif response.status_code == 429:
                        print("Rate limit hit! Sleeping for 10 seconds...")
                        time.sleep(10) # Back off if they ask us to
                
                except requests.exceptions.ConnectionError:
                    print(f"Connection lost for {filename}. Sleeping 5s and skipping...")
                    time.sleep(5)
                
                time.sleep(1.0) # INCREASED SLEEP: Give the server breathing room

                
    conn.close()


# 4. Where to put the path
if __name__ == "__main__":
    my_movies_path = r'D:\Aswin Krishna\Videos\Movies\English' 
    run_scanner(my_movies_path)