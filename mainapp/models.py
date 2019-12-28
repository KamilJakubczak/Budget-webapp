from django.db import models
from datetime import datetime
# Create your models here.
class Type(models.Model):
    type_name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.type_name

class Category(models.Model):
    parent_type_name = models.ForeignKey(Type, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=30)

    def __str__(self):
        return self.category_name # (self.parent_type_name.type_name + ' - ' + self.category_name)

class SubCategory(models.Model):
    parent_category_name = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory_name = models.CharField(max_length=30)

    def __str__(self):
        return  self.subcategory_name #self.parent_category_name.category_name + ' - ' + self.subcategory_name

class Payment(models.Model):
    parent_type_name = models.ForeignKey(Type, on_delete=models.CASCADE)
    payment_name = models.CharField(max_length=30)

    def __str__(self):
        return ( self.payment_name) #self.parent_type_name.type_name + '-' + str(self.id) + '-' + self.payment_name)

class Entry(models.Model):
    added_date = models.DateField(auto_now_add=True)
    last_modification_date = models.DateField(auto_now = True)
    transaction_date = models.DateField(null=True, blank=True)
    desc = models.CharField(max_length=100)
    types = models.ForeignKey(Type,on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return (str(format_date(self.transaction_date)) + ' - ' + str(self.id) +' - '+ str(self.added_date) + ' - '+ str(self.desc)+ ' - ' + str(self.types)) + ' ' + str(self.payment)#+ ' - ' + caption(self.category.category_name) + ' - [' + str(self.amount)) 
        # + '] - ' + str(self.last_modification_date))

def caption(input):
    try:
        return str(input)
    except:
        return ' [-] '


def format_date(x):
    return x.strftime("%Y-%m-%d")