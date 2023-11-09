from django.db import models

from customer.models import Seller
from eKart_admin.models import Category

# Create your models here.

class Product(models.Model):
    product_no = models.CharField(max_length = 20)
    product_name = models.CharField(max_length = 50)
    product_category = models.ForeignKey(Category,on_delete = models.CASCADE)
    description = models.CharField(max_length = 50)
    stock = models.IntegerField()
    price = models.FloatField()
    image = models.ImageField(upload_to= 'product/')
    seller = models.ForeignKey(Seller,on_delete = models.CASCADE)
    status = models. CharField(max_length = 20,default = 'available')

    class Meta:
        db_table = 'product_tb'

