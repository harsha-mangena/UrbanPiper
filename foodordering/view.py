from django.conf import settings
from .models import User, Item, Store, Order
from .tasks import create_store, create_order

from rest_framework.decorators import api_view, permission_classes
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsCustomer, IsMerchant, IsSuperUser
from rest_framework import generics, status 
from .serializers import RegisterUserSerializer, UserSerializer, LoginUserSerializer, StoreSerializer, ItemSerializer, OrderSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.reverse import reverse_lazy
from rest_framework import viewsets
from django.contrib.auth import authenticate, login
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
import structlog
import redis
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views.decorators.vary import vary_on_headers

log = structlog.get_logger(__name__)


# Redis Instance
redis_instance = redis.StrictRedis(host='127.0.0.1', port=9000, db="onboard")
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


'''
Type : GET
View for Listing all the user
'''
class UserListView(viewsets.ReadOnlyModelViewSet):
    """
    View for listing all the user
    """
    permission_classes = [IsAuthenticated, IsSuperUser, ]
    log.msg("Extracting the customers list")
    queryset = User.objects.filter(user_type="Customer")
    serializer_class = UserSerializer

'''
Type : GET
View for listing all the Merchant with name
'''
class MerchantListView(viewsets.ReadOnlyModelViewSet):
    """
    View for listing all the Merchant with name
    """
    permission_classes = [IsAuthenticated, IsSuperUser, ]
    log.msg("Extracting the merchants list")
    queryset = User.objects.filter(user_type="Merchant")
    serializer_class = UserSerializer

'''
Type : POST
Registering new user.
'''
class UserRegistrationView(APIView):
    serializer_class = RegisterUserSerializer
    authentication_classes = [JWTAuthentication,]
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save()
            status_code = status.HTTP_201_CREATED
            response = {
                "message" : "Created successfully",
                "user" : serializer.data
            }

            log.info(event='New User Registration ', user=request.user.username,
                         message='User Registration completed')

            return Response(response, status=status_code)
        

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''
Type : POST
Logging in existing user.
'''
class UserLoginView(APIView):
    serializer_class = LoginUserSerializer
    authentication_classes = [JWTAuthentication,]
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            username = request.data['username']
            password = request.data['password']
            user = authenticate(username=username, password=password)
            login(request, user)

            log.msg("{0} : logged into the system".format(request.data['username']))


            response = {
                'message': 'User logged in successfully',
                'access': serializer.data['access'],
                'refresh': serializer.data['refresh'],
                'user' : user.username
                }

            print(response)

            log.info(event='Exisiting User Login ', user=request.user.username,
                         message='Login Successful')

            return Response(response, status=status.HTTP_200_OK)


'''
Type : GET
Logging out current user.
'''
@api_view(["GET"])
@permission_classes([AllowAny,])
def UserLogout(request):
    request.session.flush()
    log.info(event = 'Logging out user')
    return Response(status=status.HTTP_200_OK)


'''
Type : POST || GET
Crud operations on the stores
'''
class StoreViewSet(viewsets.ModelViewSet):
    JWTAuthentication = (JWTAuthentication,)
    serializer_class = StoreSerializer
    permission_classes = [IsAuthenticated, IsMerchant, ]


    def get_queryset(self):
        return Store.objects.filter(merchant=self.request.user)
    
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            print(serializer.data)
            log.msg("Creating new store", req=serializer.data)
            pk = self.request.user.pk
            # import pdb ; pdb.set_trace()
            create_store(pk, serializer.data)

            response = {
                "message" : "Store created successfully",
                "Merchant" : self.request.user.username,
                "data" : serializer.data
            }

            return Response(response, status=status.HTTP_201_CREATED)
        
        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

    # @method_decorator(cache_page(CACHE_TTL))
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)

'''
Type : POST || GET
Crud operations on the Items
'''
class ItemViewSet(viewsets.ModelViewSet):

    log.msg("Listing all avaliable stores")
    JWTAuthentication = [JWTAuthentication,]
    permission_classes = [IsAuthenticated, IsMerchant]
    serializer_class = ItemSerializer
    
    # @method_decorator(cache_page(CACHE_TTL))
    def get_queryset(self):
        user = User.objects.filter(username=self.request.user.username).first()
        return Item.objects.filter(merchant=user)

    def create(self, request, *args, **kwargs):

        log.msg("Creating new Item", req = request.data)
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save(merchant=request.user)

            response = {
               'message' : 'item created successfully',
               'store' : serializer.data
            }

            return Response(response)

    # @method_decorator(cache_page(CACHE_TTL))
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)
        

'''
Type : POST || GET
Creating Order 
'''
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    JWTAuthentication = [JWTAuthentication,]
    permission_classes = [IsAuthenticated,]

    
    def get_queryset(self):
        user = User.objects.filter(username=self.request.user.username).first()
        return Order.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            log.msg("Creating_new_ store", req=serializer.data)
            pk = self.request.user.pk
            create_order.delay(pk, serializer.data)

            response = {
                "message" : "Order placed successfully",
                "User" : self.request.user.username,
                "data" : serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        
        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

    # @method_decorator(cache_page(CACHE_TTL))
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)