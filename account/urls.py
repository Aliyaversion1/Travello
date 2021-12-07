from django.contrib.auth.views import LogoutView
from django.urls import path

from account.views import *

urlpatterns = [
    path('sign_up/', RegisterView.as_view(), name='register'),
    path('login/', SignInView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', profile, name='profile'),
    path('favourite/<int:pk>/', favourite_add, name='favourite-add'),
    path('profile/favourites/', favourite_list, name='favourite-list')
]