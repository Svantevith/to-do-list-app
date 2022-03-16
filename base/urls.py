from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import TaskList, TaskDetails, TaskCreate, TaskUpdate, TaskDelete, UserLogin, UserRegister

urlpatterns = [
    path('', TaskList.as_view(), name='task-list'),

    path('login/', UserLogin.as_view(), name='login'),
    path('register/', UserRegister.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    
    path('view-task/<int:pk>/', TaskDetails.as_view(), name='task'),  # <pk> stands for primary key, int is for regex
    path('create-task/', TaskCreate.as_view(), name='task-create'),
    path('update-task/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('delete-task/<int:pk>/', TaskDelete.as_view(), name='task-delete'),
]
