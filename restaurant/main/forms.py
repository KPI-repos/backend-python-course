from django import forms
from .models import User, Dish, Order

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email']
        
    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.strip():
            raise forms.ValidationError("Email cannot be empty")
        return email

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