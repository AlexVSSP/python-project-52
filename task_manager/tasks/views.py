from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django_filters.views import FilterView
from django.utils.translation import gettext as _

from task_manager.tasks.forms import TaskForm
from task_manager.tasks.models import Task
from task_manager.tasks.filter import TaskFilter


class TasksView(LoginRequiredMixin, FilterView):
    """
    Class of task list display.
    """
    model = Task
    template_name = 'tasks/tasks.html'
    context_object_name = 'tasks'
    login_url = reverse_lazy('user_login')
    # login_url = 'user_login'
    filterset_class = TaskFilter

    def handle_no_permission(self):
        # message = 'Вы не авторизованы! Пожалуйста, выполните вход'
        message = _('You are not logged in! Please log in')
        messages.warning(self.request, message)
        return redirect(self.login_url)


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Class of displaying the page for creating a new task.
    """
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks_list')
    # success_message = 'Задача успешно создана'
    success_message = _('The task was created successfully')
    # extra_context = {'button_name': 'Создать'}
    extra_context = {'button_name': _('Create')}
    login_url = reverse_lazy('user_login')
    # login_url = 'user_login'

    # def handle_no_permission(self):
    #     message = 'Вы не авторизованы! Пожалуйста, выполните вход'
    #     messages.warning(self.request, message)
    #     return redirect(self.login_url)

    def handle_no_permission(self):
        url = reverse_lazy('user_login')
        # messages.warning(self.request,
        # 'Вы не авторизованы! Пожалуйста, выполните вход')
        messages.warning(self.request,
                         _('You are not logged in!, Please log in'))
        return redirect(url)

    # def form_valid(self, form):
    #     success_message = 'Задача успешно создана'
    #     self.object = form.save(commit=False)
    #     self.object.author = self.request.user
    #     self.object.save()
    #     messages.success(self.request, success_message)
    #     return super(TaskCreateView, self).form_valid(form)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Class of displaying the page for editing a task.
    """
    model = Task
    form_class = TaskForm
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('tasks_list')
    # success_message = 'Задача успешно изменена'
    success_message = _('The task updated successfully')
    # extra_context = {'button_name': 'Изменить'}
    extra_context = {'button_name': _('To change')}
    login_url = reverse_lazy('user_login')

    # def handle_no_permission(self):
    #     message = 'Вы не авторизованы! Пожалуйста, выполните вход'
    #     messages.warning(self.request, message)
    #     return redirect(self.login_url)

    def handle_no_permission(self):
        url = reverse_lazy('user_login')
        # messages.warning(self.request,
        # 'Вы не авторизованы! Пожалуйста, выполните вход')
        messages.warning(self.request,
                         _('You are not logged in! Please log in'))
        return redirect(url)


class TaskDestroyView(LoginRequiredMixin, SuccessMessageMixin,
                      UserPassesTestMixin, DeleteView):
    """
    Class of displaying the page for deletion a task.
    """
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks_list')
    # success_message = 'Задача успешно удалена'
    success_message = _('The task was successfully deleted')
    # extra_context = {'button_name': 'Да, удалить'}
    extra_context = {'button_name': _('Yes, delete')}
    login_url = reverse_lazy('user_login')

    def test_func(self):
        task = self.get_object()
        return self.request.user.id == task.author.id

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            # message = 'Задачу может удалить только ее автор'
            message = _('A task can only be deleted by its author')
            url = reverse_lazy('tasks_list')
        else:
            # message = 'Вы не авторизованы! Пожалуйста, выполните вход'
            message = _('You are not logged in! Please log in')
            url = self.login_url
        messages.warning(self.request, message)
        return redirect(url)


class TaskDetailView(LoginRequiredMixin, DetailView):
    """
    Class of displaying detailed information about the task.
    """
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'
    login_url = reverse_lazy('user_login')

    def handle_no_permission(self):
        # message = 'Вы не авторизованы! Пожалуйста, выполните вход'
        message = _('You are not logged in! Please log in')
        messages.warning(self.request, message)
        return redirect(self.login_url)
