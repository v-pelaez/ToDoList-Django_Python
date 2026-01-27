from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import TaskListView, TaskDetailView, TaskCreateView, TaskUpdateView, TaskDeleteView, Signup


urlpatterns = [
    path('', TaskListView.as_view(), name='home'),
    path('login/', LoginView.as_view(template_name='base/login.html', next_page='home'), name='login'),
    path('signup/', Signup.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(next_page = 'login'), name='logout'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task'),
    path('add/', TaskCreateView.as_view(), name='add'),
    path('update/<int:pk>/', TaskUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', TaskDeleteView.as_view(), name='delete'),

]
