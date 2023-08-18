from django.urls import path, include
from . import views
from .views import *


urlpatterns = [
    path('', views.movies),
    path('delete/<str:id>', views.delete, name='delete_url'),
    path('details/<str:id>', views.details, name='details_url')
]