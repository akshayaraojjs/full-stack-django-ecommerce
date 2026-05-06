from django import forms
from .models import Product, ProductImage, Category


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'product_name', 'description', 'price', 'stock']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['category'].empty_label = 'Select a Category'


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image', 'is_primary']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs['class'] = 'form-control'
        self.fields['is_primary'].widget.attrs['class'] = 'form-check-input'
