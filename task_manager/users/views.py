from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from task_manager.users.models import User
from task_manager.users.forms import UserForm


class IndexView(ListView):
    model = User
    template_name = 'users/users.html'
    context_object_name = 'users'


class UserFormCreateView(SuccessMessageMixin, CreateView):
    form_class = UserForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('user_login')
    success_message = 'Пользователь успешно зарегистрирован'
    extra_context = {'button_name': 'Зарегистрировать'}


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin,
                     SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users_list')
    success_message = 'Пользователь успешно изменен'
    extra_context = {'button_name': 'Изменить'}
    login_url = reverse_lazy('user_login')

    def test_func(self):
        user = self.get_object()
        return self.request.user.id == user.id

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            url = reverse_lazy('users_list')
            message = 'У вас недостаточно прав, ' \
                      'чтобы редактировать другого пользователя'
        else:
            url = self.login_url
            message = 'Вы не авторизованы! Пожалуйста, выполните вход.'
        messages.warning(self.request, message)
        return redirect(url)

    def form_valid(self, form):
        form.save()
        username = self.request.POST['username']
        password = self.request.POST['password1']
        user = authenticate(self.request, username=username, password=password)
        login(self.request, user)
        messages.success(self.request, 'Пользователь успешно изменен')
        return redirect(self.success_url)


class UserDestroyView(LoginRequiredMixin, UserPassesTestMixin,
                      SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users_list')
    success_message = 'Пользователь успешно удален'
    extra_context = {'button_name': 'Да, удалить'}
    login_url = reverse_lazy('user_login')

    def test_func(self):
        user = self.get_object()
        return self.request.user.id == user.id

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            url = reverse_lazy('users_list')
            message = 'У вас недостаточно прав, ' \
                      'чтобы редактировать другого пользователя'
        else:
            url = self.login_url
            message = 'Вы не авторизованы! Пожалуйста, выполните вход.'
        messages.warning(self.request, message)
        return redirect(url)
