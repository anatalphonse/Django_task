from django.urls import path
from .views import MyTasksView, UpdateTaskView, TaskReportView

urlpatterns = [
  path("tasks/", MyTasksView.as_view()),
  path("tasks/<int:pk>/", UpdateTaskView.as_view()),
  path("tasks/<int:pk>/report/", TaskReportView.as_view()),
]