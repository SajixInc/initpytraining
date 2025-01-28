from rest_framework import serializers
from users.models import LoginSignUp  # Assuming the model exists in `users.models`

class UserCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginSignUp
        fields = ['date_created']
