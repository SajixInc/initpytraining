from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.conf import settings

# Static mappings for search queries to specific routes
APP_URL_MAPPING = {
    # Users app routes
    "create user": "/user/create-user/",
    "get users": "/user/get-users/",
    "get user by id": "/user/get-users/<id>/",
    "update user": "/user/update-user/<id>/",
    "delete user": "/user/delete-user/<id>/",

    # Appointments app routes
    "book appointment": "/appointments/book/",
    "manage appointments": "/appointments/manage/<user_id>/",
    "manage appointment": "/appointments/manage/<user_id>/<appointmentID>/",
    "reschedule appointment": "/appointments/reschedule/<appointmentID>/",
    "cancel appointment": "/appointments/cancel/<appointmentID>/",
}

def search_apps(request):
    """
    Displays installed apps and redirects to their URLs based on user input.
    """
    query = request.GET.get('query', '').strip().lower()  # Normalize user input
    available_apps = get_installed_apps()  # Dynamically detect apps

    # Check if the query matches the static mapping
    if query in APP_URL_MAPPING:
        redirect_url = APP_URL_MAPPING[query]
        return redirect(redirect_url)

    # Render the search page with available routes
    return render(request, 'search/search.html', {
        'error': f"No match found for '{query}'." if query else None,
        'available_apps': list(APP_URL_MAPPING.keys()),
    })


def get_installed_apps():
    """
    Fetch user-defined apps from settings.INSTALLED_APPS.
    """
    excluded_apps = ['django', 'rest_framework', 'search']  # Exclude system apps
    user_apps = [
        app.split('.')[-1].lower()
        for app in settings.INSTALLED_APPS
        if not any(excl in app for excl in excluded_apps)
    ]
    return user_apps
