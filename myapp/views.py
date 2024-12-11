# myapp/views.py
import requests
from django.shortcuts import render
from django.http import JsonResponse
import pickle
import pandas as pd

API_KEY = '89eddc3e'

def fun(request):
    return render(request,"myapp/homepage.html")

# Load the movies list and similarity matrix at the start
with open('myapp/movies_list.pkl', 'rb') as f:
    movies_list = pd.DataFrame(pickle.load(f))

with open('myapp/similarity.pkl', 'rb') as f:
    similarity = pickle.load(f)

def recommend(movie_title):
    movie_title = movie_title.lower()
    movies_list['title'] = movies_list['title'].str.lower()
    try:
        index = movies_list[movies_list['title'] == movie_title].index[0]
        similarity_scores = list(enumerate(similarity[index]))
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        recommended_indices = [i[0] for i in similarity_scores[1:6]]
        recommended_movies = movies_list['title'].iloc[recommended_indices].tolist()
        return recommended_movies
    except IndexError:
        return ["Movie not found"]

def fetch_movie_details(movie_title):
    # Use the API to search by title instead of ID to handle variations
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={API_KEY}"
    response = requests.get(url)
    try:
        movie_data = response.json()
        # Check if the response contains valid data
        if movie_data.get("Response") == "True":
            return movie_data
        else:
            print("OMDB API Error:", movie_data.get("Error"))
            return None
    except ValueError:
        print("Invalid JSON received:", response.text)
        return None

def get_recommendations(request):
    movie_title = request.GET.get('title')
    recommendations = recommend(movie_title)
    
    recommended_movies = []
    for movie in recommendations:
        details = fetch_movie_details(movie)
        if details:  # Only append if details are valid
            recommended_movies.append({
                'title': details.get('Title', 'N/A'),
                'poster': details.get('Poster', ''),
                'year': details.get('Year', 'N/A'),
                'plot': details.get('Plot', 'N/A')
            })

    return render(request, 'myapp/recommendations.html', {'recommended_movies': recommended_movies})
