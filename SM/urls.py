from django.urls import path, include
from rest_framework import routers

from SM.views import PostViewSet, LikeViewSet

router = routers.DefaultRouter()
router.register("posts", PostViewSet)
router.register("likes", LikeViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "SM"
