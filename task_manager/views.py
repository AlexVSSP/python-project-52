# from django.contrib.auth import authenticate, login
# from django.shortcuts import render
# from django.views import View
# from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
# from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
# from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponse
from django.utils.translation import gettext as _
from django.views.generic import TemplateView

# def index(request):
#     """
#     Class of displaying the application's home page.
#     """
#     return render(request, 'index.html')


class IndexView(TemplateView):
    """
    Class of displaying the application's home page.
    """
    template_name = 'index.html'


class UserLoginView(SuccessMessageMixin, LoginView):
    """
    Class of displaying the Login page.
    """
    template_name = 'login.html'
    # success_message = 'Вы залогинены'
    success_message = _('You are logged in')
    # extra_context = {'button_name': 'Войти'}
    extra_context = {'button_name': _('Enter')}


class UserLogoutView(SuccessMessageMixin, LogoutView):
    """
    Class of displaying the Logout page.
    """
    def dispatch(self, request, *args, **kwargs):
        # messages.add_message(request, messages.INFO, 'Вы разлогинены')
        messages.add_message(request, messages.INFO, _('You are logged out'))
        return super().dispatch(request, *args, **kwargs)


def index(request):
    """
    Test function for checking rollbar
    """
    a = None
    a.hello()  # Creating an error with an invalid line of code
    return HttpResponse("Hello, world. You're at the pollapp index.")
