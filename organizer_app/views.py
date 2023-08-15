from django.shortcuts import render
from django.views.generic import View
import requests
from pprint import pprint
from decouple import config


headers = {
  "X-RapidAPI-Key": config('X-RapidAPI-Key'),
  "X-RapidAPI-Host": config('X-RapidAPI-Host'),
}
url = "https://imdb8.p.rapidapi.com/auto-complete"

class MoviesOrganizerView(View):

    def get(self, request):
        querystring = {"q": 'no man of god'}

        response = requests.get(url, headers=headers, params=querystring).json()
        content_data = {
          'content_id': response['d'][0]['id'],
          'content_name': response['d'][0]['l'],
          'content_image': response['d'][0]['i']['imageUrl'],
          'content_type': response['d'][0]['qid'],
          'release_year': response['d'][0]['y'],
        }
        context = {
            'content_data': content_data,
        }
        return render(request, 'organizer_app/organizer.html', context)