from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from users.models import LoginSignUp


class SignUpSerializers(serializers.ModelSerializer):
    """
    Serializer for creating and updating user records.
    """
    UserName = serializers.CharField(
        required=True,
        label="Username",
        help_text="(Mandatory and must be unique)",
        validators=[
            UniqueValidator(
                queryset=LoginSignUp.objects.all(), 
                message="This username is already in use."
            )
        ]
    )
    Email = serializers.EmailField(
        required=True,
        label="Email Address",
        help_text="(Mandatory and must be unique)",
        validators=[
            UniqueValidator(
                queryset=LoginSignUp.objects.all(), 
                message="This email is already in use."
            )
        ]
    )
    Password = serializers.CharField(
        required=True,
        write_only=True,
        label="Password",
        help_text="(Mandatory)"
    )
    profile_picture = serializers.ImageField(
        required=False,
        label="Profile Picture",
        help_text="(Optional)"
    )

    class Meta:
        model = LoginSignUp
        fields = [
            'id', 
            'Firstname', 
            'LastName', 
            'UserName', 
            'Password', 
            'Email', 
            'MobileNumber', 
            'profile_picture',
        ]
        extra_kwargs = {
            'Firstname': {
                'required': True, 
                'label': 'First Name', 
                'help_text': '(Mandatory)'
            },
            'LastName': {
                'required': True, 
                'label': 'Last Name', 
                'help_text': '(Mandatory)'
            },
            'MobileNumber': {
                'required': True, 
                'label': 'Mobile Number', 
                'help_text': '(Mandatory)'
            },
        }

    def validate(self, data):
        """
        Validate required fields and uniqueness.
        """
        if not self.instance:  # For new user creation
            required_fields = ['Firstname', 'LastName', 'UserName', 'Email', 'MobileNumber', 'Password']
            for field in required_fields:
                if field not in data or not data[field]:
                    raise serializers.ValidationError({field: f"{field} is required."})
        return data

    def create(self, validated_data):
        """
        Custom create method to handle Password hashing if needed.
        """
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Custom update method to handle specific update logic.
        """
        return super().update(instance, validated_data)


class GetSignUpSerializers(serializers.ModelSerializer):
    """
    Serializer for fetching user records, including creation date.
    """
    date_created = serializers.DateTimeField(read_only=True)  # Ensure this is read-only

    class Meta:
        model = LoginSignUp
        fields = [
            'id', 
            'Firstname', 
            'LastName', 
            'UserName', 
            'Email', 
            'MobileNumber', 
            'profile_picture', 
            'date_created',
        ]


class UserNameSerializer(serializers.ModelSerializer):
    """
    Serializer for fetching only user name details.
    """
    class Meta:
        model = LoginSignUp
        fields = ['Firstname', 'LastName']
