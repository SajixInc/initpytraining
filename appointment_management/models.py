from django.db import models
from users.models import LoginSignUp

class Appointment(models.Model):
    appointmentID = models.AutoField(primary_key=True)  # Custom primary key
    user = models.ForeignKey(LoginSignUp, on_delete=models.CASCADE, related_name="appointments")
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(max_length=50, default="Scheduled")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Appointment for {self.user.username} on {self.appointment_date}"
