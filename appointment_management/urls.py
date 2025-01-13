from django.urls import path
from appointment_management.views import (
    BookAppointmentView,
    ManageAppointmentView,
    RescheduleAppointmentView,
    CancelAppointmentView,
)

urlpatterns = [
    path('book/', BookAppointmentView.as_view(), name='book-appointment'),
    path('manage/<int:user_id>/', ManageAppointmentView.as_view(), name='manage-appointments'),
    path('manage/<int:user_id>/<int:appointmentID>/', ManageAppointmentView.as_view(), name='manage-appointment'),
    path('reschedule/<int:appointmentID>/', RescheduleAppointmentView.as_view(), name='reschedule-appointment'),
    path('cancel/<int:appointmentID>/', CancelAppointmentView.as_view(), name='cancel-appointment'),
]
