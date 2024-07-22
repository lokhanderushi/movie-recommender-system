import streamlit as st
import pickle
import pandas as pd

# Load the data
movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movie = pd.DataFrame(movie_dict)

# Load the similarity matrix
similarity = pickle.load(open('similarity.pkl', 'rb'))

def recommend(movie_name):
    # Check if the movie exists in the dataset
    movie_indices = movie[movie['title'] == movie_name].index
    if movie_indices.empty:
        st.write(f"Movie titled '{movie_name}' not found in the database.")
        return
    
    movie_index = movie_indices[0]  # Get the index of the movie
    
    distance = similarity[movie_index]
    top_similarities = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    for i in top_similarities:
        recommended_movies.append(movie.iloc[i[0]]['title'])
    
    return recommended_movies

# Streamlit interface
st.title("Movie Recommender System")

selected_movie_name = st.selectbox(
    'Select a movie:',
    movie['title'].values
)

if st.button('Recommend'):
    recommendations = recommend(selected_movie_name)
    if recommendations:
        st.write(f"Top 5 movies similar to '{selected_movie_name}':")
        for movie_title in recommendations:
            st.write(movie_title)
