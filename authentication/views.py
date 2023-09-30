from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response


from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import get_user_model


from authentication.serializers import (
    UserListSerializer,
    UserDetailSerializer,
    AdminUserListSerializer,
    AdminUserDetailSerializer,
    ChangePasswordSerializer,
)
from authentication.permissions import IsOwnerOrReadOnly


class MultipleSerializerMixin:
    """use the detail_serializer if the user is viewing the detail view."""

    detail_serializer_class = None

    def get_serializer_class(self):
        # 'retrieve' and 'update' represent the detail view
        check_list = [
            self.action == "retrieve" or self.action == "update",
            self.detail_serializer_class is not None,
        ]
        if all(check_list):
            return self.detail_serializer_class
        return super().get_serializer_class()


class UserViewset(MultipleSerializerMixin, ModelViewSet):
    # UserListSerializer with password configuration
    serializer_class = UserListSerializer
    # UserDetailSerializer without password configuration
    detail_serializer_class = UserDetailSerializer
    # permission for the detail view
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = get_user_model().objects.filter(
            can_data_be_shared=True, is_active=True
        )

        if (
            self.request.user.is_authenticated
            and not self.request.user.can_data_be_shared
        ):
            """include the connected user to the queryset if he does not share his data"""

            user = self.request.user
            connected_user = get_user_model().objects.filter(id=user.id)
            queryset |= connected_user

        # filter the queryset with the "username" argument in the url
        # http://127.0.0.1:8000/api/user/?username=alpha
        username = self.request.GET.get("username")
        if username:
            queryset = queryset.filter(username=username)

        return queryset


class AdminUserViewset(MultipleSerializerMixin, ModelViewSet):
    serializer_class = AdminUserListSerializer
    detail_serializer_class = AdminUserDetailSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        queryset = get_user_model().objects.all()

        # filter the queryset with the "username" argument in the url
        # http://127.0.0.1:8000/api/user/?username=alpha
        username = self.request.GET.get("username")
        if username:
            queryset = queryset.filter(username=username)

        return queryset


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def put(self, request):
        # create a ChangePasswordSerializer() instance
        serializer = ChangePasswordSerializer(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            user = request.user
            new_password = serializer.validated_data["password"]
            user.set_password(new_password)
            user.save()

            update_session_auth_hash(request, user)

            return Response(
                {"detail": "Mot de passe modifié avec succès."},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
