import django_filters
from .models import LoginSignUp

class UserFilter(django_filters.FilterSet):
    class Meta:
        model = LoginSignUp
        fields = {
            'Firstname': ['icontains'],  # Case-insensitive partial matching
            'LastName': ['icontains'],   # Case-insensitive partial matching
        }


