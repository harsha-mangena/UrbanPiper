from .models import User, Item, Store 

from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics, status 
from .serializers import RegisterUserSerializer, UserSerializer, LoginUserSerializer, StoreSerializer, ItemSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.reverse import reverse_lazy
from rest_framework import viewsets
from django.contrib.auth import authenticate, login
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
import structlog

log = structlog.get_logger()



'''
Type : GET
View for Listing all the user
'''
class UserListView(viewsets.ReadOnlyModelViewSet):
    """
    View for listing all the user
    """
    log.info("Extracting the customers list")
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
    log.info("Extracting the merchants list")
    queryset = User.objects.filter(user_type="Merchant")
    serializer_class = UserSerializer


'''
Type : POST
Registering new user.
'''
class UserRegistrationView(APIView):
    log.info("Registering new user into the system")
    serializer_class = RegisterUserSerializer
    authentication_classes = [JWTAuthentication,]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save()
            log.msg("% details are validated and being saved".format(serializer.data['username']))

            status_code = status.HTTP_201_CREATED
            response = {
                "message" : "Created successfully",
                "user" : serializer.data
            }

            return Response(response, status=status_code)
        

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''
Type : POST
Logging in existing user.
'''
class UserLoginView(APIView):
    serializer_class = LoginUserSerializer
    authentication_classes = [JWTAuthentication,]


    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            log.msg("%s : logging into the system".format(request.data['username']))

            username = request.data['username']
            password = request.data['password']
            user = authenticate(username=username, password=password)
            login(request, user)

            log.msg("%s : logged into the system".format(request.data['username']))


            response = {
                'message': 'User logged in successfully',
                'access': serializer.data['access'],
                'refresh': serializer.data['refresh'],
                }

            return Response(response, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''
Type : GET
Logging out current user.
'''
@api_view(["GET"])
@permission_classes([AllowAny])
def UserLogout(request):
    request.session.flush()
    return Response(status=status.HTTP_200_OK)


class ItemViewSet(viewsets.ModelViewSet):
    """
    API view to perform CRUD operations on Item
    """
    authentication_classes = [JWTAuthentication,]
    serializer_class = ItemSerializer
    queryset = Item.objects.select_related('stores').all()

    def create(self, request, *args, **kwargs):

        log.msg("Creating new Item", req = request.data)

        response = super().create(request, *args, **kwargs)
        return response

class StoreViewSet(viewsets.ModelViewSet):
    """
    API view to perform CRUD operations on Store
    """
    log.info("Listing all avaliable stores")
    authentication_classes = [JWTAuthentication,]
    serializer_class = StoreSerializer
    queryset = Store.objects.select_related(
        'merchant')

    def create(self, request, *args, **kwargs):

        log.msg("Creating new store", req=request.data)

        response = super().create(request, *args, **kwargs)
        return response