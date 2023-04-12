from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.utils.translation import gettext as _
from django.views.generic import TemplateView


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
    success_message = _('You are logged in')
    extra_context = {'button_name': _('Enter')}


class UserLogoutView(SuccessMessageMixin, LogoutView):
    """
    Class of displaying the Logout page.
    """
    def dispatch(self, request, *args, **kwargs):
        messages.add_message(request, messages.INFO,
                             _('You are logged out'))
        return super().dispatch(request, *args, **kwargs)
