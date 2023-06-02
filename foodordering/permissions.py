from .models import User
from rest_framework import permissions
import structlog 
from .enums import userType

logger = structlog.get_logger(__name__)

class IsMerchant(permissions.BasePermission):
    def has_permission(self, request, view):
        """
        Checks if the current user has the permission to access a specific view.
        
        :param request: The request object to check.
        :type request: django.http.request.HttpRequest
        
        :param view: The view object to check.
        :type view: django.views.generic.base.View
        
        :return: True if the user has the required permission, False otherwise.
        :rtype: bool
        """
        current_user = User.objects.get(username=request.user.username)

        logger.info(event='Permissions !', user=current_user,
                     message='was trying to access something which requires IsMerchant Permission')

        return current_user and current_user.user_type == 'MERCHANT'

class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        """
        Check if the current user has the required permission to access the view.
        :param request: The current request.
        :param view: The view to be accessed.
        :return: True if the user has the required permission, False otherwise.
        """
        current_user = request.user

        logger.info(event='Permissions !', user=current_user,
                     message='was trying to access something which requires IsCustomer Permission')

        return current_user and current_user.user_type == userType.CUSTOMER


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        """
        Determines if the current user has permission to access a view based on their superuser status and 
        active status. 
        
        :param request: The request object containing the user attempting to access the view.
        :type request: django.http.request.HttpRequest
        :param view: The view the user is attempting to access.
        :type view: django.views.generic.View
        :return: True if the user is a superuser and is active, False otherwise.
        :rtype: bool
        """
        current_user = request.user 

        logger.info(event='Permissions !', user=current_user,
                     message='was trying to access something which requires Super User Permission')

        return current_user.is_superuser() and current_user.is_active()






