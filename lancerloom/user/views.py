import random
import string
import json

from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
from django.contrib.auth import authenticate
# Create your views here.

from rest_framework.exceptions import ValidationError,NotFound
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics,views
from rest_framework import status

def generate_otp():
    otp=""
    for i in range(6):
        otp+=random.choice(string.digits)
    return otp

def verify_otp(email,otp):
    if cache.get(email)==otp:
        return True
    return False

def SendEmail(email):
    subject=f'This email is for verification'
    otp=generate_otp()
    cache.set(email,otp,60*5)
    print("________________>",otp)
    msg_text=f"The OTP for {email} is {otp}"
    msg_html=f"""
         <p><strong>Hi {email},</strong></p>
            <p>Your One-Time Password (OTP) for verification is:</p>
            <strong>{otp}</strong>
            <p>Please use this code to complete your verification. This OTP is valid for the next 5 minutes.</p>
            <p><strong>Do not share</strong> this code with anyone for your security.</p>
            <p>If you did not initiate this request, please contact our support team immediately.</p>
            <p>Best regards,</p>
            <strong>Lancerloom</strong>
            <p>Support Team</p>
        """
    email=EmailMultiAlternatives(subject,msg_text,"akash2005k26kaniyur12@gmail.com",[email])
    email.attach_alternative(msg_html,'text/html')
    email.send()

class SendEmailView(views.APIView):

    def post(self,requset):
        data=json.loads(self.request.body)
        email=data.get('email')
        purpose=data.get('purpose')

        if not email:
            raise ValidationError("All the fields are required.")
        
        if purpose=="forgetPassword":
            if not User.objects.filter(email=email).exists():
                raise ValidationError("An account with this email does not exists.")
        else:
            if User.objects.filter(email=email).exists():
                raise ValidationError("An account with this email already exists.")
        print("Purpose:_____",purpose)
        SendEmail(email)
        return Response({"message":"Mail Send"},status=status.HTTP_200_OK)
SendEmailClass=SendEmailView.as_view()

class verifyOtpView(views.APIView):

    def post(self,requset):
        data=json.loads(self.request.body)
        email=data.get("email")
        otp=data.get('otp')

        if not email or not otp:
            raise ValidationError("All the fields are required.")
        if cache.get('email') is None:
            raise ValidationError("You did not request for the otp")
        
        if verify_otp(email,otp):
            return Response({"otp":True},status=status.HTTP_200_OK)
        else:
            return Response({"otp":False},status=status.HTTP_406_NOT_ACCEPTABLE)
verifyOtpClass=verifyOtpView.as_view()

class SignupView(views.APIView):

    def post(self,request):
        data=json.loads(self.request.body)
        username=data.get('username')
        password=data.get('password')
        confirmPassword=data.get('confirmPassword')
        email=data.get('email')
        otp=data.get('otp')

        if not username or not password or not confirmPassword or not email or not otp:
            raise ValidationError("All the fields are required.")
        
        if User.objects.filter(email=email).exists():
            raise ValidationError("An account with this email already exists.")
        
        if User.objects.filter(username=username).exists():
            raise ValidationError("An account with this username already exists.")
        
        if password!=confirmPassword:
            raise ValidationError("Passwords do not match")
        
        if not verify_otp(email=email,otp=otp):
            raise ValidationError("Enter the valid otp")
        
        user=User(username=username,email=email)
        cache.delete(email)
        user.set_password(password)
        user.save()

        return Response({"message":"User created successfully"},status=status.HTTP_200_OK)
    
SignupClass=SignupView.as_view()

class LoginView(views.APIView):

    def post(self,request):
        data=json.loads(self.request.body)
        email=data.get('email')
        password=data.get('password')

        qs=User.objects.filter(email=email).first()
        if qs is None:
            raise NotFound("You dont have an account for thsi email")

        user = authenticate(username=qs.username, password=password)
        
        if not user:
             return Response({'message': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        token, created = Token.objects.get_or_create(user=user)
        return Response({'message':'success','token': token.key})
    
LoginClass=LoginView.as_view()

class ForgetPasswordView(views.APIView):

    def post(self,request):
        data=json.loads(self.request.body)
        password=data.get('password')
        confirmPassword=data.get('confirmPassword')
        email=data.get('email')
        otp=data.get('otp')

        if not password or not confirmPassword or not email or not otp:
            raise ValidationError("All the fields are required.")
        
        user=User.objects.filter(email=email).first()
        if user is None:
            raise ValidationError("Enter the valid email")
        
        if password!=confirmPassword:
            raise ValidationError("Passwords do not match")
        
        if not verify_otp(email=email,otp=otp):
            raise ValidationError("Enter the valid otp")
        
        user.set_password(password)
        cache.delete(email)
        return Response({"message":"Password changed successfully"},status=status.HTTP_200_OK)

ForgetPasswordClass=ForgetPasswordView.as_view()