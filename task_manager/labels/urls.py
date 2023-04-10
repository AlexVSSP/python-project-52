from django.urls import path

from task_manager.labels.views import LabelsView, LabelCreateView, \
    LabelUpdateView, LabelDestroyView

urlpatterns = [
    path('', LabelsView.as_view(), name='labels_list'),
    path('create/', LabelCreateView.as_view(),
         name='label_create'),
    path('<int:pk>/update/', LabelUpdateView.as_view(),
         name='label_update'),
    path('<int:pk>/delete/', LabelDestroyView.as_view(),
         name='label_delete'),
]
