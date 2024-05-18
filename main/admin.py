from django.contrib import admin
from .models import *

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductVideo)
admin.site.register(Enter)
admin.site.register(Out)
admin.site.register(Order)
admin.site.register(OrderProduct)