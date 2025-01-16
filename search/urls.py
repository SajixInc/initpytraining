from django.urls import path
from .views import search_apps

urlpatterns = [
    path('', search_apps, name='search_apps'),  # Root path for search
]
