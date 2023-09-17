from django.urls import path, include
from rest_framework import routers

from authentication.views import UserViewset


router = routers.SimpleRouter()
router.register("user", UserViewset, basename="user")


urlpatterns = [
    path("api/", include(router.urls)),
]
