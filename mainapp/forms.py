from django import forms
from .models import Entry, SubCategory, Category, Payment

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ('transaction_date', 'desc', 'types', 'category', 'subcategory', 'amount', 'payment')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['category'].queryset = Category.objects.none()
        
        if 'types' in self.data:

            try:
                types_id = int(self.data.get('types'))
                print(types_id,'ype of type')
                self.fields['category'].queryset = Category.objects.filter(parent_type_name_id=types_id)
            
            except (ValueError, TypeError):
                pass # print('error')#pass # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
                self.fields['types'].queryset = self.instance.types.category_set




        self.fields['subcategory'].queryset = SubCategory.objects.none()
        
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                print(category_id)
                self.fields['subcategory'].queryset = SubCategory.objects.filter(parent_category_name_id=category_id)
            except (ValueError, TypeError):
                pass # print('error')#pass # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
                self.fields['subcategory'].queryset = self.instance.category.subcategory_set

        
        
        self.fields['payment'].queryset = Payment.objects.none()
        if 'types' in self.data:
            
            try:
                types_id = int(self.data.get('types'))
                self.fields['payment'].queryset = Payment.objects.filter(parent_type_name_id=types_id)
            
            except (ValueError, TypeError):
                pass # print('error')#pass # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
                self.fields['payment'].queryset = self.instance.types.payment_set
                