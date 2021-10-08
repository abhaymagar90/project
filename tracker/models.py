from django.db import models
from django.utils import timezone
import datetime

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):    #returns name of item on reference
        return self.name

class Sub_category(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category , on_delete=models.CASCADE , default=True , null=False)
    def __str__(self):    #returns name of item on reference
        return self.name


class Item(models.Model):
    name=models.CharField(max_length=200,null=True)  #Item name
    category=models.ForeignKey(Category , on_delete=models.CASCADE , default=True , null=False)
    sub_category = models.ForeignKey(Sub_category  , on_delete=models.CASCADE , default=True , null=False)
    price=models.IntegerField(null= True)            #price name
    image=models.FileField(blank=True,null=True)     # image field
    created_at = models.DateField(auto_now_add=True ,  blank=True , null=True) #created time
    un = models.CharField(max_length=200,null=True) 

    def __str__(self):    #returns name of item on reference
        return self.name

