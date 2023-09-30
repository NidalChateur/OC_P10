from django.urls import path, include
from rest_framework import routers

from authentication.views import (
    UserViewset,
    AdminUserViewset,
    ChangePasswordView,
)


router = routers.SimpleRouter()
router.register("user", UserViewset, basename="user")
router.register("admin/user", AdminUserViewset, basename="admin-user")


urlpatterns = [
    path("api/", include(router.urls)),
    path("api/change-password/", ChangePasswordView.as_view(), name="change-password"),
]
