from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login, logout
from django.views.generic import CreateView,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserSignUpForm
from .models import Profile
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect

def index(request):
    return render(request=request, template_name='index.html')

def signup(request):
    if request.method == 'POST':
        userform = UserSignUpForm(request.POST, prefix='userform')
        if userform.is_valid():
            user = userform.save()
            user.save()
            profile = Profile(user=user)
            profile.save()
            username = userform.cleaned_data.get('username')
            raw_password = userform.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        userform = UserSignUpForm(prefix='userform')
    return render(request=request, template_name='signup/signup.html',context={'userform': userform})

def leaderboard(request):
    u=Profile.objects.order_by('-progress')
    return render(request=request,template_name='leaderboard.html',context={'profiles':u})
