from urllib import request
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from django.contrib.auth import get_user_model

from authentication.serializers import UserSerializer
from authentication.permissions import IsOwnerOrReadOnly


class UserViewset(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = get_user_model().objects.filter(can_data_be_shared=True)
        # queryset = get_user_model().objects.all()
        username = self.request.GET.get("username")
        if username:
            queryset = queryset.filter(username=username)
        return queryset
