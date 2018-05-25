import operator
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.db import transaction
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.models import User
from .models import Post, Profile, Product
from .forms import PostForm, UserForm, ProfileForm, ProductForm, CategoryForm

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

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product, 'media_url': settings.MEDIA_URL})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products, 'media_url': settings.MEDIA_URL})

def my_products(request):
    products = Product.objects.filter(seller=request.user)
    return render(request, 'products/product_list.html', {'products': products, 'media_url': settings.MEDIA_URL})

def search_list(request):
    query = request.GET.get('q')
    queryset = Product.objects.all()
    print(query)
    if query:
        result = Product.objects.filter(Q(category__name__icontains=query) |
            Q(title__icontains=query) | 
                Q(description__icontains=query))
    else:
        result = ''
    return render(request, 'products/product_list.html', {'products': result, 'media_url': settings.MEDIA_URL})

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