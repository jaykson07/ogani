from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['address', 'phone', 'note']
        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Delivery address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Order note', 'rows': 4}),
        }
