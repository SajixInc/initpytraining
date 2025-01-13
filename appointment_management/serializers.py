from rest_framework import serializers
from appointment_management.models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['appointmentID', 'user', 'appointment_date', 'appointment_time', 'status', 'created_at']
        read_only_fields = ['appointmentID', 'status', 'created_at']