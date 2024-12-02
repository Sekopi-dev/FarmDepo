from django import forms
from .models import ShippingAdd

class ShippingForm(forms.ModelForm):
    shipping_fullname = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Full Name'
    }))

    shipping_email = forms.EmailField(label="", required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email Address'
    }))
    shipping_address1 = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Address 1'
    }))
    shipping_address2 = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Address 2'
    }))
    shipping_city = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'City '
    }))
    shipping_province = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Province/State'
    }))
    shipping_code = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Code'
    }))
    shipping_country = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Country'
    }))

    class Meta:
        model = ShippingAdd
        fields = ['shipping_fullname','shipping_email', 'shipping_address1', 
                'shipping_address2', 'shipping_province', 'shipping_city', 'shipping_code', 'shipping_country']
        
        exclude = ['user',]


class paymentForm(forms.Form):
    card_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Name on Card',
        
    }), required=True)
    card_number = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Card Number'
    }), required=True)
    card_exp_date = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Card Expiration'
    }), required=True)
    card_cvv = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Card CVV'
    }),required=True)
    card_address = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Card Address'
    }), required=False)