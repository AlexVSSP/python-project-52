from django import forms
from django_filters import FilterSet, ModelChoiceFilter, BooleanFilter
from django.utils.translation import gettext as _

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import User


class TaskFilter(FilterSet):

    def task_filter(self, queryset, name, value):
        if value:
            author = getattr(self.request, 'user', None)
            queryset = queryset.filter(author=author)
        return queryset

    status = ModelChoiceFilter(
        queryset=Status.objects.all(),
        label=_('Status'),
        widget=forms.Select(attrs={'title_id': 'id_status'}))

    executor = ModelChoiceFilter(
        queryset=User.objects.all(),
        label=_('Executor'),
        widget=forms.Select(attrs={'title_id': 'id_executor'}))

    labels = ModelChoiceFilter(
        queryset=Label.objects.all(),
        label=_('Label'),
        widget=forms.Select(attrs={'title_id': 'id_label'}))

    self_task = BooleanFilter(
        label=_('Only own tasks'),
        widget=forms.widgets.CheckboxInput(attrs={'title_id': 'id_self_task'}),
        method='task_filter')

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels', 'self_task']
