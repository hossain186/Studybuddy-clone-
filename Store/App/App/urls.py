
from django.contrib import admin
from django.urls import path
from home.views import *

urlpatterns = [

    path('login/' ,loginRoom, name="login"),
    path('logout/' ,logoutuser, name="logout"),
    path('register/' ,registerpage, name="register"),
    path('admin/', admin.site.urls),
    path('' ,home , name="home"),
    path('room/<str:pk>' , room , name="room"),
    path('createroom' , createroom, name='createroom'),
    path('updateroom/<str:pk>/', updateRoom , name='updateroom'),
    path('deleteroom/<str:pk>/' , deleteroom , name="deleteroom")
]
