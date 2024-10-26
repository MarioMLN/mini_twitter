from django.urls import path, include
from feed.views import PostViewSet, FeedView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')

urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
    path('feed', FeedView.as_view(), name='feed')
]
