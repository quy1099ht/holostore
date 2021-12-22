from django.db import models
from django.db.models.fields import FloatField

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    tag = models.CharField(max_length=225)
    price = models.FloatField()
    stock = models.IntegerField()
    description = models.CharField(max_length=2000)
    image_url = models.CharField(max_length=2083)

class Payment (models.Model):
    total_price = models.FloatField(default=0)
    username = models.CharField(max_length=1000,default="")
    datetime = models.DateTimeField()

class Offer(models.Model):
    code = models.CharField(max_length=225)
    Off_description = models.CharField(max_length=225)
    discount = models.FloatField()

class Customer(models.Model):
    username = models.CharField(max_length=225)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=255,default="")
    fullname = models.CharField(max_length=500,default="")
    birthday = models.DateTimeField(auto_now_add=True)
    gender = models.CharField(max_length=255,default="")
    address = models.CharField(max_length=500,default="")
    avatar_url = models.CharField(max_length=1000,default="")
    email = models.CharField(max_length=255)
    phone = models.IntegerField(default=0)
    zipcode = models.IntegerField(default=0)
    redeem_card = models.CharField(max_length=20,default="")


class Cart(models.Model):
    user = models.CharField(max_length=1000)
    price = models.FloatField()
    item = models.CharField(max_length=1000)
    quantity = models.IntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    img_url = models.CharField(max_length= 1000,default= "img/Featured/danchou_tshirt.png")

class Comment(models.Model):
    username = models.CharField(max_length=1000)
    product_name = models.CharField(max_length=1000)
    comment = models.CharField(max_length=1000)
    