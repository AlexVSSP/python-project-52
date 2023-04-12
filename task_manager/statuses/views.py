from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, \
    UpdateView, DeleteView
from django.utils.translation import gettext as _

from task_manager.statuses.models import Status
from task_manager.statuses.forms import StatusForm


class StatusesView(LoginRequiredMixin, ListView):
    """
    Class of status list display.
    """
    model = Status
    template_name = 'statuses/statuses.html'
    context_object_name = 'statuses'
    login_url = reverse_lazy('user_login')

    def handle_no_permission(self):
        message = _('You are not logged in! Please log in')
        messages.warning(self.request, message)
        return redirect(self.login_url)


class StatusFormCreateView(LoginRequiredMixin,
                           SuccessMessageMixin, CreateView):
    """
    Class of displaying the page for creating a new status.
    """
    form_class = StatusForm
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('statuses_list')
    success_message = _('The status was created successfully')
    extra_context = {'button_name': _('Create')}
    login_url = reverse_lazy('user_login')

    def handle_no_permission(self):
        message = _('You are not logged in!, Please log in')
        messages.warning(self.request, message)
        return redirect(self.login_url)


class StatusUpdateView(LoginRequiredMixin,
                       SuccessMessageMixin, UpdateView):
    """
    Class of displaying the page for editing a status.
    """
    model = Status
    form_class = StatusForm
    template_name = 'statuses/update.html'
    success_url = reverse_lazy('statuses_list')
    success_message = _('The status updated successfully')
    extra_context = {'button_name': _('To change')}
    login_url = reverse_lazy('user_login')

    def handle_no_permission(self):
        message = _('You are not logged in! Please log in')
        messages.warning(self.request, message)
        return redirect(self.login_url)


class StatusDestroyView(LoginRequiredMixin,
                        SuccessMessageMixin, DeleteView):
    """
    Class of displaying the page for deletion a status.
    """
    model = Status
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses_list')
    extra_context = {'button_name': _('Yes, delete')}
    login_url = reverse_lazy('user_login')

    def handle_no_permission(self):
        message = _('You are not logged in! Please log in')
        messages.warning(self.request, message)
        return redirect(self.login_url)

    def form_valid(self, form):
        try:
            self.object.delete()
            messages.success(self.request,
                             _('The status was successfully deleted'))
        except ProtectedError:
            messages.warning(self.request,
                             _('Unable to delete the status '
                               'because it is being used'))
        finally:
            return redirect(self.get_success_url())
