from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        my_safe_methods = ['GET']
        if request.method in my_safe_methods:
            return True
        return obj.seller == request.user


class IsAdminOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        my_safe_methods = ['GET']
        if request.method in my_safe_methods:
            return True
        return request.user.is_staff
