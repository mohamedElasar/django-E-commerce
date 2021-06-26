from django.db import models
from django.conf import settings

# Create your models here.

class Item(models.Model):
    """(Item description)"""
    title = models.CharField(max_length=100)
    price = models.FloatField()
    def __str__(self):
        return self.title


class OrderItem(models.Model):
    item = models.ForeignKey(Item,on_delete = models.CASCADE)

    def __str__(self):
        return self.title



class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE)
    ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add = True)
    ordered_date = models.DateTimeField() # we manually set this value the moment it is ordered
    def __str__(self):
        return self.title
