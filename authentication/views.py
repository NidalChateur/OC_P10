from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

from authentication.serializers import SignUpSerializer


class UserViewset(ModelViewSet):
    serializer_class = SignUpSerializer

    def get_queryset(self):
        return get_user_model().objects.all()

