from django.contrib.auth import authenticate, login
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from . tokens import password_reset_token
from . models import User
from . serializers import UserSerializer, CreateUserProfileSerializer

class UserListAPIView(ListAPIView):
    name = 'user_list'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = []
    permission_classes = []
    
class UserCreateAPIView(APIView):
    name = 'user_create'
    serializer_class = CreateUserProfileSerializer
    authentication_classes = []
    permission_classes = []
    
    def post(self, request):
        response = None
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        gender = request.data.get("gender")
        mobile_number = request.data.get("mobile_number")
        password = request.data.get("password")
        password_confirm = request.data.get("password2")
        
        if not mobile_number:
            return Response(
                {
                    "message": "Mobile number is required", 
                    "status": "failure"
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not password:
            return Response(
                {
                    "message": "Password is required", 
                    "status": "failure"
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not password_confirm:
            return Response(
                {
                    "message": "Password confirmation is required", 
                    "status": "failure"
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
            
        if not first_name:
            return Response(
                {
                    "message": "First name is required", 
                    "status": "failure"
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not last_name:
            return Response(
                {
                    "message": "Last name is required", 
                    "status": "failure"
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not gender:
            return Response(
                {
                    "message": "Gender is required", 
                    "status": "failure"
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        if password != password_confirm:
            return Response(
                {
                    "message": "Password mismatch", 
                    "status": "failure"
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user_exists = User.objects.get(mobile_number=mobile_number)
            
            if user_exists:
               return Response(
                    {
                        "message": "User with this mobile number exists",
                        "status": "failure"
                    }    
                )             
        except User.DoesNotExist:
            pass
            
        user_serializer = CreateUserProfileSerializer(data=request.data)
        
        if user_serializer.is_valid(raise_exception=True):
            user = user_serializer.save()
            
            response = Response(
                {
                    "message": "User created successfully",
                    "status": "success",
                    "errors": None
                }
            )
        else:
            error_list = []
            
            for key in user_serializer.errors:
                error_list.append(user_serializer.errors[key]) 
                
            response = Response(
                {
                    "message": "You have the following errors: ",
                    "status": "failure",
                    "errors": error_list
                }
            )
        
        return response
    
class LoginAPIView(APIView):
    name = 'login'
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        response = None
        mobile_number = request.data.get("username")
        password = request.data.get("password")
        
        if not mobile_number:
            return Response(
                {
                    "message": "Mobile number is required", 
                    "status": "failure"
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not password:
            return Response(
                {
                    "message": "Password is required", 
                    "status": "failure"
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = authenticate(mobile_number=mobile_number, password=password)
        
        if user:
            from datetime import date, now
            today = date.today()
            login(request, user)
            if user.email_verified:
                mail_subject = ' '.join(['Login Notification for', user.mobile_number])
                mail_context = {
                    'user': user,
                    'date': today.strftime("%A %d. %B %Y"),
                    'time': now().strftime("%I:%M %p"),
                    'user_agent': request.headers.get('user-agent'),
                    'ip_address': request.headers.get('remote_addr'),
                }
                message = render_to_string('user_auth/emails/login_notification_email.html', mail_context)
                to_email = user.email
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.content_subtype = 'html'
                email.send()
            response = Response(
                {
                    "token": user.auth_token.key, 
                    "status": "success", 
                    "message": "Login successful! Redirecting..."
                }
            )
        else:
            response = Response(
                {
                    "message": "Incorrect login credentials.", 
                    "status": "failure"
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        return response
    
class PasswordResetAPIView(APIView):
    name = 'reset_password'
    permission_classes = []
    authentication_classes = []
    
    def post(self, request):
        response = None
        to_email = request.data.get("email")
        mobile_number = request.data.get("mobile_number")
        
        if not email:
            return Response(
                {
                    "message": "Email is required", 
                    "status": "failure"
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not mobile_number:
            return Response(
                {
                    "message": "Mobile number is required", 
                    "status": "failure"
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(email=to_email, mobile_number=mobile_number)
        except User.DoesNotExist:
            user = None
        
        if user is not None:
            current_site = get_current_site(request)
            mail_subject = ' '.join(['Reset', 'Account Password for', user.mobile_number])
            mail_context = {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': password_reset_token.make_token(user),
                'app_name': settings.APP_NAME
            }
            message = render_to_string('user_auth/emails/reset_password_email.html', mail_context)
            to_email = email
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.content_subtype = 'html'
            email.send()
        
        response = Response(
                {
                    "status": "success", 
                    "message": "A password reset link has been sent to your email address"
                }
            )
        return response

    

    
