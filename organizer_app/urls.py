from django.urls import path, include
from . import views
from .views import *


urlpatterns = [
    path('', views.MovieView.as_view(), name='home_url'),
    path('delete/<str:id>', views.delete, name='delete_url'),
    path('details/<str:id>', views.details, name='details_url'),
    path('mark_as_watched/<str:id>', views.mark_as_watched, name='mark_as_watched_url'),
]