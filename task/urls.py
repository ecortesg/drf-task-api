from django.urls import path
from . import views


urlpatterns = [
    path('', views.api_overview),
    path('tasks/', views.tasks),
    path('task-create/', views.task_create),
    path('owner-update/<int:task_id>/', views.owner_update),
    path('supervisor-update/<int:task_id>/', views.supervisor_update)
]
