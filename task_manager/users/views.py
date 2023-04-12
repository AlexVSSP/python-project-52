from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, \
    UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, \
    UpdateView, DeleteView
from django.utils.translation import gettext as _

from task_manager.users.models import User
from task_manager.users.forms import UserForm


class UsersView(ListView):
    """
    Class of user list display.
    """
    model = User
    template_name = 'users/users.html'
    context_object_name = 'users'


class UserFormCreateView(SuccessMessageMixin, CreateView):
    """
    Class of displaying the page for creating a new user.
    """
    form_class = UserForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('user_login')
    success_message = _('The user has been successfully registered')
    extra_context = {'button_name': _('Register')}


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin,
                     SuccessMessageMixin, UpdateView):
    """
    Class of displaying the page for editing a user.
    """
    model = User
    form_class = UserForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users_list')
    success_message = _('The user has been successfully updated')
    extra_context = {'button_name': _('To change')}
    login_url = reverse_lazy('user_login')

    def test_func(self):
        user = self.get_object()
        return self.request.user.id == user.id

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            url = reverse_lazy('users_list')
            message = _("You don't have enough rights "
                        "to edit another user")
        else:
            url = self.login_url
            message = _('You are not logged in! Please log in')
        messages.warning(self.request, message)
        return redirect(url)

    def form_valid(self, form):
        form.save()
        username = self.request.POST['username']
        password = self.request.POST['password1']
        user = authenticate(self.request,
                            username=username,
                            password=password)
        login(self.request, user)
        messages.success(self.request,
                         _('The user has been successfully updated'))
        return redirect(self.success_url)


class UserDestroyView(LoginRequiredMixin, UserPassesTestMixin,
                      SuccessMessageMixin, DeleteView):
    """
    Class of displaying the page for deletion a user.
    """
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users_list')
    extra_context = {'button_name': _('Yes, delete')}
    login_url = reverse_lazy('user_login')

    def test_func(self):
        user = self.get_object()
        return self.request.user.id == user.id

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            url = reverse_lazy('users_list')
            message = _("You don't have enough rights "
                        "to edit another user")
        else:
            url = self.login_url
            message = _('You are not logged in! Please log in')
        messages.warning(self.request, message)
        return redirect(url)

    def form_valid(self, form):
        try:
            self.object.delete()
            messages.success(self.request,
                             _('The user was successfully deleted'))
            return redirect(self.success_url)
        except ProtectedError:
            messages.warning(
                self.request,
                _('Unable to delete the user because it is being used'))
            return redirect(self.get_success_url())
