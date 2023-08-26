from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
import requests
from pprint import pprint
from decouple import config
from .models import *
from django.contrib import messages
import re

headers = {
  "X-RapidAPI-Key": config('X-RapidAPI-Key'),
  "X-RapidAPI-Host": config('X-RapidAPI-Host'),
}
most_popular_movies_url = "https://online-movie-database.p.rapidapi.com/title/get-most-popular-movies"
most_popular_movies_querystring = {"currentCountry":"US","purchaseCountry":"US","homeCountry":"US"}

content_data_url = "https://online-movie-database.p.rapidapi.com/auto-complete"
content_details_url = "https://online-movie-database.p.rapidapi.com/title/get-overview-details"

class MovieView(View):
    def get(self, request, *args, **kwargs):
        content_list = Content.objects.filter(is_watched=False)
        return render(request,'organizer_app/organizer.html', {'content_list': content_list})
    def post(self, request, *args, **kwargs):
        # getting all unwatched objects from 'content' model
        content_list = Content.objects.filter(is_watched=False)
        try:
            # get movie name from user
            query = ''
            if 'get_movie' in request.POST:
                query= request.POST.get('movie_name')
            querystring = {"q": query}

            #get json data of entered movie name
            response = requests.get(content_data_url, headers=headers, params=querystring).json()

            #get id of entered movie
            get_id = response['d'][0]['id']

            querystring = {"tconst": get_id}

            content_details_response = requests.get(content_details_url, headers=headers, params=querystring).json()

            content_details_data = {
                'id': get_id,
                'title': content_details_response['title']['title'],
                'year': content_details_response['title']['year'],
                'type': content_details_response['title']['titleType'].capitalize(),
                'top_rank': content_details_response['ratings']['topRank'],
                'image': content_details_response['title']['image']['url'],
                'duration': content_details_response['title']['runningTimeInMinutes'],
                'rating': content_details_response['ratings']['rating'],
                'genres': ', '.join(content_details_response['genres']),
                'some_plot': content_details_response['plotOutline']['text'],
                'full_plot': content_details_response['plotSummary']['text'],
            }

            #save data from json to model
            Content.objects.get_or_create(**content_details_data)
            redirect('/')

            return render(request,'organizer_app/organizer.html', {'content_list': content_list})
        except Exception:
            messages.info(request, 'Content not found, try again.')
            return render(request, 'organizer_app/organizer.html',{'content_list': content_list})

# delete content from list
def delete(request, id):
    content = Content.objects.get(id=id)
    content.delete()
    return redirect('/')

# movie details page
def details(request, id):
    content = Content.objects.get(id=id)
    return render(request, 'organizer_app/details.html', {'content': content})

# mark movie as watched
def mark_as_watched(request, id):
    content = Content.objects.get(id=id)
    content.is_watched=True
    content.save()
    return redirect('/')

# mark movie as unwatched
def mark_as_unwatched(request, id):
    content = Content.objects.get(id=id)
    content.is_watched=False
    content.save()
    return redirect('/history')

# watch history page
class HistoryView(View):
    def get(self, request, *args, **kwargs):
        content_list = Content.objects.filter(is_watched=True)
        context = {'content_list': content_list}
        return render(request, 'organizer_app/history.html', context)

class MostPopularMoviesView(View):
    def get(self, request, *args, **kwargs):
        most_popular_movies_response = requests.get(most_popular_movies_url, headers=headers,
                                                    params=most_popular_movies_querystring).json()[:10]

        pattern = r'/title/(tt\d+)/'

        top_rated_list = []

        for id in most_popular_movies_response:
            match = re.search(pattern, id)
            if match:
                movie_id = match.group(1)
                top_rated_list.append(movie_id)

        most_popular_movies_list = []

        for id in top_rated_list:
            querystring = {"tconst": id}

            content_details_response = requests.get(content_details_url, headers=headers, params=querystring).json()

            content_details_data = {
                'id': id,
                'title': content_details_response['title']['title'],
                'year': content_details_response['title']['year'],
                'image': content_details_response['title']['image']['url'],
                'duration': content_details_response['title']['runningTimeInMinutes'],
                'genres': ', '.join(content_details_response['genres']),
            }
            most_popular_movies_list.append(content_details_data)
        context = {'most_popular_movies_list': most_popular_movies_list}
        return render(request, 'organizer_app/most_popular_movies.html', context)