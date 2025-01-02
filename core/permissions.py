from rest_framework.permissions import BasePermission

class HasRole(BasePermission):
    """
    Allows access only to users with a specific role.
    """
    def __init__(self, role):
        self.role = role

    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'role', None) == self.role

class IsAdmin(HasRole):
    """
    Allows access only to admin users.
    """
    def __init__(self):
        super().__init__('Admin')

class IsDesigner(HasRole):
    """
    Allows access only to designer users.
    """
    def __init__(self):
        super().__init__('Designer')

class IsReviewer(HasRole):
    """
    Allows access only to reviewer users.
    """
    def __init__(self):
        super().__init__('Reviewer')
