from datetime import date
from enum import auto
import pickle
from unittest import result
import streamlit as st
import requests
from streamlit_player import st_player
import json

st.set_page_config(
   page_title="MovieMaze",
   page_icon="icons8-movie-projector-16.png",
   layout="wide",
   initial_sidebar_state="expanded",
)
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path
def fetch_trailer(movie_id):
    vurl = "https://api.themoviedb.org/3/movie/{}/videos?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data2 = requests.get(vurl)  
    data2 = data2.json()  
    result = data2['results']
    for x in result:
        key = x["key"]
    video = "https://www.youtube.com/watch?v=" + key    
    return video
# "https://www.youtube.com/watch?v=" + 
def fetch_detail(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data1 = requests.get(url)
    data1 = data1.json()
    overview = data1['overview']
    name = data1['original_title']
    genre = data1['genres']
    genre_name = []
    for x in genre:
        genre_name.append(x["name"])

    rdate = data1['release_date']
    rtime = data1['runtime']
    popularity = data1['popularity']
    language = data1['original_language']
    adult = data1['adult']
    vote_count = data1['vote_count']
    return overview,name,genre_name,rdate,rtime,popularity,language,adult,vote_count

def fetch_reviews(movie_id):
    rurl = "https://api.themoviedb.org/3/movie/{}/reviews?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data3 = requests.get(rurl)
    data3 = data3.json()
    result = data3['results']
    review = []
    for x in result:
        review.append(x["content"])
    return review   
      
def post_ratings(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}/rating?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data4 = requests.post(url, data = {'object':'rating'})

def fetch_cast(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}/credits?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    cast = data['cast']
    cast_name = []
    for x in cast:
        cast_name.append(x["name"])
    return cast_name    

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_details = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_details.append(fetch_detail(movie_id))

    return recommended_movie_names,recommended_movie_posters,recommended_movie_details,movie_id,index


st.header('MovieMaze')
movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))
sentiment = pickle.load(open('sentiment.pkl','rb'))
vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))

def sentimental(review):
    vec = vectorizer.transform(review)
    return sentiment.predict(vec)

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters,recommended_movie_details,movie_id,index = recommend(selected_movie)
    id = movies.iloc[index].movie_id  
    overview,name,genre_name,rdate,rtime,popularity,language,adult,vote_count = fetch_detail(id)  
    video = fetch_trailer(id)
    review = fetch_reviews(id)
    

    rating = post_ratings(id)
    cast_name = fetch_cast(id)
    st.header(selected_movie)
    
    c1,c2 = st.columns([2,2])
    with c1:
        st.image(fetch_poster(id))
    with c2:
        st.write('*Name*: ', name)
        st.write('*Overview*:  ', overview)
        #st.write('Hello, World! :sunglasses:')
        st.write('*Genre*: ')
        for x in genre_name:
            st.success(x)
        st.write('*Cast*:')
        for x in cast_name[0:4]:
            st.write(x)    
        st.write('*Release Date*: ', rdate)
        st.write('*Runtime*: ', rtime)
        st.write('*Popularity*: ',popularity)
        st.write('*Language*: ',language)
        
        # st.write('*Adult*:',adult)
        st.write('*Vote Count*:',vote_count)
        rating = st.number_input("Rate the movie:")
        if rating > 0:

            st.write('Movie Score: ', rating)
        # st_player(video)
    st_player(video)    
    st.write('*Reviews*:')
    col1, col2 = st.columns(2)
    with col1:
        for x in review:
            st.write(x)
    with col2:
        snt = sentimental(review)
        for i in snt:
            if(i == 1):
                st.write('good')
            else:
                st.write('Bad')
    st.success('Recommended for you')        
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
         
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])








