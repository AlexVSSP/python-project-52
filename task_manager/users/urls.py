from django.urls import path

from task_manager.users.views import UsersView, UserFormCreateView, \
    UserUpdateView, UserDestroyView

urlpatterns = [
    path('', UsersView.as_view(),
         name='users_list'),
    path('create/', UserFormCreateView.as_view(),
         name='user_create'),
    path('<int:pk>/update/', UserUpdateView.as_view(),
         name='user_update'),
    path('<int:pk>/delete/', UserDestroyView.as_view(),
         name='user_delete'),
]
