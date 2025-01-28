from django.db import models

class LoginSignUp(models.Model):
    Firstname = models.CharField(max_length=100, null=False, blank=False)  # Mandatory
    LastName = models.CharField(max_length=100, null=False, blank=False)  # Mandatory
    UserName = models.CharField(max_length=100, unique=True, null=False, blank=False)  # Mandatory and Unique
    Password = models.CharField(max_length=100, null=False, blank=False)  # Mandatory
    Email = models.EmailField(unique=True, null=False, blank=False)  # Mandatory and Unique
    MobileNumber = models.CharField(max_length=15, null=False, blank=False)  # Mandatory
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)  # Optional
    date_created = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    class Meta:
        db_table = "SignUp_Data"

    def __str__(self):
        return f"{self.Firstname} {self.LastName}"