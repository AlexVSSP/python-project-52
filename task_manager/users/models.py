# from django.db import models
from django.contrib.auth.models import AbstractUser


# class User(models.Model):
#     """Пользователи"""
#     username = models.CharField(max_length=50)
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     # last_name = models.CharField(max_length=100, default='Cool')
#     created_at = models.DateTimeField(auto_now_add=True)
#     password = models.CharField(max_length=100)
#     # password = models.CharField(max_length=100, default='easy')
#
#     def __str__(self):
#         return self.username


class User(AbstractUser):

    def __str__(self):
        return self.get_full_name()
