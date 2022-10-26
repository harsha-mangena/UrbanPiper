from django.urls import path, include
from .view import UserRegistrationView, UserListView, MerchantListView, UserLoginView, StoreViewSet, ItemViewSet, UserLogout, OrderViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'items', ItemViewSet)
router.register(r'stores', StoreViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('users/', UserListView.as_view({'get' : 'list'}), name="users"),
    path('merchants/',MerchantListView.as_view({'get' : 'list'}), name="merchants"),
    path('register/', UserRegistrationView.as_view(), name="register"), 
    path('login/', UserLoginView.as_view(), name="login"),
    path('logout/', UserLogout, name="logout"),
    path('', include(router.urls)),
]

urlpatterns += router.urls

