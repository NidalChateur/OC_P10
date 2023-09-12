from django.urls import path, include
from rest_framework import routers

# vue permettant generic JWT permettant d'obtenir et de rafraîchir un token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from authentication.views import UserViewset

router = routers.SimpleRouter()
router.register("signup", UserViewset, basename="signup" )

urlpatterns = [
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include(router.urls)),
    # url to get a token
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # url to refresh a token
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
