from rest_framework.permissions import BasePermission


class IsAdminOrReadOnly(BasePermission):
    '''
    Allows manipulate only admin, or read nly
    '''

    def has_permission(self, request, view):
        user_accessible_only = 'GET'

        if request.method == user_accessible_only:
            return bool(request.user and request.user.is_authenticated)
        else:
            return bool(request.user and request.user.is_admin)