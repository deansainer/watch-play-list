# import requests
# from decouple import config
# from pprint import pprint
#
#
# headers = {
#   "X-RapidAPI-Key": config('X-RapidAPI-Key'),
#   "X-RapidAPI-Host": config('X-RapidAPI-Host'),
# }
# content_data_url = "https://online-movie-database.p.rapidapi.com/auto-complete"
# content_details_url = "https://online-movie-database.p.rapidapi.com/title/get-overview-details"
#
#
#
# querystring = {"q": 'Inception'}
# response = requests.get(content_data_url, headers=headers, params=querystring).json()
#
# #get id of entered movie
# get_id = response['d'][0]['id']
#
# querystring = {"tconst": get_id}
#
# content_details_response = requests.get(content_details_url, headers=headers, params=querystring).json()
#
# content_details_data = {
#     'id': get_id,
#     'title': content_details_response['title']['title'],
#     'year': content_details_response['title']['year'],
#     'type': content_details_response['title']['titleType'].capitalize(),
#     'top_rank': content_details_response['ratings']['topRank'],
#     'image': content_details_response['title']['image']['url'],
#     'duration': content_details_response['title']['runningTimeInMinutes'],
#     'rating': content_details_response['ratings']['rating'],
#     'genres': ', '.join(content_details_response['genres']),
#     'some_plot': content_details_response['plotOutline']['text'],
#     'full_plot': content_details_response['plotSummary']['text'],
# }
# pprint(content_details_data)

import requests
import re
from decouple import config


most_popular_movies_url = "https://online-movie-database.p.rapidapi.com/title/get-most-popular-movies"
most_popular_movies_querystring = {"currentCountry":"US","purchaseCountry":"US","homeCountry":"US"}

content_data_url = "https://online-movie-database.p.rapidapi.com/auto-complete"
content_details_url = "https://online-movie-database.p.rapidapi.com/title/get-overview-details"

headers = {
  "X-RapidAPI-Key": config('X-RapidAPI-Key'),
  "X-RapidAPI-Host": config('X-RapidAPI-Host'),
}

most_popular_movies_response = requests.get(most_popular_movies_url, headers=headers, params=most_popular_movies_querystring).json()[:10]

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
print(most_popular_movies_list)

