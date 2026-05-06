from django import forms


class CheckoutForm(forms.Form):
    shipping_name    = forms.CharField(
        max_length=200,
        label='Full Name',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'John Doe'})
    )
    shipping_phone   = forms.CharField(
        max_length=20,
        label='Phone Number',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+91 XXXXX XXXXX'})
    )
    shipping_address = forms.CharField(
        label='Shipping Address',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'House No, Street, City, State, PIN'
        })
    )
