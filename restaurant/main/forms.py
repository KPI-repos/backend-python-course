from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Dish, Order

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'role']
        
    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.strip():
            raise forms.ValidationError("Email cannot be empty")
        return email

class LoginForm(forms.Form):
    username = forms.CharField()  # Changed from email to username to match template
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    
    class Meta:
        model = User
        fields = ['name', 'email', 'password']
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ['name', 'price', 'description']
        
    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0:
            raise forms.ValidationError("Price must be positive")
        return price

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'dish', 'status']