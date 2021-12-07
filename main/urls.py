from django.urls import path

from main.views import *

urlpatterns = [
    path('', HomePageView.as_view(), name='homepage'),
    path('search', HomePageView.as_view(), name='search'),
    path('category/<str:slug>/', CategoryDetailView.as_view(), name='category'),
    path('post-detail/<int:pk>/', post_single, name='post-detail'),
    path('add-post/', add_post, name='add-post'),
    path('update-post/<int:pk>/', update_post, name='update-post'),
    path('delete-post/<int:pk>/', delete_post, name='delete-post'),
    path('like/<int:pk>/', LikeView, name='like_post'),


]
