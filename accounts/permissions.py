from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):

    def has_permission(self, request, view):

        return request.user.profile.role == 'admin'


class IsManager(BasePermission):

    def has_permission(self, request, view):

        return request.user.profile.role == 'manager'


class IsSales(BasePermission):

    def has_permission(self, request, view):

        return request.user.profile.role == 'sales'