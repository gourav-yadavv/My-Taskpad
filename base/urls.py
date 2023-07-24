from django.urls import path
from .views import TaskList,TaskDetail,TaskCreate,TaskUpdate,DeleteView,CustomLoginView,RegisterPage
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/',CustomLoginView.as_view(),name='login'),
    # logout wale url ko customlogoutView nhi bnaya sidhe logoutView ka use krke kr diya but here what after logout so we passed where to go next after loggin out we will refdirect the user to the login page
    path('logout/',LogoutView.as_view(next_page = 'login'),name='logout'),
    path('register/',RegisterPage.as_view(),name='register'),
    # path('',views.taskList,name = 'tasks'),
    path('',TaskList.as_view(),name='tasks'),
    # in this case the view by default looks for a primary key so a pk value so in this case we will set that as an integer 
    # this below path will look for the detailed view of a task
    path('task/<int:pk>/',TaskDetail.as_view(),name='task'),
    path('task-create/',TaskCreate.as_view(),name='task-create'),
    path('task-update/<int:pk>/',TaskUpdate.as_view(),name='task-update'),
    path('task-delete/<int:pk>/',DeleteView.as_view(),name='task-delete'),
]