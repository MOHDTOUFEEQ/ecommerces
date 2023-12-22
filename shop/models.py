from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    prod_id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=50,default='')
    subcategory = models.CharField(max_length=50, default='')
    prod_name = models.CharField(max_length=50)
    price = models.IntegerField()
    prod_desc = models.CharField(max_length=300)
    pub_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to="shop/images",default='')
    def __str__(self):
        return self.prod_name

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    price = models.IntegerField()
    image = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    

class UserAddress(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    house = models.CharField(max_length=50)
    postalcode = models.CharField(max_length=20)
    zip = models.CharField(max_length=10)
    message_to_seller = models.TextField(blank=True)