from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext as _


from task_manager.labels.forms import LabelForm
from task_manager.labels.models import Label


class LabelsView(LoginRequiredMixin, ListView):
    """
    Class of label list display.
    """
    model = Label
    template_name = 'labels/labels.html'
    context_object_name = 'labels'
    login_url = reverse_lazy('user_login')

    def handle_no_permission(self):
        # message = 'Вы не авторизованы! Пожалуйста, выполните вход'
        message = _('You are not logged in! Please log in')
        messages.warning(self.request, message)
        return redirect(self.login_url)


class LabelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Class of displaying the page for creating a new label.
    """
    model = Label
    form_class = LabelForm
    template_name = 'labels/create.html'
    success_url = reverse_lazy('labels_list')
    # success_message = 'Метка успешно создана'
    success_message = _('The label was created successfully')
    # extra_context = {'button_name': 'Создать'}
    extra_context = {'button_name': _('Create label')}
    login_url = reverse_lazy('user_login')

    def handle_no_permission(self):
        # message = 'Вы не авторизованы! Пожалуйста, выполните вход'
        message = _('You are not logged in! Please log in')
        messages.warning(self.request, message)
        return redirect(self.login_url)


class LabelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Class of displaying the page for editing a label.
    """
    model = Label
    form_class = LabelForm
    template_name = 'labels/update.html'
    success_url = reverse_lazy('labels_list')
    # success_message = 'Метка успешно изменена'
    success_message = _('The label updated successfully')
    # extra_context = {'button_name': 'Изменить'}
    extra_context = {'button_name': _('To change')}
    login_url = reverse_lazy('user_login')

    def handle_no_permission(self):
        # message = 'Вы не авторизованы! Пожалуйста, выполните вход'
        message = _('You are not logged in! Please log in')
        messages.warning(self.request, message)
        return redirect(self.login_url)


class LabelDestroyView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    """
    Class of displaying the page for deletion a label.
    """
    model = Label
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('labels_list')
    # extra_context = {'button_name': 'Да, удалить'}
    extra_context = {'button_name': _('Yes, delete')}
    login_url = reverse_lazy('user_login')

    def handle_no_permission(self):
        # message = 'Вы не авторизованы! Пожалуйста, выполните вход'
        message = _('You are not logged in! Please log in')
        messages.warning(self.request, message)
        return redirect(self.login_url)

    def form_valid(self, form):
        try:
            self.object.delete()
            # messages.success(self.request,
            # 'Метка успешно удалена')
            messages.success(self.request,
                             _('The label was successfully deleted'))
        except ProtectedError:
            # messages.warning(self.request,
            # 'Невозможно удалить метку, потому что она используется')
            messages.warning(self.request,
                             _('Unable to delete the label '
                               'because it is being used'))
        finally:
            return redirect(self.get_success_url())
