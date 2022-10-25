from django.contrib import admin
from .models import User, Item, Store
# Register your models here.
admin.site.register([User, Item, Store])