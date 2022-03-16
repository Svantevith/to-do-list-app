import random
from typing import Any, Dict
from django.shortcuts import redirect
from django.forms.models import BaseModelForm
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, redirect_to_login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

# LoginRequiredMixin should be the first derived class!
# Add the LoginRequiredMixin to prevent users from accessing others data
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Task


# Create your views here.
class UserLogin(LoginView):
    
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    # Override super().get_success_url()
    def get_success_url(self) -> str:
        return reverse_lazy('task-list')


class UserRegister(FormView):
    
    form_class = UserCreationForm
    template_name = 'base/register.html'
    redirect_to_login = True
    success_url = reverse_lazy('task-list')

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        user = form.save()
        if user:
            login(self.request, user)
        return super().form_valid(form)

    # Redirect the user to logged in panel if authenticated, else register
    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if self.request.user.is_authenticated:
            return redirect('task-list')
        return super().get(request, *args, **kwargs)
    


# Default template_name: <model>_list.html (task_list.html)
# Default object_context_name: <model>_list (task_list)
class TaskList(LoginRequiredMixin, ListView):
    
    model = Task
    text = 'task_description'

    @property
    def greeting(self) -> str:
        return random.choice([
            'How are you,\n{}?',
            'Welcome back,\n{}!',
            'We were missing you,\n{}!',
            "It's great to see you back,\n{}!",
            "It's such a lovely day, isn't it \n{}?",
        ]).format(str(self.request.user).title())


    # Prevent users from viewing not owned tasks
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['task_list'] = context['task_list'].filter(user=self.request.user)
        context['task_count'] = context['task_list'].filter(complete=False).count()
        context['greeting'] = self.greeting
        # Searchbar
        search_query = self.request.GET.get('search-field') or ''
        if search_query:
            context['task_list'] = context['task_list'].filter(title__icontains=search_query)  # title__startswith

        context['search_query'] = search_query
        return context


# Default template_name: <model>_detail.html (task_detail.html)
# Default object_context_name: <model>_detail (task_detail)
class TaskDetails(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = f'base/task.html'


# Default template_name: <model>_form.html (task_form.html)
# Default object_context_name: <model>_create (task_create)
class TaskCreate(CreateView):
    
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('task-list')  # Redirect user after action

    # Prevent users from adding new tasks to other users
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.user = self.request.user
        return super().form_valid(form)



# Default template_name: <model>_form.html (task_form.html)
# Default object_context_name: <model>_update (task_update)
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('task-list')


# Default template_name: <model>_form.html (task_form.html)
# Default object_context_name: <model>_delete (task_delete)
class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'base/task_delete.html'
    fields = '__all__'  # List all fields from the Task object
    success_url = reverse_lazy('task-list')
