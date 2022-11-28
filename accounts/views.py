from django.shortcuts import render

from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from django.views.generic import DetailView
from .forms import SignUpForm, UserProfile


class SignUp(CreateView):
    model = User
    form_class = SignUpForm
    success_url = '/accounts/login'

    template_name = 'registration/signup.html'


class UserProfile(DetailView):
    model = User
    form_class = UserProfile
    context_object_name = 'user'
    success_url = '/accounts/{{ user.id }}' # тут нарываемся на 405 ошибкe - сервер запрещает влоб менять email
    template_name = 'profile.html'
