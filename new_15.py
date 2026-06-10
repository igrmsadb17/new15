import streamlit as st
import requests
import pickle

st.title("Movie Recommendation System ")

movies_df = pickle.load(open("movies.pkl", "rb"))
movies_list = movies_df["title"]

similarity_matrix = pickle.load(open("similarity.pkl", "rb"))

movie_name = st.selectbox("Select Movie:", movies_list)

def create_poster_url(movie_id):
    my_api = st.secrets["TMDB_API_KEY"]
    search_url = f"https://api.themoviedb.org/movie/{movie_id}?api_key={my_api}"
    response = requests.get(search_url).json()

    base_url = "https://image.tmdb.org/t/p/"
    image_size = "w500"
    poster_path = response["poster_path"]
    if poster_path:
        poster_url = base_url + image_size + poster_path
        return poster_url
    
    return None



def recommendation(movie_name):
    movie_names = []
    poster_urls = []

    movie_index = movies_df[movies_df["title"] == movie_name].index[0]
    similarity_values = sorted(list(enumerate(similarity_matrix[movie_index])), reverse = True, key = lambda x : x[1])[1:6]
    for i in similarity_values:
        movie_names.append[movies_df.iloc[i[0]]["title"]]
        poster_urls.append(create_poster_url(movies_df.iloc[i[0]]["id"]))
    return movie_names, poster_urls

movie_names, poster_urls = recommendation(movie_name)
cols = st.column(5)

if st.button("Recommendations: ", width="stretch"):
    for i in range(len(movie_names)):
        with cols[i]:
            st.image(poster_urls[i])
            st.write(movie_names[i])
            


