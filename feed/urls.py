from django.urls import path, include
from feed.views import LikesView, PostViewSet, FeedView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
    path('feed', FeedView.as_view(), name='feed'),
    path('post', PostViewSet.as_view(), name='post'),
    path('post/<int:pk>', PostViewSet.as_view(), name='post'),
    path('likes/<int:post_pk>', LikesView.as_view(), name='likes')
]
