from urllib import request
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from django.contrib.auth import get_user_model

from authentication.serializers import (
    # UserSerializer,
    UserNoPasswordSerializer,
    AdminUserSerializer,
)
from authentication.permissions import IsOwnerOrReadOnly, IsAdminAuthenticated


<<<<<<< HEAD
class MultipleSerializerMixin:
    """select detail_serializer if the user selects the detail view"""

    detail_serializer_class = None

    def get_serializer_class(self):
        # retrieve means detail
        if self.action == "retrieve" and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


# créer un serializer list et serializer detail
class UserViewset(ReadOnlyModelViewSet):
    serializer_class = SignUpSerializer
    detail_serializer_class = None
    permission_classes = []

    def get_queryset(self):
        return get_user_model().objects.filter(can_be_shared=True)
=======
class UserViewset(ModelViewSet):
    serializer_class = UserNoPasswordSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        # queryset = get_user_model().objects.all()
        # return queryset
        queryset = get_user_model().objects.filter(
            can_data_be_shared=True, is_active=True
        )
        # queryset = get_user_model().objects.all()

        # filter the queryset with the "username" argument in the url
        # http://127.0.0.1:8000/api/user/?username=alpha
        username = self.request.GET.get("username")
        if username:
            queryset = queryset.filter(username=username)

        return queryset


class AdminUserViewset(ModelViewSet):
    serializer_class = AdminUserSerializer
    permission_classes = [IsAdminAuthenticated]

    def get_queryset(self):
        queryset = get_user_model().objects.all()

        # filter the queryset with the "username" argument in the url
        # http://127.0.0.1:8000/api/user/?username=alpha
        username = self.request.GET.get("username")
        if username:
            queryset = queryset.filter(username=username)

        return queryset
>>>>>>> dev2
