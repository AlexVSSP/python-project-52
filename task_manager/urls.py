"""task_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from task_manager.views import index, IndexView, UserFormCreateView, \
    UserLoginView, UserUpdateView, UserDestroyView, UserLogoutView

urlpatterns = [
    path('', index, name='home'),
    path('admin/', admin.site.urls),
    path('users/create/', UserFormCreateView.as_view(),
         name='user_create'),
    path('users/<int:pk>/update/', UserUpdateView.as_view(),
         name='user_update'),
    path('users/<int:pk>/delete/', UserDestroyView.as_view(),
         name='user_delete'),
    path('users/', IndexView.as_view(), name='users_list'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('logout/', UserLogoutView.as_view(), name='user_logout'),
]
