from email.policy import default
from re import L
from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken
# Create your models here.

class User(AbstractUser):
    
    USER_TYPES = (
        ('Merchant', 'Merchant'),
        ('Customer', 'Customer')
    )

    email = models.CharField(max_length=255, db_index = True, unique=True)
    name = models.CharField(max_length=100)
    user_type = models.CharField(max_length=8, choices=USER_TYPES, default='Customer')
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    REQUIRED_FIELDS = ['email', 'user_type', 'is_active', ]

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
    merchant = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField("Active")
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return "{} : {}".format(self.merchant, self.name)

    class Meta:
        db_table = "stores"
        unique_together = ("merchant", "name", )
    
class Item(models.Model):
    """
    Model : Item
    Foreign Key : With Stores, Store_Id || Item_Id, A store can have multiple items.
    """
    name = models.CharField(max_length=100)
    price = models.FloatField("Price")
    description = models.TextField("Description")
    is_active = models.BooleanField("Active")
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return "{} : {}".format(self.store, self.name)

    class Meta:
        db_table = "items"
        unique_together = ("store", "name", )

class Order(models.Model):
    """
    Model : Order
    -> Each order is associated with the User(Customer).
    -> Each order can have one or N items.
    -> Each order is associated with the single or multiple stores.
    """

    ORDER_STAT = (
        ("Active", "Active"),
        ("Cancelled", "Cancelled"),
        ("Completed", "Completed")
    )

    merchant = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item, related_name="order")
    status = models.CharField(max_length=10, choices=ORDER_STAT, default="Active")
    created_at = models.DateTimeField(auto_now_add=True, null=True)





