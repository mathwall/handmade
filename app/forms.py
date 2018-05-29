from django import forms
from django.contrib.admin import widgets
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Profile, Product, Category, Bid

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'photo', 'text')

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('photo', 'description', 'street', 'postal_code', 'city', 'country')

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category', 'title', 'photo', 'description', 'start_date_of_sale', 'end_date_of_sale', 'starting_price', 'min_bid', 'immediate_price')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_date_of_sale'].widget.attrs.update({'class': 'datepicker'})
        self.fields['end_date_of_sale'].widget.attrs.update({'class': 'datepicker'})

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('__all__')

class SearchForm(forms.Form):
    name = forms.CharField(label='Product', required=False)
    # category = forms.ChoiceField(choices=Category.objects.values_list('name'))
    price = forms.IntegerField(required=False)
    type_of_purchase = forms.ChoiceField(choices=(
        ('all', 'All'),
        ('imm', 'Immediate purchase'),
        ('bid', 'Bid'),
    ), required=False)
    start_date_of_sale = forms.DateField(required=False, widget = forms.TextInput(attrs= { 'class':'datepicker'}))
    end_date_of_sale = forms.DateField(required=False, widget = forms.TextInput(attrs= { 'class':'datepicker'}))

class BiddingForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ('bid_amount', )