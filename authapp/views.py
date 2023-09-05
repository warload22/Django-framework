from django.shortcuts import render, get_object_or_404
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.urls import reverse
from authapp.forms import PlayerLoginForm, PlayerRegisterForm, PlayerEditForm
from django.conf import settings
from django.core.mail import send_mail
from authapp.models import Player

from authapp.forms import PlayerProfileEditForm


def index(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('auth:login'))


def login(request):
    login_form = PlayerLoginForm(data=request.POST)
    if 'next' in request.GET.keys():
        next_value = request.GET['next']
    else:
        next_value = ''
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST.get('username')
        password = request.POST.get('password')

        player = auth.authenticate(username=username, password=password)
        if player and player.is_active:
            auth.login(request, player)
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])
            else:
                return HttpResponseRedirect(reverse('home'))
    context = {
        'title': 'login',
        'login_form': login_form,
        'next': next_value
    }
    return render(request, 'authapp/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('auth:login'))


def register(request):
    if request.method == 'POST':
        register_form = PlayerRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            new_user = register_form.save()
            send_verify_email(new_user)
            return HttpResponseRedirect(reverse('index'))
    else:
        register_form = PlayerRegisterForm()

    context = {
        'title': 'register',
        'register_form': register_form,
    }
    return render(request, 'authapp/register.html', context)


def edit(request):
    if request.method == 'POST':
        edit_form = PlayerEditForm(request.POST, request.FILES, instance=request.user)
        edit_profile_form = PlayerProfileEditForm(request.POST, instance=request.user.playerprofile)
        if edit_form.is_valid() and edit_profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('home'))
    else:
        edit_form = PlayerEditForm(instance=request.user)
        edit_profile_form = PlayerProfileEditForm(instance=request.user.playerprofile)

    context = {
        'title': 'edit',
        'edit_form': edit_form,
        'edit_profile_form': edit_profile_form
    }
    return render(request, 'authapp/edit.html', context)


def verify(request, email, key):
    user = get_object_or_404(Player, email=email)
    if user:
        if key == user.activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.activation_key = None
            user.activation_key_expires = None
            user.save()
            auth.login(request, user)
    return render(request, 'authapp/verify.html')


def send_verify_email(user):
    verify_link = reverse('authapp:verify', args=[user.email, user.activation_key])
    full_link = f'{settings.BASE_URL}{verify_link}'

    message = f'Your activation link: {full_link}'

    return send_mail(
        'Account activation',
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False
    )
