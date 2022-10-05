from django import forms
from customer.models import Customer


class FormSignUp(forms.ModelForm):

    customer_name = forms.CharField(max_length=200, label='Your Name', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Your Name',
        'id': 'yourName',
    }))

    username = forms.CharField(max_length=200, label='Username', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username',
        'id': 'yourUsername',
    }))

    email = forms.EmailField(label='Your Email', widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Your Email',
        'id': 'yourEmail',
    }))

    tel = forms.CharField(max_length=15, label='User Phone', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Your Phone',
        'id': 'yourPhone',
    }))

    address = forms.CharField(label='Address', widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Your Address',
        'rows': '3',
        'id': 'yourAddress',
    }))

    password = forms.CharField(max_length=100, label='Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password',
        'id': 'yourPassword',
    }))

    confirm_password = forms.CharField(max_length=100, label='Confirm Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm Password',
        'id': 'confirmyourPassword',
    }))

    class Meta:

        model = Customer
        fields = '__all__'
