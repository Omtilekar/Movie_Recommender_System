import pickle
import requests
import pandas as pd
import streamlit as st
import base64

# Function to encode background image
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


# Function to set background image
def set_bg_hack(main_bg):
    '''
    A function to unpack an image from root folder and set as bg.
    '''
    bin_str = get_base64_of_bin_file(main_bg)
    page_bg_img = '''
    <style>
    .stApp {
        background-image: url("data:image/png;base64,%s");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)


# Set page configuration
st.set_page_config(layout="wide")

# Set background image from local folder
# Replace 'background.jpg' with your image path
set_bg_hack('background_image3.jpg')

st.markdown(
    """
    <style>
    .markdown-container {
        background-color: rgba(255, 255, 255, 1);  /* Semi-transparent white */
        padding: 20px;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Add custom CSS for the links and name with enhanced visibility
st.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        background-color: rgba(240, 242, 246, 0.8);
    }
    .right-corner {
        position: absolute;
        top: 10px;
        right: 10px;
        text-align: right;
        font-size: 16px;
        background-color: rgba(255, 255, 255, 0.8);
        padding: 10px;
        border-radius: 5px;
        z-index: 1000; /* Ensure links are clickable */
    }
    .right-corner a {
        margin-left: 10px;
        text-decoration: none;
        color: #1e90ff;
    }
    .right-corner a:hover {
        text-decoration: underline;
    }
    /* Add text shadow to improve readability on any background */
    h1 {
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        color: white;
    }
    /* Style for movie titles */
    .movie-title {
        background-color: rgba(255, 255, 255, 0.8);
        padding: 5px;
        border-radius: 3px;
        margin-bottom: 5px;
    }
    /* Center and style the recommend button */
    .center-button {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .recommend-btn {
        font-size: 18px;
        padding: 15px 30px;
        background-color: #d5eaff;
        color: black;
        border-radius: 5px;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .recommend-btn:hover {
        background-color:#4578de;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Add your name and links in the upper right corner
st.markdown(
    """
    <div class="right-corner">
        <p style="font-size: 25px;text-align: center;color: Black; font-weight: bold;">Om Tilekar  </p>
        <a href="https://github.com/Omtilekar" target="_blank">GitHub</a>
        <a href="https://www.linkedin.com/in/om-tilekar-7bb427222" target="_blank">LinkedIn</a>
    </div>
    """,
    unsafe_allow_html=True
)

# Main title
st.markdown("<h1 style='text-align: center;color: Black'>Movies Recommender System</h1>", unsafe_allow_html=True)


# Function to fetch movie poster
def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=d50bcc1e4d87cd26fd6df713f7f3a97b&language=en-US')
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


# Function to recommend movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster


# Load movie data and similarity matrix
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Create a container with custom styling for the search box
with st.container():
    st.markdown(
        """
        <style>
        .stSelectbox {
            background-color: rgba(255, 255, 255, 0) !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    selected_movie_name = st.selectbox(
        '',  # Removed the 'Search Movie here' label
        movies['title']
    )

# Center the "Recommend" button and make it larger
st.markdown('<div class="center-button"><button class="recommend-btn" onclick="location.href=\'#\'">Recommend</button></div>', unsafe_allow_html=True)

# Recommendation button
if st.button('Recommend'):
    recommended_movies, recommended_movies_poster = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)

    columns = [col1, col2, col3, col4, col5]
    for i, col in enumerate(columns):
        with col:
            st.markdown(f'<div class="movie-title">{recommended_movies[i]}</div>', unsafe_allow_html=True)
            st.image(recommended_movies_poster[i])

    st.markdown("<h1 style='text-align: center;color: black;'>Thank You For Visiting!</h1>", unsafe_allow_html=True)
