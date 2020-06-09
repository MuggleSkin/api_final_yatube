from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path, include
from .views import PostViewSet, CommentViewSet, GroupView, FollowView


router = DefaultRouter()
router.register("posts", PostViewSet, basename="posts")
router.register(
    r"posts/(?P<post_id>\d+)/comments", CommentViewSet, basename="comments"
)

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("group/", GroupView.as_view(), name="groups"),
    path("follow/", FollowView.as_view(), name="groups"),
    path("", include(router.urls)),
]
