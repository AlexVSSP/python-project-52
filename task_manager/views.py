# from django.contrib.auth import authenticate, login
from django.shortcuts import render
# from django.views import View
# from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
# from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
# from django.urls import reverse_lazy
from django.contrib import messages


def index(request):
    return render(request, 'index.html')


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'login.html'
    success_message = 'Вы залогинены'
    extra_context = {'button_name': 'Войти'}


class UserLogoutView(SuccessMessageMixin, LogoutView):

    def dispatch(self, request, *args, **kwargs):
        messages.add_message(request, messages.INFO, 'Вы разлогинены.')
        return super().dispatch(request, *args, **kwargs)
