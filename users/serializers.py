from rest_framework import serializers
from .models import LoginSignUp
from django.contrib.auth.hashers import make_password


class SignUpSerializers(serializers.ModelSerializer):
    """
    Serializer for creating and updating user records.
    """
    class Meta:
        model = LoginSignUp
        fields = ['id', 'Firstname', 'LastName', 'UserName', 'Password', 'Email', 'MobileNumber']
        extra_kwargs = {
            'UserName': {'required': False},  # Optional for partial updates
            'Password': {'required': False},  # Optional for partial updates
            'Email': {'required': False},  # Optional for partial updates
            'Firstname': {'required': False},  # Optional for partial updates
            'LastName': {'required': False},  # Optional for partial updates
            'MobileNumber': {'required': False},  # Optional for partial updates
        }

    def validate(self, data):
        """
        Validate fields to ensure no duplicates for UserName and Email during updates.
        """
        # For updates, exclude the current instance from duplicate checks
        if self.instance:
            if 'UserName' in data and LoginSignUp.objects.filter(UserName=data['UserName']).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError({"UserName": "This username is already in use."})
            if 'Email' in data and LoginSignUp.objects.filter(Email=data['Email']).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError({"Email": "This email is already in use."})
        else:  # For new records, check uniqueness directly
            if 'UserName' in data and LoginSignUp.objects.filter(UserName=data['UserName']).exists():
                raise serializers.ValidationError({"UserName": "This username is already in use."})
            if 'Email' in data and LoginSignUp.objects.filter(Email=data['Email']).exists():
                raise serializers.ValidationError({"Email": "This email is already in use."})
        return data

    def create(self, validated_data):
        """
        Custom create method to handle password hashing.
        """
        if 'Password' in validated_data:
            validated_data['Password'] = make_password(validated_data['Password'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Custom update method to handle partial updates and password hashing.
        """
        if 'Password' in validated_data:
            validated_data['Password'] = make_password(validated_data['Password'])
        return super().update(instance, validated_data)


class GetSignUpSerializers(serializers.ModelSerializer):
    """
    Serializer for fetching user records.
    """
    class Meta:
        model = LoginSignUp
        fields = ['id', 'Firstname', 'LastName', 'UserName', 'Email', 'MobileNumber']
