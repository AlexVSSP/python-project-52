from django.db import models
from django.utils.translation import gettext as _

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.users.models import User


class Task(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name=_('Name'))
    description = models.TextField(
        null=True,
        verbose_name=_('Description'))
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name=_('Author'))
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        verbose_name=_('Status'))
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='executor',
        verbose_name=_('Executor'))
    created_at = models.DateTimeField(auto_now_add=True)
    labels = models.ManyToManyField(
        Label,
        through='LabelToTask',
        blank=True,
        verbose_name=_('Labels'))

    def __str__(self):
        return self.name


class LabelToTask(models.Model):
    labels = models.ForeignKey(Label, on_delete=models.PROTECT, null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True)
