from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.db import transaction
from django.contrib.auth.models import User
from .models import Post, Profile
from .forms import PostForm, UserForm, ProfileForm

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'app/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'app/post_detail.html', {'post': post})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
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
        form = PostForm(request.POST, instance=post)
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

# TODO ajouter les messages de succès/erreur
# TODO gérer les erreurs de password en particulier
def signup(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
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
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    return render(request, 'registration/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

# TODO ajouter les messages de succès/erreur
@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()
            user.profile.street = profile_form.cleaned_data.get('street')
            user.profile.postal_code = profile_form.cleaned_data.get('postal_code')
            user.profile.city = profile_form.cleaned_data.get('city')
            user.profile.country = profile_form.cleaned_data.get('country')
            user.save()
            # messages.success(request, _('Your profile was successfully updated!'))
            return redirect('settings_profile')
        else:
            user_form = UserForm(instance=request.user)
            profile_form = ProfileForm(instance=request.user.profile)
            # messages.error(request, _('Please correct the error below'))
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
