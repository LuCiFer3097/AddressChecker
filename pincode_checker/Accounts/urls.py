from django.urls import path, include

from .views import *

urlpatterns = [path('createUser/', CreateUser.as_view()),
               path('getAddress/', GetAddress.as_view()),
               path('getUsers/', getUsers.as_view()),
               #    path('addAddress/', CreateAddress.as_view()),
               ]
