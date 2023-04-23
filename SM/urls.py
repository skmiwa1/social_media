from django.urls import path, include
from rest_framework import routers

from SM.views import PostViewSet

router = routers.DefaultRouter()
router.register("posts", PostViewSet)


app_name = "SM"

urlpatterns = [
    path("", include(router.urls)),
]