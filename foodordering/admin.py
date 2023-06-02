from django.contrib import admin
from .models import User, Item, Store, Order
# Register your models here.
admin.site.register([User, Item, Store, Order])