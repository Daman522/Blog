from django.contrib import admin
from .views import *
from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static
from myapp.views import *


urlpatterns = [
    path('', home, name='home'),
     path('/base', base, name='base'),
    path('/login', Login.as_view(), name='login'),
    path('/register', Register.as_view(), name='register'),
    path('/logout', Logout.as_view(), name='logout'),
    path('/addpost', addpost, name='addpost'),
    path('/allpost', allpost, name='allpost'),
    path('/viewpost/<int:id>', viewpost, name='viewpost'),
    path('/updatepost/<int:id>', updatepost, name='updatepost'),
    path('/deletepost/<int:id>', deletepost, name="deletepost"),
    path('/stripe', stripe, name="stripe"),
    path('/design', design, name="design"),
    # path('/home', home, name="home"),

]
