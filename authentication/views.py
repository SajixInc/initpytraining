from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from genericresponse import GenericResponse 
import logging
from django.contrib.auth.hashers import make_password
from .models import SignupCredentials
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required


# def signup_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         print("Happy New Year")
#         password = request.POST['password']
#         email = request.POST['email']

#         if User.objects.filter(username=username).exists():
#             print("Inside If")
#             # response = GenericResponse("Message", "Result", "Status", "HasError")
#             # response.Message = "Username already exists"
#             # response.Result = serializer_class.data
#             # response.Status = 200
#             # response.HasError = False
#             # jsonStr = json.dumps(response.__dict__)
#             # return Response(json.loads(jsonStr), status=200) 
#             messages.success(request, 'Signup successful')
#             print(f"Messages in session after signup: {list(messages.get_messages(request))}")
#             return render(request, 'signup.html')  # Re-render the signup page with the error

#         else:
#             print("Inside else")
#             user = User.objects.create_user(username, email, password)
#             user.save()
#             messages.success(request, 'Signup successful')  # Add success message
#             return redirect('/auth/login/')  # Redirect to login page

#     return render(request, 'signup.html')  # Ensure GET request renders the signup page





logger = logging.getLogger(__name__)

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        # Check if the username or email already exists in SignupCredentials
        if SignupCredentials.objects.filter(username=username).exists():
            logger.info(f"Signup attempt failed: Username '{username}' already exists.")
            messages.error(request, 'Username already exists. Please choose a different one.')
            return render(request, 'signup.html')  # Re-render the signup page with the error message

        if SignupCredentials.objects.filter(email=email).exists():
            logger.info(f"Signup attempt failed: Email '{email}' already exists.")
            messages.error(request, 'Email already exists. Please choose a different one.')
            return render(request, 'signup.html')  # Re-render the signup page with the error message

        else:
            # Hash the password before saving it
            # hashed_password = make_password(password)

            # Save the signup credentials in SignupCredentials table
            SignupCredentials.objects.create(username=username, email=email, password=password)

            logger.info(f"User '{username}' created successfully in SignupCredentials.")
            messages.success(request, 'Signup successful! Please log in.')
            return redirect('/auth/login/')  # Redirect to login page after successful signup

    else:
        logger.debug("Rendering signup page (GET request).")
        return render(request, 'signup.html')  # Render signup page for GET requests




def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            # Check if the user exists and verify the password manually
            user = SignupCredentials.objects.get(username=username)
            if user.password == password:  # Compare the plain-text password
                request.session['user_id'] = user.id  # Simulate a login session
                messages.success(request, 'Welcome to Lifeeazy!')
                logger.info(f"User '{username}' logged in successfully.")
                return redirect('/welcome/')  # Redirect to the welcome page
            else:
                logger.warning(f"Invalid credentials for username: {username}")
                messages.error(request, 'Invalid credentials. Please try again.')
        except SignupCredentials.DoesNotExist:
            logger.warning(f"Login attempt with non-existent username: {username}")
            messages.error(request, 'Invalid credentials. Please try again.')

    return render(request, 'login.html')  # Render login page for GET or invalid credentials




def welcome_view(request):
    return render(request, 'welcome.html') #, {'message': 'Welcome to Lifeeazy!'})



def logout_view(request):
    logout(request)
    return redirect('/auth/login/')

@login_required
def delete_account_view(request):
    logger.debug(f"Request method: {request.method}")
    logger.debug(f"Logged-in user: {request.user}")
    logger.debug(f"Is user authenticated? {request.user.is_authenticated}")
    logger.debug(f"Session Key: {request.session.session_key}")

    if request.method == 'POST':
        print("hhagsdhsjdhgdh")
        try:
            print("hhagsdhsjdhgdh")
            username = request.user.username
            print("hhagsdhsjdhgdh")
            logger.debug(f"Attempting to delete account for username: {username}")

            # Fetch the account from the database
            account = SignupCredentials.objects.get(username=username)
            logger.debug(f"Account found: {account}")
            print (account,"iahdgdhhsjhs")

            # Delete the account
            account.delete()
            print("hyshjaudhsgahs")
            logger.info(f"Account for username '{username}' deleted successfully.")

            # Log the user out
            logout(request)
            messages.success(request, "Your account has been deleted successfully.")
            return redirect('/auth/signup/')
        except SignupCredentials.DoesNotExist:
            logger.error(f"No account found for username: {username}")
            messages.error(request, "Account not found.")
            return redirect('/welcome/')
    else:
        logger.debug("Invalid request method for account deletion.")
        messages.error(request, "Invalid request.")
        return redirect('/welcome/')




