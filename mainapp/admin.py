from django.contrib import admin
from .models import SubCategory,Category,Entry,Type,Payment
# Register your models here.
admin.site.register(SubCategory)
admin.site.register(Category)
admin.site.register(Entry)
admin.site.register(Type)
admin.site.register(Payment)