"""tasksproject URL Configuration

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
from tasksapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('signig/', views.signin, name="signin"),
    path('signup/', views.signup, name="signup"),
    path('logout/', views.singout, name="loguot"),
    path('tasks/', views.tasks, name="tasks"),
    path('tasks/complete', views.tasks_comlete, name="tasks_complete"),
    path('tasks/create', views.tasks_create, name="tasks_create"),
    path('tasks/delete/<int:task_id>', views.delete_tasks, name="tasks_delete"),
    path('tasks/detail/<int:task_id>', views.task_detail, name="task_detail"),
    path('tasks/complete/<int:task_id>', views.complete_tasks, name="complete_tasks"),
    
]
