from rest_framework import permissions


class AllowNone(permissions.BasePermission):
    """
    Allow nobody to access a view or object. We'll use per_object permissions
    on the views to check if a user is allowed to access.
    """

    def has_permission(self, request, view):
        """
        :returns: `False`
        """
        return False

    def has_object_permission(self, request, view, obj):
        """
        :returns: `False`
        """
        return False


class ModelPermission(permissions.IsAuthenticated):
    """
    Check for model permissions
    """

    def has_object_permission(self, request, view, obj):
        """
        Depending on :data:`rest_framework.permissions.SAFE_METHODS`, returns
        either the value of `obj.can_read()` or `obj.can_write()` if the
        respective method exists. Defaults to `False`.
        """
        if request.method in permissions.SAFE_METHODS:
            if hasattr(obj, 'can_read'):
                return obj.can_read(request.user)
        else:
            if hasattr(obj, 'can_write'):
                return obj.can_write(request.user)
        return False
