# posts/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PostViewSet,
    CommentViewSet,
    user_feed,
    like_post,
    unlike_post,
)

# Setting up the router for Post and Comment viewsets
router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

# Additional URL patterns for custom views
custom_urlpatterns = [
    path('feed/', user_feed, name='user_feed'),
    path('posts/<int:post_id>/like/', like_post, name='like_post'),
    path('posts/<int:post_id>/unlike/', unlike_post, name='unlike_post'),
]

# Combine router-generated URLs with custom ones
urlpatterns = [
    path('', include(router.urls)),
    *custom_urlpatterns,
]
