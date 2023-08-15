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
url = "https://imdb8.p.rapidapi.com/auto-complete"

def movies(request):
    content_list = Content.objects.all()
    try:
        # get movie name
        query = ''
        if 'get_movie' in request.POST:
            query= request.POST.get('movie_name')
        querystring = {"q": query}

        #get json data of entered movie
        response = requests.get(url, headers=headers, params=querystring).json()
        content_data = {
          'content_id': response['d'][0]['id'],
          'content_name': response['d'][0]['l'],
          'content_image': response['d'][0]['i']['imageUrl'],
          'content_type': response['d'][0]['qid'],
          'release_year': response['d'][0]['y'],
        }

        #save data from json to model
        Content.objects.get_or_create(**content_data)
        redirect('/')
        context = {
            'content_list': content_list
        }
        return render(request, 'organizer_app/organizer.html', {'content_list': content_list})
    except Exception:
        return render(request, 'organizer_app/organizer.html',{'content_list': content_list})