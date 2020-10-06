from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path('', views.api_overview, name="api-overview"),
    path('task-list/', views.task_list, name="task-list"),
    path('task-create/', views.task_create, name="task-create"),
    path('task-update/<str:primary_key>/', views.task_update, name="task-update"),
    path('task-history/<str:primary_key>/', views.task_history, name="task-history"),
    path('register', views.registration, name='register'),
    path('login', obtain_auth_token, name="login"),
]
