from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User, Group
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import redirect, reverse
from .forms import SignUpForm, MyUserProfile


class SignUp(CreateView):
    model = User
    form_class = SignUpForm
    success_url = '/accounts/login'

    template_name = 'registration/signup.html'


# class UserProfile(LoginRequiredMixin, UpdateView):
class UserProfile(UpdateView):
    permission_required = ('auth.change_user',)
    form_class = MyUserProfile
    model = User
    # success_url = '/accounts/{{ user.id }}' # тут нарываемся на 405 ошибкe - сервер запрещает влоб менять email
    template_name = 'profile.html'
    context_object_name = 'user'

    # Метод get_context_data позволяет нам изменить набор данных,
    # который будет передан в шаблон.
    def get_context_data(self, **kwargs):
        # получим объект пользователя
        user = super().get_object()
        # print(f'user={user}')
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим признак того, что user входит в группу authors
        # группа автора
        # authors=Group.objects.get(name="authors")
        if user.groups.filter(name='authors').exists():
            context['author'] = True
        else:
            context['author'] = False
        return context

    def form_valid(self, form):
        print(type(form))
        user = form.save(commit=False)
        # print(user)
        checked = form.cleaned_data['author']
        print(f'author = {checked}')
        if checked:
            authors = Group.objects.get(name="authors")
            user.groups.add(authors)
            print(f'added user {user}')
        return super().form_valid(form)

    def get_success_url(self):  # new
        pk = self.kwargs["pk"]
        return reverse("profile", kwargs={"pk": pk})  # здесь "profile" является именем паттерна в urls.py
        """
        accounts\\urls.py
        path('<int:pk>', UserProfile.as_view(), name='profile'),
        """

