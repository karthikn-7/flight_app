from django.urls import path
from .views import *


urlpatterns = [
    path('login/',login_view,name="login"),
    path('signup/',signup_view,name="signup"),
    path('logout/',user_logout,name="logout"),
    path('home/',user_home,name='user_home')
]
