from urllib import request
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from django.contrib.auth import get_user_model

from authentication.serializers import (
    UserSerializer,
    UserNoPasswordSerializer,
    AdminUserSerializer,
)
from authentication.permissions import IsOwnerOrReadOnly, IsAdminAuthenticated


class UserViewset(ModelViewSet):
    serializer_class = UserNoPasswordSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = get_user_model().objects.filter(
            can_data_be_shared=True, is_active=True
        )
        # queryset = get_user_model().objects.all()
        username = self.request.GET.get("username")
        if username:
            queryset = queryset.filter(username=username)

        return queryset


class AdminUserViewset(ModelViewSet):
    serializer_class = AdminUserSerializer
    permission_classes = [IsAdminAuthenticated]

    def get_queryset(self):
        queryset = get_user_model().objects.all()
        username = self.request.GET.get("username")
        if username:
            queryset = queryset.filter(username=username)

        return queryset
