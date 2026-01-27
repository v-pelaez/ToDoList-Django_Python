from re import search

from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from base.forms import TaskForm, TaskCreateForm
from base.models import Task
from django.shortcuts import redirect

class Login(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')

class Signup(FormView):
    template_name = 'base/signup.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')

    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super(Signup, self).get(*args,**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super(Signup,self).form_valid(form)

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(completed=False).count()

        search_value = self.request.GET.get('search') or ''
        if search_value:
            context['tasks'] = context['tasks'].filter(title__icontains=search_value)
        context['search_value'] = search_value
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    queryset = Task.objects.all()


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskCreateForm
    success_url = reverse_lazy('home')
    context_object_name = 'task'
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.completed = False
        return super(TaskCreateView, self).form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('home')
    context_object_name = 'task'
    queryset = Task.objects.all()


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('home')
    queryset = Task.objects.all()
