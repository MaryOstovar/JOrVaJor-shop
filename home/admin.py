from django.contrib import admin
from home.models import Product, Category, Comment


# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Comment)