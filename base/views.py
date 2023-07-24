from typing import Any, Dict
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect
# from django.http import HttpResponse
from django.views.generic.list import ListView
# for detailed view we will use detailView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView

from django.urls import reverse_lazy

# ye login logout ka puri functionality de dega
from django.contrib.auth.views import LoginView
# ye niche jo import kra hai LoginRequiredMixin ye isliye kr rhe ki agar user login nahi hai to user ko task_lists nahi dikhna chahiye
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Task

# Create your views here.
#---------------------------------------------
class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    # now  we will make our custom success url
    def get_success_url(self):
        return reverse_lazy('tasks')

# here we will create class for the registration of a new user

class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request,user)
        return super(RegisterPage,self).form_valid(form)
    
    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage,self).get(*args,**kwargs)
#----------------------------------------------
# is view ko urls .py me le add krna  pdega then we will be able to see that 
# this below view named as TaskList will look for the template named as task_list.html in the templates of app
# LoginRequiredMixin  ye pass krne se agar user logged in hai to hi wo task list dekh payega otherwise nahi dekh payega but dikkat hai ye restriction agar user logged in nahi hai to pta ni kha redirect kr dega kuch error type dega so we will override that functionality and we will redirect as our wish so for that we need to make chnages in the settings.py file me last me ye add kra hai LOGIN_URL = 'login'
class TaskList(LoginRequiredMixin,ListView):
	# our model is Task so 
    model = Task
    # ye niche wali line define ni krenge to hme html template me object_list krke krna pdega 
    # ab ye define kr diya hai to we will directly use tasks
    context_object_name = 'tasks'

    # ab ye task list me kuch aaisa krna pdega ki jo user logged in hai usi ki task list btaye insteadof ki saare users ke task btaye so we will handle that also
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        
        # search area me jo doge wahi context aapko display hoga 
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)

        context['search_input'] = search_input
        return context




# now for detaled view of a task we will create an another class and we will be inheriting it from DetailedView class
# this below view named as TaskDetail will look for the template named as task_detail.html in the templates of app
# and it will look for an object not object list  in the template names as task_detail.html
class TaskDetail(LoginRequiredMixin,DetailView):
    # our model name is talk so telling to this class that we need to pick the task details from the model names as Task
    model = Task
    context_object_name = 'task'
    # by default it looks for default template name in templates named as task_detail.html but if we provides template name here i.e. if we overide the default name then we we can give custom name to our template
    # aaise hi override krke  saari templates ko custom name de skte hai 
    # ab ye default template name ko na dekhkr ye jo name diya hai us naam ki template dekhega
    template_name = 'base/task.html'

# now we will be creating a class for creating items/tasks and we will inherit our class from django default class named as : CreateView
# CreateView will be having more complex logic as we will be sending a post request as we have to create an item
# by default it will look for a template named as : task_form.html here task is the model name and form is to create a new task &  we can override this default name also
# already create will provides us model form to work with 
# its basically a model form and it will create all the fields for us that a Task have  which are in our model 'Task' 
# model form basically means model se form bnana thats it
class TaskCreate(LoginRequiredMixin,CreateView):
    # this create view class is like magic it will create form for you it will automatically add the data to the db by just clicking on submit 
    # instead of this class-based-view if we uses function-based-views then it will be very complecated har chiz likhni pdti logic me 
    model = Task
    # here we can give a list of fields which we want in our form we can list them here
    # ye niche jo list bnai hai waise bhi de skte hai 
    # and if you want all fields of model then iske next wali line likhdo bs
    fields = ['title','description','complete']
    # fields = '__all__'
    # after submitting this form we need to assure that our user will get redirected to other page successfully and for that we imported the reverse_lazy which just redirects the user to a ertain part of our page/application 
    # i.e. if everything correct just redirect the user to the tasks url which is already mentioned in our urls .py names as tasks
    success_url = reverse_lazy('tasks')

    # agar koi user already logged in hai to usse user name select krwane ka koi sense nahi  hai so we so we will be auto fetching the user and for that we will be using form_valid
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate,self).form_valid(form)

# this update class also looks for the same template names as task_form.html 
class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    # fields = '__all__'
    fields = ['title','description','complete']
    success_url = reverse_lazy('tasks')

# this DeleteView by default looks for the temapled names as : task_confirm_delete.html 
class DeleteView(LoginRequiredMixin,DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')

