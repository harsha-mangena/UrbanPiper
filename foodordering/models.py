from .enums import userType, OrderStatus
from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken

class User(AbstractUser):
    """
    Model : User
    Choices :  Customer || Merchant
    """
    email = models.CharField(max_length=255, db_index = True, unique=True)
    name = models.CharField(max_length=100)
    user_type = models.CharField(max_length=8, choices=userType.choices(), default=userType.CUSTOMER)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    REQUIRED_FIELDS = ['email', 'name', 'user_type', 'is_active', ]

    def __str__(self) -> str:
        return self.username

    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            "refresh" : str(refresh),
            "access" : str(refresh.access_token)
        }

class Store(models.Model):
    """
    Model : Store
    Foreign Key : User, One or more stores can come under a single merchant. 
    """
    name = models.CharField(max_length=100)
    store_address = models.TextField("Store Address",blank=True, null=True)
    latitude = models.FloatField("Latitude", default=0, blank=True, null=True)
    longitude = models.FloatField("Longitude", default=0, blank=True, null=True)
    merchant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="stores")
    is_active = models.BooleanField("Active")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "stores"
    
class Item(models.Model):
    """
    Model : Item
    Foreign Key : With Stores, Store_Id || Item_Id, A store can have multiple items.
    """
    name = models.CharField(max_length=100)
    price = models.FloatField("Price")
    description = models.TextField("Description")
    is_active = models.BooleanField("Active")
    merchant = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ManyToManyField(Store)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "items"

class Order(models.Model):
    """
    Model : Order
    -> Each order is associated with the User(Customer).
    -> Each order can have one or N items.
    -> Each order is associated with the single store.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="store")
    items = models.ManyToManyField(Item, related_name="item")
    status = models.CharField(max_length=10, choices=OrderStatus.choices(), default=OrderStatus.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.pk





