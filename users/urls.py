from django.urls import path
from .views import CreateUserView, GetUserView, UpdateUserView, DeleteUserView,search_users



urlpatterns = [
    # Route for creating a new user
    path('create-user/', CreateUserView.as_view(), name='create-user'),

    # Route for retrieving all users or a specific user by ID
    path('get-users/', GetUserView.as_view(), name='get-all-users'),
    path('get-users/<int:id>/', GetUserView.as_view(), name='get-user-by-id'),

    # Route for updating a user by ID
    path('update-user/<int:id>/', UpdateUserView.as_view(), name='update-user'),

    # Route for deleting a user by ID
    path('delete-user/<int:id>/', DeleteUserView.as_view(), name='delete-user'),
    path('searchusers/', search_users, name='search-users'),
]