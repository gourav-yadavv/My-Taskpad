from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Task(models.Model):
    # user name ka ek col hoga
    # here  we will create 1 to many relationship 
    # bcoz a single user can have many items
    # we will make it a foreign key and whenever any user is getting deleted  we will delete all tasks related to that user
    # if you wants ki user agar delete ho jaye but uske tasks delete nahi to to instead of doing on_delete = models.CASCADE we can do on_delete = models.SET_NULL i.e. if a user is getting deleted items remains there only
    # user bnane ke liye hm django ka khuska model use krenge names as User which is in django.contrib.auth.models
    # null = True this means in the database this could be an empty field
    # blank =    as whenever we submit a form  we also want to allow value to be blank right there
    # we also set the values of null and blank to true whenever we starts with our application and whenver we are testing our applications 
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    # task ke title ka ek col hoga
    # here title will be just a string so we will make it a char field 
    # and if you are creating a task so the title should be there so we  will not assign by default null & blank to be true
    title = models.CharField(max_length=130,null=True,blank=True)
    # task ke description ka ek col hoga
    # task description we will make it a text field 
    description = models.TextField(null=True,blank=True)
    # task status is it completed or not
    # task status will be a boolean value either the task will be completed or pending 
    complete = models.BooleanField(default=False)
    # date and time or creationof task
    # here auto_now_add ko true kr diya hai it will  automaticallly capture the date and time whenver we will add an item
    created_at = models.DateTimeField(auto_now_add=True)

    # to close a class in python its like a constructor
    def __str__(self):
        return self.title
    # this below class is for ordering the tasks the tasks that are getting completed will go down in the list
    class Meta:
        ordering = ['complete']
