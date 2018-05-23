from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Profile, Product

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text')

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('street', 'postal_code', 'city', 'country')

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('id_category', 'title', 'description', 'start_date_of_sale', 'starting_price', 'min_bid', 'immediate_price', 'end_date_of_sale')