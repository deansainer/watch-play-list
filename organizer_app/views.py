from django.shortcuts import render, redirect
from django.views.generic import View
import requests
from pprint import pprint
from decouple import config
from .models import *

headers = {
  "X-RapidAPI-Key": config('X-RapidAPI-Key'),
  "X-RapidAPI-Host": config('X-RapidAPI-Host'),
}
content_data_url = "https://imdb8.p.rapidapi.com/auto-complete"
content_details_url = "https://online-movie-database.p.rapidapi.com/title/get-overview-details"

def movies(request):
    # getting all objects from 'content' model
    content_list = Content.objects.all()

    try:
        # get movie name
        query = ''
        if 'get_movie' in request.POST:
            query= request.POST.get('movie_name')
        querystring = {"q": query}

        #get json data of entered movie name
        response = requests.get(content_data_url, headers=headers, params=querystring).json()
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

        return render(request, 'organizer_app/organizer.html', {'content_list': content_list})
    except Exception:
        return render(request, 'organizer_app/organizer.html',{'content_list': content_list})