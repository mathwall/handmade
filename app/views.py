import operator
import datetime
import json
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.db import transaction
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.models import User
from .models import Post, Profile, Product, Category, Bid
from .forms import PostForm, UserForm, ProfileForm, ProductForm, CategoryForm, SearchForm, BiddingForm

# BLOG

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'app/post_list.html', {'posts': posts, 'media_url': settings.MEDIA_URL})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'app/post_detail.html', {'post': post, 'media_url': settings.MEDIA_URL})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'app/post_edit.html', {'form': form})

# TODO trouver le moyen de concaténer les fonctions post_edit et post_new
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'app/post_edit.html', {'form': form})

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

# USERS

def signup(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()
            user.profile.street = profile_form.cleaned_data.get('street')
            user.profile.postal_code = profile_form.cleaned_data.get('postal_code')
            user.profile.city = profile_form.cleaned_data.get('city')
            user.profile.country = profile_form.cleaned_data.get('country')
            user.save()
            raw_password = user_form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('post_list')
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    return render(request, 'registration/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()
            user.profile.street = profile_form.cleaned_data.get('street')
            user.profile.postal_code = profile_form.cleaned_data.get('postal_code')
            user.profile.city = profile_form.cleaned_data.get('city')
            user.profile.country = profile_form.cleaned_data.get('country')
            user.save()
            raw_password = user_form.cleaned_data.get('password2')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            print('test')
            return redirect('product_list')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'registration/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

# TODO ajouter les messages de succès/erreur
@login_required
def delete_profile(request):
    request.user.delete()
    return redirect('post_list')

def users_list(request):
    users = User.objects.all()
    return render(request, 'products/users_list.html', {'users': users, 'media_url': settings.MEDIA_URL})


# PRODUCTS

@login_required
def product_new(request):
    if request.method == "POST":
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            product = product_form.save(commit=False)
            product.seller = request.user
            if(request.POST.get('starting_price')):
                product.current_price = request.POST.get('starting_price')
            if(request.POST.get('immediate_price')):
                product.current_price = request.POST.get('immediate_price')
            product.save()
            return redirect('product_detail', pk=product.pk)
    else:
        product_form = ProductForm()
    return render(request, 'products/product_edit.html', {
        'product_form': product_form
    })

@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product_form = ProductForm(request.POST, request.FILES, instance=product)
        if product_form.is_valid():
            product = product_form.save(commit=False)
            product.seller = request.user
            if(request.POST.get('immediate_price')):
                product.current_price = request.POST.get('immediate_price')
            product.save()
            return redirect('product_detail', pk=product.pk)
    else:
        product_form = ProductForm(instance=product)
    return render(request, 'products/product_edit.html', {
        'product_form': product_form
    })

@login_required
def product_remove(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('product_list')

def product_detail(request, pk, bid=None):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product, 'media_url': settings.MEDIA_URL, 'bid': bid})

def product_list(request, user=None):
    products = Product.objects.all()
    for product in products:
        if product.end_date_of_sale < datetime.date.today() and product.buyer:
            product.purchased = True
            product.save()
    search_form = SearchForm()    
    seller = None
    if(user != None):
        seller = get_object_or_404(User, pk=user)
        products = Product.objects.filter(seller=user, end_date_of_sale__gte=datetime.date.today(), start_date_of_sale__lte=datetime.date.today())
    else:
        products = Product.objects.filter(purchased=False, end_date_of_sale__gte=datetime.date.today(), start_date_of_sale__lte=datetime.date.today())
    return render(request, 'products/product_list.html', {'search_form': search_form, 'seller': seller, 'products': products, 'media_url': settings.MEDIA_URL})

def my_products(request):
    search_form = SearchForm()
    products = Product.objects.filter(seller=request.user)
    return render(request, 'products/product_list.html', {'search_form': search_form, 'products': products, 'media_url': settings.MEDIA_URL})

@login_required
def buy_now(request, product):
    product = get_object_or_404(Product, pk=product)
    product.buyer = request.user
    product.purchased = True
    product.save()
    success = "Thank you for your purchase :)"
    return render(request, 'products/product_detail.html', {'success': success, 'product': product, 'media_url': settings.MEDIA_URL})                

@login_required
def bidding(request, product):
    product = get_object_or_404(Product, pk=product)
    if request.method == "POST":
        bidding_form = BiddingForm(request.POST)
        if bidding_form.is_valid():
            if float(request.POST.get('bid_amount')) >= product.min_bid:
                # enregistrer l'enchère
                bid = bidding_form.save(commit=False)
                bid.product = product
                bid.user = request.user
                bid.save()
                # mettre à jour le current_price du produit
                product.current_price += bid.bid_amount
                product.buyer = request.user
                product.save()
                success = "Thank you, your bid has been taken into account"
                return render(request, 'products/bidding.html', {'bidding_form': bidding_form, 'success': success, 'product': product, 'media_url': settings.MEDIA_URL})
            else:
                error = "You must bid at least the minimum bid amount"
                return render(request, 'products/bidding.html', {'bidding_form': bidding_form, 'error': error, 'product': product, 'media_url': settings.MEDIA_URL})                
    else:
        bidding_form = BiddingForm()
    return render(request, 'products/bidding.html', {'bidding_form': bidding_form, 'product': product, 'media_url': settings.MEDIA_URL})

def purchase_history(request):
    search_form = SearchForm()    
    products = Product.objects.filter(buyer=request.user)
    return render(request, 'products/product_list.html', {'purchase_history': True, 'search_form': search_form, 'products': products, 'media_url': settings.MEDIA_URL})

def search_list(request):
    search_form = SearchForm()
    query = request.GET.get('q')
    queryset = Product.objects.all()
    print(query)
    if query:
        result = Product.objects.filter(Q(category__name__icontains=query) |
            Q(title__icontains=query) | 
                Q(description__icontains=query))
    else:
        result = ''
    return render(request, 'products/product_list.html', {'search_form': search_form, 'products': result, 'media_url': settings.MEDIA_URL})

def advanced_search(request):
    search_form = SearchForm(request.GET)
    result = Product.objects.all()
    if(request.GET.get('name') != ""):
        result = result.filter(
            title__icontains=request.GET.get('name')            
        )
    if(request.GET.get('price') != ""):
        result = result.filter(
            current_price__lte=request.GET.get('price')        
        )
    if(request.GET.get('type_of_purchase') == 'imm'):
        result = result.filter(
            immediate_price__gt=0
        )
    elif(request.GET.get('type_of_purchase') == 'bid'):
        result = result.filter(        
            starting_price__gt=0
        )
    if(request.GET.get('start_date_of_sale') != ""):
        result = result.filter(        
            start_date_of_sale__gte=request.GET.get('start_date_of_sale'),
        )
    if(request.GET.get('end_date_of_sale') != ""):
        result = result.filter(        
            end_date_of_sale__gte=request.GET.get('end_date_of_sale'),
        )
    return render(request, 'products/product_list.html', {'search_form': search_form, 'products': result, 'media_url': settings.MEDIA_URL})

# CATEGORIES

def category_new(request):
    if request.method == "POST":
        category_form = CategoryForm(request.POST)
        if category_form.is_valid():
            category = category_form.save(commit=False)
            category.save()
            return redirect('product_list')
    else:
        category_form = CategoryForm()
    return render(request, 'products/category_new.html', {
        'category_form': category_form
    })

def get_categories(request):
    print("it wooorks")
    if request.is_ajax():
        q = request.GET.get('term', '')
        categories = Category.objects.filter(name__icontains=q)
        results = []
        for categ in categories:
            cat_json = {}
            cat_json = categ.name
            results.append(cat_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)