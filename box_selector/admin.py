from django.contrib import admin

from .models import Box, Product


admin.site.register(Product)
admin.site.register(Box)