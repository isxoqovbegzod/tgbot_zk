from django.contrib import admin
from users.models import User, Category, Product, Order, OrderProduct, Region, Branch


admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)