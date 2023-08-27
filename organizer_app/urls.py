from django.urls import path, include
from . import views
from .views import *

urlpatterns = [
    path('register/', views.register, name='register_url'),
    path('login/', views.user_login, name='login_url'),
    path('logout/', views.user_logout, name='logout_url'),
    path('', views.MovieView.as_view(), name='home_url'),
    path('delete/<str:id>', views.delete, name='delete_url'),
    path('details/<str:id>', views.details, name='details_url'),
    path('mark_as_watched/<str:id>', views.mark_as_watched, name='mark_as_watched_url'),
    path('history', views.HistoryView.as_view(), name='history_url'),
    path('mark_as_unwatched/<str:id>', views.mark_as_unwatched, name='mark_as_unwatched_url'),
    path('most_popular_movies', views.MostPopularMoviesView.as_view(), name='most_popular_movies_url'),
    path('api/', include('rest_framework.urls')),

]
