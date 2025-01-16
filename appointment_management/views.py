from rest_framework import generics, status
from rest_framework.response import Response
from appointment_management.models import Appointment
from appointment_management.serializers import AppointmentSerializer
from users.models import LoginSignUp
import traceback

class BookAppointmentView(generics.GenericAPIView):
    serializer_class = AppointmentSerializer

    def post(self, request, *args, **kwargs):
        try:
            user_id = request.data.get('user')
            if not user_id:
                return Response({"Message": "User ID is required", "Status": 400, "HasError": True},
                                status=status.HTTP_400_BAD_REQUEST)
            user = LoginSignUp.objects.get(id=user_id)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            appointment = serializer.save(user=user)
            return Response(
                {
                    "Message": "Appointment Booked Successfully",
                    "Result": AppointmentSerializer(appointment).data,
                    "Status": 201,
                    "HasError": False,
                },
                status=status.HTTP_201_CREATED,
            )
        except LoginSignUp.DoesNotExist:
            return Response({"Message": "User not found", "Status": 404, "HasError": True},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            traceback.print_exc()
            return Response(
                {"Message": "Failed to Book Appointment", "Result": str(e), "Status": 400, "HasError": True},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ManageAppointmentView(generics.GenericAPIView):
    serializer_class = AppointmentSerializer

    def get(self, request, user_id=None, appointmentID=None, *args, **kwargs):
        try:
            user = LoginSignUp.objects.get(id=user_id)
            if appointmentID:
                appointment = Appointment.objects.get(user=user, appointmentID=appointmentID)
                serialized_data = self.serializer_class(appointment)
                message = "Appointment Retrieved Successfully"
            else:
                appointments = Appointment.objects.filter(user=user)
                serialized_data = self.serializer_class(appointments, many=True)
                message = "All Appointments Retrieved Successfully"

            return Response(
                {"Message": message, "Result": serialized_data.data, "Status": 200, "HasError": False},
                status=status.HTTP_200_OK,
            )
        except LoginSignUp.DoesNotExist:
            return Response({"Message": "User not found", "Status": 404, "HasError": True},
                            status=status.HTTP_404_NOT_FOUND)
        except Appointment.DoesNotExist:
            return Response({"Message": "Appointment not found", "Status": 404, "HasError": True},
                            status=status.HTTP_404_NOT_FOUND)


class RescheduleAppointmentView(generics.GenericAPIView):
    serializer_class = AppointmentSerializer

    def put(self, request, appointmentID, *args, **kwargs):
        try:
            user_id = request.data.get('user')
            user = LoginSignUp.objects.get(id=user_id)
            appointment = Appointment.objects.get(user=user, appointmentID=appointmentID)
            serializer = self.get_serializer(appointment, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            updated_appointment = serializer.save()
            return Response(
                {
                    "Message": "Appointment Rescheduled Successfully",
                    "Result": AppointmentSerializer(updated_appointment).data,
                    "Status": 200,
                    "HasError": False,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            traceback.print_exc()
            return Response(
                {"Message": "Failed to Reschedule Appointment", "Result": str(e), "Status": 400, "HasError": True},
                status=status.HTTP_400_BAD_REQUEST,
            )



class CancelAppointmentView(generics.GenericAPIView):
    def delete(self, request, appointmentID, *args, **kwargs):
        try:
            # Fetch the appointment using only the appointmentID
            appointment = Appointment.objects.get(appointmentID=appointmentID)
            appointment.delete()
            return Response(
                {
                    "Message": "Appointment Cancelled Successfully",
                    "Result": None,
                    "Status": 200,
                    "HasError": False,
                },
                status=status.HTTP_200_OK,
            )
        except Appointment.DoesNotExist:
            return Response(
                {
                    "Message": "Appointment not found",
                    "Result": None,
                    "Status": 404,
                    "HasError": True,
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            traceback.print_exc()
            return Response(
                {
                    "Message": "Failed to Cancel Appointment",
                    "Result": str(e),
                    "Status": 400,
                    "HasError": True,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )