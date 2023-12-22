from django.contrib import admin
from .models import Product , CartItem , UserAddress


admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(UserAddress)
