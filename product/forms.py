from django import forms
from .models import Product,SalesRecord,StockMovement
from django.contrib.auth.models import User

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'




class SalesRecordForm(forms.ModelForm):
    class Meta:
        model = SalesRecord
        fields = ['product', 'quantity_sold', 'date', 'customer','sold_by']




class StockMovementForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ['product', 'quantity', 'reason']


