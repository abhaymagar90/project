from django.contrib import admin

# Register your models here.
from . models import Item
from .models import Category
from .models import Sub_category

admin.site.register(Item) #registering the model
admin.site.register(Category)
admin.site.register(Sub_category)
