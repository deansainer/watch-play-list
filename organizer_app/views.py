from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
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

def mark_as_unwatched(request, id):
    content = Content.objects.get(id=id)
    content.is_watched=False
    content.save()
    return redirect('/history')

class HistoryView(View):
    def get(self, request, *args, **kwargs):
        content_list = Content.objects.filter(is_watched=True)
        context = {'content_list': content_list}
        return render(request, 'organizer_app/history.html', context)