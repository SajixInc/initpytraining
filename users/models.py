from django.db import models
class LoginSignUp(models.Model):
    Firstname = models.CharField(max_length=100)
    LastName = models.CharField(max_length=100)
    UserName = models.CharField(max_length=100, unique=True)  # Unique username
    Password = models.CharField(max_length=100)  # For production, use hashed passwords
    Email = models.EmailField(unique=True)  # Unique email
    MobileNumber = models.CharField(max_length=15, blank=True, null=True)  # Optional field
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    objects = models.Manager()

    class Meta:
        db_table = "SignUp_Data"

    def __str__(self):
        return self.UserName
