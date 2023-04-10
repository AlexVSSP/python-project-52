from django.urls import path

from task_manager.tasks.views import TasksView, TaskCreateView, \
    TaskUpdateView, TaskDestroyView, TaskDetailView

urlpatterns = [
    path('', TasksView.as_view(), name='tasks_list'),
    path('create/', TaskCreateView.as_view(),
         name='task_create'),
    path('<int:pk>/update/', TaskUpdateView.as_view(),
         name='task_update'),
    path('<int:pk>/delete/', TaskDestroyView.as_view(),
         name='task_delete'),
    path('<int:pk>/', TaskDetailView.as_view(),
         name='task_detail'),
]
