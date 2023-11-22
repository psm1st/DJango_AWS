from django.db import models
from django.shortcuts import render

from .forms import UserCreateForm
# Create your models here.
def signup_view(request):
    if request.method == 'GET':
        form = UserCreateForm
        context = {'form':form}
        return render(request,'accounts/signup.html',context)
    else:
        pass