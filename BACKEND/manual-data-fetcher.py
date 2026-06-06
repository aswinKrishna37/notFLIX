# Input file location, tmdb id to add poster url and title on local database

import sqlite3
import requests
import os
from dotenv import load_dotenv

load_dotenv()
BEARER_TOKEN = os.getenv("TMDB_TOKEN")
HEADERS = {
    "accept": "application/json",
    "Authorization": f"Bearer {BEARER_TOKEN}",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def add_movie_manually(tmdb_id, file_path):
    # 1. Fetch details directly from TMDb using the ID
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        data = response.json()
        title = data.get('title')
        poster_path = data.get('poster_path')
        
        # 2. Add to Database
        conn = sqlite3.connect('movies.db')
        cursor = conn.cursor()
        try:
            cursor.execute('''INSERT OR REPLACE INTO movies 
                              (title, tmdb_id, file_path, poster_url) 
                              VALUES (?, ?, ?, ?)''', 
                           (title, tmdb_id, file_path, poster_path))
            conn.commit()
            print(f"Successfully added: {title} (ID: {tmdb_id})")
        except Exception as e:
            print(f"Database error: {e}")
        finally:
            conn.close()
    else:
        print(f"Failed to fetch ID {tmdb_id}. Check if the ID is correct. Status: {response.status_code}")

# 3. User Input Section
if __name__ == "__main__":
    while True:
        t_id = input("Enter the TMDb ID: ")
        f_path = input("Enter the full file path: ")
        add_movie_manually(t_id, f_path)