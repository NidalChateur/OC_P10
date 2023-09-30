from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        """grant permissions to the list view (CREATE)"""
        return True

    def has_object_permission(self, request, view, obj):
        """grant permissions to the detail view (PUT, DELETE)"""

        try:
            # for projects, issues and comments
            return obj.author == request.user
        except AttributeError:
            # for contributors
            return obj.project.author == request.user
