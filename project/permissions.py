from rest_framework.permissions import BasePermission


class IsAdminAuthenticated(BasePermission):
    """permission personnalisée qui limite l'accès aux utilisateur de type admin et connecté"""

    def has_permission(self, request, view) -> bool:
        """doit retourner un booléen suivant si l'accès est permis ou non"""

        # Ne donnons l’accès qu’aux utilisateurs administrateurs authentifiés
        return bool(
            request.user and request.user.is_authenticated and request.user.is_superuser
        )


class IsStaffAuthenticated(BasePermission):
    """permission personnalisée qui limite l'accès aux utilisateur de type admin et connecté"""

    def has_permission(self, request, view) -> bool:
        """doit retourner un booléen suivant si l'accès est permis ou non"""

        # Ne donnons l’accès qu’aux utilisateurs administrateurs authentifiés
        return bool(
            request.user and request.user.is_authenticated and request.user.is_staff
        )

class IsOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # Cette méthode vérifie la permission pour l'accès à la vue (par exemple, la liste des objets).
        return True  # Vous pouvez personnaliser cette logique selon vos besoins.

    def has_object_permission(self, request, view, obj):
        # Cette méthode vérifie la permission pour les opérations sur un objet individuel (par exemple, update et destroy).
        # Vérifie si l'utilisateur connecté est le propriétaire de l'objet.
        return obj.username == request.user.username