from django.urls import path
from android_rest.views import lists, loginandroid

urlpatterns = [
    path('lists', lists, name="lists"),
    path('loginandroid', loginandroid, name="loginandroid"),
]