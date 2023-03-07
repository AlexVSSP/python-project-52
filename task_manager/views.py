from django.shortcuts import render
# from django.views import View
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages

from task_manager.models import User
from task_manager.forms import UserForm


def index(request):
    return render(request, 'index.html')


class IndexView(ListView):
    model = User
    template_name = 'users.html'
    context_object_name = 'users'


class UserFormCreateView(SuccessMessageMixin, CreateView):
    form_class = UserForm
    template_name = 'create.html'
    success_url = reverse_lazy('user_login')
    success_message = 'Пользователь успешно зарегистрирован'
    extra_context = {'button_name': 'Зарегистрировать'}


class UserLoginView(SuccessMessageMixin, LoginView):
    # form_class = UserLogin
    template_name = 'login.html'
    # success_url = reverse_lazy('home')
    success_message = 'Вы залогинены'
    extra_context = {'button_name': 'Войти'}


class UserLogoutView(SuccessMessageMixin, LogoutView):

    def dispatch(self, request, *args, **kwargs):
        messages.add_message(request, messages.INFO, 'Вы разлогинены.')
        return super().dispatch(request, *args, **kwargs)


class UserUpdateView(SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'update.html'
    success_url = reverse_lazy('users_list')
    success_message = 'Пользователь успешно изменен'
    extra_context = {'button_name': 'Изменить'}


class UserDestroyView(SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'delete.html'
    success_url = reverse_lazy('users_list')
    success_message = 'Пользователь успешно удален'
    extra_context = {'button_name': 'Да, удалить'}
