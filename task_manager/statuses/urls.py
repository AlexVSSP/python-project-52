from django.urls import path

from task_manager.statuses.views import StatusesView, \
    StatusFormCreateView, StatusUpdateView, StatusDestroyView

urlpatterns = [
    path('', StatusesView.as_view(),
         name='statuses_list'),
    path('create/', StatusFormCreateView.as_view(),
         name='status_create'),
    path('<int:pk>/update/', StatusUpdateView.as_view(),
         name='status_update'),
    path('<int:pk>/delete/', StatusDestroyView.as_view(),
         name='status_delete'),
]
