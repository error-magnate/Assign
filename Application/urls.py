from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home),
    path('add/project/', views.add_project, name="add_project"),
    path('add/task/<int:project_id>', views.add_task, name="add_task"),
    path('project/<int:project_id>', views.show_project, name="show_project"),
    path('project/delete/<int:project_id>', views.delete_project, name="delete_project"),
    path('task/done/<int:project_id>/<int:task_id>', views.task_status, name="task_status"),
    path('task/delete/<int:project_id>/<int:task_id>', views.task_delete, name="task_delete")

]
