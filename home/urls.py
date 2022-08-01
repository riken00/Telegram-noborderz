
# from cgi import test
from django.contrib import admin
from django.urls import path, include
from home.views import application,login,testing,test
urlpatterns = [
    path('login/<str:number>',login.as_view()),
    path('testing/<str:otp>',testing.as_view()),
    path('application/<str:otp>',application.as_view()),
    path('test/',test.as_view())
]
