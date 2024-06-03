from django.contrib import admin

# Register your models here.
from .models import Product, Customer, Transaction,Store

admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Transaction)
admin.site.register(Transaction)
