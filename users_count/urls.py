from django.urls import path
from .views import user_registration_aggregated

urlpatterns = [
    path('api/user-count/', user_registration_aggregated, name='user_registration_aggregated'),
]
