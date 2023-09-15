from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

from authentication.serializers import SignUpSerializer


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
