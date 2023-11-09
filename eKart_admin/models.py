from django.db import models

# Create your models here.

class EkartAdmin (models.Model):
    username = models.CharField(max_length = 30)
    password = models.CharField(max_length = 20)

    class Meta :
        db_table = 'admin_tbl'

class Category(models.Model):
    category_name = models.CharField(max_length = 30)
    description = models.CharField(max_length = 200)
    cover_picture = models.ImageField( upload_to = 'category/' )    

    class Meta:
        db_table = 'category_tb'    