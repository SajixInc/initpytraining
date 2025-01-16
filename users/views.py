from rest_framework import generics, status
from rest_framework.response import Response
from users.serializers import SignUpSerializers, GetSignUpSerializers
from users.models import LoginSignUp
import traceback


class CreateUserView(generics.GenericAPIView):
    serializer_class = SignUpSerializers

    def post(self, request, *args, **kwargs):
        """
        Create a new user without hashing passwords.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # Directly save the validated data without hashing the password
            serializer.save()
            return Response(
                {"Message": "User Created Successfully", "Result": serializer.data, "Status": 201, "HasError": False},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"Message": "Failed to Create User", "Result": serializer.errors, "Status": 400, "HasError": True},
            status=status.HTTP_400_BAD_REQUEST,
        )


class GetUserView(generics.GenericAPIView):
    serializer_class = GetSignUpSerializers

    def get(self, request, id=None, *args, **kwargs):
        """
        Retrieve a specific user by ID or all users.
        """
        if id:
            try:
                user = LoginSignUp.objects.get(id=id)
                serializer = self.serializer_class(user)
                return Response(
                    {"Message": "User Retrieved Successfully", "Result": serializer.data, "Status": 200, "HasError": False},
                    status=status.HTTP_200_OK,
                )
            except LoginSignUp.DoesNotExist:
                return Response(
                    {"Message": "User Not Found", "Result": None, "Status": 404, "HasError": True},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            users = LoginSignUp.objects.all()
            serializer = self.serializer_class(users, many=True)
            return Response(
                {"Message": "All Users Retrieved Successfully", "Result": serializer.data, "Status": 200, "HasError": False},
                status=status.HTTP_200_OK,
            )


class UpdateUserView(generics.GenericAPIView):
    serializer_class = SignUpSerializers

    def put(self, request, id, *args, **kwargs):
        """
        Update a user record by ID without hashing passwords.
        """
        try:
            # Fetch the user record by ID
            user = LoginSignUp.objects.get(id=id)

            # Pass partial=True to allow partial updates
            serializer = self.serializer_class(user, data=request.data, partial=True)
            
            if serializer.is_valid():
                # Save the updated user record without hashing passwords
                serializer.save()
                return Response(
                    {
                        "Message": "User Updated Successfully",
                        "Result": serializer.data,
                        "Status": 200,
                        "HasError": False,
                    },
                    status=status.HTTP_200_OK,
                )

            return Response(
                {
                    "Message": "Failed to Update User",
                    "Result": serializer.errors,
                    "Status": 400,
                    "HasError": True,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except LoginSignUp.DoesNotExist:
            return Response(
                {
                    "Message": "User Not Found",
                    "Result": None,
                    "Status": 404,
                    "HasError": True,
                },
                status=status.HTTP_404_NOT_FOUND,
            )


class DeleteUserView(generics.GenericAPIView):
    def delete(self, request, id, *args, **kwargs):
        """
        Delete a user record by ID.
        """
        try:
            # Fetch the user
            user = LoginSignUp.objects.get(id=id)

            # Delete the user (appointments will be deleted due to CASCADE)
            user.delete()

            return Response(
                {
                    "Message": "User Deleted Successfully",
                    "Result": None,
                    "Status": 200,
                    "HasError": False,
                },
                status=status.HTTP_200_OK,
            )
        except LoginSignUp.DoesNotExist:
            return Response(
                {
                    "Message": "User Not Found",
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
                    "Message": "Failed to Delete User",
                    "Result": str(e),
                    "Status": 400,
                    "HasError": True,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )