from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from api.models import Users
# Create your views here.

def home(request):
    return render(request,"Home.html")

def register(request):
    form=UserCreationForm(request.POST)
    if form.is_valid():
      form.save()
      username=form.cleaned_data.get("username")
      messages.success(request, f'your account was created Successfully')
      a=Users.objects.create(name=username)
      a.save()
      return redirect('index')
    context = {
        'form':form  
    } 
    return render(request, "register.html", context)

@login_required(login_url='login')
def profile(request):
    return render(request, 'profile.html')