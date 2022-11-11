from .models import User
from rest_framework import permissions
import structlog 
from .enums import userType

logger = structlog.get_logger(__name__)

class IsMerchant(permissions.BasePermission):
    def has_permission(self, request, view):
        current_user = User.objects.get(username=request.user.username)

        logger.info(event='Permissions !', user=current_user,
                     message='was trying to access something which requires IsMerchant Permission')

        return current_user and current_user.user_type == 'MERCHANT'

class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        current_user = request.user

        logger.info(event='Permissions !', user=current_user,
                     message='was trying to access something which requires IsCustomer Permission')

        return current_user and current_user.user_type == userType.CUSTOMER


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        current_user = request.user 

        logger.info(event='Permissions !', user=current_user,
                     message='was trying to access something which requires Super User Permission')

        return current_user.is_superuser() and current_user.is_active()






