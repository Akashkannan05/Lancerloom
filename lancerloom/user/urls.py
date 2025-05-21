from django.urls import path
from . import views

urlpatterns=[
    path('login/',views.LoginClass,name="Login"),
    path('signup/',views.SignupClass,name="signup"),
    path('forgetPassword/',views.ForgetPasswordClass),
    path('verifyOtp/',views.verifyOtpClass),
    path('sendEmail/',views.SendEmailClass),
]