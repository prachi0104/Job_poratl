from rest_framework import permissions

class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow HRs (staff) to edit or delete their own posts.
    """

    def has_permission(self, request, view):
        # Allow all users to view posts
        if request.method in permissions.SAFE_METHODS:
            return True
        # Only allow authenticated users to edit/delete posts
        return request.user.is_authenticated and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        # Allow all users to view posts
        if request.method in permissions.SAFE_METHODS:
            return True
        # Only allow staff (HRs) to edit/delete their own posts
        return request.user.is_staff and obj.hr == request.user
