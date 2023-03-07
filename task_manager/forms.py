from django.contrib.auth.forms import UserCreationForm
# from django.forms import ModelForm
from .models import User


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'password1', 'password2']


# class UserForm(ModelForm):
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'username', 'password']


# class UserLogin(ModelForm):
#     class Meta:
#         model = User
#         fields = ['username', 'password']
