from django.db import models

# Create your models here.
class Product(models.Model):
    pid=models.TextField()
    name=models.TextField()
    descri=models.TextField()
    price=models.IntegerField()
    off_price=models.IntegerField()
    stock=models.IntegerField()
    img=models.FileField()