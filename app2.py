import streamlit as st
import pickle
import pandas as pd
import requests
import gzip  # Import gzip module for decompressing .pkl.gz file

def fetch_poster(movie_id):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US")
    data = response.json()
    poster_path = data.get('poster_path')
    if poster_path:
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    else:
        return None

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    dist = similar[movie_index]
    movie_list = sorted(list(enumerate(dist)), reverse=True, key=lambda x: x[1])[1:6]
    recommend_movies = []
    recommended_movie_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].tmdbId
        recommend_movies.append(movies.iloc[i[0]].title)
        poster = fetch_poster(movie_id)
        if poster:
            recommended_movie_posters.append(poster)
        else:
            recommended_movie_posters.append("No poster available")
    return recommend_movies, recommended_movie_posters

# Set page config
st.set_page_config(layout="wide")

# Load data from compressed pickle file
movie_dict = pickle.load(open("movies_web.pkl", "rb"))

movies = pd.DataFrame(movie_dict)

with gzip.open("similar_web.pkl.gz", "rb") as f:
    similar = pickle.load(f)

# Title
st.title("Movie recommender System")

# HTML for setting background color
bg_color = "#102C57"  # Set your desired background color
html_code = f"""
    <style>
        .stApp {{
            background-color: {bg_color};
            color: white;
        }}
    </style>
"""
st.markdown(html_code, unsafe_allow_html=True)


# Selectbox for movie
selected_movie = st.selectbox("Select a movie", movies["title"])

# Button to recommend movies
if st.button("Recommend movies", key="recommend_button", help="Click to get movie recommendations",):
    # Your recommendation logic here

    name, posters = recommend(selected_movie)
    cols = st.columns(5)
    for i, col in enumerate(cols):
        col.text(name[i])
        if posters[i] != "No poster available":
            col.image(posters[i])
        else:
            col.write(posters[i])
